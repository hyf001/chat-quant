from __future__ import annotations

from datetime import date
from math import isfinite
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.contracts.json_types import JsonObject


class BacktestMetricPayload(BaseModel):
    initial_value: float
    final_value: float
    total_return_pct: float
    annual_return_pct: float | None = None
    max_drawdown_pct: float | None = None
    max_drawdown_start: date | None = None
    max_drawdown_end: date | None = None
    max_drawdown_duration_days: int | None = None
    sharpe_ratio: float | None = None
    win_rate_pct: float | None = None
    total_trades: int = 0

    @field_validator(
        "initial_value",
        "final_value",
        "total_return_pct",
        "annual_return_pct",
        "max_drawdown_pct",
        "sharpe_ratio",
        "win_rate_pct",
    )
    @classmethod
    def validate_finite_number(cls, value: float | None) -> float | None:
        if value is not None and not isfinite(value):
            raise ValueError("metric values must be finite numbers")
        return value


class BacktestResultPayload(BaseModel):
    status: Literal["succeeded", "failed"]
    metrics: BacktestMetricPayload
    trades: list[JsonObject] = Field(default_factory=list)
    equity_curve: list[JsonObject] = Field(default_factory=list)
    drawdown_curve: list[JsonObject] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    data_source: JsonObject = Field(default_factory=dict)
    assumptions: JsonObject = Field(default_factory=dict)
