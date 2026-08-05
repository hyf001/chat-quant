from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

StrategyParamValue = int | float | str | bool
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def utc_now() -> datetime:
    return datetime.now(UTC)


class StrategyStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class StrategyMode(StrEnum):
    SINGLE_SYMBOL = "single_symbol"
    MULTI_SYMBOL = "multi_symbol"
    PORTFOLIO = "portfolio"
    UNIVERSE_SELECTION = "universe_selection"


class StrategyCustomParameter(BaseModel):
    name_cn: str = Field(min_length=1, max_length=64)
    name_en: str = Field(min_length=1, max_length=64)
    type: Literal["integer", "number", "string", "boolean"]
    default: StrategyParamValue
    required: bool = True

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_parameter(self) -> StrategyCustomParameter:
        if not self.name_en.isidentifier():
            raise ValueError(f"name_en must be a Python identifier: {self.name_en}")
        validate_param_value(self.name_en, self.default, self.type)
        return self


class StrategyVersionCreate(BaseModel):
    source_code: str = Field(min_length=1)
    strategy_mode: StrategyMode = StrategyMode.SINGLE_SYMBOL
    risk_notes: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class StrategyCreate(StrategyVersionCreate):
    name: str = Field(min_length=1, max_length=128)
    description: str | None = None


class StrategyRecord(BaseModel):
    id: str
    project_id: str
    name: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    current_version_id: str | None = None
    status: StrategyStatus = StrategyStatus.ACTIVE
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StrategyVersionRecord(BaseModel):
    id: str
    strategy_id: str
    version: int
    source_code: str
    strategy_mode: StrategyMode = StrategyMode.SINGLE_SYMBOL
    custom_params: list[StrategyCustomParameter] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class StrategySummary(BaseModel):
    strategy_id: str
    strategy_version_id: str
    version: int
    name: str
    status: StrategyStatus
    tags: list[str]
    strategy_mode: StrategyMode
    custom_params: list[StrategyCustomParameter]
    updated_at: datetime


class StrategyDetail(BaseModel):
    strategy: StrategyRecord


class StrategyCreateResult(BaseModel):
    strategy_id: str


class StrategyValidationIssue(BaseModel):
    code: str
    message: str
    severity: Literal["error", "warning"] = "error"
    detail: dict[str, JsonValue] = Field(default_factory=dict)


def validate_param_value(
    name: str,
    value: StrategyParamValue,
    param_type: Literal["integer", "number", "string", "boolean"],
) -> None:
    if param_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        raise ValueError(f"{name} must be an integer")
    if param_type == "number" and (not isinstance(value, int | float) or isinstance(value, bool)):
        raise ValueError(f"{name} must be a number")
    if param_type == "string" and not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if param_type == "boolean" and not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
