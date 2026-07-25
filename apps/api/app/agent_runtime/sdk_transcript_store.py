from __future__ import annotations

from dataclasses import asdict, is_dataclass

from claude_agent_sdk import get_session_messages


class ClaudeSDKTranscriptReader:
    def __init__(self, directory: str | None = None) -> None:
        self.directory = directory

    def get_messages(
        self,
        sdk_session_id: str,
        limit: int | None = None,
    ) -> list[dict[str, object]]:
        messages = get_session_messages(
            sdk_session_id,
            directory=self.directory,
            limit=limit,
        )
        return [_to_jsonable(message) for message in messages]


def _to_jsonable(value: object) -> dict[str, object]:
    if is_dataclass(value):
        converted = asdict(value)
    elif hasattr(value, "model_dump"):
        converted = value.model_dump(mode="json")  # type: ignore[union-attr]
    elif isinstance(value, dict):
        converted = value
    else:
        converted = {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    normalized = _normalize_json_value(converted)
    if isinstance(normalized, dict):
        return normalized
    return {"value": normalized}


def _normalize_json_value(value: object) -> object:
    if is_dataclass(value):
        return _normalize_json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _normalize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    return str(value)
