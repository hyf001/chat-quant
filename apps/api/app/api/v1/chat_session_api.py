from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.chat_session import (
    AssetLinkResponse,
    ChatSessionContextResponse,
    ChatSessionCreateRequest,
    ChatSessionDetailResponse,
    ChatSessionListResponse,
    ChatSessionResponse,
    ChatSessionUpdateRequest,
    LinkAssetRequest,
    SDKMessageResponse,
    SendMessageRequest,
    SendMessageResponse,
    sdk_messages_to_response,
)
from app.service import chat_session as chat_session_service
from app.service.chat_session import (
    ChatSessionNotFoundError,
    SDKSessionReadError,
)

router = APIRouter()


def _raise_not_found() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")


def _raise_sdk_unavailable(error: SDKSessionReadError) -> None:
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"Claude Agent SDK unavailable: {error}",
    )


@router.post("", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    payload: ChatSessionCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await chat_session_service.chat_session_service(db).create_chat_session(
        project_id=payload.project_id,
        title=payload.title,
        initial_prompt=payload.initial_prompt,
        kind=payload.kind,
        task_type=payload.task_type,
        symbols=payload.symbols,
        markets=payload.markets,
        tags=payload.tags,
        sdk_project_key=payload.sdk_project_key,
        data_scope_label=payload.data_scope_label,
    )


@router.get("", response_model=ChatSessionListResponse)
async def list_chat_sessions(
    db: Annotated[AsyncSession, Depends(get_db)],
    project_id: str = Query(min_length=1),
    query: str | None = Query(default=None, max_length=120),
    kind: str | None = Query(default=None, max_length=32),
    task_type: str | None = Query(default=None, max_length=32),
    include_archived: bool = False,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = await chat_session_service.chat_session_service(db).list_chat_sessions(
        project_id=project_id,
        query=query,
        kind=kind,
        task_type=task_type,
        include_archived=include_archived,
        limit=limit,
        offset=offset,
    )
    return ChatSessionListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{chat_session_id}", response_model=ChatSessionDetailResponse)
async def get_chat_session_detail(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    message_limit: int | None = Query(default=None, ge=1, le=200),
):
    try:
        session, messages, assets = await chat_session_service.chat_session_service(
            db
        ).get_chat_session_detail(chat_session_id, message_limit=message_limit)
    except ChatSessionNotFoundError:
        _raise_not_found()
    except SDKSessionReadError as exc:
        _raise_sdk_unavailable(exc)
    return ChatSessionDetailResponse(
        session=session,
        messages=sdk_messages_to_response(messages),
        assets=assets,
    )


@router.patch("/{chat_session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    chat_session_id: str,
    payload: ChatSessionUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await chat_session_service.chat_session_service(db).update_chat_session(
            chat_session_id,
            title=payload.title,
            snippet=payload.snippet,
            summary=payload.summary,
            kind=payload.kind,
            task_type=payload.task_type,
            symbols=payload.symbols,
            markets=payload.markets,
            tags=payload.tags,
            current_strategy_version_id=payload.current_strategy_version_id,
            current_backtest_run_id=payload.current_backtest_run_id,
            data_scope_label=payload.data_scope_label,
            sdk_session_id=payload.sdk_session_id,
            sdk_project_key=payload.sdk_project_key,
            archived=payload.archived,
        )
    except ChatSessionNotFoundError:
        _raise_not_found()


@router.delete("/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await chat_session_service.chat_session_service(db).soft_delete_chat_session(
            chat_session_id
        )
    except ChatSessionNotFoundError:
        _raise_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{chat_session_id}/messages", response_model=SendMessageResponse)
async def send_message(
    chat_session_id: str,
    payload: SendMessageRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    del payload
    try:
        await chat_session_service.chat_session_service(db).get_context(
            chat_session_id
        )
    except ChatSessionNotFoundError:
        _raise_not_found()
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Sending messages is owned by M2 Claude Agent Runtime; "
            "M1 only reads SDK session messages."
        ),
    )


@router.get("/{chat_session_id}/messages", response_model=list[SDKMessageResponse])
async def get_messages(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int | None = Query(default=None, ge=1, le=200),
):
    try:
        _, messages, _ = await chat_session_service.chat_session_service(
            db
        ).get_chat_session_detail(chat_session_id, message_limit=limit)
    except ChatSessionNotFoundError:
        _raise_not_found()
    except SDKSessionReadError as exc:
        _raise_sdk_unavailable(exc)
    return sdk_messages_to_response(messages)


@router.get("/{chat_session_id}/stream")
async def stream_messages(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        _, messages, _ = await chat_session_service.chat_session_service(
            db
        ).get_chat_session_detail(chat_session_id)
    except ChatSessionNotFoundError:
        _raise_not_found()
    except SDKSessionReadError as exc:
        _raise_sdk_unavailable(exc)

    async def event_stream():
        for message in sdk_messages_to_response(messages)[-10:]:
            yield f"event: message\ndata: {message.uuid}\n\n"
        yield "event: done\ndata: ok\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/{chat_session_id}/assets", response_model=AssetLinkResponse, status_code=201)
async def link_asset(
    chat_session_id: str,
    payload: LinkAssetRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await chat_session_service.asset_link_service(db).link_asset(
            chat_session_id=chat_session_id,
            sdk_session_id=payload.sdk_session_id,
            sdk_message_uuid=payload.sdk_message_uuid,
            sdk_tool_use_id=payload.sdk_tool_use_id,
            asset_type=payload.asset_type,
            asset_id=payload.asset_id,
            relation_type=payload.relation_type,
            display_snapshot=payload.display_snapshot,
        )
    except ChatSessionNotFoundError:
        _raise_not_found()


@router.get("/{chat_session_id}/context", response_model=ChatSessionContextResponse)
async def get_context(
    chat_session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        session, assets = await chat_session_service.chat_session_service(db).get_context(
            chat_session_id
        )
    except ChatSessionNotFoundError:
        _raise_not_found()
    return ChatSessionContextResponse(
        chat_session_id=session.id,
        sdk_session_id=session.sdk_session_id,
        summary=session.summary,
        current_strategy_version_id=session.current_strategy_version_id,
        current_backtest_run_id=session.current_backtest_run_id,
        assets=assets,
    )
