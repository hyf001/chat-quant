from __future__ import annotations

from datetime import datetime

import pytest
from app.db.session import get_session_factory
from app.service.job_runtime import (
    ExecutionResult,
    InstanceStatus,
    JobRef,
    JobRuntimeConcurrencyController,
    JobRuntimeDispatcher,
    JobRuntimeInstanceService,
    JobRuntimeRegistry,
    TriggerType,
)


class CompletingExecutor:
    async def execute_job_instance(self, db, *, instance, instance_service):
        _ = db, instance, instance_service
        return ExecutionResult(result_status="ok", summary="completed")


@pytest.mark.parametrize("active_status", [InstanceStatus.DISPATCHING, InstanceStatus.RUNNING])
@pytest.mark.asyncio
async def test_dispatch_pauses_when_active_instances_reach_limit(
    active_status: InstanceStatus,
) -> None:
    registry = JobRuntimeRegistry()
    instance_service = JobRuntimeInstanceService(registry=registry)
    now = datetime.now()

    async with get_session_factory()() as db:
        active = await instance_service.create_job_instance(
            db,
            job_ref=JobRef(job_type="test", job_id="active"),
            trigger_type=TriggerType.MANUAL,
            trigger_key=f"manual:active:{active_status}",
            scheduled_for=now,
        )
        await instance_service.mark_dispatching(db, active)
        if active_status == InstanceStatus.RUNNING:
            await instance_service.start_instance(db, active)

        waiting = await instance_service.create_job_instance(
            db,
            job_ref=JobRef(job_type="test", job_id="waiting"),
            trigger_type=TriggerType.MANUAL,
            trigger_key=f"manual:waiting:{active_status}",
            scheduled_for=now,
        )
        dispatcher = JobRuntimeDispatcher(
            instance_service,
            concurrency_controller=JobRuntimeConcurrencyController(max_concurrent_instances=1),
            registry=registry,
        )

        dispatched = await dispatcher.dispatch_due_instances(db, limit=10, now=now)

        assert dispatched == 0
        await db.refresh(waiting)
        assert waiting.status == InstanceStatus.WAITING


@pytest.mark.asyncio
async def test_dispatch_continues_when_active_instances_are_below_limit() -> None:
    registry = JobRuntimeRegistry()
    registry.register_job_executor(job_type="test", executor=CompletingExecutor())
    instance_service = JobRuntimeInstanceService(registry=registry)
    now = datetime.now()

    async with get_session_factory()() as db:
        active = await instance_service.create_job_instance(
            db,
            job_ref=JobRef(job_type="test", job_id="active"),
            trigger_type=TriggerType.MANUAL,
            trigger_key="manual:active:below-limit",
            scheduled_for=now,
        )
        await instance_service.mark_dispatching(db, active)

        waiting = await instance_service.create_job_instance(
            db,
            job_ref=JobRef(job_type="test", job_id="waiting"),
            trigger_type=TriggerType.MANUAL,
            trigger_key="manual:waiting:below-limit",
            scheduled_for=now,
        )
        dispatcher = JobRuntimeDispatcher(
            instance_service,
            concurrency_controller=JobRuntimeConcurrencyController(max_concurrent_instances=2),
            registry=registry,
        )

        dispatched = await dispatcher.dispatch_due_instances(db, limit=10, now=now)

        assert dispatched == 1
        await db.refresh(waiting)
        assert waiting.status == InstanceStatus.COMPLETED
