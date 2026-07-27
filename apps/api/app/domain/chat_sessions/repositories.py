from __future__ import annotations

from app.domain.chat_sessions.models import AssetLink, ChatSession


class ChatSessionNotFoundError(LookupError):
    pass


class ChatSessionRepository:
    async def create(self, session: ChatSession) -> ChatSession:
        raise NotImplementedError

    async def update(self, session: ChatSession) -> ChatSession:
        raise NotImplementedError

    async def get(self, chat_session_id: str) -> ChatSession | None:
        raise NotImplementedError

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
        raise NotImplementedError


class AssetLinkRepository:
    async def upsert(self, link: AssetLink) -> AssetLink:
        raise NotImplementedError

    async def list_for_chat_session(self, chat_session_id: str) -> list[AssetLink]:
        raise NotImplementedError

    async def list_for_sdk_message(
        self, *, sdk_session_id: str, sdk_message_uuid: str
    ) -> list[AssetLink]:
        raise NotImplementedError
