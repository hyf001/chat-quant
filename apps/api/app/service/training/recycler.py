"""后台回收：把已经自退的训练引擎句柄从注册表里摘掉。

引擎线程在收局（`finish` / 自动收局）或空闲超时后会自己退出，但
``TrainingEngineManager`` 里的条目只会在这个会话下次被访问时顺手清掉。这里按
固定间隔扫一遍，避免打过的每一局都把整局快照与成交留在进程内存里。收局那一
次已经由 ``TrainingService._build_report`` 立即摘掉，这里兜的是"空闲超时退出"
和"收局后再没人访问"的会话。
"""

from __future__ import annotations

import asyncio

from app.core.logging import get_logger
from app.service.training.engine_manager import training_engine_manager

logger = get_logger(__name__)

DEFAULT_RECYCLE_INTERVAL_SECONDS = 60.0


class TrainingEngineRecycler:
    """定时任务：周期调用 ``recycle()``，只回收线程已经退出的引擎。"""

    def __init__(self, *, interval_seconds: float = DEFAULT_RECYCLE_INTERVAL_SECONDS) -> None:
        self._interval_seconds = max(1.0, float(interval_seconds))
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._loop(), name="training-engine-recycler")

    async def stop(self) -> None:
        task, self._task = self._task, None
        if task is None:
            return
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    def recycle_once(self) -> list[str]:
        dead = training_engine_manager.recycle()
        if dead:
            logger.info("训练引擎线程已回收", extra={"session_ids": dead})
        return dead

    async def _loop(self) -> None:
        while True:
            await asyncio.sleep(self._interval_seconds)
            self.recycle_once()


training_engine_recycler = TrainingEngineRecycler()

__all__ = [
    "DEFAULT_RECYCLE_INTERVAL_SECONDS",
    "TrainingEngineRecycler",
    "training_engine_recycler",
]
