from __future__ import annotations

from dataclasses import replace

from sqlalchemy import String, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.chat_sessions.models import (
    AssetLink,
    AssetRelationType,
    AssetType,
    ChatSession,
    ChatSessionKind,
)
from app.domain.chat_sessions.repositories import (
    AssetLinkRepository,
    ChatSessionNotFoundError,
    ChatSessionRepository,
)
from app.infrastructure.db.models.chat_session import (
    ChatSessionAssetLinkRow,
    ChatSessionRow,
)


class SQLAlchemyChatSessionRepository(ChatSessionRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(self, session: ChatSession) -> ChatSession:
        async with self._session_factory() as db:
            db.add(_session_to_row(session))
            await db.commit()
        return replace(session)

    async def update(self, session: ChatSession) -> ChatSession:
        async with self._session_factory() as db:
            row = await db.get(ChatSessionRow, session.id)
            if row is None:
                raise ChatSessionNotFoundError(session.id)
            _apply_session(row, session)
            await db.commit()
        return replace(session)

    async def get(self, chat_session_id: str) -> ChatSession | None:
        async with self._session_factory() as db:
            row = await db.get(ChatSessionRow, chat_session_id)
            return _row_to_session(row) if row is not None else None

    async def list_for_user(
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

        async with self._session_factory() as db:
            total = await db.scalar(
                select(func.count()).select_from(ChatSessionRow).where(*filters)
            ) or 0
            result = await db.scalars(
                select(ChatSessionRow)
                .where(*filters)
                .order_by(ChatSessionRow.updated_at.desc())
                .limit(limit)
                .offset(offset)
            )
            rows = result.all()
            return [_row_to_session(row) for row in rows], total


class SQLAlchemyAssetLinkRepository(AssetLinkRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def upsert(self, link: AssetLink) -> AssetLink:
        async with self._session_factory() as db:
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

    async def list_for_chat_session(self, chat_session_id: str) -> list[AssetLink]:
        async with self._session_factory() as db:
            result = await db.scalars(
                select(ChatSessionAssetLinkRow)
                .where(ChatSessionAssetLinkRow.chat_session_id == chat_session_id)
                .order_by(ChatSessionAssetLinkRow.created_at.asc())
            )
            rows = result.all()
            return [_row_to_link(row) for row in rows]

    async def list_for_sdk_message(
        self, *, sdk_session_id: str, sdk_message_uuid: str
    ) -> list[AssetLink]:
        async with self._session_factory() as db:
            result = await db.scalars(
                select(ChatSessionAssetLinkRow)
                .where(
                    ChatSessionAssetLinkRow.sdk_session_id == sdk_session_id,
                    ChatSessionAssetLinkRow.sdk_message_uuid == sdk_message_uuid,
                )
                .order_by(ChatSessionAssetLinkRow.created_at.asc())
            )
            rows = result.all()
            return [_row_to_link(row) for row in rows]


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
