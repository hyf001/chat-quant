from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.schemas.contracts.agent_runtime import (
    AssetReference,
    ChatHistoryMessage,
    SDKStreamEnvelope,
)


@dataclass
class AgentSession:
    chat_session_id: str
    sdk_session_id: str | None
    title: str
    summary: str | None = None
    messages: list[ChatHistoryMessage] = field(default_factory=list)
    assets: list[AssetReference] = field(default_factory=list)
    cancelled: bool = False


class InMemoryAgentSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, AgentSession] = {}

    def ensure_session(
        self,
        *,
        chat_session_id: str,
        sdk_session_id: str | None,
        title: str,
    ) -> AgentSession:
        existing = self._sessions.get(chat_session_id)
        if existing is not None:
            if sdk_session_id and existing.sdk_session_id != sdk_session_id:
                existing.sdk_session_id = sdk_session_id
            return existing

        session = AgentSession(
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            title=title,
        )
        self._sessions[chat_session_id] = session
        return session

    def append_message(self, chat_session_id: str, message: ChatHistoryMessage) -> None:
        self._sessions[chat_session_id].messages.append(message)

    def append_sdk_message(
        self,
        *,
        chat_session_id: str,
        message_id: str,
        role: str,
        content: str,
    ) -> None:
        self.append_message(
            chat_session_id,
            ChatHistoryMessage(
                message_id=message_id,
                role=role,
                content=content,
                created_at=datetime.now(UTC),
            ),
        )

    def get_session(self, chat_session_id: str) -> AgentSession | None:
        return self._sessions.get(chat_session_id)

    def list_messages(self, chat_session_id: str) -> list[ChatHistoryMessage]:
        session = self._sessions.get(chat_session_id)
        if session is None:
            return []
        return list(session.messages)

    def cancel(self, chat_session_id: str) -> bool:
        session = self._sessions.get(chat_session_id)
        if session is None:
            return False
        session.cancelled = True
        return True

    def update_summary(self, chat_session_id: str, summary: str) -> None:
        self._sessions[chat_session_id].summary = summary

    def add_envelope_assets(self, chat_session_id: str, envelopes: list[SDKStreamEnvelope]) -> None:
        session = self._sessions[chat_session_id]
        known = {(asset.asset_type, asset.asset_id) for asset in session.assets}
        for envelope in envelopes:
            event = envelope.sdk_event
            artifacts = event.get("artifacts")
            if not isinstance(artifacts, list):
                continue
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    continue
                asset_type = str(artifact.get("type") or "artifact")
                asset_id = str(artifact.get("id") or artifact.get("uri") or "")
                if not asset_id or (asset_type, asset_id) in known:
                    continue
                known.add((asset_type, asset_id))
                session.assets.append(
                    AssetReference(
                        asset_type=asset_type,
                        asset_id=asset_id,
                        title=_optional_str(artifact.get("title")),
                        sdk_tool_use_id=_optional_str(event.get("tool_use_id")),
                    )
                )

    def clear(self) -> None:
        self._sessions.clear()


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
