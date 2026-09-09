from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.mindgo import MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_minute_price.constants import (
    STOCK_A_MINUTE_PRICE_SOURCE_ID,
    STOCK_A_MINUTE_PRICE_SYNC_JOB_TYPE,
)
from app.service.job_runtime import (
    ExecutionResult,
    JobRef,
    JobRuntimeInstanceService,
    JobRuntimeRegistry,
    JobTrigger,
    TriggerType,
    job_runtime_registry,
)

if TYPE_CHECKING:
    from app.model.job_runtime import JobInstanceRow


def stock_a_minute_price_sync_job_ref() -> JobRef:
    return JobRef(
        job_type=STOCK_A_MINUTE_PRICE_SYNC_JOB_TYPE,
        job_id=STOCK_A_MINUTE_PRICE_SYNC_JOB_TYPE,
    )


class StockAMinutePriceSyncInstanceFactory:
    async def create_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        trigger: JobTrigger,
        instance_service: JobRuntimeInstanceService,
    ) -> list[JobInstanceRow]:
        payload = _sync_payload_for_trigger(trigger)
        return [
            await instance_service.create_job_instance(
                db,
                job_ref=job_ref,
                trigger_type=trigger.trigger_type,
                trigger_key=trigger.trigger_key,
                scheduled_for=trigger.scheduled_for,
                payload=payload,
            )
        ]


class StockAMinutePriceSyncExecutor:
    async def execute_job_instance(
        self,
        db: AsyncSession,
        *,
        instance: JobInstanceRow,
        instance_service: JobRuntimeInstanceService,
    ) -> ExecutionResult:
        _ = db, instance_service
        from app.service.datasource.mindgo import service as mindgo_service

        request = MindgoSourceSyncRequest.model_validate(instance.trigger_payload_json or {})
        result = await mindgo_service.sync_source(STOCK_A_MINUTE_PRICE_SOURCE_ID, request)
        return ExecutionResult(
            result_status=result.status,
            summary=f"synced {result.synced_count} rows",
            payload={
                "source_id": STOCK_A_MINUTE_PRICE_SOURCE_ID,
                "elapsed_ms": result.elapsed_ms,
                "synced_count": result.synced_count,
            },
        )


def register_stock_a_minute_price_job_runtime_handlers(
    registry: JobRuntimeRegistry | None = None,
) -> JobRuntimeRegistry:
    registry = registry or job_runtime_registry
    registry.register_instance_factory(
        job_type=STOCK_A_MINUTE_PRICE_SYNC_JOB_TYPE,
        factory=StockAMinutePriceSyncInstanceFactory(),
    )
    registry.register_job_executor(
        job_type=STOCK_A_MINUTE_PRICE_SYNC_JOB_TYPE,
        executor=StockAMinutePriceSyncExecutor(),
    )
    return registry


def _sync_payload_for_trigger(trigger: JobTrigger) -> dict[str, Any]:
    if trigger.trigger_type == TriggerType.SCHEDULE:
        query_window = dict((trigger.payload or {}).get("query_window") or {})
        start_offset_days = int(query_window.get("start_offset_days") or 0)
        end_offset_days = int(query_window.get("end_offset_days") or 0)
        base_date = trigger.scheduled_for.date()
        start_date = (base_date + timedelta(days=start_offset_days)).isoformat()
        end_date = (base_date + timedelta(days=end_offset_days)).isoformat()
        return {
            "start_date": start_date,
            "end_date": end_date,
            "write_mode": (trigger.payload or {}).get("write_mode", "overwrite"),
            "query_window": {
                "start_offset_days": start_offset_days,
                "end_offset_days": end_offset_days,
            },
            "params": dict((trigger.payload or {}).get("params") or {}),
        }
    return dict(trigger.payload or {})
