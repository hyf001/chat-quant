from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.agent_runtime import (
    CancelSessionRequest,
    CancelSessionResponse,
    ChatMessageAccepted,
    ChatMessageRequest,
    ChatSessionDetail,
)
from app.service import chat_session as chat_session_service
from app.service.chat import ChatApplicationService, chat_application_service

router = APIRouter()


StreamAfterQuery = Annotated[int, Query(ge=0)]


@router.post("/messages", response_model=ChatMessageAccepted)
async def post_chat_message(
    request: ChatMessageRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ChatMessageAccepted:
    return await chat_application_service.handle_user_message(
        request,
        chat_session_service.chat_session_service(db),
    )


@router.get("/sessions/{chat_session_id}/stream")
async def stream_chat_session(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    after: StreamAfterQuery = 0,
) -> StreamingResponse:
    chat_sessions = chat_session_service.chat_session_service(db)
    detail = await chat_application_service.get_session_detail(chat_session_id, chat_sessions)
    if detail is None:
        raise HTTPException(status_code=404, detail="chat session not found")
    return StreamingResponse(
        _sse_events(chat_application_service, chat_session_id, chat_sessions, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@router.post("/sessions/{chat_session_id}/cancel", response_model=CancelSessionResponse)
async def cancel_chat_session(
    chat_session_id: str,
    request: CancelSessionRequest,
) -> CancelSessionResponse:
    cancelled = await chat_application_service.cancel_session(chat_session_id, request.reason)
    if not cancelled:
        raise HTTPException(status_code=404, detail="chat session not found")
    return CancelSessionResponse(chat_session_id=chat_session_id, cancelled=True)


@router.get("/sessions/{chat_session_id}", response_model=ChatSessionDetail)
async def get_chat_session(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ChatSessionDetail:
    chat_sessions = chat_session_service.chat_session_service(db)
    detail = await chat_application_service.get_session_detail(chat_session_id, chat_sessions)
    if detail is None:
        raise HTTPException(status_code=404, detail="chat session not found")
    return detail


async def _sse_events(
    chat_service: ChatApplicationService,
    chat_session_id: str,
    chat_sessions: object,
    after: int,
) -> AsyncIterator[str]:
    del after
    async for envelope in chat_service.stream_chat_session(
        chat_session_id,
        chat_sessions,
    ):
        payload = envelope.model_dump(mode="json")
        yield f"event: sdk\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
        if envelope.sdk_event.get("type") in {"result_message", "runtime_error", "cancelled"}:
            yield "event: done\ndata: {}\n\n"
            return
    yield "event: done\ndata: {}\n\n"
