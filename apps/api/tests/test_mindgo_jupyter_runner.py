from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
import websockets.exceptions
from app.service.datasource.mindgo import jupyter_runner
from app.service.datasource.mindgo.jupyter_runner import (
    MindgoJupyterConfig,
    MindgoJupyterRunner,
    MindgoRemoteExecutionError,
)

MARKER_START = "MARK_START"
MARKER_END = "MARK_END"
NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"


@dataclass
class FakeExecution:
    stdout: list[str] = field(default_factory=list)
    stderr: list[str] = field(default_factory=list)
    result: Any = None
    error: dict[str, Any] | None = None


def ok_execution(payload: str = '{"rows":1}') -> FakeExecution:
    return FakeExecution(stdout=[f"{MARKER_START}\n{payload}\n{MARKER_END}\n"])


def make_runner() -> MindgoJupyterRunner:
    return MindgoJupyterRunner(
        MindgoJupyterConfig(
            url="https://example.invalid/notebook/user/1",
            token="token",
            notebook_path=NOTEBOOK_PATH,
            timeout_seconds=5.0,
        )
    )


@pytest.fixture(autouse=True)
def _no_retry_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(jupyter_runner, "DEFAULT_MINDGO_TRANSPORT_RETRY_DELAY_SECONDS", 0.0)


async def run(runner: MindgoJupyterRunner) -> dict[str, Any]:
    return await runner.run_json("print()", marker_start=MARKER_START, marker_end=MARKER_END)


async def test_run_json_returns_parsed_payload() -> None:
    runner = make_runner()
    calls: list[int] = []

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        calls.append(1)
        return ok_execution()

    runner._execute = fake_execute  # type: ignore[method-assign]

    assert await run(runner) == {"rows": 1}
    assert len(calls) == 1


async def test_preflight_faults_are_retried_with_a_fresh_kernel() -> None:
    runner = make_runner()
    seen_kernel_ids: list[str | None] = []

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        seen_kernel_ids.append(runner._kernel_id)
        runner._kernel_id = "kernel-1"
        if len(seen_kernel_ids) == 1:
            raise ConnectionRefusedError("connection refused")
        return ok_execution()

    runner._execute = fake_execute  # type: ignore[method-assign]

    assert await run(runner) == {"rows": 1}
    assert seen_kernel_ids == [None, None]


async def test_transient_kernel_listing_5xx_is_retried() -> None:
    runner = make_runner()

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        if not hasattr(fake_execute, "attempted"):
            fake_execute.attempted = True  # type: ignore[attr-defined]
            raise jupyter_runner.MindgoTransientError(
                "Jupyter API returned HTTP 503 while listing Jupyter sessions"
            )
        return ok_execution()

    runner._execute = fake_execute  # type: ignore[method-assign]

    assert await run(runner) == {"rows": 1}


async def test_kernel_websocket_loss_is_never_retried() -> None:
    runner = make_runner()
    attempts: list[int] = []
    runner._kernel_id = "kernel-1"

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        attempts.append(1)
        raise websockets.exceptions.ConnectionClosedError(None, None)

    runner._execute = fake_execute  # type: ignore[method-assign]

    with pytest.raises(MindgoRemoteExecutionError) as excinfo:
        await run(runner)

    assert len(attempts) == 1
    assert runner._kernel_id is None
    message = str(excinfo.value)
    assert "kernel stopped while a cell was running" in message
    assert "no close frame received or sent" in message
    assert NOTEBOOK_PATH in message
    assert "Completed windows are already stored" in message


async def test_dropped_output_points_at_the_iopub_rate_limit() -> None:
    runner = make_runner()
    attempts: list[int] = []

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        attempts.append(1)
        return FakeExecution(stdout=['{"rows":111220,"data_b64":"AAAA'])

    runner._execute = fake_execute  # type: ignore[method-assign]

    with pytest.raises(MindgoRemoteExecutionError) as excinfo:
        await run(runner)

    assert len(attempts) == 1
    message = str(excinfo.value)
    assert "output was lost in transit" in message
    assert "iopub_data_rate_limit" in message


async def test_remote_execution_error_is_not_retried() -> None:
    runner = make_runner()
    attempts: list[int] = []

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        attempts.append(1)
        return FakeExecution(
            error={
                "ename": "NameError",
                "evalue": "name 'get_price' is not defined",
                "traceback": [],
            }
        )

    runner._execute = fake_execute  # type: ignore[method-assign]

    with pytest.raises(MindgoRemoteExecutionError) as excinfo:
        await run(runner)

    assert len(attempts) == 1
    assert "does not define get_price" in str(excinfo.value)


async def test_kernel_timeout_is_not_retried() -> None:
    runner = make_runner()
    attempts: list[int] = []

    async def fake_execute(code: str, *, token: str, timeout: float) -> FakeExecution:
        attempts.append(1)
        return FakeExecution(
            error={"ename": "TimeoutError", "evalue": "Execution exceeded 300s", "traceback": []}
        )

    runner._execute = fake_execute  # type: ignore[method-assign]

    with pytest.raises(MindgoRemoteExecutionError) as excinfo:
        await run(runner)

    assert len(attempts) == 1
    assert "did not answer within 5s" in str(excinfo.value)
