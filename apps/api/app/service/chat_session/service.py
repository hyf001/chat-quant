from __future__ import annotations

from dataclasses import dataclass, replace
from uuid import uuid4

from claude_agent_sdk import get_session_info as sdk_get_session_info
from claude_agent_sdk import get_session_messages as sdk_get_session_messages
from sqlalchemy import String, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.project_dirs import project_dir
from app.model.chat_session import ChatSessionAssetLinkRow, ChatSessionRow
from app.service.chat_session.types import (
    AssetLink,
    AssetRelationType,
    AssetType,
    ChatSession,
    ChatSessionKind,
    JSONValue,
    utc_now,
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


def _initial_answer_title(prompt: str) -> str:
    stripped = " ".join(prompt.strip().split())
    if not stripped:
        return "新的分析会话"
    return stripped[:20]


def _valid_title(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = " ".join(value.strip().split())
    return stripped[:200] if stripped else None


@dataclass(frozen=True, slots=True)
class EnsuredChatSession:
    session: ChatSession
    created: bool


class ChatSessionAccessError(PermissionError):
    pass


class SDKSessionReadError(RuntimeError):
    pass


class ChatSessionNotFoundError(LookupError):
    pass


class ChatSessionService:
    def __init__(
        self,
        db: AsyncSession,
        *,
        claude_agent_cwd: str | None = None,
        project_home: str | None = None,
    ) -> None:
        self._db = db
        self._claude_agent_cwd = claude_agent_cwd
        self._project_home = project_home

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
            id=chat_session_id or _new_id("chat"),
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
        self._db.add(_session_to_row(session))
        await self._db.commit()
        return replace(session)

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
        row = await self._db.get(ChatSessionRow, updated.id)
        if row is None:
            raise ChatSessionNotFoundError(updated.id)
        _apply_session(row, updated)
        await self._db.commit()
        return replace(updated)

    async def list_chat_sessions(
        self,
        *,
        user_id: str,
        project_id: str | None = None,
        query: str | None = None,
        kind: str | None = None,
        task_type: str | None = None,
        include_archived: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ChatSession], int]:
        return await _list_sessions(
            self._db,
            user_id=user_id,
            project_id=project_id,
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
        ensured = await self.ensure_chat_session_with_status(
            chat_session_id=chat_session_id,
            user_id=user_id,
            project_id=project_id,
            title=title,
            initial_prompt=initial_prompt,
        )
        return ensured.session

    async def ensure_chat_session_with_status(
        self,
        *,
        chat_session_id: str,
        user_id: str,
        project_id: str,
        title: str | None = None,
        initial_prompt: str | None = None,
    ) -> EnsuredChatSession:
        session = await _get_session(self._db, chat_session_id)
        if session is None or session.deleted_at is not None:
            return EnsuredChatSession(
                session=await self.create_chat_session(
                    user_id=user_id,
                    project_id=project_id,
                    chat_session_id=chat_session_id,
                    title=title,
                    initial_prompt=initial_prompt,
                ),
                created=True,
            )
        if session.user_id != user_id:
            raise ChatSessionAccessError(chat_session_id)
        return EnsuredChatSession(session=session, created=False)

    def initial_answer_title(
        self,
        chat_session_id: str,
        *,
        project_id: str,
        initial_prompt: str,
        sdk_session_id: str | None,
    ) -> str:
        return (
            self._sdk_session_title(project_id, sdk_session_id)
            or _initial_answer_title(
                self._sdk_first_user_prompt(project_id, sdk_session_id) or initial_prompt
            )
        )

    async def get_chat_session_detail(
        self, chat_session_id: str, *, user_id: str, message_limit: int | None = None
    ) -> tuple[ChatSession, list[object], list[AssetLink]]:
        session = await self._require_session(chat_session_id, user_id)
        messages: list[object] = []
        if session.sdk_session_id:
            try:
                messages = sdk_get_session_messages(
                    session.sdk_session_id,
                    directory=self._sdk_message_directory(session.project_id),
                    limit=message_limit,
                )
            except Exception as exc:  # pragma: no cover - exact SDK exceptions vary by version.
                raise SDKSessionReadError(str(exc)) from exc
        assets = await _list_links_for_chat_session(self._db, session.id)
        return session, messages, assets

    async def get_context(
        self, chat_session_id: str, *, user_id: str
    ) -> tuple[ChatSession, list[AssetLink]]:
        session = await self._require_session(chat_session_id, user_id)
        assets = await _list_links_for_chat_session(self._db, chat_session_id)
        return session, assets[-20:]

    async def soft_delete_chat_session(self, chat_session_id: str, *, user_id: str) -> None:
        session = await self._require_session(chat_session_id, user_id)
        now = utc_now()
        deleted = replace(session, deleted_at=now, updated_at=now)
        row = await self._db.get(ChatSessionRow, deleted.id)
        if row is None:
            raise ChatSessionNotFoundError(deleted.id)
        _apply_session(row, deleted)
        await self._db.commit()

    async def _require_session(self, chat_session_id: str, user_id: str) -> ChatSession:
        session = await _get_session(self._db, chat_session_id)
        if session is None or session.deleted_at is not None:
            raise ChatSessionNotFoundError(chat_session_id)
        if session.user_id != user_id:
            raise ChatSessionAccessError(chat_session_id)
        return session

    def _sdk_message_directory(self, project_id: str) -> str | None:
        if self._claude_agent_cwd:
            return self._claude_agent_cwd
        if self._project_home:
            return project_dir(self._project_home, project_id)
        return None

    def _sdk_session_title(self, project_id: str, sdk_session_id: str | None) -> str | None:
        if not sdk_session_id:
            return None
        try:
            info = sdk_get_session_info(
                sdk_session_id,
                directory=self._sdk_message_directory(project_id),
            )
        except Exception:  # pragma: no cover - SDK metadata failures should not break chat sync.
            return None
        if info is None:
            return None
        title = (
            info.get("custom_title")
            if isinstance(info, dict)
            else getattr(info, "custom_title", None)
        )
        return _valid_title(title)

    def _sdk_first_user_prompt(
        self, project_id: str, sdk_session_id: str | None
    ) -> str | None:
        if not sdk_session_id:
            return None
        try:
            messages = sdk_get_session_messages(
                sdk_session_id,
                directory=self._sdk_message_directory(project_id),
            )
        except Exception:  # pragma: no cover - SDK history failures fall back to request prompt.
            return None
        for message in messages:
            role = _sdk_message_role(message)
            if role != "user":
                continue
            content = _sdk_message_content(message)
            if content:
                return content
        return None


def _sdk_message_role(message: object) -> str | None:
    message_type = getattr(message, "type", None)
    if isinstance(message_type, str) and message_type:
        return "user" if message_type in {"user", "user_message"} else message_type
    if isinstance(message, dict):
        dict_type = message.get("type")
        if isinstance(dict_type, str) and dict_type:
            return "user" if dict_type in {"user", "user_message"} else dict_type
        role = message.get("role")
        return role if isinstance(role, str) else None
    return None


def _sdk_message_content(message: object) -> str | None:
    if isinstance(message, str):
        return _valid_title(message)
    if isinstance(message, dict):
        return _content_text(message.get("content") or message.get("message"))
    content = getattr(message, "content", None)
    if content is not None:
        return _content_text(content)
    return _content_text(getattr(message, "message", None))


def _content_text(content: object) -> str | None:
    if isinstance(content, str):
        return _valid_title(content)
    if isinstance(content, dict):
        return _content_text(content.get("content"))
    if isinstance(content, list):
        parts = [text for item in content if (text := _content_text(item))]
        return _valid_title(" ".join(parts))
    text = getattr(content, "text", None)
    if isinstance(text, str):
        return _valid_title(text)
    return None


class AssetLinkService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

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
        session = await _get_session(self._db, chat_session_id)
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
        return await _upsert_link(self._db, link)

    async def list_assets_for_sdk_message(
        self, *, sdk_session_id: str, sdk_message_uuid: str, user_id: str
    ) -> list[AssetLink]:
        links = await _list_links_for_sdk_message(
            self._db,
            sdk_session_id=sdk_session_id, sdk_message_uuid=sdk_message_uuid
        )
        visible_links: list[AssetLink] = []
        for link in links:
            session = await _get_session(self._db, link.chat_session_id)
            if session and session.user_id == user_id and session.deleted_at is None:
                visible_links.append(link)
        return visible_links


def chat_session_service(db: AsyncSession) -> ChatSessionService:
    settings = get_settings()
    return ChatSessionService(
        db,
        claude_agent_cwd=settings.claude_agent_cwd,
        project_home=settings.project_home,
    )


def asset_link_service(db: AsyncSession) -> AssetLinkService:
    return AssetLinkService(db)


async def _get_session(db: AsyncSession, chat_session_id: str) -> ChatSession | None:
    row = await db.get(ChatSessionRow, chat_session_id)
    return _row_to_session(row) if row is not None else None


async def _list_sessions(
    db: AsyncSession,
    *,
    user_id: str,
    project_id: str | None = None,
    query: str | None = None,
    kind: str | None = None,
    task_type: str | None = None,
    include_archived: bool = False,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[ChatSession], int]:
    filters = [
        ChatSessionRow.user_id == user_id,
        ChatSessionRow.deleted_at.is_(None),
    ]
    if project_id is not None:
        filters.append(ChatSessionRow.project_id == project_id)
    if not include_archived:
        filters.append(ChatSessionRow.archived_at.is_(None))
    if kind is not None:
        filters.append(ChatSessionRow.kind == kind)
    if task_type is not None:
        filters.append(ChatSessionRow.task_type == task_type)
    if query:
        pattern = f"%{query.casefold()}%"
        filters.append(
            func.lower(ChatSessionRow.title).like(pattern)
            | func.lower(func.coalesce(ChatSessionRow.snippet, "")).like(pattern)
            | func.lower(cast(ChatSessionRow.tags, String)).like(pattern)
        )

    total = await db.scalar(select(func.count()).select_from(ChatSessionRow).where(*filters)) or 0
    result = await db.scalars(
        select(ChatSessionRow)
        .where(*filters)
        .order_by(ChatSessionRow.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [_row_to_session(row) for row in result.all()], total


async def _upsert_link(db: AsyncSession, link: AssetLink) -> AssetLink:
    row = await db.scalar(
        select(ChatSessionAssetLinkRow).where(
            ChatSessionAssetLinkRow.chat_session_id == link.chat_session_id,
            ChatSessionAssetLinkRow.asset_type == link.asset_type.value,
            ChatSessionAssetLinkRow.asset_id == link.asset_id,
            ChatSessionAssetLinkRow.relation_type == link.relation_type.value,
        )
    )
    if row is not None:
        updated = replace(
            _row_to_link(row),
            sdk_session_id=link.sdk_session_id or row.sdk_session_id,
            sdk_message_uuid=link.sdk_message_uuid or row.sdk_message_uuid,
            sdk_tool_use_id=link.sdk_tool_use_id or row.sdk_tool_use_id,
            display_snapshot=link.display_snapshot,
            updated_at=link.updated_at,
        )
        _apply_link(row, updated)
        await db.commit()
        return updated

    db.add(_link_to_row(link))
    await db.commit()
    return replace(link)


async def _list_links_for_chat_session(
    db: AsyncSession, chat_session_id: str
) -> list[AssetLink]:
    result = await db.scalars(
        select(ChatSessionAssetLinkRow)
        .where(ChatSessionAssetLinkRow.chat_session_id == chat_session_id)
        .order_by(ChatSessionAssetLinkRow.created_at.asc())
    )
    return [_row_to_link(row) for row in result.all()]


async def _list_links_for_sdk_message(
    db: AsyncSession,
    *,
    sdk_session_id: str,
    sdk_message_uuid: str,
) -> list[AssetLink]:
    result = await db.scalars(
        select(ChatSessionAssetLinkRow)
        .where(
            ChatSessionAssetLinkRow.sdk_session_id == sdk_session_id,
            ChatSessionAssetLinkRow.sdk_message_uuid == sdk_message_uuid,
        )
        .order_by(ChatSessionAssetLinkRow.created_at.asc())
    )
    return [_row_to_link(row) for row in result.all()]


def _session_to_row(session: ChatSession) -> ChatSessionRow:
    row = ChatSessionRow()
    _apply_session(row, session)
    return row


def _apply_session(row: ChatSessionRow, session: ChatSession) -> None:
    row.id = session.id
    row.user_id = session.user_id
    row.project_id = session.project_id
    row.title = session.title
    row.kind = session.kind.value
    row.sdk_session_id = session.sdk_session_id
    row.sdk_project_key = session.sdk_project_key
    row.snippet = session.snippet
    row.summary = session.summary
    row.task_type = session.task_type
    row.symbols = list(session.symbols)
    row.markets = list(session.markets)
    row.tags = list(session.tags)
    row.current_strategy_version_id = session.current_strategy_version_id
    row.current_backtest_run_id = session.current_backtest_run_id
    row.data_scope_label = session.data_scope_label
    row.last_saved_at = session.last_saved_at
    row.archived_at = session.archived_at
    row.deleted_at = session.deleted_at
    row.created_at = session.created_at
    row.updated_at = session.updated_at


def _row_to_session(row: ChatSessionRow) -> ChatSession:
    return ChatSession(
        id=row.id,
        user_id=row.user_id,
        project_id=row.project_id,
        title=row.title,
        kind=ChatSessionKind(row.kind),
        sdk_session_id=row.sdk_session_id,
        sdk_project_key=row.sdk_project_key,
        snippet=row.snippet,
        summary=row.summary,
        task_type=row.task_type,
        symbols=_string_list(row.symbols),
        markets=_string_list(row.markets),
        tags=_string_list(row.tags),
        current_strategy_version_id=row.current_strategy_version_id,
        current_backtest_run_id=row.current_backtest_run_id,
        data_scope_label=row.data_scope_label,
        last_saved_at=row.last_saved_at,
        archived_at=row.archived_at,
        deleted_at=row.deleted_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _link_to_row(link: AssetLink) -> ChatSessionAssetLinkRow:
    row = ChatSessionAssetLinkRow()
    _apply_link(row, link)
    return row


def _apply_link(row: ChatSessionAssetLinkRow, link: AssetLink) -> None:
    row.id = link.id
    row.chat_session_id = link.chat_session_id
    row.asset_type = link.asset_type.value
    row.asset_id = link.asset_id
    row.relation_type = link.relation_type.value
    row.sdk_session_id = link.sdk_session_id
    row.sdk_message_uuid = link.sdk_message_uuid
    row.sdk_tool_use_id = link.sdk_tool_use_id
    row.display_snapshot = link.display_snapshot
    row.created_at = link.created_at
    row.updated_at = link.updated_at


def _row_to_link(row: ChatSessionAssetLinkRow) -> AssetLink:
    return AssetLink(
        id=row.id,
        chat_session_id=row.chat_session_id,
        asset_type=AssetType(row.asset_type),
        asset_id=row.asset_id,
        relation_type=AssetRelationType(row.relation_type),
        sdk_session_id=row.sdk_session_id,
        sdk_message_uuid=row.sdk_message_uuid,
        sdk_tool_use_id=row.sdk_tool_use_id,
        display_snapshot=row.display_snapshot if _is_json_value(row.display_snapshot) else None,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _string_list(value: object) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _is_json_value(value: object) -> bool:
    return value is None or isinstance(value, str | int | float | bool | list | dict)
