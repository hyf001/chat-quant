from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import ProjectId, UserId
from app.domain.strategies.models import (
    StrategyCopyMode,
    StrategyCopySummary,
    StrategyCreateResult,
    StrategyDetail,
    StrategyPackage,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
    StrategyValidationResult,
    StrategyVersionRecord,
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


class CreateStrategyVersionRequest(BaseModel):
    package: StrategyPackage
    parent_version_id: str | None = None
    change_summary: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None

    model_config = ConfigDict(extra="forbid")


class CopyStrategyVersionRequest(BaseModel):
    mode: StrategyCopyMode = StrategyCopyMode.SUMMARY
    user_id: str | None = None
    project_id: str | None = None
    target_chat_session_id: str | None = None

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


@router.post(
    "/strategies/{strategy_id}/versions",
    response_model=StrategyCreateResult,
    status_code=201,
)
async def create_strategy_version(
    strategy_id: str,
    request: CreateStrategyVersionRequest,
) -> StrategyCreateResult:
    try:
        return strategy_service.create_strategy_version(
            strategy_id,
            package=request.package,
            parent_version_id=request.parent_version_id,
            change_summary=request.change_summary,
            source_sdk_session_id=request.source_sdk_session_id,
            source_sdk_message_uuid=request.source_sdk_message_uuid,
            source_sdk_tool_use_id=request.source_sdk_tool_use_id,
        )
    except StrategyError as error:
        raise _http_error(error) from error


@router.get("/strategy-versions/{version_id}", response_model=StrategyVersionRecord)
async def get_strategy_version(version_id: str) -> StrategyVersionRecord:
    try:
        return strategy_service.get_version(version_id)
    except StrategyError as error:
        raise _http_error(error) from error


@router.post("/strategy-versions/{version_id}/validate", response_model=StrategyValidationResult)
async def validate_strategy_version(version_id: str) -> StrategyValidationResult:
    try:
        return strategy_service.validate_version(version_id)
    except StrategyError as error:
        raise _http_error(error) from error


@router.post("/strategy-versions/{version_id}/copy", response_model=StrategyCopySummary)
async def copy_strategy_version(
    version_id: str,
    request: CopyStrategyVersionRequest,
    user_id: UserId,
    project_id: ProjectId,
) -> StrategyCopySummary:
    try:
        return strategy_service.copy_strategy_version(
            version_id,
            mode=request.mode,
            user_id=request.user_id or user_id,
            project_id=request.project_id or project_id,
            target_chat_session_id=request.target_chat_session_id,
        )
    except StrategyError as error:
        raise _http_error(error) from error


def _http_error(error: StrategyError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"error_code": error.error_code, "message": error.message},
    )
