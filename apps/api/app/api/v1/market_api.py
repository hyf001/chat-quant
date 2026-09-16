from __future__ import annotations

from datetime import date as date_type
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.schema.market import (
    StockIntradayResponse,
    StockPreviewPeriod,
    StockPreviewResponse,
)
from app.service.market import StockPreviewError, StockPreviewService

router = APIRouter()


@router.get("/stocks/{symbol}/preview", response_model=StockPreviewResponse)
async def get_stock_preview(
    symbol: str,
    period: StockPreviewPeriod = "daily",
    limit: Annotated[int, Query(ge=2, le=500)] = 120,
) -> StockPreviewResponse:
    try:
        return StockPreviewService().stock_preview(symbol, period=period, limit=limit)
    except StockPreviewError as error:
        detail = {"error_code": error.error_code, "message": error.message}
        if error.detail:
            detail.update(error.detail)
        raise HTTPException(status_code=error.status_code, detail=detail) from error


@router.get("/stocks/{symbol}/intraday", response_model=StockIntradayResponse)
async def get_stock_intraday(
    symbol: str,
    trade_date: Annotated[date_type, Query(alias="date")],
) -> StockIntradayResponse:
    """某一天的 1 分钟分时（K 线上的"查看分时"）。"""
    try:
        return StockPreviewService().stock_intraday(symbol, trade_date=trade_date)
    except StockPreviewError as error:
        detail = {"error_code": error.error_code, "message": error.message}
        if error.detail:
            detail.update(error.detail)
        raise HTTPException(status_code=error.status_code, detail=detail) from error
