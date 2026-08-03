from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schema.strategy import StrategyMode

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
    strategy_mode: StrategyMode = StrategyMode.SINGLE_SYMBOL
    asset_class: Literal["stock", "etf", "index", "crypto", "futures"] = "stock"
    market: Literal["CN", "US", "HK"] = "CN"
    symbols: list[str] = Field(default_factory=lambda: ["600519.SH"])
    symbol_source: Literal["manual", "strategy_fixed", "universe"] = "manual"
    universe: str | None = None
    benchmark_symbol: str | None = "000300.SH"
    start_date: date = date(2024, 1, 1)
    end_date: date = date(2024, 4, 30)
    timeframe: Literal["1d"] = "1d"
    initial_cash: Decimal = Field(default=Decimal("100000"), gt=0)
    commission: Decimal = Field(default=Decimal("0.001"), ge=0)
    slippage: Decimal = Field(default=Decimal("0"), ge=0)
    data_adjust: str = "qfq"
    currency: Literal["CNY", "USD", "HKD"] = "CNY"
    rebalance_frequency: Literal["none", "daily", "weekly", "monthly", "quarterly"] = "none"
    position_sizing: Literal[
        "fixed_percent",
        "equal_weight",
        "target_weight",
        "cash_per_order",
    ] = "fixed_percent"
    max_position_count: int | None = Field(default=None, ge=1)
    allow_short: bool = False
    risk_control_enabled: bool = False
    stop_loss_pct: float | None = Field(default=None, ge=0)
    take_profit_pct: float | None = Field(default=None, ge=0)
    max_drawdown_stop_pct: float | None = Field(default=None, ge=0)
    notes: list[str] = Field(default_factory=list)
    params: dict[str, JsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_run_config(self) -> StrategyBacktestConfig:
        symbols = [symbol.strip().upper() for symbol in self.symbols if symbol.strip()]
        if self.symbol_source != "universe" and not symbols:
            raise ValueError("symbols must contain at least one non-empty symbol")
        self.symbols = symbols
        if self.symbol_source == "universe" and not self.universe:
            raise ValueError("universe is required when symbol_source is universe")
        if self.strategy_mode == "single_symbol" and len(self.symbols) != 1:
            raise ValueError("single_symbol strategy_mode requires exactly one symbol")
        if self.strategy_mode in {"multi_symbol", "portfolio"} and len(self.symbols) < 2:
            raise ValueError(f"{self.strategy_mode} strategy_mode requires at least two symbols")
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


class StrategyMarketCandle(BaseModel):
    symbol: str
    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


class StrategyMarketSeries(BaseModel):
    symbol: str
    candles: list[StrategyMarketCandle] = Field(default_factory=list)


class StrategyBenchmarkPoint(BaseModel):
    date: date
    value: Decimal
    normalized_value: Decimal


class StrategyBenchmarkSeries(BaseModel):
    symbol: str
    total_return_pct: Decimal | None = None
    points: list[StrategyBenchmarkPoint] = Field(default_factory=list)


class StrategyDailyPosition(BaseModel):
    symbol: str
    size: Decimal
    close_price: Decimal
    market_value: Decimal
    unrealized_pnl: Decimal | None = None


class StrategyDailyPortfolioSnapshot(BaseModel):
    date: date
    cash: Decimal
    total_value: Decimal
    daily_pnl: Decimal
    positions: list[StrategyDailyPosition] = Field(default_factory=list)


class StrategyBacktestResultRecord(BaseModel):
    id: str
    strategy_backtest_id: str
    summary: str
    metrics: StrategyBacktestMetrics
    trades: list[StrategyTradeRecord] = Field(default_factory=list)
    curves: list[StrategyCurve] = Field(default_factory=list)
    market_data: list[StrategyMarketSeries] = Field(default_factory=list)
    benchmark: StrategyBenchmarkSeries | None = None
    daily_positions: list[StrategyDailyPortfolioSnapshot] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    engine: str
    protocol: str
    data_source: dict[str, JsonValue] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class StrategyBacktestDetail(BaseModel):
    backtest: StrategyBacktestRecord
    result: StrategyBacktestResultRecord | None = None


class StrategyBacktestProtocol(BaseModel):
    name: str = "chatq_backtrader_strategy_v2"
    source_format: str = "A single Python source string defining one backtrader.Strategy subclass"
    base_class: str = "backtrader.Strategy"
    required_contract: list[str] = Field(
        default_factory=lambda: [
            "The source code must define exactly one backtrader.Strategy subclass.",
            (
                "Strategy parameters should be declared through a class-level chatq_params() "
                "method; Chat-Quant stores the returned schema as the strategy version "
                "custom_params snapshot."
            ),
            (
                "Chat-Quant injects custom_params into Backtrader params before execution, "
                "then passes StrategyBacktestConfig.params as runtime overrides."
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
