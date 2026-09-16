from __future__ import annotations

import math
from datetime import date
from typing import Any

import pandas as pd

from app.core.config import get_settings
from app.schema.market import (
    StockIntradayPoint,
    StockIntradayResponse,
    StockPreviewCandle,
    StockPreviewPeriod,
    StockPreviewResponse,
)
from app.schema.stock_pool import normalize_symbol
from app.service.datasource.mindgo.stock_a_snapshot_info.constants import (
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
)
from app.service.market_data.minute_price import (
    MINUTE_PRICE_SOURCE_ID,
    load_minute_prices,
)
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path

STOCK_PREVIEW_PRICE_SOURCE_ID = "a_stock_daily_price_pre_adjusted"
DEFAULT_LIMIT = 120
MAX_LIMIT = 500


class StockPreviewError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class StockPreviewService:
    def stock_preview(
        self,
        symbol: str,
        *,
        period: StockPreviewPeriod = "daily",
        limit: int = DEFAULT_LIMIT,
    ) -> StockPreviewResponse:
        normalized_symbol = normalize_symbol(symbol)
        if not normalized_symbol:
            raise StockPreviewError("STOCK_SYMBOL_EMPTY", "symbol must not be empty", 422)
        checked_limit = max(2, min(limit, MAX_LIMIT))
        name = self._stock_name(normalized_symbol)
        daily_frame = self._daily_prices(normalized_symbol, _fetch_limit(period, checked_limit))
        candles = _period_candles(daily_frame, period, checked_limit)
        if len(candles) < 1:
            raise StockPreviewError(
                "STOCK_PREVIEW_NOT_FOUND",
                "No pre-adjusted price data found for symbol",
                404,
                detail={"symbol": normalized_symbol, "dataset": STOCK_PREVIEW_PRICE_SOURCE_ID},
            )
        latest = candles[-1]
        previous = candles[-2] if len(candles) >= 2 else None
        change = latest.close - previous.close if previous is not None else None
        pct_change = (
            change / previous.close * 100
            if change is not None and previous is not None and previous.close
            else None
        )
        return StockPreviewResponse(
            symbol=normalized_symbol,
            name=name,
            period=period,
            trade_date=latest.date,
            open=latest.open,
            high=latest.high,
            low=latest.low,
            close=latest.close,
            prev_close=previous.close if previous is not None else None,
            change=change,
            pct_change=pct_change,
            volume=latest.volume,
            turnover=latest.turnover,
            candles=candles,
            source_dataset=STOCK_PREVIEW_PRICE_SOURCE_ID,
        )

    def stock_intraday(self, symbol: str, *, trade_date: date) -> StockIntradayResponse:
        """某只股票某一天的 1 分钟分时（行情预览的"查看分时"）。

        这里只负责分钟序列（不复权原始价）：标的名与分时基准（前收）由调用方从它已经拿到的
        日线预览里算，省掉一次"上一根日线"的查询（``trade_date`` 有 8 位 / ISO 两种写法，
        在 SQL 里归一化会退化成全表表达式、慢一个量级）。当天没有分钟数据时返回空
        ``points``（分钟数据集只同步了最近若干个交易日），不报错。
        """
        normalized_symbol = normalize_symbol(symbol)
        if not normalized_symbol:
            raise StockPreviewError("STOCK_SYMBOL_EMPTY", "symbol must not be empty", 422)
        return StockIntradayResponse(
            symbol=normalized_symbol,
            trade_date=trade_date.isoformat(),
            points=[
                StockIntradayPoint(t=item.minute, p=item.price, v=item.volume)
                for item in load_minute_prices(normalized_symbol, trade_date)
            ],
            source_dataset=MINUTE_PRICE_SOURCE_ID,
        )

    def _stock_name(self, symbol: str) -> str:
        frame = _query_frame(
            f"""
                SELECT name
                FROM a_stock_snapshot_info
                WHERE upper(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
                LIMIT 1
            """,
            error_code="STOCK_PREVIEW_SNAPSHOT_UNAVAILABLE",
            message="a_stock_snapshot_info dataset is unavailable",
            dataset=STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
        )
        if frame.empty:
            raise StockPreviewError(
                "STOCK_PREVIEW_SNAPSHOT_NOT_FOUND",
                "Stock was not found in a_stock_snapshot_info",
                404,
                detail={"symbol": symbol, "dataset": STOCK_A_SNAPSHOT_INFO_SOURCE_ID},
            )
        name = _string_or_none(frame.iloc[0].get("name"))
        if name is None:
            raise StockPreviewError(
                "STOCK_PREVIEW_SNAPSHOT_NAME_EMPTY",
                "Stock name is empty in a_stock_snapshot_info",
                422,
                detail={"symbol": symbol, "dataset": STOCK_A_SNAPSHOT_INFO_SOURCE_ID},
            )
        return name

    def _daily_prices(self, symbol: str, limit: int) -> pd.DataFrame:
        frame = _query_frame(
            f"""
                SELECT
                    CAST(trade_date AS VARCHAR) AS trade_date,
                    CAST(open AS DOUBLE) AS open,
                    CAST(high AS DOUBLE) AS high,
                    CAST(low AS DOUBLE) AS low,
                    CAST(close AS DOUBLE) AS close,
                    CAST(volume AS DOUBLE) AS volume,
                    CAST(turnover AS DOUBLE) AS turnover
                FROM {STOCK_PREVIEW_PRICE_SOURCE_ID}
                WHERE upper(CAST(symbol AS VARCHAR)) = {_sql_string_literal(symbol)}
                ORDER BY trade_date DESC
                LIMIT {max(limit, 2)}
            """,
            error_code="STOCK_PREVIEW_PRICE_UNAVAILABLE",
            message="a_stock_daily_price_pre_adjusted dataset is unavailable",
            dataset=STOCK_PREVIEW_PRICE_SOURCE_ID,
        )
        if frame.empty:
            raise StockPreviewError(
                "STOCK_PREVIEW_NOT_FOUND",
                "No pre-adjusted price data found for symbol",
                404,
                detail={"symbol": symbol, "dataset": STOCK_PREVIEW_PRICE_SOURCE_ID},
            )
        return frame


def _period_candles(
    frame: pd.DataFrame,
    period: StockPreviewPeriod,
    limit: int,
) -> list[StockPreviewCandle]:
    prepared = frame.copy()
    prepared["date"] = pd.to_datetime(prepared["trade_date"].map(_date_text), errors="coerce")
    prepared = prepared.dropna(subset=["date", "open", "high", "low", "close"])
    prepared = prepared.sort_values("date")
    if period != "daily":
        group_key = prepared["date"].dt.to_period("W-FRI" if period == "weekly" else "M")
        prepared = (
            prepared.assign(_period=group_key)
            .groupby("_period", sort=True)
            .agg(
                date=("date", "max"),
                open=("open", "first"),
                high=("high", "max"),
                low=("low", "min"),
                close=("close", "last"),
                volume=("volume", "sum"),
                turnover=("turnover", "sum"),
            )
            .reset_index(drop=True)
        )
    prepared = prepared.tail(limit).copy()
    for window in (5, 10, 20, 60):
        prepared[f"ma{window}"] = prepared["close"].rolling(window).mean()
    records: list[StockPreviewCandle] = []
    for item in prepared.to_dict(orient="records"):
        records.append(
            StockPreviewCandle(
                date=pd.Timestamp(item["date"]).strftime("%Y-%m-%d"),
                open=_float_value(item["open"]),
                high=_float_value(item["high"]),
                low=_float_value(item["low"]),
                close=_float_value(item["close"]),
                volume=_nullable_float(item.get("volume")),
                turnover=_nullable_float(item.get("turnover")),
                ma5=_nullable_float(item.get("ma5")),
                ma10=_nullable_float(item.get("ma10")),
                ma20=_nullable_float(item.get("ma20")),
                ma60=_nullable_float(item.get("ma60")),
            )
        )
    return records


def _fetch_limit(period: StockPreviewPeriod, limit: int) -> int:
    if period == "weekly":
        return min(max(limit * 8, 240), 2500)
    if period == "monthly":
        return min(max(limit * 32, 720), 5000)
    return limit


def _query_frame(
    sql: str,
    *,
    error_code: str,
    message: str,
    dataset: str,
) -> pd.DataFrame:
    view_store = DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))
    try:
        return view_store.query_frame(sql)
    except DuckDBViewStoreError as exc:
        raise StockPreviewError(
            error_code,
            message,
            422,
            detail={"dataset": dataset, "error": str(exc)},
        ) from exc


def _date_text(value: object) -> str:
    text = str(value).strip()
    if len(text) == 8 and text.isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    return text


def _float_value(value: object) -> float:
    result = _nullable_float(value)
    if result is None:
        raise StockPreviewError("STOCK_PREVIEW_VALUE_INVALID", "Price value is invalid", 422)
    return result


def _nullable_float(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None
    result = float(value)
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _string_or_none(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    stripped = str(value).strip()
    return stripped or None


def _sql_string_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
