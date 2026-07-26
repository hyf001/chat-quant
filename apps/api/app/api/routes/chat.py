from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.api.dependencies import ServicesDep, UserId
from app.application.chat_service import ChatApplicationService, chat_application_service
from app.domain.chat_sessions.services import ChatSessionAccessError
from app.schemas.contracts.agent_runtime import (
    CancelSessionRequest,
    CancelSessionResponse,
    ChatMessageAccepted,
    ChatMessageRequest,
    ChatSessionDetail,
)

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_application_service() -> ChatApplicationService:
    return chat_application_service


ChatServiceDep = Annotated[ChatApplicationService, Depends(get_chat_application_service)]
StreamAfterQuery = Annotated[int, Query(ge=0)]


@router.post("/messages", response_model=ChatMessageAccepted)
async def post_chat_message(
    request: ChatMessageRequest,
    service: ChatServiceDep,
    services: ServicesDep,
) -> ChatMessageAccepted:
    try:
        return await service.handle_user_message(request, services.chat_sessions)
    except ChatSessionAccessError:
        raise HTTPException(status_code=403, detail="chat session access denied") from None


@router.get("/sessions/{chat_session_id}/stream")
async def stream_chat_session(
    chat_session_id: str,
    service: ChatServiceDep,
    services: ServicesDep,
    user_id: UserId,
    after: StreamAfterQuery = 0,
) -> StreamingResponse:
    try:
        detail = await service.get_session_detail(
            chat_session_id,
            services.chat_sessions,
            user_id=user_id,
        )
        if detail is None:
            raise HTTPException(status_code=404, detail="chat session not found")
    except ChatSessionAccessError:
        raise HTTPException(status_code=403, detail="chat session access denied") from None
    return StreamingResponse(
        _sse_events(service, chat_session_id, services, user_id, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@router.post("/sessions/{chat_session_id}/cancel", response_model=CancelSessionResponse)
async def cancel_chat_session(
    chat_session_id: str,
    request: CancelSessionRequest,
    service: ChatServiceDep,
) -> CancelSessionResponse:
    cancelled = await service.cancel_session(chat_session_id, request.reason)
    if not cancelled:
        raise HTTPException(status_code=404, detail="chat session not found")
    return CancelSessionResponse(chat_session_id=chat_session_id, cancelled=True)


@router.get("/sessions/{chat_session_id}", response_model=ChatSessionDetail)
async def get_chat_session(
    chat_session_id: str,
    service: ChatServiceDep,
    services: ServicesDep,
    user_id: UserId,
) -> ChatSessionDetail:
    try:
        detail = await service.get_session_detail(
            chat_session_id,
            services.chat_sessions,
            user_id=user_id,
        )
        if detail is None:
            raise HTTPException(status_code=404, detail="chat session not found")
    except ChatSessionAccessError:
        raise HTTPException(status_code=403, detail="chat session access denied") from None
    return detail


async def _sse_events(
    service: ChatApplicationService,
    chat_session_id: str,
    services: ServicesDep,
    user_id: str,
    after: int,
) -> AsyncIterator[str]:
    del after
    async for envelope in service.stream_chat_session(
        chat_session_id,
        services.chat_sessions,
        user_id=user_id,
    ):
        payload = envelope.model_dump(mode="json")
        yield f"event: sdk\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
        if envelope.sdk_event.get("type") in {"result_message", "runtime_error", "cancelled"}:
            yield "event: done\ndata: {}\n\n"
            return
    yield "event: done\ndata: {}\n\n"
