from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from app.schemas.contracts.agent_runtime import SDKStreamEnvelope


class InMemoryStreamRelay:
    def __init__(self) -> None:
        self._streams: dict[str, list[SDKStreamEnvelope]] = defaultdict(list)

    def publish(
        self,
        chat_session_id: str,
        sdk_session_id: str | None,
        sdk_event: dict[str, object],
    ) -> SDKStreamEnvelope:
        sequence = len(self._streams[chat_session_id]) + 1
        envelope = SDKStreamEnvelope(
            sequence=sequence,
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            received_at=datetime.now(UTC),
            sdk_event=sdk_event,
        )
        self._streams[chat_session_id].append(envelope)
        return envelope

    def list_envelopes(self, chat_session_id: str, after: int = 0) -> list[SDKStreamEnvelope]:
        return [
            envelope
            for envelope in self._streams.get(chat_session_id, [])
            if envelope.sequence > after
        ]

    def latest_sequence(self, chat_session_id: str) -> int:
        envelopes = self._streams.get(chat_session_id, [])
        return envelopes[-1].sequence if envelopes else 0

    def clear(self) -> None:
        self._streams.clear()
