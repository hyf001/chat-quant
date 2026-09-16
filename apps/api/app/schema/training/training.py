"""双盲 K 线训练（Phase 1，日线单标的）请求 / 响应契约。

脱敏规则（见设计方案 §5.2）：训练期响应只由这里的白名单模型产出，不含
``symbol`` / ``name`` / 真实日期，K 线字段固定为 ``{i, o, h, l, c, v}``，X 轴是序号。
只有 ``finish`` / ``report`` 的响应才揭晓真实标的与窗口。
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TrainingMode = Literal["daily"]
TrainingPeriod = Literal["1d"]
TrainingAction = Literal["buy", "sell", "close", "cancel", "hold"]
TrainingCurveType = Literal["equity", "drawdown"]

DEFAULT_WARMUP_BARS = 180
DEFAULT_TRAINING_BARS_MIN = 60
DEFAULT_TRAINING_BARS_MAX = 180
DEFAULT_INITIAL_CASH = Decimal("100000")
DEFAULT_COMMISSION = Decimal("0.0005")
DEFAULT_SLIPPAGE = Decimal("0.001")
DEFAULT_IDLE_TTL_SECONDS = 1800
MIN_POSITION_RATIO = 0.000001


class TrainingSessionStatus(StrEnum):
    ACTIVE = "active"
    FINISHED = "finished"


class TrainingEventType(StrEnum):
    BUY = "buy"
    SELL = "sell"
    CLOSE = "close"
    CANCEL = "cancel"
    HOLD = "hold"


class TrainingSessionConfig(BaseModel):
    """会话级参数；佣金与滑点只作用于训练这一局，回测口径不动（无最低佣金 / 无印花税）。"""

    warmup_bars: int = Field(default=DEFAULT_WARMUP_BARS, ge=60, le=500)
    training_bars_min: int = Field(default=DEFAULT_TRAINING_BARS_MIN, ge=10, le=500)
    training_bars_max: int = Field(default=DEFAULT_TRAINING_BARS_MAX, ge=10, le=500)
    initial_cash: Decimal = Field(default=DEFAULT_INITIAL_CASH, gt=0)
    commission: Decimal = Field(default=DEFAULT_COMMISSION, ge=0)
    #: 成交价按比例向不利方向滑：买入 ×(1+slip)、卖出 ×(1-slip)，越不过当根 high / low。
    slippage: Decimal = Field(default=DEFAULT_SLIPPAGE, ge=0, le=Decimal("0.1"))
    #: 出题时先在候选标的里剔掉当前名称带 ST 的（快照数据集不可用时退化为不过滤）。
    exclude_st: bool = True
    idle_ttl_seconds: int = Field(default=DEFAULT_IDLE_TTL_SECONDS, ge=60, le=86400)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_bar_range(self) -> TrainingSessionConfig:
        if self.training_bars_min > self.training_bars_max:
            raise ValueError("training_bars_min must not exceed training_bars_max")
        return self


class TrainingSessionCreate(BaseModel):
    project_id: str = Field(min_length=1, max_length=128)
    mode: TrainingMode = "daily"
    period: TrainingPeriod = "1d"
    config: TrainingSessionConfig | None = None

    model_config = ConfigDict(extra="forbid")


class TrainingBar(BaseModel):
    """训练期 K 线：只有序号与价格，没有日期 / 标的。"""

    i: int
    o: float
    h: float
    l: float  # noqa: E741 - 与设计方案 §5.2 的字段白名单一致
    c: float
    v: float


class TrainingRevealedBar(BaseModel):
    """复盘用 K 线：会话已揭晓，可以带真实日期。"""

    i: int
    date: str
    o: float
    h: float
    l: float  # noqa: E741 - 与设计方案 §5.2 的字段白名单一致
    c: float
    v: float


class TrainingMarker(BaseModel):
    i: int
    side: Literal["buy", "sell"]
    text: str


class TrainingFill(BaseModel):
    i: int
    side: Literal["buy", "sell"]
    price: Decimal
    size: float
    value: Decimal
    commission: Decimal


class TrainingOrderRejection(BaseModel):
    """拒单：资金不足（``margin``）或卖出超过持仓（``oversell``），前端据此提示。"""

    i: int
    side: Literal["buy", "sell"]
    size: float
    reason: str


class TrainingAccount(BaseModel):
    """账户口径：全部是 backtrader 的实时值，服务端不做二次加工。

    市价单按本根 close 成交（``set_coc(True)``），撮合与结算点在同一个响应里，
    所以点完按钮拿到的 ``cash`` / ``position_size`` 就是成交后的值——没有挂单，
    也没有"可用"与"实际"两套口径（§5.3）。
    """

    initial_cash: Decimal
    cash: Decimal
    position_size: float
    position_price: Decimal
    position_value: Decimal
    position_pct: Decimal
    total_return: Decimal
    open_return: Decimal


class TrainingSessionView(BaseModel):
    id: str
    status: TrainingSessionStatus
    instrument_alias: str
    started_at: datetime
    elapsed_seconds: int
    warmup_bars: int
    training_bars: int
    cursor_index: int
    remaining: int
    account: TrainingAccount


class TrainingSessionResponse(BaseModel):
    session: TrainingSessionView
    bars: list[TrainingBar] = Field(default_factory=list)
    markers: list[TrainingMarker] = Field(default_factory=list)


class TrainingSessionSummary(BaseModel):
    """列表页条目：字段白名单与训练期一致（不带 symbol / name / 真实窗口日期）。

    ``training_bars`` 在新会话上由开局时的切片长度决定；早期会话没存这个值时为
    ``None``，前端只展示"已推进"的根数。
    """

    id: str
    status: TrainingSessionStatus
    instrument_alias: str
    initial_cash: Decimal
    started_at: datetime
    finished_at: datetime | None = None
    elapsed_seconds: int
    warmup_bars: int
    training_bars: int | None = None
    cursor_index: int
    remaining: int | None = None


class TrainingSessionListResponse(BaseModel):
    items: list[TrainingSessionSummary] = Field(default_factory=list)
    total: int = 0


class TrainingRevealRequest(BaseModel):
    """一次点击 = 一条事件 = 一根推进；``size`` 是仓位比例（0~1）。"""

    seq: int = Field(ge=0)
    action: TrainingAction = "hold"
    size: float | None = Field(default=None, gt=0, le=1)
    reason: str | None = Field(default=None, max_length=200)

    model_config = ConfigDict(extra="forbid")


class TrainingRevealResponse(BaseModel):
    session: TrainingSessionView
    bar: TrainingBar | None = None
    markers: list[TrainingMarker] = Field(default_factory=list)
    fills: list[TrainingFill] = Field(default_factory=list)
    rejected: list[TrainingOrderRejection] = Field(default_factory=list)


class TrainingIntradayPoint(BaseModel):
    """分时点：X 轴只有 ``HH:MM``，不带交易日（双盲口径与 K 线的序号轴一致）。"""

    t: str
    p: float
    v: float


class TrainingIntradayResponse(BaseModel):
    """双击某一根日线时的当日分时：只覆盖**已揭示**的那一根。

    分时线本身是这一根日内路径的展开，日线的开高低收早已在图上，所以它不引入新的
    未来信息；出口与 K 线同口径脱敏（无标的名 / 无真实日期）。
    """

    session_id: str
    seq: int
    available: bool
    bar: TrainingBar | None = None
    #: 分时涨跌幅基准：切片里前一根的 close；第一根没有前一根时为 ``None``。
    prev_close: Decimal | None = None
    points: list[TrainingIntradayPoint] = Field(default_factory=list)


class TrainingCurvePoint(BaseModel):
    i: int
    date: str | None = None
    value: Decimal
    normalized_value: Decimal | None = None


class TrainingCurve(BaseModel):
    curve_type: TrainingCurveType
    point_count: int
    points: list[TrainingCurvePoint] = Field(default_factory=list)


class TrainingClosedTrade(BaseModel):
    date: str
    size: float
    price: Decimal
    value: Decimal
    pnl: Decimal
    pnl_pct: Decimal | None = None


class TrainingMetrics(BaseModel):
    initial_cash: Decimal
    final_value: Decimal
    total_return_pct: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    open_return_pct: Decimal
    position_size: float
    position_pct: Decimal
    max_drawdown_pct: Decimal
    max_drawdown_start: date | None = None
    max_drawdown_end: date | None = None
    sharpe_ratio: Decimal | None = None
    win_rate_pct: Decimal | None = None
    total_trades: int = 0
    duration_seconds: int = 0
    settlement_note: str


class TrainingReport(BaseModel):
    metrics: TrainingMetrics
    equity_curve: TrainingCurve
    drawdown_curve: TrainingCurve
    bars: list[TrainingRevealedBar] = Field(default_factory=list)
    markers: list[TrainingMarker] = Field(default_factory=list)
    fills: list[TrainingFill] = Field(default_factory=list)
    closed_trades: list[TrainingClosedTrade] = Field(default_factory=list)


class TrainingInstrument(BaseModel):
    symbol: str
    name: str | None = None
    instrument_alias: str


class TrainingWindow(BaseModel):
    start_date: date
    end_date: date
    warmup_bars: int
    training_bars: int


class TrainingReportResponse(BaseModel):
    session: TrainingSessionView
    instrument: TrainingInstrument
    window: TrainingWindow
    report: TrainingReport
