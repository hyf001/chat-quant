import json
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator

from src.graph import builder
from src.server.chat_request import ChatRequest, FeedbackRequest
from langchain_core.messages import HumanMessage
from langgraph.types import Command
import uvicorn
from src.utils import logger

app = FastAPI(title="Chat Quant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logger.get_logger("__name__")
financial_workflow = builder.create_financial_workflow()



async def sse_wrapper(generator: AsyncGenerator[dict, None]) -> AsyncGenerator[str, None]:
    """Wrap generator output in SSE format"""
    async for data in generator:
        yield f"data: {json.dumps(data)}\n\n"

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    log.info(f"start chat {request}")
    thread_id = request.thread_id
    if thread_id == "__default__" or thread_id is None:
        thread_id = str(uuid4())
    return StreamingResponse(
            sse_wrapper(_astream_workflow_generator(thread_id, request.user_content)),
            media_type="text/event-stream"
    )


@app.post("/api/feedback")
async def human_feedback_stream(request: FeedbackRequest):
    thread_id = request.thread_id
    if thread_id is None:
        raise HTTPException(status_code=400, detail="thread_id is required")
    return StreamingResponse(
        sse_wrapper(_astream_human_feedback_generator(thread_id, request.feedback)),
        media_type="text/event-stream"
    )


async def _astream_workflow_generator(thread_id: str, user_content: str) -> AsyncGenerator[dict, None]:
    state = {"messages": [HumanMessage(content=user_content)]}
    config = {"configurable": {"thread_id": thread_id}}  # type: ignore
    async for chunk in financial_workflow.astream(state, config):
        if isinstance(chunk, dict):
            for node_name, state_update in chunk.items():
                if node_name == "__interrupt__":
                    yield {
                        "node_name": node_name,
                        "thread_id": thread_id
                    }
                else:
                    yield {
                        "node_name": node_name,
                        "message": state_update["messages"][-1].content if state_update["messages"] else "",
                        "thread_id": thread_id
                    }


async def _astream_human_feedback_generator(thread_id: str, feedback: str) -> AsyncGenerator[dict, None]:
    config = {"configurable": {"thread_id": thread_id}}  # type: ignore
    async for chunk in financial_workflow.astream(Command(resume=feedback), config):
        if isinstance(chunk, dict):
            for node_name, state_update in chunk.items():
                yield {
                    "node_name": node_name,
                    "message": state_update["messages"][-1].content if state_update["messages"] else "",
                    "thread_id": thread_id
                }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

