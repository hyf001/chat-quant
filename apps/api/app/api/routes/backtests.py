from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.dependencies import ProjectId, UserId
from app.domain.backtests.service import (
    BacktestConflictError,
    BacktestNotFoundError,
    BacktestValidationError,
    backtest_service,
)
from app.schemas.contracts.backtests import (
    BacktestComparisonDTO,
    BacktestDetailDTO,
    BacktestRunDTO,
    BacktestRunStatus,
    CompareBacktestsRequest,
    CreateBacktestRunRequest,
    RerunBacktestRequest,
    RunBacktestRequest,
)

router = APIRouter(prefix="/backtests", tags=["backtests"])
strategy_backtests_router = APIRouter(prefix="/strategy-versions", tags=["backtests"])


@router.post("", response_model=BacktestRunDTO, status_code=status.HTTP_201_CREATED)
async def create_backtest(
    request: CreateBacktestRunRequest,
    user_id: UserId,
    project_id: ProjectId,
) -> BacktestRunDTO:
    try:
        return backtest_service.create_run(
            request.model_copy(
                update={
                    "user_id": request.user_id or user_id,
                    "project_id": request.project_id or project_id,
                }
            )
        )
    except BacktestValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/{backtest_run_id}/run", response_model=BacktestDetailDTO)
async def run_backtest(backtest_run_id: str, request: RunBacktestRequest) -> BacktestDetailDTO:
    try:
        if request.mode.value == "async":
            return backtest_service.get_detail(
                backtest_run_id,
                include_trades=False,
                include_curves=False,
            )
        return backtest_service.run(backtest_run_id)
    except BacktestNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest run not found",
        ) from exc


@router.get("/{backtest_run_id}", response_model=BacktestDetailDTO)
async def get_backtest(
    backtest_run_id: str,
    include_trades: bool = Query(default=False),
    include_curves: bool = Query(default=True),
) -> BacktestDetailDTO:
    try:
        return backtest_service.get_detail(
            backtest_run_id,
            include_trades=include_trades,
            include_curves=include_curves,
        )
    except BacktestNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest run not found",
        ) from exc


@strategy_backtests_router.get(
    "/{strategy_version_id}/backtests",
    response_model=list[BacktestRunDTO],
)
async def list_strategy_backtests(
    strategy_version_id: str,
    status_filter: Annotated[BacktestRunStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[BacktestRunDTO]:
    return backtest_service.list_by_strategy_version(strategy_version_id, status_filter, limit)


@router.post(
    "/{backtest_run_id}/rerun",
    response_model=BacktestDetailDTO,
    status_code=status.HTTP_201_CREATED,
)
async def rerun_backtest(backtest_run_id: str, request: RerunBacktestRequest) -> BacktestDetailDTO:
    try:
        return backtest_service.rerun(backtest_run_id, request)
    except BacktestNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest run not found",
        ) from exc
    except BacktestValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/compare", response_model=BacktestComparisonDTO)
async def compare_backtests(request: CompareBacktestsRequest) -> BacktestComparisonDTO:
    try:
        return backtest_service.compare(request)
    except BacktestNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest run not found",
        ) from exc
    except BacktestConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
