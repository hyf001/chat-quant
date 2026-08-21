from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.backtest import (
    StrategyBacktestConfig,
    StrategyBacktestDetail,
    StrategyBacktestProtocol,
)
from app.schema.job_runtime import JobRuntimeInstanceResponse
from app.schema.strategy import (
    StrategyCreate,
    StrategyCreateResult,
    StrategyDeploymentCreate,
    StrategyDeploymentRecord,
    StrategyDeploymentUpdate,
    StrategyDetail,
    StrategyRecord,
    StrategySignalActionCount,
    StrategySignalActionType,
    StrategySignalListResponse,
    StrategySignalRecord,
    StrategyStatus,
    StrategySummary,
    StrategyVersionCreate,
    StrategyVersionRecord,
)
from app.service import backtest as backtest_service
from app.service import strategy as strategy_service
from app.service.backtest import BacktestError
from app.service.strategy import StrategyDeploymentError, StrategyDeploymentService, StrategyError

router = APIRouter()


class CreateStrategyRequest(StrategyCreate):
    project_id: str = Field(min_length=1)

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
    project_id: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class CreateStrategyDeploymentRequest(StrategyDeploymentCreate):
    pass


class UpdateStrategyDeploymentRequest(StrategyDeploymentUpdate):
    pass


class TriggerStrategyDeploymentRequest(BaseModel):
    trigger_key: str | None = Field(default=None, min_length=1, max_length=256)
    payload: dict[str, object] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class StrategyDeploymentScheduleRequest(BaseModel):
    cron: str = Field(min_length=1, max_length=120)

    model_config = ConfigDict(extra="forbid")


@router.get("/strategies", response_model=list[StrategySummary])
async def list_strategies(
    db: Annotated[AsyncSession, Depends(get_db)],
    project_id: Annotated[str, Query(min_length=1)],
) -> list[StrategySummary]:
    return await strategy_service.list_strategies(db, project_id=project_id)


@router.post("/strategies", response_model=StrategyCreateResult, status_code=201)
async def create_strategy(
    request: CreateStrategyRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyCreateResult:
    try:
        return await strategy_service.create_strategy(
            db,
            project_id=request.project_id,
            strategy_input=StrategyCreate.model_validate(
                request.model_dump(exclude={"project_id"})
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


@router.get("/strategy-versions/{version_id}", response_model=StrategyVersionRecord)
async def get_strategy_version(
    version_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyVersionRecord:
    try:
        return await strategy_service.get_version(db, version_id)
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
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyBacktestDetail:
    try:
        return await backtest_service.backtest_strategy(
            db,
            strategy_id=strategy_id,
            project_id=request.project_id,
            config=request.config,
            strategy_version_id=request.strategy_version_id,
        )
    except BacktestError as error:
        raise _http_error(error) from error
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategy-deployments", response_model=list[StrategyDeploymentRecord])
async def list_strategy_deployments(
    db: Annotated[AsyncSession, Depends(get_db)],
    project_id: Annotated[str, Query(min_length=1)],
    strategy_id: Annotated[str | None, Query(min_length=1)] = None,
) -> list[StrategyDeploymentRecord]:
    try:
        return await strategy_service.list_deployments(
            db,
            project_id=project_id,
            strategy_id=strategy_id,
        )
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.post("/strategy-deployments", response_model=StrategyDeploymentRecord, status_code=201)
async def create_strategy_deployment(
    request: CreateStrategyDeploymentRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.create_deployment(
            db,
            StrategyDeploymentCreate.model_validate(request.model_dump()),
        )
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.get("/strategy-deployments/{deployment_id}", response_model=StrategyDeploymentRecord)
async def get_strategy_deployment(
    deployment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.get_deployment(db, deployment_id)
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.patch("/strategy-deployments/{deployment_id}", response_model=StrategyDeploymentRecord)
async def update_strategy_deployment(
    deployment_id: str,
    request: UpdateStrategyDeploymentRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.update_deployment(
            db,
            deployment_id,
            StrategyDeploymentUpdate.model_validate(request.model_dump(exclude_unset=True)),
        )
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.delete("/strategy-deployments/{deployment_id}", response_model=StrategyDeploymentRecord)
async def delete_strategy_deployment(
    deployment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.delete_deployment(db, deployment_id)
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.post(
    "/strategy-deployments/{deployment_id}/trigger",
    response_model=JobRuntimeInstanceResponse,
    status_code=201,
)
async def trigger_strategy_deployment(
    deployment_id: str,
    request: TriggerStrategyDeploymentRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JobRuntimeInstanceResponse:
    try:
        instance = await StrategyDeploymentService(db).trigger_run(
            deployment_id,
            trigger_key=request.trigger_key,
            payload=request.payload,
        )
        return _job_instance_response(instance)
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.put(
    "/strategy-deployments/{deployment_id}/schedule",
    response_model=StrategyDeploymentRecord,
)
async def upsert_strategy_deployment_schedule(
    deployment_id: str,
    request: StrategyDeploymentScheduleRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.upsert_strategy_deployment_schedule(
            db,
            deployment_id,
            cron=request.cron,
        )
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.delete(
    "/strategy-deployments/{deployment_id}/schedule",
    response_model=StrategyDeploymentRecord,
)
async def delete_strategy_deployment_schedule(
    deployment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyDeploymentRecord:
    try:
        return await strategy_service.delete_strategy_deployment_schedule(db, deployment_id)
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


@router.get(
    "/strategy-deployments/{deployment_id}/signals",
    response_model=StrategySignalListResponse,
)
async def list_strategy_deployment_signals(
    deployment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    action_filter: Annotated[StrategySignalActionType | None, Query(alias="action")] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> StrategySignalListResponse:
    try:
        items = await strategy_service.list_strategy_signals(
            db,
            deployment_id=deployment_id,
            action=action_filter,
            limit=limit,
            offset=offset,
        )
        total = await strategy_service.count_strategy_signals(
            db,
            deployment_id=deployment_id,
            action=action_filter,
        )
        action_counts = await strategy_service.count_strategy_signals_by_action(
            db,
            deployment_id=deployment_id,
        )
        return StrategySignalListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
            action_counts=[
                StrategySignalActionCount(
                    action=action,
                    count=action_counts.get(action, 0),
                )
                for action in StrategySignalActionType
            ],
        )
    except StrategyDeploymentError as error:
        raise _http_error(error) from error


def _http_error(error: StrategyError) -> HTTPException:
    detail = {"error_code": error.error_code, "message": error.message}
    if getattr(error, "detail", None):
        detail.update(error.detail)
    return HTTPException(
        status_code=error.status_code,
        detail=detail,
    )


def _job_instance_response(instance) -> JobRuntimeInstanceResponse:
    return JobRuntimeInstanceResponse(
        id=instance.id,
        job_type=instance.job_type,
        job_id=instance.job_id,
        trigger_type=instance.trigger_type,
        trigger_key=instance.trigger_key,
        payload=dict(instance.trigger_payload_json or {}),
        priority=instance.priority,
        scheduled_for=instance.scheduled_for,
        started_at=instance.started_at,
        completed_at=instance.completed_at,
        status=instance.status,
        result_status=instance.result_status,
        summary=instance.summary,
        error_message=instance.error_message,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )
