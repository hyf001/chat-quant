from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import ProjectId, ServicesDep, UserId
from app.domain.chat_sessions.repositories import ChatSessionNotFoundError
from app.domain.chat_sessions.services import ChatSessionAccessError, SDKSessionReadError
from app.schemas.conversations import (
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

router = APIRouter(prefix="/conversations", tags=["conversations"])


def _raise_not_found() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")


def _raise_forbidden() -> None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chat session access denied")


def _raise_sdk_unavailable(error: SDKSessionReadError) -> None:
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"Claude Agent SDK unavailable: {error}",
    )


@router.post("", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    payload: ChatSessionCreateRequest,
    services: ServicesDep,
    user_id: UserId = "demo_user",
    project_id: ProjectId = "default_project",
):
    return await services.chat_sessions.create_chat_session(
        user_id=user_id,
        project_id=project_id,
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
    services: ServicesDep,
    user_id: UserId = "demo_user",
    query: str | None = Query(default=None, max_length=120),
    kind: str | None = Query(default=None, max_length=32),
    task_type: str | None = Query(default=None, max_length=32),
    include_archived: bool = False,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = await services.chat_sessions.list_chat_sessions(
        user_id=user_id,
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
    services: ServicesDep,
    user_id: UserId = "demo_user",
    message_limit: int | None = Query(default=None, ge=1, le=200),
):
    try:
        session, messages, assets = await services.chat_sessions.get_chat_session_detail(
            chat_session_id, user_id=user_id, message_limit=message_limit
        )
    except ChatSessionAccessError:
        _raise_forbidden()
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
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        return await services.chat_sessions.update_chat_session(
            chat_session_id,
            user_id=user_id,
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
    except ChatSessionAccessError:
        _raise_forbidden()
    except ChatSessionNotFoundError:
        _raise_not_found()


@router.delete("/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    chat_session_id: str,
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        await services.chat_sessions.soft_delete_chat_session(chat_session_id, user_id=user_id)
    except ChatSessionAccessError:
        _raise_forbidden()
    except ChatSessionNotFoundError:
        _raise_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{chat_session_id}/messages", response_model=SendMessageResponse)
async def send_message(
    chat_session_id: str,
    payload: SendMessageRequest,
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        await services.chat_sessions.get_context(chat_session_id, user_id=user_id)
    except ChatSessionAccessError:
        _raise_forbidden()
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
    services: ServicesDep,
    user_id: UserId = "demo_user",
    limit: int | None = Query(default=None, ge=1, le=200),
):
    try:
        _, messages, _ = await services.chat_sessions.get_chat_session_detail(
            chat_session_id, user_id=user_id, message_limit=limit
        )
    except ChatSessionAccessError:
        _raise_forbidden()
    except ChatSessionNotFoundError:
        _raise_not_found()
    except SDKSessionReadError as exc:
        _raise_sdk_unavailable(exc)
    return sdk_messages_to_response(messages)


@router.get("/{chat_session_id}/stream")
async def stream_messages(
    chat_session_id: str,
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        _, messages, _ = await services.chat_sessions.get_chat_session_detail(
            chat_session_id, user_id=user_id
        )
    except ChatSessionAccessError:
        _raise_forbidden()
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
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        return await services.asset_links.link_asset(
            chat_session_id=chat_session_id,
            user_id=user_id,
            sdk_session_id=payload.sdk_session_id,
            sdk_message_uuid=payload.sdk_message_uuid,
            sdk_tool_use_id=payload.sdk_tool_use_id,
            asset_type=payload.asset_type,
            asset_id=payload.asset_id,
            relation_type=payload.relation_type,
            display_snapshot=payload.display_snapshot,
        )
    except ChatSessionAccessError:
        _raise_forbidden()
    except ChatSessionNotFoundError:
        _raise_not_found()


@router.get("/{chat_session_id}/context", response_model=ChatSessionContextResponse)
async def get_context(
    chat_session_id: str,
    services: ServicesDep,
    user_id: UserId = "demo_user",
):
    try:
        session, assets = await services.chat_sessions.get_context(
            chat_session_id, user_id=user_id
        )
    except ChatSessionAccessError:
        _raise_forbidden()
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
