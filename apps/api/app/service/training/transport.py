"""信号传输抽象 + 内存实现（本期桌面端零外部依赖）。

引擎线程与服务线程之间只有两件事：

* 服务 → 引擎：一次点击对应的一条 ``ChatQAction``（或一个停止信号）；
* 引擎 → 服务：每根结算点上的 broker 快照（现金 / 权益 / 持仓 / 本根成交），
  以及收局时的分析器结果。

引擎线程不产出 K 线、不落库、不认识 ``training_events``：这些都在 service。
"""

from __future__ import annotations

import queue
import threading
import time
from typing import Any, Protocol


class TrainingTransportStopped(Exception):
    """收到停止信号：收局 / 空闲回收，引擎线程应当退出。"""


class TrainingTransportTimeout(Exception):
    """等不到引擎的结算点（空闲超时或线程已退出）。"""


class TrainingTransportFailed(Exception):
    """引擎线程内部异常，原样透传。"""

    def __init__(self, message: str, *, detail: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or {}


class TrainingSignalTransport(Protocol):
    """引擎侧接口（由适配器调用）。"""

    def next_action(self, index: int) -> dict[str, Any] | None: ...

    def publish_bar(self, index: int, snapshot: dict[str, Any]) -> None: ...

    def publish_result(self, result: dict[str, Any]) -> None: ...


class InMemoryTrainingSignalTransport:
    """进程内实现：动作下发走队列，结算点回报走事件。"""

    def __init__(
        self,
        *,
        idle_ttl_seconds: float,
        poll_seconds: float = 1.0,
    ) -> None:
        self._idle_ttl_seconds = max(1.0, float(idle_ttl_seconds))
        self._poll_seconds = max(0.1, float(poll_seconds))
        self._actions: queue.Queue[Any] = queue.Queue()
        self._lock = threading.RLock()
        self._bar_events: dict[int, threading.Event] = {}
        self._snapshots: dict[int, dict[str, Any]] = {}
        self._fills: list[dict[str, Any]] = []
        self._result_event = threading.Event()
        self._result: dict[str, Any] | None = None
        self._failure: TrainingTransportFailed | None = None
        self._last_touch = time.monotonic()

    # -- 服务侧 -----------------------------------------------------------

    def touch(self) -> None:
        """每次 reveal / GET 刷新空闲计时（超时只回收引擎线程，会话保持 active）。"""
        with self._lock:
            self._last_touch = time.monotonic()

    def send_action(self, action: dict[str, Any] | None, *, touch: bool = True) -> None:
        if touch:
            self.touch()
        self._actions.put({"kind": "action", "action": action})

    def request_stop(self) -> None:
        self._actions.put({"kind": "stop"})

    def wait_bar(self, index: int, *, timeout: float) -> dict[str, Any]:
        event = self._bar_event(index)
        if not event.wait(timeout):
            self._raise_engine_failure()
            raise TrainingTransportTimeout(f"训练引擎未在 {timeout:.1f}s 内推进到第 {index} 根")
        self._raise_engine_failure()
        with self._lock:
            snapshot = self._snapshots.get(index)
        if snapshot is None:
            raise TrainingTransportTimeout(f"训练引擎没有第 {index} 根的结算快照")
        return dict(snapshot)

    def snapshot(self, index: int) -> dict[str, Any] | None:
        with self._lock:
            snapshot = self._snapshots.get(index)
        return None if snapshot is None else dict(snapshot)

    def latest_snapshot(self) -> dict[str, Any] | None:
        with self._lock:
            if not self._snapshots:
                return None
            return dict(self._snapshots[max(self._snapshots)])

    def fills(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._fills]

    def bar_indices(self) -> list[int]:
        with self._lock:
            return sorted(self._snapshots)

    def result(self) -> dict[str, Any] | None:
        with self._lock:
            return None if self._result is None else dict(self._result)

    def wait_result(self, *, timeout: float) -> dict[str, Any]:
        if not self._result_event.wait(timeout):
            self._raise_engine_failure()
            raise TrainingTransportTimeout(f"训练引擎未在 {timeout:.1f}s 内收局")
        self._raise_engine_failure()
        with self._lock:
            result = self._result
        if result is None:
            raise TrainingTransportTimeout("训练引擎没有产出收局结果")
        return dict(result)

    def has_result(self) -> bool:
        return self._result_event.is_set()

    # -- 引擎侧 -----------------------------------------------------------

    def next_action(self, index: int) -> dict[str, Any] | None:
        while True:
            remaining = self._remaining_idle_seconds()
            if remaining <= 0:
                raise TrainingTransportStopped("训练引擎空闲超时")
            try:
                item = self._actions.get(timeout=min(self._poll_seconds, remaining))
            except queue.Empty:
                continue
            self.touch()
            if item.get("kind") == "stop":
                raise TrainingTransportStopped("收到停止信号")
            return item.get("action")

    def publish_bar(self, index: int, snapshot: dict[str, Any]) -> None:
        payload = {**snapshot, "index": index}
        with self._lock:
            self._snapshots[index] = payload
            for fill in snapshot.get("fills", []):
                self._fills.append(dict(fill))
            self._last_touch = time.monotonic()
            event = self._bar_events.setdefault(index, threading.Event())
        event.set()

    def publish_result(self, result: dict[str, Any]) -> None:
        with self._lock:
            self._result = {**result, "fills": self.fills(), "bars": self.bar_indices()}
            self._last_touch = time.monotonic()
        self._result_event.set()

    def publish_failure(self, message: str, *, detail: dict[str, Any] | None = None) -> None:
        with self._lock:
            self._failure = TrainingTransportFailed(message, detail=detail)
        for index in self.bar_indices():
            self._bar_event(index).set()
        self._result_event.set()

    # -- 内部 -------------------------------------------------------------

    def _bar_event(self, index: int) -> threading.Event:
        with self._lock:
            return self._bar_events.setdefault(index, threading.Event())

    def _remaining_idle_seconds(self) -> float:
        with self._lock:
            return self._idle_ttl_seconds - (time.monotonic() - self._last_touch)

    def _raise_engine_failure(self) -> None:
        with self._lock:
            failure = self._failure
        if failure is not None:
            raise failure
