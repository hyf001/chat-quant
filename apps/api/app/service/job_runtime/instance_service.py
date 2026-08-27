"""Job runtime instance operations."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow

from .priority import resolve_priority
from .registry import JobRuntimeRegistry, job_runtime_registry
from .types import (
    ExecutionError,
    ExecutionResult,
    InstanceStatus,
    JobRef,
    JobRuntimeEvent,
    NotificationEvent,
    PrioritySpec,
    TriggerType,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class JobInstanceListPage:
    """Paginated job instance query result."""

    items: list[JobInstanceRow]
    total: int
    page: int
    page_size: int


class DuplicateJobInstanceError(ValueError):
    """Raised when an instance already exists for the same job trigger key."""


class JobRuntimeInstanceService:
    """Owns creation, querying, and state transitions for job instances."""

    def __init__(self, *, registry: JobRuntimeRegistry | None = None) -> None:
        self._registry = registry or job_runtime_registry

    async def create_job_instance(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        trigger_type: TriggerType,
        trigger_key: str,
        scheduled_for: datetime | None = None,
        priority: PrioritySpec | None = None,
        payload: dict | None = None,
    ) -> JobInstanceRow:
        scheduled_for = _to_second(scheduled_for or _now())
        payload = payload or {}
        if await self._job_instance_exists(
            db,
            job_ref=job_ref,
            trigger_key=trigger_key,
        ):
            raise DuplicateJobInstanceError(
                "instance already exists for the same job and trigger key"
            )

        now = _now()
        instance = JobInstanceRow(
            id=_new_id("inst"),
            job_type=job_ref.job_type,
            job_id=job_ref.job_id,
            trigger_type=trigger_type,
            trigger_key=trigger_key,
            trigger_payload_json=payload,
            priority=resolve_priority(priority, now=now),
            status=InstanceStatus.WAITING,
            scheduled_for=scheduled_for,
            summary="",
            error_message="",
            created_at=now,
            updated_at=now,
        )
        db.add(instance)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise DuplicateJobInstanceError(
                "instance already exists for the same job and trigger key"
            ) from exc
        await db.refresh(instance)
        return instance

    async def list_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef | None = None,
        job_type: str | None = None,
        job_id: str | None = None,
        status: InstanceStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[JobInstanceRow]:
        stmt = select(JobInstanceRow).order_by(
            JobInstanceRow.scheduled_for.desc(),
            JobInstanceRow.id.desc(),
        )
        stmt = self._apply_instance_filters(
            stmt,
            job_ref=job_ref,
            job_type=job_type,
            job_id=job_id,
            status=status,
        )
        result = await db.execute(stmt.offset(offset).limit(limit))
        return list(result.scalars().all())

    async def list_job_instances_page(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef | None = None,
        job_type: str | None = None,
        job_id: str | None = None,
        status: InstanceStatus | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> JobInstanceListPage:
        offset = (page - 1) * page_size
        items = await self.list_job_instances(
            db,
            job_ref=job_ref,
            job_type=job_type,
            job_id=job_id,
            status=status,
            limit=page_size,
            offset=offset,
        )
        total = await self.count_job_instances(
            db,
            job_ref=job_ref,
            job_type=job_type,
            job_id=job_id,
            status=status,
        )
        return JobInstanceListPage(items=items, total=total, page=page, page_size=page_size)

    async def count_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef | None = None,
        job_type: str | None = None,
        job_id: str | None = None,
        status: InstanceStatus | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(JobInstanceRow)
        stmt = self._apply_instance_filters(
            stmt,
            job_ref=job_ref,
            job_type=job_type,
            job_id=job_id,
            status=status,
        )
        return int(await db.scalar(stmt) or 0)

    async def count_job_instances_by_status(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef | None = None,
        job_type: str | None = None,
        job_id: str | None = None,
    ) -> dict[InstanceStatus, int]:
        stmt = select(JobInstanceRow.status, func.count()).select_from(JobInstanceRow)
        stmt = self._apply_instance_filters(
            stmt,
            job_ref=job_ref,
            job_type=job_type,
            job_id=job_id,
            status=None,
        )
        result = await db.execute(stmt.group_by(JobInstanceRow.status))
        return {
            status: int(count)
            for status, count in result.all()
        }

    def _apply_instance_filters(
        self,
        stmt,
        *,
        job_ref: JobRef | None = None,
        job_type: str | None = None,
        job_id: str | None = None,
        status: InstanceStatus | None = None,
    ):
        if job_ref is not None:
            job_type = job_ref.job_type
            job_id = job_ref.job_id
        if job_type is not None:
            stmt = stmt.where(JobInstanceRow.job_type == job_type)
        if job_id is not None:
            stmt = stmt.where(JobInstanceRow.job_id == job_id)
        if status is not None:
            stmt = stmt.where(JobInstanceRow.status == status)
        return stmt

    async def get_job_instance(self, db: AsyncSession, instance_id: str) -> JobInstanceRow | None:
        return await db.get(JobInstanceRow, instance_id)

    async def delete_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef | None = None,
        instance_ids: list[str] | None = None,
    ) -> int:
        stmt = select(JobInstanceRow)
        if job_ref is not None:
            stmt = stmt.where(
                JobInstanceRow.job_type == job_ref.job_type,
                JobInstanceRow.job_id == job_ref.job_id,
            )
        if instance_ids is not None:
            stmt = stmt.where(JobInstanceRow.id.in_(instance_ids))

        result = await db.execute(stmt)
        instances = list(result.scalars().all())
        for instance in instances:
            await db.delete(instance)
        await db.commit()
        return len(instances)

    async def list_due_waiting_instances(
        self,
        db: AsyncSession,
        *,
        limit: int = 20,
        now: datetime | None = None,
    ) -> list[JobInstanceRow]:
        now = now or _now()
        result = await db.execute(
            select(JobInstanceRow)
            .where(
                JobInstanceRow.status == InstanceStatus.WAITING,
                JobInstanceRow.scheduled_for <= now,
            )
            .order_by(
                JobInstanceRow.priority.desc(),
                JobInstanceRow.scheduled_for.asc(),
                JobInstanceRow.id.asc(),
            )
            .limit(limit)
        )
        return list(result.scalars().all())

    async def dispatch_not_ready_reason(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
        *,
        now: datetime | None = None,
    ) -> tuple[str, str]:
        now = now or _now()
        scheduled_for = instance.scheduled_for
        if instance.status != InstanceStatus.WAITING:
            return "not_waiting", "instance is not waiting"
        if scheduled_for > now:
            return "scheduled_time", "scheduled time has not arrived"
        return "", ""

    async def mark_dispatching(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
    ) -> JobInstanceRow:
        instance.status = InstanceStatus.DISPATCHING
        instance.error_message = ""
        instance.updated_at = _now()
        await db.commit()
        await db.refresh(instance)
        _log_job_instance_event("dispatching", instance)
        return instance

    async def cancel_waiting_instance(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
        *,
        reason: str,
    ) -> JobInstanceRow:
        instance.status = InstanceStatus.CANCELLED
        instance.summary = "instance cancelled"
        instance.error_message = reason
        instance.completed_at = _now()
        instance.updated_at = _now()
        await db.commit()
        await self._registry.publish_event(
            db,
            _job_runtime_event(
                instance,
                NotificationEvent.CANCELLED,
                error=ExecutionError(message=reason),
            ),
        )
        await db.commit()
        await db.refresh(instance)
        _log_job_instance_event("cancelled", instance, reason=reason)
        return instance

    async def rerun_job_instance(
        self,
        db: AsyncSession,
        source_instance: JobInstanceRow,
    ) -> JobInstanceRow:
        source_instance.status = InstanceStatus.WAITING
        source_instance.trigger_type = TriggerType.RERUN
        source_instance.started_at = None
        source_instance.completed_at = None
        source_instance.result_status = None
        source_instance.summary = ""
        source_instance.error_message = ""
        source_instance.updated_at = _now()
        await db.commit()
        await db.refresh(source_instance)
        _log_job_instance_event("rerun_waiting", source_instance)
        return source_instance

    async def start_instance(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
    ) -> JobInstanceRow:
        instance.status = InstanceStatus.RUNNING
        instance.started_at = _now()
        instance.completed_at = None
        instance.error_message = ""
        instance.updated_at = _now()
        await db.commit()
        await db.refresh(instance)
        _log_job_instance_event("started", instance)
        return instance

    async def complete_instance(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
        result: ExecutionResult,
    ) -> JobInstanceRow:
        instance.status = InstanceStatus.COMPLETED
        instance.result_status = result.result_status
        instance.summary = result.summary
        instance.error_message = ""
        instance.completed_at = _now()
        instance.updated_at = _now()
        await db.commit()
        await self._registry.publish_event(
            db,
            _job_runtime_event(instance, NotificationEvent.COMPLETED, result=result),
        )
        await db.commit()
        await db.refresh(instance)
        _log_job_instance_event(
            "completed",
            instance,
            reason=f"result_status={result.result_status}",
        )
        return instance

    async def fail_instance(
        self,
        db: AsyncSession,
        instance: JobInstanceRow,
        error: ExecutionError,
    ) -> JobInstanceRow:
        instance.status = InstanceStatus.FAILED
        instance.result_status = None
        instance.summary = error.summary
        instance.error_message = error.message
        instance.completed_at = _now()
        instance.updated_at = _now()
        await db.commit()
        await self._registry.publish_event(
            db,
            _job_runtime_event(instance, NotificationEvent.FAILED, error=error),
        )
        await db.commit()
        await db.refresh(instance)
        _log_job_instance_event("failed", instance, level=logging.WARNING, reason=error.message)
        return instance

    async def _job_instance_exists(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        trigger_key: str,
    ) -> bool:
        result = await db.execute(
            select(JobInstanceRow.id).where(
                JobInstanceRow.job_type == job_ref.job_type,
                JobInstanceRow.job_id == job_ref.job_id,
                JobInstanceRow.trigger_key == trigger_key,
            )
        )
        return result.scalar_one_or_none() is not None


def _job_runtime_event(
    instance: JobInstanceRow,
    event: NotificationEvent,
    *,
    result: ExecutionResult | None = None,
    error: ExecutionError | None = None,
) -> JobRuntimeEvent:
    return JobRuntimeEvent(
        event=event,
        job_ref=JobRef(job_type=instance.job_type, job_id=instance.job_id),
        instance=instance,
        result=result,
        error=error,
        payload=instance.trigger_payload_json or {},
    )


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


def _now() -> datetime:
    return _to_second(datetime.now())


def _to_second(value: datetime) -> datetime:
    return value.replace(microsecond=0)


def _log_job_instance_event(
    event: str,
    instance: JobInstanceRow,
    *,
    level: int = logging.INFO,
    reason: str | None = None,
) -> None:
    logger.log(
        level,
        (
            "[job_instance] event=%s instance_id=%s job_type=%s job_id=%s "
            "status=%s scheduled_for=%s reason=%s"
        ),
        event,
        instance.id,
        instance.job_type,
        instance.job_id,
        instance.status,
        instance.scheduled_for,
        reason or "",
    )
