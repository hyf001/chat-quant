from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.api.dependencies import ServicesDep
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
    after: StreamAfterQuery = 0,
) -> StreamingResponse:
    detail = service.get_session_detail(chat_session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="chat session not found")
    return StreamingResponse(
        _sse_events(service, chat_session_id, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@router.post("/sessions/{chat_session_id}/cancel", response_model=CancelSessionResponse)
async def cancel_chat_session(
    chat_session_id: str,
    request: CancelSessionRequest,
    service: ChatServiceDep,
) -> CancelSessionResponse:
    cancelled = await service.cancel_session_turn(chat_session_id, request.reason)
    if not cancelled:
        raise HTTPException(status_code=404, detail="chat session not found")
    return CancelSessionResponse(chat_session_id=chat_session_id, cancelled=True)


@router.get("/sessions/{chat_session_id}", response_model=ChatSessionDetail)
async def get_chat_session(
    chat_session_id: str,
    service: ChatServiceDep,
) -> ChatSessionDetail:
    detail = service.get_session_detail(chat_session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="chat session not found")
    return detail


async def _sse_events(
    service: ChatApplicationService,
    chat_session_id: str,
    after: int,
) -> AsyncIterator[str]:
    last_sequence = after
    idle_ticks = 0
    while idle_ticks < 600:
        envelopes = service.stream_relay.list_envelopes(chat_session_id, after=last_sequence)
        if not envelopes:
            if service.is_turn_running(chat_session_id):
                idle_ticks = 0
                yield ": keepalive\n\n"
                await asyncio.sleep(0.5)
                continue
            idle_ticks += 1
            await asyncio.sleep(0.05)
            continue

        idle_ticks = 0
        for envelope in envelopes:
            last_sequence = envelope.sequence
            payload = envelope.model_dump(mode="json")
            yield f"event: sdk\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
            if envelope.sdk_event.get("type") in {"result_message", "runtime_error", "cancelled"}:
                yield "event: done\ndata: {}\n\n"
                return
    yield "event: done\ndata: {}\n\n"
