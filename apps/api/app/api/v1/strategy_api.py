from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import ProjectId, UserId
from app.db.session import get_db
from app.schema.backtest import (
    StrategyBacktestConfig,
    StrategyBacktestDetail,
    StrategyBacktestProtocol,
)
from app.schema.strategy import (
    StrategyCreate,
    StrategyCreateResult,
    StrategyDetail,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
    StrategyVersionCreate,
    StrategyVersionRecord,
)
from app.service import backtest as backtest_service
from app.service import strategy as strategy_service
from app.service.backtest import BacktestError
from app.service.strategy import StrategyError

router = APIRouter()


class CreateStrategyRequest(StrategyCreate):
    user_id: str | None = None
    project_id: str | None = None

    model_config = ConfigDict(extra="forbid")


class UpdateStrategyRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    tags: list[str] | None = None
    status: StrategyStatus | None = None

    model_config = ConfigDict(extra="forbid")


class CreateStrategyVersionRequest(StrategyVersionCreate):
    pass


class SwitchCurrentVersionRequest(BaseModel):
    strategy_version_id: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class StrategyBacktestRequest(BaseModel):
    config: StrategyBacktestConfig
    strategy_version_id: str | None = None
    user_id: str | None = None
    project_id: str | None = None

    model_config = ConfigDict(extra="forbid")


@router.get("/strategies", response_model=list[StrategySummary])
async def list_strategies(
    user_id: UserId,
    project_id: ProjectId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[StrategySummary]:
    return await strategy_service.list_strategies(db, user_id=user_id, project_id=project_id)


@router.post("/strategies", response_model=StrategyCreateResult, status_code=201)
async def create_strategy(
    request: CreateStrategyRequest,
    user_id: UserId,
    project_id: ProjectId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyCreateResult:
    try:
        return await strategy_service.create_strategy(
            db,
            user_id=request.user_id or user_id,
            project_id=request.project_id or project_id,
            strategy_input=StrategyCreate.model_validate(
                request.model_dump(exclude={"user_id", "project_id"})
            ),
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategies/{strategy_id}", response_model=StrategyDetail)
async def get_strategy(
    strategy_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDetail:
    try:
        return await strategy_service.get_strategy(db, strategy_id)
    except StrategyError as error:
        raise _http_error(error) from error


@router.patch("/strategies/{strategy_id}", response_model=StrategyRecord)
async def update_strategy(
    strategy_id: str,
    request: UpdateStrategyRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyRecord:
    try:
        return await strategy_service.update_strategy_metadata(
            db,
            strategy_id,
            name=request.name,
            description=request.description,
            tags=request.tags,
            status=request.status,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.post(
    "/strategies/{strategy_id}/versions",
    response_model=StrategyVersionRecord,
    status_code=201,
)
async def create_strategy_version(
    strategy_id: str,
    request: CreateStrategyVersionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyVersionRecord:
    try:
        return await strategy_service.create_strategy_version(
            db,
            strategy_id=strategy_id,
            version_input=request,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategies/{strategy_id}/versions", response_model=list[StrategyVersionRecord])
async def list_strategy_versions(
    strategy_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[StrategyVersionRecord]:
    try:
        return await strategy_service.list_versions(db, strategy_id)
    except StrategyError as error:
        raise _http_error(error) from error


@router.patch("/strategies/{strategy_id}/current-version", response_model=StrategySummary)
async def switch_current_strategy_version(
    strategy_id: str,
    request: SwitchCurrentVersionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategySummary:
    try:
        return await strategy_service.switch_current_version(
            db,
            strategy_id,
            version_id=request.strategy_version_id,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.delete("/strategies/{strategy_id}", response_model=StrategyRecord)
async def delete_strategy(
    strategy_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyRecord:
    try:
        return await strategy_service.update_strategy_metadata(
            db,
            strategy_id,
            status=StrategyStatus.DELETED,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategy-backtest/protocol", response_model=StrategyBacktestProtocol)
async def get_strategy_backtest_protocol() -> StrategyBacktestProtocol:
    return StrategyBacktestProtocol()


@router.post("/strategies/{strategy_id}/backtest", response_model=StrategyBacktestDetail)
async def backtest_strategy(
    strategy_id: str,
    request: StrategyBacktestRequest,
    user_id: UserId,
    project_id: ProjectId,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyBacktestDetail:
    try:
        return await backtest_service.backtest_strategy(
            db,
            strategy_id=strategy_id,
            user_id=request.user_id or user_id,
            project_id=request.project_id or project_id,
            config=request.config,
            strategy_version_id=request.strategy_version_id,
        )
    except BacktestError as error:
        raise _http_error(error) from error
    except StrategyError as error:
        raise _http_error(error) from error


def _http_error(error: StrategyError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"error_code": error.error_code, "message": error.message},
    )
