from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

StockPreviewPeriod = Literal["daily", "weekly", "monthly"]


class StockPreviewCandle(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None
    turnover: float | None = None
    ma5: float | None = None
    ma10: float | None = None
    ma20: float | None = None
    ma60: float | None = None


class StockPreviewResponse(BaseModel):
    symbol: str
    name: str
    period: StockPreviewPeriod = "daily"
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    prev_close: float | None = None
    change: float | None = None
    pct_change: float | None = None
    volume: float | None = None
    turnover: float | None = None
    candles: list[StockPreviewCandle] = Field(default_factory=list)
    source_dataset: str = "a_stock_daily_price_pre_adjusted"
