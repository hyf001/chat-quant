from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LogEntryResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    timestamp: str
    level: str
    logger: str
    message: str
    request_id: str
    category: str
    method: str | None = None
    path: str | None = None
    status_code: int | None = None
    duration_ms: int | None = None
    client_host: str | None = None
    error: str | None = None
    exception: str | None = None
    stack: str | None = None


class LogListResponse(BaseModel):
    items: list[LogEntryResponse] = Field(default_factory=list)
