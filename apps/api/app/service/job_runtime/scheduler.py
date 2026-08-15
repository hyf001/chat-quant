"""Background scheduling facade for job runtime instances."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow

from .concurrency import JobRuntimeConcurrencyController
from .dispatcher import JobRuntimeDispatcher
from .instance_service import JobRuntimeInstanceService
from .registry import JobRuntimeRegistry, job_runtime_registry
from .schedule_service import JobRuntimeScheduleService


class JobRuntimeSchedulerService:
    """Job runtime loop that creates and dispatches due instances."""

    def __init__(
        self,
        *,
        schedule_service: JobRuntimeScheduleService | None = None,
        dispatcher: JobRuntimeDispatcher | None = None,
        instance_service: JobRuntimeInstanceService | None = None,
        concurrency_controller: JobRuntimeConcurrencyController | None = None,
        max_concurrent_instances: int = 20,
        registry: JobRuntimeRegistry | None = None,
    ) -> None:
        self._registry = registry or job_runtime_registry
        self._instance_service = instance_service or JobRuntimeInstanceService(
            registry=self._registry,
        )
        self._schedule_service = schedule_service or JobRuntimeScheduleService(
            registry=self._registry,
        )
        self._concurrency_controller = concurrency_controller or JobRuntimeConcurrencyController(
            max_concurrent_instances=max_concurrent_instances,
        )
        self._dispatcher = dispatcher or JobRuntimeDispatcher(
            self._instance_service,
            concurrency_controller=self._concurrency_controller,
            registry=self._registry,
        )

    async def create_due_instances(
        self,
        db: AsyncSession,
        target_date: date | None = None,
        now: datetime | None = None,
    ) -> int:
        return len(await self.create_due_instance_records(db, target_date=target_date, now=now))

    async def create_due_instance_records(
        self,
        db: AsyncSession,
        target_date: date | None = None,
        *,
        now: datetime | None = None,
        job_types: set[str] | None = None,
    ) -> list[JobInstanceRow]:
        now = now or datetime.now()
        target_date = target_date or now.date()
        return await self._schedule_service.create_due_instance_records(
            db,
            target_date,
            instance_service=self._instance_service,
            job_types=job_types,
        )

    async def dispatch_due_instances(
        self,
        db: AsyncSession,
        *,
        limit: int = 20,
        now: datetime | None = None,
    ) -> int:
        return await self._dispatcher.dispatch_due_instances(db, limit=limit, now=now)
