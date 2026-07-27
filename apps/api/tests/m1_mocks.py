from __future__ import annotations

from dataclasses import replace

from app.api.dependencies import M1Services
from app.domain.chat_sessions.models import AssetLink, ChatSession
from app.domain.chat_sessions.repositories import (
    AssetLinkRepository,
    ChatSessionNotFoundError,
    ChatSessionRepository,
)


def make_mock_m1_services() -> M1Services:
    return M1Services(MockChatSessionRepository(), MockAssetLinkRepository())


class MockChatSessionRepository(ChatSessionRepository):
    def __init__(self) -> None:
        self._items: dict[str, ChatSession] = {}

    async def create(self, session: ChatSession) -> ChatSession:
        self._items[session.id] = replace(session)
        return replace(session)

    async def update(self, session: ChatSession) -> ChatSession:
        if session.id not in self._items:
            raise ChatSessionNotFoundError(session.id)
        self._items[session.id] = replace(session)
        return replace(session)

    async def get(self, chat_session_id: str) -> ChatSession | None:
        session = self._items.get(chat_session_id)
        return replace(session) if session else None

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
        normalized_query = query.casefold() if query else None
        matches = [
            session
            for session in self._items.values()
            if session.user_id == user_id
            and session.deleted_at is None
            and (project_id is None or session.project_id == project_id)
            and (include_archived or session.archived_at is None)
            and (kind is None or session.kind == kind)
            and (task_type is None or session.task_type == task_type)
            and (
                normalized_query is None
                or normalized_query in session.title.casefold()
                or normalized_query in (session.snippet or "").casefold()
                or any(normalized_query in tag.casefold() for tag in session.tags)
            )
        ]
        matches.sort(key=lambda item: item.updated_at, reverse=True)
        total = len(matches)
        return [replace(item) for item in matches[offset : offset + limit]], total


class MockAssetLinkRepository(AssetLinkRepository):
    def __init__(self) -> None:
        self._items: dict[str, AssetLink] = {}

    async def upsert(self, link: AssetLink) -> AssetLink:
        existing = next(
            (
                item
                for item in self._items.values()
                if item.chat_session_id == link.chat_session_id
                and item.asset_type == link.asset_type
                and item.asset_id == link.asset_id
                and item.relation_type == link.relation_type
            ),
            None,
        )
        if existing:
            updated = replace(
                existing,
                sdk_session_id=link.sdk_session_id or existing.sdk_session_id,
                sdk_message_uuid=link.sdk_message_uuid or existing.sdk_message_uuid,
                sdk_tool_use_id=link.sdk_tool_use_id or existing.sdk_tool_use_id,
                display_snapshot=link.display_snapshot,
                updated_at=link.updated_at,
            )
            self._items[existing.id] = updated
            return replace(updated)

        self._items[link.id] = replace(link)
        return replace(link)

    async def list_for_chat_session(self, chat_session_id: str) -> list[AssetLink]:
        links = [item for item in self._items.values() if item.chat_session_id == chat_session_id]
        links.sort(key=lambda item: item.created_at)
        return [replace(item) for item in links]

    async def list_for_sdk_message(
        self, *, sdk_session_id: str, sdk_message_uuid: str
    ) -> list[AssetLink]:
        links = [
            item
            for item in self._items.values()
            if item.sdk_session_id == sdk_session_id and item.sdk_message_uuid == sdk_message_uuid
        ]
        links.sort(key=lambda item: item.created_at)
        return [replace(item) for item in links]
