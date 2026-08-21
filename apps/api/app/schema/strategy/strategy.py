from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

StrategyParamValue = int | float | str | bool
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def local_now() -> datetime:
    return datetime.now()


class StrategyStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class StrategyMode(StrEnum):
    SINGLE_SYMBOL = "single_symbol"
    MULTI_SYMBOL = "multi_symbol"
    PORTFOLIO = "portfolio"
    UNIVERSE_SELECTION = "universe_selection"


class StrategyDeploymentMode(StrEnum):
    SIGNAL = "signal"
    PAPER = "paper"
    LIVE = "live"


class StrategySignalStatus(StrEnum):
    GENERATED = "generated"
    REJECTED = "rejected"
    CONVERTED = "converted"
    IGNORED = "ignored"


class StrategySignalActionType(StrEnum):
    BUY = "buy"
    SELL = "sell"
    CLOSE = "close"
    CANCEL = "cancel"


class StrategySignalAction(BaseModel):
    action: StrategySignalActionType
    symbol: str | None = Field(default=None, min_length=1, max_length=64)
    order_type: Literal["market", "limit"] | None = None
    size: float | None = None
    price: float | None = None
    ref: str | int | None = None
    reason: str | None = None
    client_signal_id: str | None = Field(default=None, min_length=1, max_length=128)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_action(self) -> StrategySignalAction:
        if self.action == StrategySignalActionType.CANCEL:
            if not self.ref:
                raise ValueError("cancel action must define ref")
            return self
        if not self.symbol:
            raise ValueError(f"{self.action} action must define symbol")
        if self.action in {StrategySignalActionType.BUY, StrategySignalActionType.SELL}:
            if self.size is None or self.size <= 0:
                raise ValueError(f"{self.action} action must define size > 0")
            if self.order_type == "limit" and self.price is None:
                raise ValueError("limit order must define price")
            return self
        if (
            self.action == StrategySignalActionType.CLOSE
            and self.size is not None
            and self.size <= 0
        ):
            raise ValueError("close action size must be empty or > 0")
        return self


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
    created_at: datetime = Field(default_factory=local_now)
    updated_at: datetime = Field(default_factory=local_now)


class StrategyVersionRecord(BaseModel):
    id: str
    strategy_id: str
    version: int
    source_code: str
    strategy_mode: StrategyMode = StrategyMode.SINGLE_SYMBOL
    custom_params: list[StrategyCustomParameter] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=local_now)


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


class StrategyDeploymentCreate(BaseModel):
    project_id: str = Field(min_length=1, max_length=128)
    strategy_id: str = Field(min_length=1, max_length=64)
    strategy_version_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    mode: StrategyDeploymentMode = StrategyDeploymentMode.SIGNAL
    symbols: list[str] = Field(default_factory=list)
    lookback_bars: int = Field(default=250, ge=1, le=10000)
    params: dict[str, JsonValue] = Field(default_factory=dict)
    broker_id: str | None = Field(default=None, max_length=128)
    requires_manual_confirm: bool = True
    risk_config: dict[str, JsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_deployment(self) -> StrategyDeploymentCreate:
        if self.mode == StrategyDeploymentMode.SIGNAL:
            return self
        if not self.broker_id:
            raise ValueError("broker_id is required for paper/live deployments")
        return self


class StrategyDeploymentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    strategy_version_id: str | None = Field(default=None, min_length=1, max_length=64)
    mode: StrategyDeploymentMode | None = None
    symbols: list[str] | None = None
    lookback_bars: int | None = Field(default=None, ge=1, le=10000)
    params: dict[str, JsonValue] | None = None
    broker_id: str | None = Field(default=None, max_length=128)
    requires_manual_confirm: bool | None = None
    risk_config: dict[str, JsonValue] | None = None
    state: dict[str, JsonValue] | None = None

    model_config = ConfigDict(extra="forbid")


class StrategyDeploymentRecord(BaseModel):
    id: str
    project_id: str
    strategy_id: str
    strategy_version_id: str
    name: str
    mode: StrategyDeploymentMode = StrategyDeploymentMode.SIGNAL
    scheduled: bool = False
    schedule_cron: str | None = None
    scheduler_id: str | None = None
    symbols: list[str] = Field(default_factory=list)
    lookback_bars: int = 250
    params: dict[str, JsonValue] = Field(default_factory=dict)
    broker_id: str | None = None
    requires_manual_confirm: bool = True
    risk_config: dict[str, JsonValue] = Field(default_factory=dict)
    state: dict[str, JsonValue] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=local_now)
    updated_at: datetime = Field(default_factory=local_now)


class StrategySignalRecord(BaseModel):
    id: str
    deployment_id: str
    job_instance_id: str | None = None
    strategy_version_id: str
    signal_datetime: datetime
    action: dict[str, JsonValue]
    status: StrategySignalStatus = StrategySignalStatus.GENERATED
    reason: str | None = None
    created_at: datetime = Field(default_factory=local_now)


class StrategySignalActionCount(BaseModel):
    action: StrategySignalActionType
    count: int = 0


class StrategySignalListResponse(BaseModel):
    items: list[StrategySignalRecord] = Field(default_factory=list)
    total: int = 0
    limit: int = 100
    offset: int = 0
    action_counts: list[StrategySignalActionCount] = Field(default_factory=list)


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
