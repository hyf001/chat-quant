"""Dispatch orchestration for job runtime instances."""
from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow

from .concurrency import JobRuntimeConcurrencyController
from .instance_service import JobRuntimeInstanceService
from .registry import JobRuntimeRegistry, job_runtime_registry
from .types import ExecutionError, InstanceStatus, JobRef, JobRuntimeEvent, NotificationEvent

logger = logging.getLogger(__name__)


class JobRuntimeDispatcher:
    """Owns dispatch readiness checks and executor invocation."""

    def __init__(
        self,
        instance_service: JobRuntimeInstanceService | None = None,
        *,
        concurrency_controller: JobRuntimeConcurrencyController | None = None,
        registry: JobRuntimeRegistry | None = None,
    ) -> None:
        self._registry = registry or job_runtime_registry
        self._instance_service = instance_service or JobRuntimeInstanceService(
            registry=self._registry,
        )
        self._concurrency_controller = concurrency_controller or JobRuntimeConcurrencyController()

    async def dispatch_due_instances(
        self,
        db: AsyncSession,
        *,
        limit: int = 20,
        now: datetime | None = None,
    ) -> int:
        instances = await self._instance_service.list_due_waiting_instances(
            db,
            limit=limit,
            now=now,
        )
        dispatched = 0
        for instance in instances:
            concurrency = await self._concurrency_controller.can_dispatch(db)
            if not concurrency.allowed:
                logger.info(
                    "[job_runtime] dispatch paused reason=%s active_count=%s "
                    "max_concurrent_instances=%s",
                    concurrency.reason,
                    concurrency.active_count,
                    concurrency.max_concurrent_instances,
                )
                break
            if await self.dispatch_instance(db, instance):
                dispatched += 1
        return dispatched

    async def dispatch_instance(self, db: AsyncSession, instance: JobInstanceRow) -> bool:
        await db.refresh(instance)
        job_ref = JobRef(job_type=instance.job_type, job_id=instance.job_id)

        reason, _message = await self._instance_service.dispatch_not_ready_reason(db, instance)
        if reason:
            logger.info(
                "[job_runtime] dispatch skipped instance_id=%s reason=%s",
                instance.id,
                reason,
            )
            return False

        executor = self._registry.job_executor(instance.job_type)
        if executor is None:
            await self._instance_service.fail_instance(
                db,
                instance,
                ExecutionError(
                    message=f"no job executor registered for job_type={instance.job_type}",
                ),
            )
            return False

        await self._instance_service.mark_dispatching(db, instance)

        try:
            await self._registry.publish_event(
                db,
                JobRuntimeEvent(
                    event=NotificationEvent.DISPATCH,
                    job_ref=job_ref,
                    instance=instance,
                    payload=instance.trigger_payload_json or {},
                ),
            )
            await self._instance_service.start_instance(db, instance)
            result = await executor.execute_job_instance(
                db,
                instance=instance,
                instance_service=self._instance_service,
            )
            await db.refresh(instance)
            if instance.status in {
                InstanceStatus.COMPLETED,
                InstanceStatus.FAILED,
                InstanceStatus.CANCELLED,
            }:
                return instance.status == InstanceStatus.COMPLETED
            await self._instance_service.complete_instance(db, instance, result)
            return True
        except Exception as exc:
            await db.refresh(instance)
            if instance.status in {
                InstanceStatus.COMPLETED,
                InstanceStatus.FAILED,
                InstanceStatus.CANCELLED,
            }:
                logger.exception(
                    "[job_runtime] executor raised after terminal state instance_id=%s",
                    instance.id,
                )
                return instance.status == InstanceStatus.COMPLETED
            await self._instance_service.fail_instance(
                db,
                instance,
                ExecutionError(message=str(exc)),
            )
            return False
