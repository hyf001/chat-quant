from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonScalar] | dict[str, JsonScalar]


class BacktestRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


class BacktestRunMode(StrEnum):
    SYNC = "sync"
    ASYNC = "async"


class TradeSide(StrEnum):
    BUY = "buy"
    SELL = "sell"
    SHORT = "short"
    COVER = "cover"


class TradeStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"
    PARTIAL = "partial"


class CurveType(StrEnum):
    EQUITY = "equity"
    DRAWDOWN = "drawdown"
    BENCHMARK_EQUITY = "benchmark_equity"
    BENCHMARK_DRAWDOWN = "benchmark_drawdown"


class BacktestConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbols: list[str] = Field(min_length=1)
    universe_ref: str | None = None
    market: str = Field(min_length=1)
    benchmark_symbol: str | None = None
    start_date: date
    end_date: date
    timeframe: str = "1d"
    data_source: str = "akshare"
    data_adjust: str = "qfq"
    data_as_of: datetime | None = None
    initial_cash: Decimal = Field(gt=0)
    commission: Decimal = Field(ge=0)
    slippage: Decimal = Field(default=Decimal("0"), ge=0)
    tax: Decimal | None = Field(default=None, ge=0)
    order_size_mode: str = "percent_cash"
    params: dict[str, JsonValue] = Field(default_factory=dict)
    risk_free_rate: Decimal = Decimal("0")
    calendar: str = "CN_A_SHARE"
    currency: str = "CNY"
    assumptions: list[str] = Field(default_factory=list)
    symbol_order_mode: Literal["preserve", "sorted"] = "preserve"

    @field_validator("symbols")
    @classmethod
    def normalize_symbols(cls, symbols: list[str]) -> list[str]:
        normalized = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
        if not normalized:
            raise ValueError("symbols must contain at least one non-empty symbol")
        return normalized

    @model_validator(mode="after")
    def validate_date_range(self) -> BacktestConfig:
        if self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return self


class CreateBacktestRunRequest(BaseModel):
    chat_session_id: str
    strategy_version_id: str
    symbols: list[str] = Field(min_length=1)
    market: str
    start_date: date
    end_date: date
    initial_cash: Decimal = Field(gt=0)
    commission: Decimal = Field(ge=0)
    user_id: str | None = None
    project_id: str | None = None
    strategy_id: str | None = None
    code_artifact_id: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    benchmark_symbol: str | None = None
    universe_ref: str | None = None
    timeframe: str = "1d"
    data_source: str = "akshare"
    data_adjust: str = "qfq"
    data_as_of: datetime | None = None
    slippage: Decimal = Field(default=Decimal("0"), ge=0)
    tax: Decimal | None = Field(default=None, ge=0)
    order_size_mode: str = "percent_cash"
    params: dict[str, JsonValue] = Field(default_factory=dict)
    risk_free_rate: Decimal = Decimal("0")
    calendar: str = "CN_A_SHARE"
    currency: str = "CNY"
    assumptions: list[str] = Field(default_factory=list)


class RunBacktestRequest(BaseModel):
    mode: BacktestRunMode = BacktestRunMode.SYNC
    timeout_seconds: Annotated[int, Field(gt=0, le=900)] = 300


class RerunBacktestRequest(BaseModel):
    override_config: dict[str, JsonValue] = Field(default_factory=dict)
    strategy_version_id: str | None = None
    run_immediately: bool = False


class CompareBacktestsRequest(BaseModel):
    backtest_run_ids: list[str] = Field(min_length=2, max_length=5)
    base_backtest_run_id: str | None = None
    curve_sampling: Literal["daily", "weekly", "monthly"] = "daily"


class BacktestMetrics(BaseModel):
    initial_value: Decimal
    final_value: Decimal
    total_return_pct: Decimal
    annual_return_pct: Decimal | None = None
    max_drawdown_pct: Decimal
    max_drawdown_abs_pct: Decimal
    max_drawdown_start: date | None = None
    max_drawdown_end: date | None = None
    max_drawdown_recovery_date: date | None = None
    max_drawdown_duration_days: int | None = None
    volatility_annual_pct: Decimal | None = None
    sharpe_ratio: Decimal | None = None
    sortino_ratio: Decimal | None = None
    calmar_ratio: Decimal | None = None
    win_rate_pct: Decimal | None = None
    total_trades: int
    profit_factor: Decimal | None = None
    turnover_rate: Decimal | None = None
    annualization_basis: Literal["calendar_days", "trading_days"] = "calendar_days"
    trade_count_basis: Literal["closed_trade", "order_fill"] = "closed_trade"


class BacktestResultDTO(BaseModel):
    id: str
    backtest_run_id: str
    summary: str
    metrics: BacktestMetrics
    benchmark_metrics: BacktestMetrics | None = None
    warnings: list[str]
    config_snapshot: BacktestConfig
    artifact_refs: dict[str, str]
    created_at: datetime


class TradeRecordDTO(BaseModel):
    id: str
    backtest_run_id: str
    symbol: str
    order_id: str | None = None
    trade_id: str | None = None
    side: TradeSide
    status: TradeStatus
    trade_datetime: datetime
    price: Decimal
    size: Decimal
    value: Decimal
    commission: Decimal
    pnl: Decimal | None = None
    pnl_pct: Decimal | None = None
    holding_days: int | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class CurvePointDTO(BaseModel):
    date: date
    value: Decimal
    normalized_value: Decimal | None = None
    benchmark_value: Decimal | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class CurveArtifactDTO(BaseModel):
    id: str
    backtest_run_id: str
    backtest_result_id: str
    curve_type: CurveType
    storage_mode: Literal["inline_points", "artifact_file", "hybrid"] = "inline_points"
    artifact_file_id: str | None = None
    point_count: int
    start_date: date
    end_date: date
    sampling: Literal["daily", "weekly", "monthly"] = "daily"
    metadata: dict[str, JsonValue] = Field(default_factory=dict)
    points: list[CurvePointDTO] = Field(default_factory=list)
    created_at: datetime


class BacktestRunDTO(BaseModel):
    id: str
    user_id: str
    project_id: str
    chat_session_id: str
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    strategy_id: str
    strategy_version_id: str
    code_artifact_id: str
    runtime_artifact_id: str | None = None
    parent_backtest_run_id: str | None = None
    status: BacktestRunStatus
    config: BacktestConfig
    config_hash: str
    execution_result_id: str | None = None
    result_id: str | None = None
    failure_code: str | None = None
    failure_message: str | None = None
    failure_detail: dict[str, JsonValue] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class BacktestDetailDTO(BaseModel):
    run: BacktestRunDTO
    result: BacktestResultDTO | None = None
    trades: list[TradeRecordDTO] = Field(default_factory=list)
    curves: list[CurveArtifactDTO] = Field(default_factory=list)


class BacktestComparisonMetricRow(BaseModel):
    backtest_run_id: str
    strategy_version_id: str
    summary: str
    annual_return_pct: Decimal | None
    total_return_pct: Decimal
    max_drawdown_pct: Decimal
    sharpe_ratio: Decimal | None
    win_rate_pct: Decimal | None
    total_trades: int


class BacktestComparisonSeries(BaseModel):
    backtest_run_id: str
    label: str
    points: list[CurvePointDTO]


class BacktestComparisonDifference(BaseModel):
    metric: str
    best_backtest_run_id: str
    worst_backtest_run_id: str
    spread: Decimal


class BacktestComparisonDTO(BaseModel):
    comparison_id: str
    base_backtest_run_id: str | None
    backtest_run_ids: list[str]
    metrics_table: list[BacktestComparisonMetricRow]
    equity_series: list[BacktestComparisonSeries]
    drawdown_series: list[BacktestComparisonSeries]
    differences: list[BacktestComparisonDifference]
    warnings: list[str]
