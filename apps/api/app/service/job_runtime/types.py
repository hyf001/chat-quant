"""Shared types for the job runtime."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime.enums import InstanceStatus, TriggerType

if TYPE_CHECKING:
    from app.model.job_runtime import JobInstanceRow, JobSchedulerRow
    from app.service.job_runtime.instance_service import JobRuntimeInstanceService


class NotificationEvent(StrEnum):
    DISPATCH = "dispatch"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class JobRef:
    job_type: str
    job_id: str


@dataclass(frozen=True)
class JobTrigger:
    trigger_type: TriggerType
    trigger_key: str
    scheduled_for: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    scheduler: "JobSchedulerRow | None" = None


@dataclass(frozen=True)
class PrioritySpec:
    business_priority: int = 0
    trigger_priority: int = 0
    due_at: datetime | None = None
    created_at: datetime | None = None
    custom_score: int = 0


@dataclass(frozen=True)
class ExecutionResult:
    result_status: str | None = None
    summary: str = ""
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionError:
    message: str
    summary: str = ""
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class JobRuntimeEvent:
    event: NotificationEvent
    job_ref: JobRef
    instance: "JobInstanceRow"
    result: ExecutionResult | None = None
    error: ExecutionError | None = None
    payload: dict[str, Any] = field(default_factory=dict)


class JobRuntimeEventHandler(Protocol):
    async def handle_job_runtime_event(self, db: AsyncSession, event: JobRuntimeEvent) -> None:
        ...


class JobExecutor(Protocol):
    async def execute_job_instance(
        self,
        db: AsyncSession,
        *,
        instance: "JobInstanceRow",
        instance_service: "JobRuntimeInstanceService",
    ) -> ExecutionResult:
        ...


class JobInstanceFactory(Protocol):
    async def create_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        trigger: JobTrigger,
        instance_service: "JobRuntimeInstanceService",
    ) -> list["JobInstanceRow"]:
        ...
