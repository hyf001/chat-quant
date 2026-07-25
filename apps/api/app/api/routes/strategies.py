from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import ProjectId, UserId
from app.application.dependencies import get_strategy_backtest_engine
from app.domain.backtests.models import (
    StrategyBacktestConfig,
    StrategyBacktestDetail,
    StrategyBacktestProtocol,
)
from app.domain.strategies.models import (
    StrategyCreateResult,
    StrategyDetail,
    StrategyPackage,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
)
from app.domain.strategies.service import StrategyError, strategy_service

router = APIRouter()


class CreateStrategyRequest(BaseModel):
    chat_session_id: str = Field(min_length=1)
    package: StrategyPackage
    user_id: str | None = None
    project_id: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None

    model_config = ConfigDict(extra="forbid")


class UpdateStrategyRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    tags: list[str] | None = None
    status: StrategyStatus | None = None

    model_config = ConfigDict(extra="forbid")


class StrategyBacktestRequest(BaseModel):
    chat_session_id: str = Field(min_length=1)
    config: StrategyBacktestConfig
    user_id: str | None = None
    project_id: str | None = None

    model_config = ConfigDict(extra="forbid")


@router.get("/strategies", response_model=list[StrategySummary])
async def list_strategies(
    user_id: UserId,
    project_id: ProjectId,
) -> list[StrategySummary]:
    return strategy_service.list_strategies(user_id=user_id, project_id=project_id)


@router.post("/strategies", response_model=StrategyCreateResult, status_code=201)
async def create_strategy(
    request: CreateStrategyRequest,
    user_id: UserId,
    project_id: ProjectId,
) -> StrategyCreateResult:
    try:
        return strategy_service.create_strategy(
            user_id=request.user_id or user_id,
            project_id=request.project_id or project_id,
            chat_session_id=request.chat_session_id,
            package=request.package,
            source_sdk_session_id=request.source_sdk_session_id,
            source_sdk_message_uuid=request.source_sdk_message_uuid,
            source_sdk_tool_use_id=request.source_sdk_tool_use_id,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategies/{strategy_id}", response_model=StrategyDetail)
async def get_strategy(strategy_id: str) -> StrategyDetail:
    try:
        return strategy_service.get_strategy(strategy_id)
    except StrategyError as error:
        raise _http_error(error) from error


@router.patch("/strategies/{strategy_id}", response_model=StrategyRecord)
async def update_strategy(strategy_id: str, request: UpdateStrategyRequest) -> StrategyRecord:
    try:
        return strategy_service.update_strategy_metadata(
            strategy_id,
            name=request.name,
            description=request.description,
            tags=request.tags,
            status=request.status,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.delete("/strategies/{strategy_id}", response_model=StrategyRecord)
async def delete_strategy(strategy_id: str) -> StrategyRecord:
    try:
        return strategy_service.update_strategy_metadata(
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
) -> StrategyBacktestDetail:
    try:
        return strategy_service.backtest_strategy(
            strategy_id=strategy_id,
            user_id=request.user_id or user_id,
            project_id=request.project_id or project_id,
            chat_session_id=request.chat_session_id,
            config=request.config,
            engine=get_strategy_backtest_engine(),
        )
    except StrategyError as error:
        raise _http_error(error) from error


def _http_error(error: StrategyError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"error_code": error.error_code, "message": error.message},
    )
