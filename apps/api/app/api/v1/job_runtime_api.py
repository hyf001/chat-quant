from __future__ import annotations

from math import ceil
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.api.v1.dependencies import DatabaseSession
from app.model.job_runtime import JobInstanceRow
from app.schema.job_runtime import (
    JobRuntimeInstanceListResponse,
    JobRuntimeInstanceResponse,
    JobRuntimeInstanceStatusCount,
)
from app.service.job_runtime import InstanceStatus, JobRuntimeInstanceService, job_runtime_registry

router = APIRouter()


@router.get("/instances", response_model=JobRuntimeInstanceListResponse)
async def list_job_instances(
    db: DatabaseSession,
    job_type: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
    job_id: Annotated[str | None, Query(min_length=1, max_length=128)] = None,
    status_filter: Annotated[InstanceStatus | None, Query(alias="status")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> JobRuntimeInstanceListResponse:
    service = JobRuntimeInstanceService(registry=job_runtime_registry)
    result = await service.list_job_instances_page(
        db,
        job_type=job_type,
        job_id=job_id,
        status=status_filter,
        page=page,
        page_size=page_size,
    )
    status_counts = await service.count_job_instances_by_status(
        db,
        job_type=job_type,
        job_id=job_id,
    )
    return JobRuntimeInstanceListResponse(
        items=[_instance_response(instance) for instance in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=ceil(result.total / result.page_size) if result.total else 0,
        status_counts=[
            JobRuntimeInstanceStatusCount(
                status=instance_status,
                count=status_counts.get(instance_status, 0),
            )
            for instance_status in InstanceStatus
        ],
    )


@router.post(
    "/instances/{instance_id}/rerun",
    response_model=JobRuntimeInstanceResponse,
)
async def rerun_job_instance(
    instance_id: str,
    db: DatabaseSession,
) -> JobRuntimeInstanceResponse:
    service = JobRuntimeInstanceService(registry=job_runtime_registry)
    instance = await service.get_job_instance(db, instance_id)
    if instance is None:
        _raise_not_found()
    return _instance_response(await service.rerun_job_instance(db, instance))


@router.delete("/instances/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_instance(
    instance_id: str,
    db: DatabaseSession,
) -> Response:
    service = JobRuntimeInstanceService(registry=job_runtime_registry)
    deleted = await service.delete_job_instances(db, instance_ids=[instance_id])
    if deleted == 0:
        _raise_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _instance_response(instance: JobInstanceRow) -> JobRuntimeInstanceResponse:
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


def _raise_not_found() -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Job instance not found",
    )
