from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.schema.market import StockPreviewPeriod, StockPreviewResponse
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
