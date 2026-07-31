from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def utc_now() -> datetime:
    return datetime.now(UTC)


class StrategyBacktestStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


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


class StrategyBacktestConfig(BaseModel):
    symbols: list[str] = Field(min_length=1)
    market: Literal["CN", "US"] = "CN"
    benchmark_symbol: str | None = None
    start_date: date
    end_date: date
    timeframe: Literal["1d"] = "1d"
    initial_cash: Decimal = Field(gt=0)
    commission: Decimal = Field(ge=0)
    slippage: Decimal = Field(default=Decimal("0"), ge=0)
    data_adjust: str = "qfq"
    params: dict[str, JsonValue] = Field(default_factory=dict)
    currency: str = "CNY"

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_run_config(self) -> StrategyBacktestConfig:
        symbols = [symbol.strip().upper() for symbol in self.symbols if symbol.strip()]
        if not symbols:
            raise ValueError("symbols must contain at least one non-empty symbol")
        self.symbols = symbols
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        if self.end_date > date.today():
            raise ValueError("end_date cannot be in the future")
        return self


class StrategyBacktestRecord(BaseModel):
    id: str
    user_id: str
    project_id: str
    strategy_id: str
    strategy_version_id: str
    status: StrategyBacktestStatus = StrategyBacktestStatus.PENDING
    config: StrategyBacktestConfig
    execution_engine: str | None = None
    result_id: str | None = None
    failure_code: str | None = None
    failure_message: str | None = None
    failure_detail: dict[str, JsonValue] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StrategyBacktestMetrics(BaseModel):
    initial_value: Decimal
    final_value: Decimal
    total_return_pct: Decimal
    annual_return_pct: Decimal | None = None
    max_drawdown_pct: Decimal
    max_drawdown_start: date | None = None
    max_drawdown_end: date | None = None
    max_drawdown_duration_days: int | None = None
    sharpe_ratio: Decimal | None = None
    win_rate_pct: Decimal | None = None
    total_trades: int


class StrategyTradeRecord(BaseModel):
    id: str
    strategy_backtest_id: str
    symbol: str
    side: TradeSide
    status: TradeStatus
    trade_datetime: datetime
    price: Decimal
    size: Decimal
    value: Decimal
    commission: Decimal = Decimal("0")
    pnl: Decimal | None = None
    pnl_pct: Decimal | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class StrategyCurvePoint(BaseModel):
    date: date
    value: Decimal
    normalized_value: Decimal | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class StrategyCurve(BaseModel):
    id: str
    strategy_backtest_id: str
    strategy_backtest_result_id: str
    curve_type: CurveType
    point_count: int
    start_date: date
    end_date: date
    points: list[StrategyCurvePoint] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class StrategyBacktestResultRecord(BaseModel):
    id: str
    strategy_backtest_id: str
    summary: str
    metrics: StrategyBacktestMetrics
    trades: list[StrategyTradeRecord] = Field(default_factory=list)
    curves: list[StrategyCurve] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    engine: str
    protocol: str
    data_source: dict[str, JsonValue] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class StrategyBacktestDetail(BaseModel):
    backtest: StrategyBacktestRecord
    result: StrategyBacktestResultRecord | None = None


class StrategyBacktestProtocol(BaseModel):
    name: str = "chatq_backtrader_strategy_v1"
    entrypoint_format: str = "<relative_python_file.py>:<StrategyClassName>"
    base_class: str = "backtrader.Strategy"
    required_contract: list[str] = Field(
        default_factory=lambda: [
            "The entrypoint class must subclass backtrader.Strategy.",
            (
                "Strategy parameters must be declared through params and are injected "
                "from StrategyBacktestConfig.params."
            ),
            (
                "Trading logic should use Backtrader lifecycle methods such as __init__, "
                "next, notify_order, and notify_trade."
            ),
            (
                "The strategy must not fetch market data or place live orders; market data "
                "and broker simulation are provided by Chat-Quant backtesting."
            ),
        ]
    )
    result_contract: list[str] = Field(
        default_factory=lambda: [
            "Backtesting produces StrategyBacktestResultRecord.",
            (
                "Metrics include initial/final value, returns, drawdown, Sharpe, "
                "win rate, and total trades."
            ),
            "Equity and drawdown curves are emitted as dated points.",
            "Trades are best-effort records derived from Backtrader trade notifications.",
        ]
    )
