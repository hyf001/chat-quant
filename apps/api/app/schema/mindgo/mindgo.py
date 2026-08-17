from __future__ import annotations

from datetime import date, datetime, time
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schema.job_runtime import JobRuntimeInstanceResponse

type MindgoJsonScalar = str | int | float | bool | None
type MindgoJsonValue = MindgoJsonScalar | list[MindgoJsonValue] | dict[str, MindgoJsonValue]


class MindgoSourceSyncWriteMode(StrEnum):
    OVERWRITE = "overwrite"
    SKIP = "skip"


class MindgoParameterOption(BaseModel):
    label: str = Field(min_length=1)
    value: MindgoJsonScalar

    model_config = ConfigDict(extra="forbid")


class MindgoParameterSpec(BaseModel):
    name: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value_type: Literal["string", "string[]", "integer", "number", "boolean", "enum", "date"]
    required: bool = False
    default: MindgoJsonValue = None
    options: list[MindgoParameterOption] = Field(default_factory=list)
    description: str = ""
    validation: dict[str, MindgoJsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class MindgoFieldSpec(BaseModel):
    name: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value_type: Literal["string", "integer", "number", "boolean", "date"]
    required: bool = False
    description: str = ""

    model_config = ConfigDict(extra="forbid")


class MindgoSourceStorageSpec(BaseModel):
    path: str = Field(min_length=1)
    format: Literal["parquet"]
    partitioned_by: list[str] = Field(default_factory=list)
    min_partition: str | None = None
    max_partition: str | None = None
    partition_count: int = Field(default=0, ge=0)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSchema(BaseModel):
    name: str = Field(min_length=1)
    category_path: list[str] = Field(min_length=1)
    description: str = ""
    mindgo_function: str = Field(min_length=1)
    storage: MindgoSourceStorageSpec
    query_params: list[MindgoParameterSpec]
    result_schema: list[MindgoFieldSpec]

    model_config = ConfigDict(extra="forbid")


class MindgoConnectionConfig(BaseModel):
    execution_mode: Literal["jupyter"] = "jupyter"
    url: str = ""
    auth_scheme: str = "Bearer"
    token: str | None = None
    notebook_path: str = ""
    kernel_id: str | None = None
    timeout_seconds: float = Field(default=120, ge=1)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceQueryRequest(BaseModel):
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSyncRequest(BaseModel):
    start_date: date
    end_date: date
    write_mode: MindgoSourceSyncWriteMode = MindgoSourceSyncWriteMode.OVERWRITE
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_date_range(self) -> MindgoSourceSyncRequest:
        if self.start_date > self.end_date:
            msg = "start_date must be less than or equal to end_date"
            raise ValueError(msg)
        return self


class MindgoSourceSyncTriggerRequest(BaseModel):
    trigger_start_date: date
    trigger_end_date: date
    trigger_time: time
    write_mode: MindgoSourceSyncWriteMode = MindgoSourceSyncWriteMode.OVERWRITE
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_date_range(self) -> MindgoSourceSyncTriggerRequest:
        if self.trigger_start_date > self.trigger_end_date:
            msg = "trigger_start_date must be less than or equal to trigger_end_date"
            raise ValueError(msg)
        return self


class MindgoSourceSyncResult(BaseModel):
    status: Literal["success", "failed"]
    elapsed_ms: int = Field(ge=0)
    synced_count: int = Field(ge=0)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSyncTriggerResponse(BaseModel):
    instance: JobRuntimeInstanceResponse
    instances: list[JobRuntimeInstanceResponse] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSyncSchedulerRequest(BaseModel):
    cron: str = Field(min_length=1, max_length=120)
    write_mode: MindgoSourceSyncWriteMode = MindgoSourceSyncWriteMode.OVERWRITE
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSyncSchedulerState(BaseModel):
    configured: bool
    scheduler_id: str | None = None
    cron: str | None = None
    write_mode: MindgoSourceSyncWriteMode = MindgoSourceSyncWriteMode.OVERWRITE
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSyncStatusResponse(BaseModel):
    source_id: str = Field(min_length=1)
    job_type: str = Field(min_length=1)
    job_id: str = Field(min_length=1)
    scheduler: MindgoSourceSyncSchedulerState

    model_config = ConfigDict(extra="forbid")


class MindgoSourceSummary(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category_path: list[str] = Field(min_length=1)
    description: str = ""
    storage: MindgoSourceStorageSpec

    model_config = ConfigDict(extra="forbid")


class MindgoSourceListResponse(BaseModel):
    sources: list[MindgoSourceSummary]

    model_config = ConfigDict(extra="forbid")


class MindgoSourceQueryResponse(BaseModel):
    source_id: str = Field(min_length=1)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    columns: list[MindgoFieldSpec]
    rows: list[dict[str, MindgoJsonValue]]

    model_config = ConfigDict(extra="forbid")


class MindgoConnectionTestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MindgoConnectionTestResponse(BaseModel):
    ok: bool
    message: str

    model_config = ConfigDict(extra="forbid")
