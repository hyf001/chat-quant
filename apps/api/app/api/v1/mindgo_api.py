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
    MindgoDatasetDuckDBQueryRequest,
    MindgoDatasetListResponse,
    MindgoDatasetQueryRequest,
    MindgoDatasetQueryResponse,
    MindgoDatasetSchema,
    MindgoDatasetSyncRequest,
    MindgoDatasetSyncSchedulerRequest,
    MindgoDatasetSyncSchedulerState,
    MindgoDatasetSyncStatusResponse,
    MindgoDatasetSyncTriggerRequest,
    MindgoDatasetSyncTriggerResponse,
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
from app.service.mindgo.stock_a_daily_price.constants import STOCK_A_DAILY_PRICE_DATASET_ID
from app.service.mindgo.stock_a_daily_price.job import stock_a_daily_price_sync_job_ref

router = APIRouter()


@router.get("/datasets", response_model=MindgoDatasetListResponse)
async def list_mindgo_datasets() -> MindgoDatasetListResponse:
    service = _mindgo_service()
    return await service.list_datasets()


@router.post("/test", response_model=MindgoConnectionTestResponse)
async def test_mindgo_connection(
    payload: MindgoConnectionTestRequest,
) -> MindgoConnectionTestResponse:
    service = _mindgo_service()
    return await service.test_connection(payload)


@router.get("/datasets/{dataset_id}/schema", response_model=MindgoDatasetSchema)
async def get_mindgo_dataset_schema(dataset_id: str) -> MindgoDatasetSchema:
    service = _mindgo_service()
    try:
        return await service.get_schema(dataset_id)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error


@router.post("/datasets/{dataset_id}/query", response_model=MindgoDatasetQueryResponse)
async def query_mindgo_dataset(
    dataset_id: str,
    payload: MindgoDatasetQueryRequest,
) -> MindgoDatasetQueryResponse:
    service = _mindgo_service()
    try:
        return await service.query_dataset(dataset_id, payload)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


@router.post("/datasets/{dataset_id}/query_from_duckdb", response_model=MindgoDatasetQueryResponse)
async def query_mindgo_dataset_from_duckdb(
    dataset_id: str,
    payload: MindgoDatasetDuckDBQueryRequest,
) -> MindgoDatasetQueryResponse:
    service = _mindgo_service()
    try:
        return await service.query_dataset_from_duckdb(dataset_id, payload)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


@router.get("/datasets/{dataset_id}/sync", response_model=MindgoDatasetSyncStatusResponse)
async def get_mindgo_dataset_sync_status(
    dataset_id: str,
    db: DatabaseSession,
) -> MindgoDatasetSyncStatusResponse:
    job_ref = _sync_job_ref_for_dataset(dataset_id)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    scheduler = await schedule_service.get_scheduler(db, job_ref=job_ref)
    return MindgoDatasetSyncStatusResponse(
        dataset_id=dataset_id,
        job_type=job_ref.job_type,
        job_id=job_ref.job_id,
        scheduler=_scheduler_state(scheduler),
    )


@router.post("/datasets/{dataset_id}/sync", response_model=MindgoDatasetSyncTriggerResponse)
async def sync_mindgo_dataset(
    dataset_id: str,
    payload: MindgoDatasetSyncTriggerRequest,
    db: DatabaseSession,
) -> MindgoDatasetSyncTriggerResponse:
    job_ref = _sync_job_ref_for_dataset(dataset_id)
    register_default_job_runtime_events(job_runtime_registry)
    instance_service = JobRuntimeInstanceService(registry=job_runtime_registry)
    instances = []
    for sync_day in _date_range(payload.trigger_start_date, payload.trigger_end_date):
        scheduled_for = _manual_scheduled_for(sync_day, payload.trigger_time)
        daily_payload = _sync_payload_for_scheduled_for(payload, scheduled_for)
        try:
            instances.append(
                await instance_service.create_job_instance(
                    db,
                    job_ref=job_ref,
                    trigger_type=TriggerType.MANUAL,
                    trigger_key=f"manual:{dataset_id}:{scheduled_for.isoformat()}",
                    scheduled_for=scheduled_for,
                    payload=daily_payload.model_dump(mode="json"),
                )
            )
        except DuplicateJobInstanceError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Job instance already exists for the same manual trigger time",
            ) from error
    instance_responses = [_instance_response(instance) for instance in instances]
    return MindgoDatasetSyncTriggerResponse(
        instance=instance_responses[0],
        instances=instance_responses,
    )


@router.post(
    "/datasets/{dataset_id}/sync/scheduler",
    response_model=MindgoDatasetSyncStatusResponse,
)
async def upsert_mindgo_dataset_sync_scheduler(
    dataset_id: str,
    payload: MindgoDatasetSyncSchedulerRequest,
    db: DatabaseSession,
) -> MindgoDatasetSyncStatusResponse:
    job_ref = _sync_job_ref_for_dataset(dataset_id)
    register_default_job_runtime_events(job_runtime_registry)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    try:
        await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron=payload.cron,
            payload={
                "write_mode": payload.write_mode,
                "params": payload.params,
            },
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    return await get_mindgo_dataset_sync_status(dataset_id, db)


@router.delete(
    "/datasets/{dataset_id}/sync/scheduler",
    response_model=MindgoDatasetSyncStatusResponse,
)
async def delete_mindgo_dataset_sync_scheduler(
    dataset_id: str,
    db: DatabaseSession,
) -> MindgoDatasetSyncStatusResponse:
    job_ref = _sync_job_ref_for_dataset(dataset_id)
    schedule_service = JobRuntimeScheduleService(registry=job_runtime_registry)
    await schedule_service.delete_scheduler(db, job_ref=job_ref)
    return await get_mindgo_dataset_sync_status(dataset_id, db)


def _mindgo_service() -> Any:
    return import_module("app.service.mindgo.service")


def _sync_job_ref_for_dataset(dataset_id: str) -> JobRef:
    if dataset_id != STOCK_A_DAILY_PRICE_DATASET_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集暂未配置同步任务：{dataset_id}",
        )
    return stock_a_daily_price_sync_job_ref()


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


def _scheduler_state(scheduler: JobSchedulerRow | None) -> MindgoDatasetSyncSchedulerState:
    if scheduler is None:
        return MindgoDatasetSyncSchedulerState(configured=False)
    payload = dict(scheduler.payload_json or {})
    params = payload.get("params")
    return MindgoDatasetSyncSchedulerState(
        configured=True,
        scheduler_id=scheduler.id,
        cron=scheduler.cron,
        write_mode=payload.get("write_mode", "overwrite"),
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


def _sync_payload_for_scheduled_for(
    payload: MindgoDatasetSyncTriggerRequest,
    scheduled_for: datetime,
) -> MindgoDatasetSyncRequest:
    sync_date = scheduled_for.date()
    return MindgoDatasetSyncRequest(
        start_date=sync_date,
        end_date=sync_date,
        write_mode=payload.write_mode,
        params=dict(payload.params),
    )
