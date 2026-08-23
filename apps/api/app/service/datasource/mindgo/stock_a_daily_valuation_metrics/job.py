from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.mindgo import MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.constants import (
    STOCK_A_VALUATION_METRICS_SOURCE_ID,
    STOCK_A_VALUATION_METRICS_SYNC_JOB_TYPE,
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


def stock_a_daily_valuation_metrics_sync_job_ref() -> JobRef:
    return JobRef(
        job_type=STOCK_A_VALUATION_METRICS_SYNC_JOB_TYPE,
        job_id=STOCK_A_VALUATION_METRICS_SYNC_JOB_TYPE,
    )


class StockAValuationMetricsSyncInstanceFactory:
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


class StockAValuationMetricsSyncExecutor:
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
        result = await mindgo_service.sync_source(STOCK_A_VALUATION_METRICS_SOURCE_ID, request)
        return ExecutionResult(
            result_status=result.status,
            summary=f"synced {result.synced_count} rows",
            payload={
                "source_id": STOCK_A_VALUATION_METRICS_SOURCE_ID,
                "elapsed_ms": result.elapsed_ms,
                "synced_count": result.synced_count,
            },
        )


def register_stock_a_daily_valuation_metrics_job_runtime_handlers(
    registry: JobRuntimeRegistry | None = None,
) -> JobRuntimeRegistry:
    registry = registry or job_runtime_registry
    registry.register_instance_factory(
        job_type=STOCK_A_VALUATION_METRICS_SYNC_JOB_TYPE,
        factory=StockAValuationMetricsSyncInstanceFactory(),
    )
    registry.register_job_executor(
        job_type=STOCK_A_VALUATION_METRICS_SYNC_JOB_TYPE,
        executor=StockAValuationMetricsSyncExecutor(),
    )
    return registry


def _sync_payload_for_trigger(trigger: JobTrigger) -> dict[str, Any]:
    if trigger.trigger_type == TriggerType.SCHEDULE:
        sync_date = trigger.scheduled_for.date().isoformat()
        return {
            "start_date": sync_date,
            "end_date": sync_date,
            "write_mode": (trigger.payload or {}).get("write_mode", "overwrite"),
            "params": dict((trigger.payload or {}).get("params") or {}),
        }
    return dict(trigger.payload or {})
