from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_DUCKDB_VIEW_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
type DatasetJsonScalar = str | int | float | bool | None
type DatasetJsonValue = DatasetJsonScalar | list[DatasetJsonValue] | dict[str, DatasetJsonValue]


class DatasetPayload(BaseModel):
    id: str | None = Field(default=None, min_length=1, max_length=64)
    name: str = Field(
        min_length=1,
        max_length=128,
        description="DuckDB view name bound to this dataset.",
    )
    description: str = Field(default="", max_length=2000)
    category_path: list[str] = Field(min_length=1)
    exposed_to_agent: bool = False
    create_sql: str = Field(
        min_length=1,
        description="DuckDB CREATE VIEW statement used to bind the dataset name.",
    )

    model_config = ConfigDict(extra="forbid")

    @field_validator("id", "name")
    @classmethod
    def validate_non_empty_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            msg = "value must contain non-whitespace characters"
            raise ValueError(msg)
        return stripped

    @field_validator("name")
    @classmethod
    def validate_duckdb_view_name(cls, value: str) -> str:
        if not _DUCKDB_VIEW_NAME_PATTERN.match(value):
            msg = "name must be a valid DuckDB view identifier"
            raise ValueError(msg)
        return value

    @field_validator("create_sql")
    @classmethod
    def validate_create_sql(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "create_sql must contain non-whitespace characters"
            raise ValueError(msg)
        return stripped

    @model_validator(mode="after")
    def validate_category_path(self) -> DatasetPayload:
        cleaned = [part.strip() for part in self.category_path if part.strip()]
        if not cleaned:
            msg = "category_path must contain at least one non-empty item"
            raise ValueError(msg)
        self.category_path = cleaned
        return self


class DatasetUpdatePayload(BaseModel):
    description: str | None = Field(default=None, max_length=2000)
    category_path: list[str] | None = None
    exposed_to_agent: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_category_path(self) -> DatasetUpdatePayload:
        if self.category_path is None:
            return self
        cleaned = [part.strip() for part in self.category_path if part.strip()]
        if not cleaned:
            msg = "category_path must contain at least one non-empty item"
            raise ValueError(msg)
        self.category_path = cleaned
        return self


class DatasetQueryPayload(BaseModel):
    sql: str = Field(min_length=1)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)

    model_config = ConfigDict(extra="forbid")

    @field_validator("sql")
    @classmethod
    def validate_sql(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "sql must contain non-whitespace characters"
            raise ValueError(msg)
        return stripped


class DatasetResponse(BaseModel):
    id: str
    name: str
    description: str
    category_path: list[str]
    exposed_to_agent: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="forbid")


class DatasetDetailResponse(DatasetResponse):
    create_sql: str


class DatasetListResponse(BaseModel):
    datasets: list[DatasetResponse]

    model_config = ConfigDict(extra="forbid")


class DatasetQueryColumn(BaseModel):
    name: str
    value_type: str

    model_config = ConfigDict(extra="forbid")


class DatasetQueryResponse(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    columns: list[DatasetQueryColumn]
    rows: list[dict[str, DatasetJsonValue]]

    model_config = ConfigDict(extra="forbid")
