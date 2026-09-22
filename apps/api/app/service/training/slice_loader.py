"""末端切片：180 根展示段 + 随机 60~180 根训练段 + 除权 / ST 过滤。

口径（设计方案 §5.1）：

* 价格来源固定为 ``a_stock_daily_price_unadjusted``（不复权真实价，前复权视图含未来函数，禁用）；
* 终点固定贴到数据末端，往前数 ``warmup_bars + N`` 根，warmup 与训练段连续不重叠；
* 两个可选过滤：窗口内含除权除息的切片直接丢弃（照旧）；``exclude_st`` 打开时
  先在候选里剔掉当前名称带 ST 的标的（见 §5.1）；
* 不做缺失过滤：停牌 / 缺 bar 就按实际存在的序列训练。
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date

import pandas as pd

from app.core.config import get_settings
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path

TRAINING_PRICE_SOURCE_ID = "a_stock_daily_price_unadjusted"
TRAINING_ADJUST_FACTOR_SOURCE_ID = "a_stock_daily_adjust_factor"
TRAINING_SNAPSHOT_SOURCE_ID = "a_stock_snapshot_info"


class TrainingSliceError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


@dataclass(frozen=True)
class SliceBar:
    trade_date: date
    trade_date_text: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class TrainingSlice:
    symbol: str
    name: str | None
    warmup_bars: int
    training_bars: int
    bars: list[SliceBar]

    @property
    def slice_start(self) -> date:
        return self.bars[0].trade_date

    @property
    def slice_end(self) -> date:
        return self.bars[-1].trade_date

    @property
    def warmup(self) -> list[SliceBar]:
        return self.bars[: self.warmup_bars]

    @property
    def training(self) -> list[SliceBar]:
        return self.bars[self.warmup_bars :]

    def revealed(self, count: int) -> list[SliceBar]:
        end = self.warmup_bars + max(0, min(count, self.training_bars))
        return self.bars[:end]

    def bar(self, index: int) -> SliceBar:
        return self.bars[index]

    def training_frame(self, bar_indices: list[int] | None = None) -> pd.DataFrame:
        """喂给 backtrader 的结算段：从最后一根已展示 K 线开始。

        每次点击先在当前可见 K 线的尾盘成交，再由 service 揭示下一根。因此引擎处理
        的第 0 根是 ``warmup[-1]``，最后一根是最终训练 K 线的前一根；最后一根训练
        K 线只负责在最后一次点击后揭示并做期末市值计价。
        """
        indices = bar_indices or list(
            range(self.warmup_bars - 1, self.warmup_bars + self.training_bars - 1)
        )
        settlement_bars = [self.bars[index] for index in indices]
        rows = [
            {
                "datetime": pd.Timestamp(bar.trade_date),
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
                "openinterest": 0.0,
            }
            for bar in settlement_bars
        ]
        frame = pd.DataFrame(rows)
        return frame.set_index("datetime")


def load_training_slice(
    *,
    warmup_bars: int,
    training_bars_min: int,
    training_bars_max: int,
    exclude_st: bool = False,
    rng: random.Random | None = None,
    max_attempts: int = 12,
) -> TrainingSlice:
    generator = rng or random.Random()
    low = max(1, min(training_bars_min, training_bars_max))
    high = max(low, training_bars_max)
    training_bars = generator.randint(low, high)
    total_bars = warmup_bars + training_bars

    candidates = _candidate_symbols(total_bars, exclude_st=exclude_st)
    if not candidates:
        raise TrainingSliceError(
            "TRAINING_SLICE_UNAVAILABLE",
            "没有满足长度要求的标的可出题" + ("（已剔除 ST 标的）" if exclude_st else ""),
            detail={
                "required_bars": total_bars,
                "dataset": TRAINING_PRICE_SOURCE_ID,
                "exclude_st": exclude_st,
            },
        )

    attempts = min(len(candidates), max(1, max_attempts))
    for symbol in generator.sample(candidates, attempts):
        bars = _tail_bars(symbol, total_bars)
        if len(bars) < total_bars:
            continue
        if _window_has_adjust_factor(symbol, bars[0], bars[-1]):
            continue
        return TrainingSlice(
            symbol=symbol,
            name=_symbol_name(symbol),
            warmup_bars=warmup_bars,
            training_bars=training_bars,
            bars=bars,
        )

    raise TrainingSliceError(
        "TRAINING_SLICE_UNAVAILABLE",
        "没有可用的切片（候选窗口含除权除息或行情不足）",
        detail={
            "required_bars": total_bars,
            "attempts": attempts,
            "dataset": TRAINING_PRICE_SOURCE_ID,
        },
    )


RELOAD_BAR_LIMIT = 2500


def load_slice_window(
    *,
    symbol: str,
    slice_start: date,
    slice_end: date,
    warmup_bars: int,
) -> TrainingSlice:
    """按已存会话的窗口重新装载切片（引擎回收 / 进程重启后重建用）。"""
    bars = _tail_bars(symbol, RELOAD_BAR_LIMIT)
    window = [bar for bar in bars if slice_start <= bar.trade_date <= slice_end]
    if len(window) <= warmup_bars:
        raise TrainingSliceError(
            "TRAINING_SLICE_UNAVAILABLE",
            "训练窗口的行情已经无法重新装载",
            detail={
                "symbol": symbol,
                "slice_start": slice_start.isoformat(),
                "slice_end": slice_end.isoformat(),
                "window_bars": len(window),
            },
        )
    return TrainingSlice(
        symbol=symbol,
        name=_symbol_name(symbol),
        warmup_bars=warmup_bars,
        training_bars=len(window) - warmup_bars,
        bars=window,
    )


def _candidate_symbols(required_bars: int, *, exclude_st: bool = False) -> list[str]:
    frame = _query_frame(
        f"""
            SELECT UPPER(CAST(symbol AS VARCHAR)) AS symbol, COUNT(*) AS bar_count
            FROM {TRAINING_PRICE_SOURCE_ID}
            WHERE symbol IS NOT NULL
            GROUP BY 1
            HAVING COUNT(*) >= {int(required_bars)}
            ORDER BY 1
        """,
        message=f"{TRAINING_PRICE_SOURCE_ID} 不可用",
    )
    if frame.empty:
        return []
    symbols = [str(value) for value in frame["symbol"].tolist()]
    if not exclude_st:
        return symbols
    blocked = _st_symbols()
    return [symbol for symbol in symbols if symbol not in blocked]


def _st_symbols() -> set[str]:
    """当前名称里带 ST 的标的（含 ``*ST``）。快照数据集不可用时不阻塞出题，只是不过滤。"""
    try:
        frame = _query_frame(
            f"""
                SELECT UPPER(CAST(symbol AS VARCHAR)) AS symbol
                FROM {TRAINING_SNAPSHOT_SOURCE_ID}
                WHERE UPPER(CAST(name AS VARCHAR)) LIKE '%ST%'
            """,
            message=f"{TRAINING_SNAPSHOT_SOURCE_ID} 不可用",
        )
    except TrainingSliceError:
        return set()
    if frame.empty:
        return set()
    return {str(value) for value in frame["symbol"].tolist()}


def _tail_bars(symbol: str, count: int) -> list[SliceBar]:
    frame = _query_frame(
        f"""
            SELECT
                CAST(trade_date AS VARCHAR) AS trade_date,
                CAST(open AS DOUBLE) AS open,
                CAST(high AS DOUBLE) AS high,
                CAST(low AS DOUBLE) AS low,
                CAST(close AS DOUBLE) AS close,
                CAST(volume AS DOUBLE) AS volume
            FROM {TRAINING_PRICE_SOURCE_ID}
            WHERE UPPER(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
            ORDER BY CAST(trade_date AS VARCHAR) DESC
            LIMIT {int(count)}
        """,
        message=f"{TRAINING_PRICE_SOURCE_ID} 不可用",
    )
    bars: list[SliceBar] = []
    for item in frame.to_dict(orient="records"):
        parsed_date = _parse_trade_date(item.get("trade_date"))
        if parsed_date is None:
            continue
        bars.append(
            SliceBar(
                trade_date=parsed_date,
                trade_date_text=str(item["trade_date"]).strip(),
                open=float(item["open"]),
                high=float(item["high"]),
                low=float(item["low"]),
                close=float(item["close"]),
                volume=float(item["volume"] or 0.0),
            )
        )
    bars.reverse()
    return bars


def _window_has_adjust_factor(symbol: str, first: SliceBar, last: SliceBar) -> bool:
    """窗口内含除权除息（复权因子发生变化）时丢弃该切片。"""
    try:
        frame = _query_frame(
            f"""
                SELECT COUNT(DISTINCT CAST(factor AS DOUBLE)) AS factor_count
                FROM {TRAINING_ADJUST_FACTOR_SOURCE_ID}
                WHERE UPPER(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
                  AND CAST(trade_date AS VARCHAR) >= {_sql_string_literal(first.trade_date_text)}
                  AND CAST(trade_date AS VARCHAR) <= {_sql_string_literal(last.trade_date_text)}
            """,
            message=f"{TRAINING_ADJUST_FACTOR_SOURCE_ID} 不可用",
        )
    except TrainingSliceError:
        # 复权因子数据集缺失时不阻塞出题，只是放弃了这一层过滤。
        return False
    if frame.empty:
        return False
    value = frame.iloc[0].get("factor_count")
    if value is None or pd.isna(value):
        return False
    return int(value) > 1


def _symbol_name(symbol: str) -> str | None:
    try:
        frame = _query_frame(
            f"""
                SELECT CAST(name AS VARCHAR) AS name
                FROM {TRAINING_SNAPSHOT_SOURCE_ID}
                WHERE UPPER(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
                LIMIT 1
            """,
            message=f"{TRAINING_SNAPSHOT_SOURCE_ID} 不可用",
        )
    except TrainingSliceError:
        return None
    if frame.empty:
        return None
    value = frame.iloc[0].get("name")
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _query_frame(sql: str, *, message: str) -> pd.DataFrame:
    view_store = DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))
    try:
        return view_store.query_frame(sql)
    except DuckDBViewStoreError as exc:
        raise TrainingSliceError(
            "TRAINING_SLICE_UNAVAILABLE",
            message,
            detail={"error": str(exc)},
        ) from exc


def _parse_trade_date(value: object) -> date | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if len(text) == 8 and text.isdigit():
        try:
            return date(int(text[:4]), int(text[4:6]), int(text[6:]))
        except ValueError:
            return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _sql_string_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
