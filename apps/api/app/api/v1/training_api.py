"""双盲 K 线训练 API（薄层：错误映射 + 出口脱敏）。"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.api.v1.dependencies import DatabaseSession
from app.schema.training import (
    TrainingIntradayResponse,
    TrainingReportResponse,
    TrainingRevealRequest,
    TrainingRevealResponse,
    TrainingSessionCreate,
    TrainingSessionListResponse,
    TrainingSessionResponse,
    TrainingSessionStatus,
)
from app.service.training import TrainingError, TrainingService, masking

router = APIRouter()


@router.post(
    "/sessions",
    response_model=TrainingSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_training_session(
    payload: TrainingSessionCreate,
    db: DatabaseSession,
) -> TrainingSessionResponse:
    try:
        response = await TrainingService(db).create_session(payload)
    except TrainingError as error:
        raise _http_error(error) from error
    return _masked(response, TrainingSessionResponse)


@router.get("/sessions/{session_id}", response_model=TrainingSessionResponse)
async def get_training_session(
    session_id: str,
    db: DatabaseSession,
) -> TrainingSessionResponse:
    try:
        response = await TrainingService(db).get_session(session_id)
    except TrainingError as error:
        raise _http_error(error) from error
    return _masked(response, TrainingSessionResponse)


@router.get("/sessions", response_model=TrainingSessionListResponse)
async def list_training_sessions(
    db: DatabaseSession,
    project_id: Annotated[str, Query(min_length=1, max_length=128)],
    status: Annotated[TrainingSessionStatus | None, Query()] = None,
    keyword: Annotated[str | None, Query(max_length=128)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> TrainingSessionListResponse:
    try:
        response = await TrainingService(db).list_sessions(
            project_id,
            status=status.value if status is not None else None,
            keyword=keyword,
            limit=limit,
            offset=offset,
        )
    except TrainingError as error:
        raise _http_error(error) from error
    return _masked(response, TrainingSessionListResponse)


@router.post("/sessions/{session_id}/reveal", response_model=TrainingRevealResponse)
async def reveal_training_bar(
    session_id: str,
    payload: TrainingRevealRequest,
    db: DatabaseSession,
) -> TrainingRevealResponse:
    try:
        response = await TrainingService(db).reveal(session_id, payload)
    except TrainingError as error:
        raise _http_error(error) from error
    return _masked(response, TrainingRevealResponse)


@router.post("/sessions/{session_id}/finish", response_model=TrainingReportResponse)
async def finish_training_session(
    session_id: str,
    db: DatabaseSession,
) -> TrainingReportResponse:
    try:
        return await TrainingService(db).finish(session_id)
    except TrainingError as error:
        raise _http_error(error) from error


@router.get("/sessions/{session_id}/intraday", response_model=TrainingIntradayResponse)
async def get_training_intraday(
    session_id: str,
    db: DatabaseSession,
    seq: Annotated[int, Query(ge=0)],
) -> TrainingIntradayResponse:
    """第 ``seq`` 根日线当天的分时（只有已揭示的根可看）。"""
    try:
        response = await TrainingService(db).intraday(session_id, seq=seq)
    except TrainingError as error:
        raise _http_error(error) from error
    return _masked(response, TrainingIntradayResponse)


@router.get("/sessions/{session_id}/report", response_model=TrainingReportResponse)
async def get_training_report(
    session_id: str,
    db: DatabaseSession,
) -> TrainingReportResponse:
    try:
        return await TrainingService(db).report(session_id)
    except TrainingError as error:
        raise _http_error(error) from error


def _masked[T: BaseModel](response: BaseModel, model: type[T]) -> T:
    """出口收口：训练期响应统一过一遍 masking 的白名单递归。"""
    return model.model_validate(masking.scrub_mapping(response.model_dump()))


def _http_error(error: TrainingError) -> HTTPException:
    detail: dict[str, Any] = {"error_code": error.error_code, "message": error.message}
    detail.update(error.detail)
    return HTTPException(status_code=error.status_code, detail=detail)
