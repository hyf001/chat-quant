from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

type MindgoJsonScalar = str | int | float | bool | None
type MindgoJsonValue = MindgoJsonScalar | list[MindgoJsonValue] | dict[str, MindgoJsonValue]


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


class MindgoDatasetStorageSpec(BaseModel):
    path: str = Field(min_length=1)
    format: Literal["parquet"]
    partitioned_by: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class MindgoDatasetSchema(BaseModel):
    name: str = Field(min_length=1)
    category_path: list[str] = Field(min_length=1)
    description: str = ""
    mindgo_function: str = Field(min_length=1)
    storage: MindgoDatasetStorageSpec
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


class MindgoDatasetQueryRequest(BaseModel):
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)

    model_config = ConfigDict(extra="forbid")


class MindgoDatasetSyncRequest(BaseModel):
    start_date: date
    end_date: date
    params: dict[str, MindgoJsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_date_range(self) -> MindgoDatasetSyncRequest:
        if self.start_date > self.end_date:
            msg = "start_date must be less than or equal to end_date"
            raise ValueError(msg)
        return self


class MindgoDatasetSyncResult(BaseModel):
    status: Literal["success", "failed"]
    elapsed_ms: int = Field(ge=0)
    synced_count: int = Field(ge=0)

    model_config = ConfigDict(extra="forbid")


class MindgoDatasetSummary(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category_path: list[str] = Field(min_length=1)
    description: str = ""
    actions: list[Literal["get_schema", "query", "sync"]]

    model_config = ConfigDict(extra="forbid")


class MindgoDatasetListResponse(BaseModel):
    datasets: list[MindgoDatasetSummary]

    model_config = ConfigDict(extra="forbid")


class MindgoDatasetQueryResponse(BaseModel):
    dataset_id: str = Field(min_length=1)
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
