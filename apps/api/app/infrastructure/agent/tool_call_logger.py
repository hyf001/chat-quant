from __future__ import annotations

import json

from app.schemas.contracts.agent_runtime import SDKToolUseRef

SENSITIVE_MARKERS = ("token", "api_key", "apikey", "secret", "cookie", "password")


class ToolCallLogger:
    def __init__(self, stdout_limit_bytes: int = 4096) -> None:
        self.stdout_limit_bytes = stdout_limit_bytes

    def from_tool_use(
        self,
        *,
        event: dict[str, object],
        chat_session_id: str,
        sdk_session_id: str,
    ) -> SDKToolUseRef | None:
        if event.get("type") != "tool_use" or event.get("name") != "Bash":
            return None
        sdk_tool_use_id = str(event.get("id") or "")
        bash_command = str(event.get("command") or "")
        if not sdk_tool_use_id or not bash_command:
            return None
        return SDKToolUseRef(
            sdk_tool_use_id=sdk_tool_use_id,
            sdk_message_uuid=_optional_str(event.get("message_id")),
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            bash_command=bash_command,
            chatq_command=_extract_chatq_command(bash_command),
            input_preview=self._redact(bash_command[: self.stdout_limit_bytes]),
        )

    def merge_tool_result(
        self,
        tool_use: SDKToolUseRef,
        result_event: dict[str, object],
    ) -> SDKToolUseRef:
        content = str(result_event.get("content") or "")
        parsed = _parse_json_object(content)
        output_ref = None
        if parsed is not None:
            artifacts = parsed.get("artifacts")
            if isinstance(artifacts, list) and artifacts:
                first = artifacts[0]
                if isinstance(first, dict):
                    output_ref = str(first.get("id") or first.get("uri") or "") or None
        return tool_use.model_copy(
            update={
                "tool_result_json": parsed,
                "is_error": bool(result_event.get("is_error")) or (parsed or {}).get("ok") is False,
                "output_ref": output_ref,
            }
        )

    def _redact(self, value: str) -> str:
        redacted = value
        lower_value = value.lower()
        for marker in SENSITIVE_MARKERS:
            if marker in lower_value:
                redacted = "[REDACTED]"
                break
        return redacted


def _extract_chatq_command(command: str) -> str | None:
    parts = command.strip().split()
    if len(parts) < 3 or parts[0] != "chatq":
        return None
    return " ".join(parts[:3])


def _parse_json_object(value: str) -> dict[str, object] | None:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
