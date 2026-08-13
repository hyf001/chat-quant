from __future__ import annotations

from typing import Literal

from app.core.logging import recent_log_entries
from app.schema.logs import LogEntryResponse, LogListResponse

LogCategory = Literal["access", "business"]


class LogService:
    def list_logs(
        self,
        *,
        limit: int = 100,
        category: LogCategory | None = None,
    ) -> LogListResponse:
        return LogListResponse(
            items=[
                LogEntryResponse.model_validate(entry)
                for entry in recent_log_entries(limit, category=category)
            ]
        )


def log_service() -> LogService:
    return LogService()
