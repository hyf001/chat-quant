"""Database-backed concurrency controls for job runtime dispatch."""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow

from .types import InstanceStatus


@dataclass(frozen=True)
class DispatchConcurrencyDecision:
    allowed: bool
    active_count: int
    max_concurrent_instances: int
    reason: str = ""


class JobRuntimeConcurrencyController:
    """Decides whether more job instances can be dispatched."""

    def __init__(self, *, max_concurrent_instances: int = 20) -> None:
        if max_concurrent_instances <= 0:
            raise ValueError("max concurrent instances must be greater than 0")
        self._max_concurrent_instances = max_concurrent_instances

    @property
    def max_concurrent_instances(self) -> int:
        return self._max_concurrent_instances

    async def can_dispatch(self, db: AsyncSession) -> DispatchConcurrencyDecision:
        active_count = await self.count_active_instances(db)
        if active_count >= self._max_concurrent_instances:
            return DispatchConcurrencyDecision(
                allowed=False,
                active_count=active_count,
                max_concurrent_instances=self._max_concurrent_instances,
                reason="max_concurrent_instances",
            )
        return DispatchConcurrencyDecision(
            allowed=True,
            active_count=active_count,
            max_concurrent_instances=self._max_concurrent_instances,
        )

    async def count_active_instances(self, db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count(JobInstanceRow.id)).where(
                JobInstanceRow.status.in_(
                    [
                        InstanceStatus.DISPATCHING,
                        InstanceStatus.RUNNING,
                    ]
                )
            )
        )
        return int(result.scalar_one())
