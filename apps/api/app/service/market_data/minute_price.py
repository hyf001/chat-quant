"""A 股 1 分钟行情（``a_stock_minute_price``）的最小读取层。

训练分时（双击日线看分时）与行情预览的分时共用这一层：输入标的名 + 交易日，输出
``HH:MM`` 的分钟收盘序列。**只读、容错**：数据集缺失或当天没有分钟数据都返回空
列表，让调用方按"没有分时数据"处理，而不是把训练 / 预览整条链路带崩。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date

import pandas as pd

from app.core.config import get_settings
from app.core.logging import get_logger
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path

logger = get_logger(__name__)

MINUTE_PRICE_SOURCE_ID = "a_stock_minute_price"
#: 分时时间轴只保留到分钟：``2026-08-03 09:31:00`` → ``09:31``。
MINUTE_TEXT_LENGTH = 5


@dataclass(frozen=True)
class MinutePricePoint:
    minute: str
    price: float
    volume: float


def load_minute_prices(symbol: str, trade_date: date) -> list[MinutePricePoint]:
    """按标的名 + 自然日取分钟收盘序列；没有数据（或没有数据集）时返回空列表。"""
    frame = _query_minute_frame(symbol, trade_date)
    if frame.empty:
        return []
    points: list[MinutePricePoint] = []
    for item in frame.to_dict(orient="records"):
        minute = _minute_text(item.get("trade_date"))
        price = _float_or_none(item.get("close"))
        if minute is None or price is None:
            continue
        points.append(
            MinutePricePoint(
                minute=minute,
                price=price,
                volume=_float_or_none(item.get("volume")) or 0.0,
            )
        )
    return points


def _query_minute_frame(symbol: str, trade_date: date) -> pd.DataFrame:
    day_text = trade_date.isoformat()
    try:
        view_store = DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))
        return view_store.query_frame(
            f"""
                SELECT
                    CAST(trade_date AS VARCHAR) AS trade_date,
                    CAST(close AS DOUBLE) AS close,
                    CAST(volume AS DOUBLE) AS volume
                FROM {MINUTE_PRICE_SOURCE_ID}
                WHERE UPPER(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
                  AND CAST(trade_date AS VARCHAR) LIKE {_sql_string_literal(f"{day_text}%")}
                ORDER BY CAST(trade_date AS VARCHAR) ASC
            """
        )
    except DuckDBViewStoreError as exc:
        logger.warning("[market_data.minute_price] %s unavailable: %s", MINUTE_PRICE_SOURCE_ID, exc)
        return pd.DataFrame(columns=["trade_date", "close", "volume"])


def _minute_text(value: object) -> str | None:
    """``2026-08-03 09:31:00`` → ``09:31``；只有日期没有时刻的行直接丢掉。"""
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    _, _, clock = text.partition(" ")
    clock = clock.strip()
    if len(clock) < MINUTE_TEXT_LENGTH:
        return None
    return clock[:MINUTE_TEXT_LENGTH]


def _float_or_none(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None
    result = float(value)
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _sql_string_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
