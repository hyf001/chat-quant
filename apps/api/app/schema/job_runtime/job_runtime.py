from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.model.job_runtime.enums import InstanceStatus, TriggerType


class JobRuntimeInstanceResponse(BaseModel):
    id: str = Field(min_length=1)
    job_type: str = Field(min_length=1)
    job_id: str = Field(min_length=1)
    trigger_type: TriggerType
    trigger_key: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: int
    scheduled_for: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: InstanceStatus
    result_status: str | None = None
    summary: str = ""
    error_message: str = ""
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="forbid")


class JobRuntimeInstanceStatusCount(BaseModel):
    status: InstanceStatus
    count: int = Field(ge=0)

    model_config = ConfigDict(extra="forbid")


class JobRuntimeInstanceListResponse(BaseModel):
    items: list[JobRuntimeInstanceResponse]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_pages: int = Field(ge=0)
    status_counts: list[JobRuntimeInstanceStatusCount] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")
