from __future__ import annotations

from datetime import date, datetime, time, timedelta
from importlib import import_module
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.v1.dependencies import DatabaseSession
from app.model.job_runtime import JobInstanceRow, JobSchedulerRow
from app.schema.job_runtime import JobRuntimeInstanceResponse
from app.schema.mindgo import (
    MindgoConnectionTestRequest,
    MindgoConnectionTestResponse,
    MindgoSourceListResponse,
    MindgoSourceQueryRequest,
    MindgoSourceQueryResponse,
    MindgoSourceSchema,
    MindgoSourceSyncRequest,
    MindgoSourceSyncSchedulerRequest,
    MindgoSourceSyncSchedulerState,
    MindgoSourceSyncStatusResponse,
    MindgoSourceSyncTriggerRequest,
    MindgoSourceSyncTriggerResponse,
)
from app.service.datasource.mindgo.index_a_daily_price.constants import (
    INDEX_A_DAILY_PRICE_SOURCE_ID,
)
from app.service.datasource.mindgo.index_a_daily_price.job import (
    index_a_daily_price_sync_job_ref,
)
from app.service.datasource.mindgo.stock_a_adjust_factor.constants import (
    STOCK_A_ADJUST_FACTOR_SOURCE_ID,
)
from app.service.datasource.mindgo.stock_a_adjust_factor.job import (
    stock_a_adjust_factor_sync_job_ref,
)
from app.service.datasource.mindgo.stock_a_daily_price.constants import (
    STOCK_A_DAILY_PRICE_SOURCE_ID,
)
from app.service.datasource.mindgo.stock_a_daily_price.job import stock_a_daily_price_sync_job_ref
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.constants import (
    STOCK_A_VALUATION_METRICS_SOURCE_ID,
)
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.job import (
    stock_a_daily_valuation_metrics_sync_job_ref,
)
from app.service.datasource.mindgo.stock_a_snapshot_info.constants import (
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
)
from app.service.datasource.mindgo.stock_a_snapshot_info.job import (
    stock_a_snapshot_info_sync_job_ref,
)
from app.service.job_runtime import (
    DuplicateJobInstanceError,
    JobRef,
    JobRuntimeInstanceService,
    JobRuntimeScheduleService,
    TriggerType,
    job_runtime_registry,
    register_default_job_runtime_events,
)

router = APIRouter()


@router.get("/sources", response_model=MindgoSourceListResponse)
async def list_mindgo_sources() -> MindgoSourceListResponse:
    service = _mindgo_service()
    return await service.list_sources()


@router.post("/test", response_model=MindgoConnectionTestResponse)
async def test_mindgo_connection(
    payload: MindgoConnectionTestRequest,
) -> MindgoConnectionTestResponse:
    service = _mindgo_service()
    return await service.test_connection(payload)


@router.get("/sources/{source_id}/schema", response_model=MindgoSourceSchema)
async def get_mindgo_source_schema(source_id: str) -> MindgoSourceSchema:
    service = _mindgo_service()
    try:
        return await service.get_source_schema(source_id)
    except service.MindgoSourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据源不存在：{error.source_id}",
        ) from error


@router.post("/sources/{source_id}/query", response_model=MindgoSourceQueryResponse)
async def query_mindgo_source(
    source_id: str,
    payload: MindgoSourceQueryRequest,
) -> MindgoSourceQueryResponse:
    service = _mindgo_service()
    try:
        return await service.query_source(source_id, payload)
    except service.MindgoSourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据源不存在：{error.source_id}",
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


@router.get("/sources/{source_id}/sync", response_model=MindgoSourceSyncStatusResponse)
async def get_mindgo_source_sync_status(
    source_id: str,
    db: DatabaseSession,
) -> MindgoSourceSyncStatusResponse:
    job_ref = _sync_job_ref_for_source(source_id)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    scheduler = await schedule_service.get_scheduler(db, job_ref=job_ref)
    return MindgoSourceSyncStatusResponse(
        source_id=source_id,
        job_type=job_ref.job_type,
        job_id=job_ref.job_id,
        scheduler=_scheduler_state(scheduler),
    )


@router.post("/sources/{source_id}/sync", response_model=MindgoSourceSyncTriggerResponse)
async def sync_mindgo_source(
    source_id: str,
    payload: MindgoSourceSyncTriggerRequest,
    db: DatabaseSession,
) -> MindgoSourceSyncTriggerResponse:
    if _has_query_window(payload) and not _source_supports_query_window(source_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MindGo 数据源不支持查询窗口：{source_id}",
        )
    job_ref = _sync_job_ref_for_source(source_id)
    register_default_job_runtime_events(job_runtime_registry)
    instance_service = JobRuntimeInstanceService(registry=job_runtime_registry)
    instances = []
    for base_date in _date_range(payload.trigger_start_date, payload.trigger_end_date):
        scheduled_for = _manual_scheduled_for(base_date, payload.trigger_time)
        instance_payload = _sync_payload_for_base_date(payload, base_date)
        try:
            instances.append(
                await instance_service.create_job_instance(
                    db,
                    job_ref=job_ref,
                    trigger_type=TriggerType.MANUAL,
                    trigger_key=f"manual:{source_id}:{scheduled_for.isoformat()}",
                    scheduled_for=scheduled_for,
                    payload=instance_payload.model_dump(mode="json"),
                )
            )
        except DuplicateJobInstanceError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Job instance already exists for the same manual trigger time",
            ) from error
    instance_responses = [_instance_response(instance) for instance in instances]
    return MindgoSourceSyncTriggerResponse(
        instance=instance_responses[0],
        instances=instance_responses,
    )


@router.post(
    "/sources/{source_id}/sync/scheduler",
    response_model=MindgoSourceSyncStatusResponse,
)
async def upsert_mindgo_source_sync_scheduler(
    source_id: str,
    payload: MindgoSourceSyncSchedulerRequest,
    db: DatabaseSession,
) -> MindgoSourceSyncStatusResponse:
    if _has_query_window(payload) and not _source_supports_query_window(source_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MindGo 数据源不支持查询窗口：{source_id}",
        )
    job_ref = _sync_job_ref_for_source(source_id)
    register_default_job_runtime_events(job_runtime_registry)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    try:
        await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron=payload.cron,
            payload={
                "write_mode": payload.write_mode,
                "query_window": payload.query_window.model_dump(mode="json"),
                "params": payload.params,
            },
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    return await get_mindgo_source_sync_status(source_id, db)


@router.delete(
    "/sources/{source_id}/sync/scheduler",
    response_model=MindgoSourceSyncStatusResponse,
)
async def delete_mindgo_source_sync_scheduler(
    source_id: str,
    db: DatabaseSession,
) -> MindgoSourceSyncStatusResponse:
    job_ref = _sync_job_ref_for_source(source_id)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    await schedule_service.delete_scheduler(db, job_ref=job_ref)
    return await get_mindgo_source_sync_status(source_id, db)


def _mindgo_service() -> Any:
    return import_module("app.service.datasource.mindgo.service")


def _sync_job_ref_for_source(source_id: str) -> JobRef:
    if source_id == STOCK_A_DAILY_PRICE_SOURCE_ID:
        return stock_a_daily_price_sync_job_ref()
    if source_id == STOCK_A_ADJUST_FACTOR_SOURCE_ID:
        return stock_a_adjust_factor_sync_job_ref()
    if source_id == STOCK_A_VALUATION_METRICS_SOURCE_ID:
        return stock_a_daily_valuation_metrics_sync_job_ref()
    if source_id == INDEX_A_DAILY_PRICE_SOURCE_ID:
        return index_a_daily_price_sync_job_ref()
    if source_id == STOCK_A_SNAPSHOT_INFO_SOURCE_ID:
        return stock_a_snapshot_info_sync_job_ref()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"MindGo 数据源暂未配置同步任务：{source_id}",
    )


def _source_supports_query_window(source_id: str) -> bool:
    if source_id == INDEX_A_DAILY_PRICE_SOURCE_ID:
        return True
    if source_id in {
        STOCK_A_DAILY_PRICE_SOURCE_ID,
        STOCK_A_ADJUST_FACTOR_SOURCE_ID,
        STOCK_A_VALUATION_METRICS_SOURCE_ID,
        STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
    }:
        return False
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"MindGo 数据源暂未配置同步任务：{source_id}",
    )


def _instance_response(instance: JobInstanceRow) -> JobRuntimeInstanceResponse:
    return JobRuntimeInstanceResponse(
        id=instance.id,
        job_type=instance.job_type,
        job_id=instance.job_id,
        trigger_type=instance.trigger_type,
        trigger_key=instance.trigger_key,
        payload=dict(instance.trigger_payload_json or {}),
        priority=instance.priority,
        status=instance.status,
        scheduled_for=instance.scheduled_for,
        started_at=instance.started_at,
        completed_at=instance.completed_at,
        result_status=instance.result_status,
        summary=instance.summary,
        error_message=instance.error_message,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )


def _scheduler_state(scheduler: JobSchedulerRow | None) -> MindgoSourceSyncSchedulerState:
    if scheduler is None:
        return MindgoSourceSyncSchedulerState(configured=False)
    payload = dict(scheduler.payload_json or {})
    params = payload.get("params")
    return MindgoSourceSyncSchedulerState(
        configured=True,
        scheduler_id=scheduler.id,
        cron=scheduler.cron,
        write_mode=payload.get("write_mode", "overwrite"),
        query_window=payload.get("query_window") or {},
        params=dict(params) if isinstance(params, dict) else {},
        last_run_at=scheduler.last_run_at,
        next_run_at=scheduler.next_run_at,
        created_at=scheduler.created_at,
        updated_at=scheduler.updated_at,
    )


def _date_range(start_date, end_date):
    day_count = (end_date - start_date).days + 1
    return [start_date + timedelta(days=offset) for offset in range(day_count)]


def _manual_scheduled_for(sync_day: date, trigger_time: time) -> datetime:
    return datetime.combine(
        sync_day,
        trigger_time.replace(microsecond=0),
    )


def _has_query_window(payload: Any) -> bool:
    return (
        payload.query_window.start_offset_days != 0
        or payload.query_window.end_offset_days != 0
    )


def _sync_payload_for_base_date(
    payload: MindgoSourceSyncTriggerRequest,
    base_date: date,
) -> MindgoSourceSyncRequest:
    start_date = base_date + timedelta(days=payload.query_window.start_offset_days)
    end_date = base_date + timedelta(days=payload.query_window.end_offset_days)
    return MindgoSourceSyncRequest(
        start_date=start_date,
        end_date=end_date,
        write_mode=payload.write_mode,
        query_window=payload.query_window,
        params=dict(payload.params),
    )
