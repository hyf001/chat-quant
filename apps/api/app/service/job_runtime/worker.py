"""Background worker loops owned by the job runtime."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from app.db.session import get_session_factory

from .scheduler import JobRuntimeSchedulerService

logger = logging.getLogger(__name__)


class JobRuntimeWorker:
    """Runs job runtime scheduling and dispatch loops."""

    def __init__(
        self,
        *,
        creation_tick_minutes: int = 1,
        dispatch_interval_seconds: int = 30,
        dispatch_limit: int = 20,
        max_concurrent_instances: int = 20,
        scheduler_service: JobRuntimeSchedulerService | None = None,
    ) -> None:
        self._creation_tick_minutes = creation_tick_minutes
        self._dispatch_interval_seconds = dispatch_interval_seconds
        self._dispatch_limit = dispatch_limit
        self._max_concurrent_instances = max_concurrent_instances
        self._scheduler_service = scheduler_service or JobRuntimeSchedulerService(
            max_concurrent_instances=max_concurrent_instances,
        )
        self._tasks: list[asyncio.Task[None]] = []

    def start(self) -> None:
        self._tasks = [
            asyncio.create_task(self._creation_loop(), name="job-runtime-instance-creator"),
            asyncio.create_task(self._dispatch_loop(), name="job-runtime-instance-dispatcher"),
        ]
        logger.info(
            "[job_runtime] worker started creation_tick_minutes=%s dispatch_interval_seconds=%s "
            "dispatch_limit=%s max_concurrent_instances=%s",
            self._creation_tick_minutes,
            self._dispatch_interval_seconds,
            self._dispatch_limit,
            self._max_concurrent_instances,
        )

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []

    async def _creation_loop(self) -> None:
        while True:
            await asyncio.sleep(
                _seconds_until_next_creation_tick(datetime.now(), self._creation_tick_minutes)
            )
            try:
                now = datetime.now()
                session_factory = get_session_factory()
                async with session_factory() as db:
                    count = await self._scheduler_service.create_due_instances(db, now=now)
                    logger.info("[job_runtime] created due instances count=%s", count)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("[job_runtime] due instance creation failed")

    async def _dispatch_loop(self) -> None:
        while True:
            try:
                session_factory = get_session_factory()
                async with session_factory() as db:
                    count = await self._scheduler_service.dispatch_due_instances(
                        db,
                        limit=self._dispatch_limit,
                    )
                    logger.debug("[job_runtime] dispatch scan completed count=%s", count)
                    if count:
                        logger.info("[job_runtime] dispatched due instances count=%s", count)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("[job_runtime] due instance dispatch failed")
            await asyncio.sleep(self._dispatch_interval_seconds)


def _seconds_until_next_creation_tick(now: datetime, tick_minutes: int) -> float:
    if tick_minutes <= 0:
        raise ValueError("creation tick minutes must be greater than 0")
    if now.minute % tick_minutes == 0 and now.second == 0 and now.microsecond == 0:
        return 0.0
    minute = now.minute - (now.minute % tick_minutes) + tick_minutes
    next_tick = now.replace(second=0, microsecond=0)
    if minute >= 60:
        next_tick = next_tick.replace(minute=0) + timedelta(hours=1)
    else:
        next_tick = next_tick.replace(minute=minute)
    return max(0.0, (next_tick - now).total_seconds())
