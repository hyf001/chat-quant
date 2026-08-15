"""Registry for job runtime extension points."""
from __future__ import annotations

from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from .types import JobInstanceFactory, JobRuntimeEvent, JobRuntimeEventHandler, JobExecutor, NotificationEvent


class JobRuntimeRegistry:
    """Keeps job runtime lifecycle logic decoupled from business execution."""

    def __init__(self) -> None:
        self._event_handlers: dict[tuple[str, str], list[JobRuntimeEventHandler]] = defaultdict(list)
        self._instance_factories: dict[str, JobInstanceFactory] = {}
        self._job_executors: dict[str, JobExecutor] = {}

    def register_event_handler(
        self,
        *,
        job_type: str,
        event: NotificationEvent,
        handler: JobRuntimeEventHandler,
    ) -> None:
        key = (job_type, event.value)
        if handler not in self._event_handlers[key]:
            self._event_handlers[key].append(handler)

    async def publish_event(self, db: AsyncSession, event: JobRuntimeEvent) -> None:
        handlers = [
            *self._event_handlers.get((event.job_ref.job_type, event.event.value), []),
            *self._event_handlers.get(("*", event.event.value), []),
        ]
        for handler in handlers:
            await handler.handle_job_runtime_event(db, event)

    def register_instance_factory(
        self,
        *,
        job_type: str,
        factory: JobInstanceFactory,
    ) -> None:
        self._instance_factories[job_type] = factory

    def instance_factory(self, job_type: str) -> JobInstanceFactory | None:
        return self._instance_factories.get(job_type)

    def register_job_executor(self, *, job_type: str, executor: JobExecutor) -> None:
        self._job_executors[job_type] = executor

    def job_executor(self, job_type: str) -> JobExecutor | None:
        return self._job_executors.get(job_type)


job_runtime_registry = JobRuntimeRegistry()
