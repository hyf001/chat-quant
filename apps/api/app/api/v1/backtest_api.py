from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.backtest import StrategyBacktestDetail, StrategyBacktestRecord
from app.service import backtest as backtest_service
from app.service.backtest import BacktestError

router = APIRouter()


@router.get("", response_model=list[StrategyBacktestRecord])
async def list_backtests(
    db: Annotated[AsyncSession, Depends(get_db)],
    strategy_version_id: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[StrategyBacktestRecord]:
    try:
        return await backtest_service.list_records(
            db,
            strategy_version_id=strategy_version_id,
            limit=limit,
        )
    except BacktestError as error:
        raise _http_error(error) from error


@router.get("/{backtest_id}", response_model=StrategyBacktestDetail)
async def get_backtest(
    backtest_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyBacktestDetail:
    try:
        return await backtest_service.get_detail(db, backtest_id)
    except BacktestError as error:
        raise _http_error(error) from error


def _http_error(error: BacktestError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"error_code": error.error_code, "message": error.message},
    )
