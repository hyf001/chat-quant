from __future__ import annotations

from dataclasses import asdict, is_dataclass


def parse_sdk_message(message: object) -> dict[str, object]:
    data = _to_jsonable(message)
    message_type = _sdk_type_name(message)
    if message_type:
        data.setdefault("type", message_type)
    if data.get("message_id") and not data.get("id"):
        data["id"] = data["message_id"]
    data = _normalize_session_message(data)
    data = _normalize_sdk_content_blocks(data)
    if data.get("type") == "stream_event":
        return _unwrap_stream_event(data)
    return data


def enrich_sdk_event_with_artifacts(event: dict[str, object]) -> dict[str, object]:
    artifacts = _extract_artifacts_from_event(event)
    if artifacts and "artifacts" not in event:
        return {**event, "artifacts": artifacts}
    return event


def extract_sdk_session_id(event: dict[str, object]) -> str | None:
    session_id = event.get("session_id")
    if isinstance(session_id, str) and session_id:
        return session_id

    data = event.get("data")
    if isinstance(data, dict):
        data_session_id = data.get("session_id")
        if isinstance(data_session_id, str) and data_session_id:
            return data_session_id

    message = event.get("message")
    if isinstance(message, dict):
        message_session_id = message.get("session_id")
        if isinstance(message_session_id, str) and message_session_id:
            return message_session_id

    return None


def _unwrap_stream_event(event: dict[str, object]) -> dict[str, object]:
    inner_event = event.get("event")
    if not isinstance(inner_event, dict):
        return event
    unwrapped = {
        **inner_event,
        "uuid": event.get("uuid"),
        "session_id": event.get("session_id"),
        "parent_tool_use_id": event.get("parent_tool_use_id"),
    }
    unwrapped.setdefault("type", "stream_event")
    return unwrapped


def _sdk_type_name(message: object) -> str:
    name = message.__class__.__name__
    mapping = {
        "AssistantMessage": "assistant_message",
        "UserMessage": "user_message",
        "SystemMessage": "system_message",
        "ResultMessage": "result_message",
        "StreamEvent": "stream_event",
        "RateLimitEvent": "rate_limit_event",
    }
    return mapping.get(name, name)


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


def _normalize_sdk_content_blocks(event: dict[str, object]) -> dict[str, object]:
    content = event.get("content")
    if not isinstance(content, list):
        return event
    return {
        **event,
        "content": [
            _normalize_sdk_content_block(block) if isinstance(block, dict) else block
            for block in content
        ],
    }


def _normalize_session_message(event: dict[str, object]) -> dict[str, object]:
    sdk_type = event.get("type")
    if sdk_type not in {"user", "assistant"}:
        return event

    raw_message = event.get("message")
    message = raw_message if isinstance(raw_message, dict) else {}
    content = message.get("content", raw_message)
    normalized_type = "user_message" if sdk_type == "user" else "assistant_message"
    normalized = {
        **event,
        "type": normalized_type,
        "content": content,
    }
    message_id = event.get("uuid") or message.get("id") or message.get("message_id")
    if isinstance(message_id, str) and message_id:
        normalized.setdefault("id", message_id)
    return normalized


def _normalize_sdk_content_block(block: dict[str, object]) -> dict[str, object]:
    if "type" in block:
        return block
    if "text" in block:
        return {"type": "text", **block}
    if "id" in block and "name" in block and "input" in block:
        return {"type": "tool_use", **block}
    if "tool_use_id" in block:
        return {"type": "tool_result", **block}
    if "thinking" in block:
        return {"type": "thinking", **block}
    return block


def _extract_tool_result_events(event: dict[str, object]) -> list[dict[str, object]]:
    if event.get("type") == "tool_result":
        return [event]
    content = event.get("content")
    if not isinstance(content, list):
        return []
    result_events: list[dict[str, object]] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_result":
            continue
        result_events.append(
            {
                "type": "tool_result",
                "tool_use_id": str(block.get("tool_use_id") or ""),
                "content": block.get("content"),
                "is_error": block.get("is_error"),
            }
        )
    return result_events


def _extract_artifacts_from_event(event: dict[str, object]) -> list[dict[str, object]]:
    artifacts: list[dict[str, object]] = []
    for tool_result in _extract_tool_result_events(event):
        content = tool_result.get("content")
        if not isinstance(content, str):
            continue
        parsed = _parse_json_object(content)
        if parsed is None:
            continue
        parsed_artifacts = parsed.get("artifacts")
        if not isinstance(parsed_artifacts, list):
            continue
        for artifact in parsed_artifacts:
            if isinstance(artifact, dict):
                artifacts.append(artifact)
    return artifacts


def _parse_json_object(value: str) -> dict[str, object] | None:
    import json

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None
