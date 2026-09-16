"""进程内会话注册表 + 空闲回收 + replay 重建。

内存中的训练引擎只属于启动它的进程（部署侧固定 ``--workers 1``）。引擎线程
空闲 30 分钟（可配）自退，会话仍旧保持 ``active``：下次请求按 ``training_events``
的信号历史 replay 重建，事件是唯一真相。
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from app.service.training.slice_loader import TrainingSlice
from app.service.training.train_adapter import run_backtrader_training
from app.service.training.transport import InMemoryTrainingSignalTransport

DEFAULT_WAIT_SECONDS = 60.0
DEFAULT_START_SECONDS = 30.0


@dataclass
class TrainingEngineHandle:
    session_id: str
    training_slice: TrainingSlice
    transport: InMemoryTrainingSignalTransport
    thread: threading.Thread
    lock: threading.RLock = field(default_factory=threading.RLock)

    def is_alive(self) -> bool:
        return self.thread.is_alive()

    def join(self, timeout: float = 5.0) -> None:
        self.thread.join(timeout)

    def send_and_wait(
        self,
        index: int,
        action: dict[str, Any] | None,
        *,
        timeout: float = DEFAULT_WAIT_SECONDS,
    ) -> dict[str, Any]:
        self.transport.send_action(action)
        return self.transport.wait_bar(index, timeout=timeout)

    def stop_and_collect(self, *, timeout: float = DEFAULT_WAIT_SECONDS) -> dict[str, Any]:
        if not self.transport.has_result():
            self.transport.request_stop()
        result = self.transport.wait_result(timeout=timeout)
        self.join(timeout=1.0)
        return result

    def latest_snapshot(self) -> dict[str, Any] | None:
        return self.transport.latest_snapshot()

    def snapshots(self) -> list[dict[str, Any]]:
        return [self.transport.snapshot(index) or {} for index in self.transport.bar_indices()]


class TrainingEngineManager:
    """单进程注册表；钥匙是 ``session_id``，值是正在跑的引擎线程。"""

    def __init__(self, *, wait_seconds: float = DEFAULT_WAIT_SECONDS) -> None:
        self._handles: dict[str, TrainingEngineHandle] = {}
        self._lock = threading.RLock()
        self._wait_seconds = wait_seconds

    def acquire(
        self,
        *,
        session_id: str,
        slice_factory: Callable[[], TrainingSlice],
        initial_cash: float,
        commission: float,
        slippage: float = 0.0,
        idle_ttl_seconds: float,
        actions: list[dict[str, Any] | None],
    ) -> TrainingEngineHandle:
        """拿到引擎（必要时新建 + replay 到当前游标）。"""
        with self._lock:
            handle = self._handles.get(session_id)
            if handle is not None and not handle.is_alive():
                self._handles.pop(session_id, None)
                handle = None
            if handle is None:
                handle = self._start(
                    session_id=session_id,
                    slice_factory=slice_factory,
                    initial_cash=initial_cash,
                    commission=commission,
                    slippage=slippage,
                    idle_ttl_seconds=idle_ttl_seconds,
                )
                self._handles[session_id] = handle
                self._replay(handle, actions)
            return handle

    def get(self, session_id: str) -> TrainingEngineHandle | None:
        with self._lock:
            return self._handles.get(session_id)

    def discard(self, session_id: str) -> None:
        with self._lock:
            handle = self._handles.pop(session_id, None)
        if handle is not None and handle.is_alive():
            handle.transport.request_stop()

    def recycle(self) -> list[str]:
        """回收已经自退的引擎线程（空闲超时 / 收局），会话状态不动。"""
        with self._lock:
            dead = [key for key, handle in self._handles.items() if not handle.is_alive()]
            for key in dead:
                self._handles.pop(key, None)
        return dead

    def active_sessions(self) -> list[str]:
        with self._lock:
            return list(self._handles)

    def _start(
        self,
        *,
        session_id: str,
        slice_factory: Callable[[], TrainingSlice],
        initial_cash: float,
        commission: float,
        slippage: float,
        idle_ttl_seconds: float,
    ) -> TrainingEngineHandle:
        training_slice = slice_factory()
        transport = InMemoryTrainingSignalTransport(idle_ttl_seconds=idle_ttl_seconds)
        frame = training_slice.training_frame()
        thread = threading.Thread(
            target=_run_engine,
            name=f"training-engine-{session_id}",
            daemon=True,
            kwargs={
                "frame": frame,
                "symbol": training_slice.symbol,
                "initial_cash": float(initial_cash),
                "commission": float(commission),
                "slippage": float(slippage),
                "transport": transport,
                "bar_offset": training_slice.warmup_bars,
            },
        )
        thread.start()
        return TrainingEngineHandle(
            session_id=session_id,
            training_slice=training_slice,
            transport=transport,
            thread=thread,
        )

    def _replay(
        self,
        handle: TrainingEngineHandle,
        actions: list[dict[str, Any] | None],
    ) -> None:
        with handle.lock:
            for action in actions:
                handle.transport.send_action(action)
            if actions:
                handle.transport.wait_bar(len(actions) - 1, timeout=self._wait_seconds)


def _run_engine(
    *,
    frame: Any,
    symbol: str,
    initial_cash: float,
    commission: float,
    slippage: float,
    transport: InMemoryTrainingSignalTransport,
    bar_offset: int,
) -> None:
    try:
        result = run_backtrader_training(
            frame=frame,
            symbol=symbol,
            initial_cash=initial_cash,
            commission=commission,
            slippage=slippage,
            transport=transport,
            bar_offset=bar_offset,
        )
    except BaseException as exc:  # noqa: BLE001 - 引擎线程必须把失败交给服务线程
        transport.publish_failure(
            str(exc) or type(exc).__name__,
            detail={"exception_type": type(exc).__name__},
        )
        return
    transport.publish_result(result)


training_engine_manager = TrainingEngineManager()
