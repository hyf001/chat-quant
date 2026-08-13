from __future__ import annotations

import json
import os
from collections import deque
from pathlib import Path
from typing import Literal

from app.schema.logs import LogEntryResponse, LogListResponse

LogCategory = Literal["access", "business"]
_DEFAULT_SCAN_LINES = 5000


class LogService:
    def __init__(self, log_file: Path | None = None) -> None:
        self._log_file = log_file or _default_log_file()

    def list_logs(
        self,
        *,
        limit: int = 100,
        category: LogCategory | None = None,
    ) -> LogListResponse:
        bounded_limit = min(max(limit, 1), 500)
        entries: list[dict[str, object]] = []
        for payload in reversed(_read_recent_json_lines(self._log_file)):
            if category is not None and payload.get("category") != category:
                continue
            entries.append(payload)
            if len(entries) >= bounded_limit:
                break
        entries.reverse()
        return LogListResponse(items=[LogEntryResponse.model_validate(entry) for entry in entries])


def log_service() -> LogService:
    return LogService()


def _read_recent_json_lines(log_file: Path) -> list[dict[str, object]]:
    if not log_file.exists():
        return []
    lines: deque[str] = deque(maxlen=_DEFAULT_SCAN_LINES)
    try:
        with log_file.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                lines.append(line)
    except OSError:
        return []

    payloads: list[dict[str, object]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            normalized = _normalize_log_entry(payload)
            if normalized is not None:
                payloads.append(normalized)
    return payloads


def _normalize_log_entry(payload: dict[str, object]) -> dict[str, object] | None:
    required_keys = ("timestamp", "level", "logger", "message")
    if not all(isinstance(payload.get(key), str) for key in required_keys):
        return None
    category = payload.get("category")
    if not isinstance(category, str):
        category = _category_from_logger(str(payload["logger"]))
    return {**payload, "category": category, "request_id": payload.get("request_id") or "-"}


def _category_from_logger(logger: str) -> str:
    if logger in {"app.request", "uvicorn.access"}:
        return "access"
    if logger.startswith("app."):
        return "business"
    return "system"


def _default_log_file() -> Path:
    override = os.environ.get("CHATQ_API_LOG_FILE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[5] / ".dev" / "logs" / "web-api.log"
