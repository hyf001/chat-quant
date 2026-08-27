from __future__ import annotations

from datetime import date

import pytest
from app.db.session import get_session_factory
from app.model.job_runtime import JobInstanceRow
from app.model.job_runtime.enums import TriggerType
from app.service.job_runtime import JobRef, JobRuntimeInstanceService, JobRuntimeScheduleService
from sqlalchemy import select


@pytest.mark.asyncio
async def test_schedule_trigger_key_omits_scheduler_id_and_payload_scheduler_id() -> None:
    job_ref = JobRef(job_type="test.schedule", job_id="daily")
    schedule_service = JobRuntimeScheduleService()

    async with get_session_factory()() as db:
        await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron="0 18 * * *",
            payload={"write_mode": "skip"},
        )

        instances = await schedule_service.create_due_instance_records(db, date(2026, 8, 14))

        assert len(instances) == 1
        assert instances[0].trigger_key == "schedule:2026-08-14T18:00:00"
        assert instances[0].trigger_payload_json == {"write_mode": "skip"}


@pytest.mark.asyncio
async def test_schedule_recreate_keeps_same_trigger_time_idempotent() -> None:
    job_ref = JobRef(job_type="test.schedule", job_id="recreate")
    schedule_service = JobRuntimeScheduleService()
    instance_service = JobRuntimeInstanceService()

    async with get_session_factory()() as db:
        scheduler = await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron="0 18 * * *",
        )
        first_instances = await schedule_service.create_due_instance_records(db, date(2026, 8, 14))

        await db.delete(scheduler)
        await db.commit()
        recreated_scheduler = await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron="0 18 * * *",
        )
        second_instances = await schedule_service.create_due_instance_records(
            db,
            date(2026, 8, 14),
            instance_service=instance_service,
        )

        rows = (
            await db.execute(
                select(JobInstanceRow).where(
                    JobInstanceRow.job_type == job_ref.job_type,
                    JobInstanceRow.job_id == job_ref.job_id,
                )
            )
        ).scalars().all()
        await db.refresh(recreated_scheduler)

        assert len(first_instances) == 1
        assert second_instances == []
        assert len(rows) == 1
        assert recreated_scheduler.last_run_at == first_instances[0].scheduled_for


@pytest.mark.asyncio
async def test_schedule_recreate_after_rerun_keeps_same_trigger_time_idempotent() -> None:
    job_ref = JobRef(job_type="test.schedule", job_id="rerun")
    schedule_service = JobRuntimeScheduleService()
    instance_service = JobRuntimeInstanceService()

    async with get_session_factory()() as db:
        await schedule_service.upsert_scheduler(
            db,
            job_ref=job_ref,
            cron="0 18 * * *",
        )
        first_instances = await schedule_service.create_due_instance_records(
            db,
            date(2026, 8, 14),
            instance_service=instance_service,
        )

        rerun_instance = await instance_service.rerun_job_instance(db, first_instances[0])
        second_instances = await schedule_service.create_due_instance_records(
            db,
            date(2026, 8, 14),
            instance_service=instance_service,
        )

        rows = (
            await db.execute(
                select(JobInstanceRow).where(
                    JobInstanceRow.job_type == job_ref.job_type,
                    JobInstanceRow.job_id == job_ref.job_id,
                )
            )
        ).scalars().all()

        assert len(first_instances) == 1
        assert rerun_instance.trigger_type == TriggerType.RERUN
        assert second_instances == []
        assert len(rows) == 1
