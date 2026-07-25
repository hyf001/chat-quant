from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from claude_agent_sdk import get_session_messages as sdk_get_session_messages

from app.domain.chat_sessions.models import (
    AssetLink,
    AssetRelationType,
    AssetType,
    ChatSession,
    ChatSessionKind,
    JSONValue,
    utc_now,
)
from app.domain.chat_sessions.repositories import (
    AssetLinkRepository,
    ChatSessionNotFoundError,
    ChatSessionRepository,
)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


def _default_title(prompt: str | None = None) -> str:
    if not prompt:
        return "新的量化会话"
    normalized = " ".join(prompt.strip().split())
    if not normalized:
        return "新的量化会话"
    return normalized[:40]


class ChatSessionAccessError(PermissionError):
    pass


class SDKSessionReadError(RuntimeError):
    pass


class ChatSessionService:
    def __init__(
        self,
        session_repository: ChatSessionRepository,
        asset_repository: AssetLinkRepository,
        *,
        claude_agent_cwd: str | None = None,
        agent_workdir_root: str | None = None,
    ) -> None:
        self._sessions = session_repository
        self._assets = asset_repository
        self._claude_agent_cwd = claude_agent_cwd
        self._agent_workdir_root = agent_workdir_root

    async def create_chat_session(
        self,
        *,
        user_id: str,
        project_id: str,
        chat_session_id: str | None = None,
        title: str | None = None,
        initial_prompt: str | None = None,
        kind: ChatSessionKind = ChatSessionKind.NORMAL,
        task_type: str | None = None,
        symbols: list[str] | None = None,
        markets: list[str] | None = None,
        tags: list[str] | None = None,
        sdk_project_key: str | None = None,
        data_scope_label: str | None = None,
    ) -> ChatSession:
        now = utc_now()
        session = ChatSession(
            id=chat_session_id or _new_id("conv"),
            user_id=user_id,
            project_id=project_id,
            title=title or _default_title(initial_prompt),
            snippet=initial_prompt[:160] if initial_prompt else None,
            kind=kind,
            task_type=task_type,
            symbols=symbols or [],
            markets=markets or [],
            tags=tags or [],
            sdk_project_key=sdk_project_key,
            data_scope_label=data_scope_label,
            last_saved_at=now,
            created_at=now,
            updated_at=now,
        )
        created = await self._sessions.create(session)
        return created

    async def update_chat_session(
        self,
        chat_session_id: str,
        *,
        user_id: str,
        title: str | None = None,
        snippet: str | None = None,
        summary: str | None = None,
        kind: ChatSessionKind | None = None,
        task_type: str | None = None,
        symbols: list[str] | None = None,
        markets: list[str] | None = None,
        tags: list[str] | None = None,
        current_strategy_version_id: str | None = None,
        current_backtest_run_id: str | None = None,
        data_scope_label: str | None = None,
        sdk_session_id: str | None = None,
        sdk_project_key: str | None = None,
        archived: bool | None = None,
    ) -> ChatSession:
        session = await self._require_session(chat_session_id, user_id)
        now = utc_now()
        archived_at = session.archived_at
        if archived is True and archived_at is None:
            archived_at = now
        if archived is False:
            archived_at = None

        updated = replace(
            session,
            title=title if title is not None else session.title,
            snippet=snippet if snippet is not None else session.snippet,
            summary=summary if summary is not None else session.summary,
            kind=kind if kind is not None else session.kind,
            task_type=task_type if task_type is not None else session.task_type,
            symbols=symbols if symbols is not None else session.symbols,
            markets=markets if markets is not None else session.markets,
            tags=tags if tags is not None else session.tags,
            current_strategy_version_id=(
                current_strategy_version_id
                if current_strategy_version_id is not None
                else session.current_strategy_version_id
            ),
            current_backtest_run_id=(
                current_backtest_run_id
                if current_backtest_run_id is not None
                else session.current_backtest_run_id
            ),
            data_scope_label=(
                data_scope_label if data_scope_label is not None else session.data_scope_label
            ),
            sdk_session_id=sdk_session_id if sdk_session_id is not None else session.sdk_session_id,
            sdk_project_key=(
                sdk_project_key if sdk_project_key is not None else session.sdk_project_key
            ),
            archived_at=archived_at,
            last_saved_at=now,
            updated_at=now,
        )
        return await self._sessions.update(updated)

    async def list_chat_sessions(
        self,
        *,
        user_id: str,
        query: str | None = None,
        kind: str | None = None,
        task_type: str | None = None,
        include_archived: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ChatSession], int]:
        return await self._sessions.list_for_user(
            user_id=user_id,
            query=query,
            kind=kind,
            task_type=task_type,
            include_archived=include_archived,
            limit=limit,
            offset=offset,
        )

    async def ensure_chat_session(
        self,
        *,
        chat_session_id: str,
        user_id: str,
        project_id: str,
        title: str | None = None,
        initial_prompt: str | None = None,
    ) -> ChatSession:
        session = await self._sessions.get(chat_session_id)
        if session is None or session.deleted_at is not None:
            return await self.create_chat_session(
                user_id=user_id,
                project_id=project_id,
                chat_session_id=chat_session_id,
                title=title,
                initial_prompt=initial_prompt,
            )
        if session.user_id != user_id:
            raise ChatSessionAccessError(chat_session_id)
        return session

    async def get_chat_session_detail(
        self, chat_session_id: str, *, user_id: str, message_limit: int | None = None
    ) -> tuple[ChatSession, list[object], list[AssetLink]]:
        session = await self._require_session(chat_session_id, user_id)
        messages: list[object] = []
        if session.sdk_session_id:
            try:
                messages = sdk_get_session_messages(
                    session.sdk_session_id,
                    directory=self._sdk_message_directory(session.id),
                    limit=message_limit,
                )
            except Exception as exc:  # pragma: no cover - exact SDK exceptions vary by version.
                raise SDKSessionReadError(str(exc)) from exc
        assets = await self._assets.list_for_chat_session(session.id)
        return session, messages, assets

    async def get_context(
        self, chat_session_id: str, *, user_id: str
    ) -> tuple[ChatSession, list[AssetLink]]:
        session = await self._require_session(chat_session_id, user_id)
        assets = await self._assets.list_for_chat_session(chat_session_id)
        return session, assets[-20:]

    async def soft_delete_chat_session(self, chat_session_id: str, *, user_id: str) -> None:
        session = await self._require_session(chat_session_id, user_id)
        now = utc_now()
        await self._sessions.update(replace(session, deleted_at=now, updated_at=now))

    async def _require_session(self, chat_session_id: str, user_id: str) -> ChatSession:
        session = await self._sessions.get(chat_session_id)
        if session is None or session.deleted_at is not None:
            raise ChatSessionNotFoundError(chat_session_id)
        if session.user_id != user_id:
            raise ChatSessionAccessError(chat_session_id)
        return session

    def _sdk_message_directory(self, chat_session_id: str) -> str | None:
        if self._claude_agent_cwd:
            return self._claude_agent_cwd
        if self._agent_workdir_root:
            return f"{self._agent_workdir_root.rstrip('/')}/{chat_session_id}"
        return None


class AssetLinkService:
    def __init__(
        self, session_repository: ChatSessionRepository, asset_repository: AssetLinkRepository
    ) -> None:
        self._sessions = session_repository
        self._assets = asset_repository

    async def link_asset(
        self,
        *,
        chat_session_id: str,
        user_id: str,
        asset_type: AssetType,
        asset_id: str,
        relation_type: AssetRelationType,
        sdk_session_id: str | None = None,
        sdk_message_uuid: str | None = None,
        sdk_tool_use_id: str | None = None,
        display_snapshot: JSONValue | None = None,
    ) -> AssetLink:
        session = await self._sessions.get(chat_session_id)
        if session is None or session.deleted_at is not None:
            raise ChatSessionNotFoundError(chat_session_id)
        if session.user_id != user_id:
            raise ChatSessionAccessError(chat_session_id)

        now = utc_now()
        link = AssetLink(
            id=_new_id("alink"),
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id or session.sdk_session_id,
            sdk_message_uuid=sdk_message_uuid,
            sdk_tool_use_id=sdk_tool_use_id,
            asset_type=asset_type,
            asset_id=asset_id,
            relation_type=relation_type,
            display_snapshot=display_snapshot,
            created_at=now,
            updated_at=now,
        )
        return await self._assets.upsert(link)

    async def list_assets_for_sdk_message(
        self, *, sdk_session_id: str, sdk_message_uuid: str, user_id: str
    ) -> list[AssetLink]:
        links = await self._assets.list_for_sdk_message(
            sdk_session_id=sdk_session_id, sdk_message_uuid=sdk_message_uuid
        )
        visible_links: list[AssetLink] = []
        for link in links:
            session = await self._sessions.get(link.chat_session_id)
            if session and session.user_id == user_id and session.deleted_at is None:
                visible_links.append(link)
        return visible_links
