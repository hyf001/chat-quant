"""Framework-owned scheduler management."""
from __future__ import annotations

import logging
from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow, JobSchedulerRow

from .instance_service import DuplicateJobInstanceError, JobRuntimeInstanceService
from .registry import JobRuntimeRegistry, job_runtime_registry
from .types import JobRef, JobTrigger, TriggerType

logger = logging.getLogger(__name__)


class JobRuntimeScheduleService:
    """Owns scheduler table scanning and instance creation."""

    def __init__(self, *, registry: JobRuntimeRegistry | None = None) -> None:
        self._registry = registry or job_runtime_registry

    async def get_scheduler(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
    ) -> JobSchedulerRow | None:
        result = await db.execute(
            select(JobSchedulerRow)
            .where(
                JobSchedulerRow.job_type == job_ref.job_type,
                JobSchedulerRow.job_id == job_ref.job_id,
            )
            .order_by(JobSchedulerRow.id.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def upsert_scheduler(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        cron: str,
        payload: dict | None = None,
    ) -> JobSchedulerRow:
        cron = cron.strip()
        if not cron:
            raise ValueError("cron must not be empty")
        scheduler = await self.get_scheduler(db, job_ref=job_ref)
        now = _now()
        if scheduler is None:
            scheduler = JobSchedulerRow(
                id=_new_id("sch"),
                job_type=job_ref.job_type,
                job_id=job_ref.job_id,
                created_at=now,
            )
            db.add(scheduler)
        scheduler.cron = cron
        scheduler.payload_json = payload or {}
        scheduler.next_run_at = None
        scheduler.updated_at = now
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            scheduler = await self.get_scheduler(db, job_ref=job_ref)
            if scheduler is None:
                raise
            scheduler.cron = cron
            scheduler.payload_json = payload or {}
            scheduler.next_run_at = None
            scheduler.updated_at = _now()
            await db.commit()
        await db.refresh(scheduler)
        return scheduler

    async def delete_scheduler(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
    ) -> bool:
        scheduler = await self.get_scheduler(db, job_ref=job_ref)
        if scheduler is None:
            return False
        await db.delete(scheduler)
        await db.commit()
        return True

    async def create_due_instance_records(
        self,
        db: AsyncSession,
        target_date: date,
        *,
        instance_service: JobRuntimeInstanceService | None = None,
        job_types: set[str] | None = None,
    ) -> list[JobInstanceRow]:
        instance_service = instance_service or JobRuntimeInstanceService()
        result = await db.execute(
            select(JobSchedulerRow).order_by(JobSchedulerRow.id.asc())
        )
        instances: list[JobInstanceRow] = []
        for scheduler in result.scalars().all():
            if job_types is not None and scheduler.job_type not in job_types:
                continue
            for scheduled_for in _scheduled_times(scheduler, target_date):
                try:
                    job_ref = JobRef(job_type=scheduler.job_type, job_id=scheduler.job_id)
                    trigger = _trigger_from_scheduler(scheduler, scheduled_for)
                    factory = self._registry.instance_factory(scheduler.job_type)
                    if factory is not None:
                        created_instances = await factory.create_job_instances(
                            db,
                            job_ref=job_ref,
                            trigger=trigger,
                            instance_service=instance_service,
                        )
                    else:
                        created_instances = [
                            await _create_instance_from_trigger(
                                db,
                                instance_service,
                                job_ref,
                                trigger,
                            )
                        ]
                except DuplicateJobInstanceError:
                    await self.mark_scheduler_processed(db, scheduler.id, scheduled_for)
                    continue
                except ValueError:
                    continue
                await self.mark_scheduler_processed(db, scheduler.id, scheduled_for)
                instances.extend(created_instances)
        return instances

    async def mark_scheduler_processed(
        self,
        db: AsyncSession,
        scheduler_id: str,
        scheduled_for: datetime,
    ) -> None:
        scheduler = await db.get(JobSchedulerRow, scheduler_id)
        if scheduler is None:
            return
        scheduler.last_run_at = scheduled_for
        scheduler.next_run_at = None
        scheduler.updated_at = _now()
        await db.commit()


async def _create_instance_from_trigger(
    db: AsyncSession,
    instance_service: JobRuntimeInstanceService,
    job_ref: JobRef,
    trigger: JobTrigger,
) -> JobInstanceRow:
    return await instance_service.create_job_instance(
        db,
        job_ref=job_ref,
        trigger_type=trigger.trigger_type,
        trigger_key=trigger.trigger_key,
        scheduled_for=trigger.scheduled_for,
        payload=dict(trigger.payload),
    )


def _trigger_from_scheduler(scheduler: JobSchedulerRow, scheduled_for: datetime) -> JobTrigger:
    payload = dict(scheduler.payload_json or {})
    return JobTrigger(
        trigger_type=TriggerType.SCHEDULE,
        trigger_key=f"schedule:{scheduled_for.isoformat()}",
        scheduled_for=scheduled_for,
        payload=payload,
        scheduler=scheduler,
    )


def _scheduled_times(scheduler: JobSchedulerRow, target_date: date) -> list[datetime]:
    return _scheduled_times_for_date(scheduler.cron, target_date)


def _scheduled_times_for_date(cron_expression: str | None, target_date: date) -> list[datetime]:
    if not cron_expression:
        return []
    parts = cron_expression.split()
    if len(parts) != 5:
        logger.warning("[job_runtime] unsupported cron expression: %s", cron_expression)
        return []
    try:
        minute_values = _cron_field_values(parts[0], 0, 59)
        hour_values = _cron_field_values(parts[1], 0, 23)
        day_of_month_values = _cron_field_values(parts[2], 1, 31)
        month_values = _cron_field_values(parts[3], 1, 12)
        day_of_week_values = _cron_field_values(parts[4], 0, 7)
    except ValueError:
        logger.warning("[job_runtime] unsupported cron expression: %s", cron_expression)
        return []
    if not _cron_field_matches(target_date.day, day_of_month_values):
        return []
    if not _cron_field_matches(target_date.month, month_values):
        return []
    cron_weekday = (target_date.weekday() + 1) % 7
    if not _cron_field_matches(cron_weekday, day_of_week_values):
        return []
    return [
        datetime.combine(target_date, datetime.min.time()).replace(
            hour=hour,
            minute=minute,
        )
        for hour in sorted(hour_values or set(range(24)))
        for minute in sorted(minute_values or set(range(60)))
    ]


def _cron_field_values(field: str, minimum: int, maximum: int) -> set[int] | None:
    if field == "*":
        return None
    values: set[int] = set()
    for part in field.split(","):
        step = 1
        base = part
        if "/" in part:
            base, step_value = part.split("/", 1)
            step = int(step_value)
        if base == "*":
            start, end = minimum, maximum
        elif "-" in base:
            start_value, end_value = base.split("-", 1)
            start, end = int(start_value), int(end_value)
        else:
            start = end = int(base)
        if step <= 0 or start < minimum or end > maximum or start > end:
            raise ValueError(f"invalid cron field: {field}")
        values.update(range(start, end + 1, step))
    return values


def _cron_field_matches(value: int, allowed_values: set[int] | None) -> bool:
    return allowed_values is None or value in allowed_values


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


def _now() -> datetime:
    return datetime.now().replace(microsecond=0)
