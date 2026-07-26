from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.dependencies import get_backtest_service
from app.domain.backtests.models import StrategyBacktestDetail, StrategyBacktestRecord
from app.domain.backtests.service import BacktestError, BacktestService

router = APIRouter(prefix="/backtests", tags=["backtests"])
BacktestServiceDep = Annotated[BacktestService, Depends(get_backtest_service)]


@router.get("", response_model=list[StrategyBacktestRecord])
async def list_backtests(
    service: BacktestServiceDep,
    strategy_version_id: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[StrategyBacktestRecord]:
    try:
        return await service.list_records(
            strategy_version_id=strategy_version_id,
            limit=limit,
        )
    except BacktestError as error:
        raise _http_error(error) from error


@router.get("/{backtest_id}", response_model=StrategyBacktestDetail)
async def get_backtest(backtest_id: str, service: BacktestServiceDep) -> StrategyBacktestDetail:
    try:
        return await service.get_detail(backtest_id)
    except BacktestError as error:
        raise _http_error(error) from error


def _http_error(error: BacktestError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"error_code": error.error_code, "message": error.message},
    )
