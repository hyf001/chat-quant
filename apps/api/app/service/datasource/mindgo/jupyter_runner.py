from __future__ import annotations

import asyncio
import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.core.logging import get_logger

DEFAULT_MINDGO_NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"
DEFAULT_MINDGO_AUTH_SCHEME = "Bearer"
# The MindGo notebook server also returns transient HTTP 5xx and rejects stale
# kernel ids, so faults raised before a cell starts running are retried against
# a freshly resolved kernel. Faults that hit a running cell are not retried: see
# ``_kernel_lost_error``.
DEFAULT_MINDGO_TRANSPORT_ATTEMPTS = 3
DEFAULT_MINDGO_TRANSPORT_RETRY_DELAY_SECONDS = 2.0

logger = get_logger(__name__)


@dataclass(frozen=True)
class MindgoJupyterConfig:
    url: str
    token: str | None = None
    auth_scheme: str = "Bearer"
    notebook_path: str = DEFAULT_MINDGO_NOTEBOOK_PATH
    kernel_id: str | None = None
    timeout_seconds: float = 120.0


class MindgoRemoteExecutionError(RuntimeError):
    """Raised when remote MindGo execution fails or returns invalid output."""


class MindgoTransientError(MindgoRemoteExecutionError):
    """A transport or notebook-server fault that a fresh kernel can recover from."""


class MindgoJupyterRunner:
    def __init__(self, config: MindgoJupyterConfig) -> None:
        self._config = config
        self._kernel_id: str | None = config.kernel_id
        self._execution_lock = asyncio.Lock()

    async def run_json(
        self,
        code: str,
        *,
        marker_start: str,
        marker_end: str,
        timeout_seconds: float | None = None,
    ) -> dict[str, Any]:
        return await self._run_json_once(
            code,
            marker_start=marker_start,
            marker_end=marker_end,
            timeout_seconds=timeout_seconds,
        )

    async def _run_json_once(
        self,
        code: str,
        *,
        marker_start: str,
        marker_end: str,
        timeout_seconds: float | None = None,
    ) -> dict[str, Any]:
        _ensure_portable_mcp_importable()

        token = (self._config.token or "").strip()
        if not token:
            raise MindgoRemoteExecutionError("Jupyter token is not available")
        effective_timeout = timeout_seconds or self._config.timeout_seconds
        async with self._execution_lock:
            return await self._execute_with_reconnect(
                code,
                token=token,
                timeout=effective_timeout,
                marker_start=marker_start,
                marker_end=marker_end,
            )

    async def _execute_with_reconnect(
        self,
        code: str,
        *,
        token: str,
        timeout: float,
        marker_start: str,
        marker_end: str,
    ) -> dict[str, Any]:
        """Run one cell, retrying only faults that happen before it starts.

        Pre-flight faults (HTTP 5xx from the notebook server, a rejected stale
        kernel id, a refused connection) are retried against a freshly resolved
        kernel, because nothing was lost. A kernel that dies while the cell runs
        is not retried: it comes back without the MindGo API globals, so the run
        stops with instructions for the human who has to restart the notebook.
        """
        last_error: Exception | None = None
        for attempt in range(1, DEFAULT_MINDGO_TRANSPORT_ATTEMPTS + 1):
            try:
                execution = await self._execute(code, token=token, timeout=timeout)
                if execution.error:
                    raise _remote_execution_error(
                        execution.error,
                        timeout=timeout,
                        notebook_path=self._config.notebook_path,
                    )
                try:
                    return _extract_marked_json(
                        "".join(execution.stdout),
                        marker_start=marker_start,
                        marker_end=marker_end,
                        stderr="".join(execution.stderr),
                        result=execution.result,
                    )
                except MindgoRemoteExecutionError as exc:
                    # The cell reported that it finished, but its output never
                    # arrived: the notebook server drops IOPub messages that
                    # exceed iopub_data_rate_limit instead of erroring out.
                    raise _output_lost_error(exc) from exc
            except MindgoTransientError as exc:
                last_error = exc
                self._kernel_id = None
                await self._wait_before_retry(attempt, exc)
            except MindgoRemoteExecutionError:
                # The cell itself failed (bad parameters, missing symbols, the
                # kernel lost its MindGo setup): retrying would only burn
                # another window's worth of remote compute.
                raise
            except Exception as exc:  # noqa: BLE001 - transport faults vary by client version
                if _is_kernel_websocket_loss(exc):
                    # The cell was already running: the kernel behind it is gone
                    # and only a human can bring the MindGo API back.
                    self._kernel_id = None
                    raise _kernel_lost_error(exc, notebook_path=self._config.notebook_path) from exc
                last_error = exc
                self._kernel_id = None
                await self._wait_before_retry(attempt, exc)
        raise MindgoRemoteExecutionError(
            f"Remote MindGo execution failed on {DEFAULT_MINDGO_TRANSPORT_ATTEMPTS} attempts: "
            f"{last_error}. The notebook server kept rejecting the connection - check that "
            "the notebook is still open in the browser, then retry."
        ) from last_error

    async def _wait_before_retry(self, attempt: int, error: Exception) -> None:
        if attempt >= DEFAULT_MINDGO_TRANSPORT_ATTEMPTS:
            return
        delay = DEFAULT_MINDGO_TRANSPORT_RETRY_DELAY_SECONDS * attempt
        logger.warning(
            "MindGo kernel transport fault on attempt %s/%s (%s: %s); retrying in %.1fs "
            "with a freshly resolved kernel",
            attempt,
            DEFAULT_MINDGO_TRANSPORT_ATTEMPTS,
            type(error).__name__,
            error,
            delay,
        )
        await asyncio.sleep(delay)

    async def _execute(self, code: str, *, token: str, timeout: float) -> Any:
        from supermind_mcp.config import resolve_config
        from supermind_mcp.jupyter_api import JupyterAPI
        from supermind_mcp.jupyter_ws import execute_code_ws

        config = resolve_config(
            url=self._config.url,
            token=token,
            auth_scheme=self._config.auth_scheme,
        )
        async with JupyterAPI(config) as api:
            if self._kernel_id is None:
                self._kernel_id = await _find_or_create_kernel(
                    api,
                    _normalize_remote_path(self._config.notebook_path),
                )
            try:
                return await execute_code_ws(
                    self._kernel_id,
                    code,
                    url=self._config.url,
                    token=token,
                    auth_scheme=self._config.auth_scheme,
                    timeout=timeout,
                )
            except TimeoutError as exc:
                raise _kernel_timeout_error(
                    timeout,
                    notebook_path=self._config.notebook_path,
                ) from exc


def _is_kernel_timeout(error: Mapping[str, Any]) -> bool:
    return str(error.get("ename") or "") == "TimeoutError"


def _is_kernel_websocket_loss(exc: BaseException) -> bool:
    """True when the kernel websocket died mid-flight instead of closing cleanly.

    ``ConnectionClosedError("no close frame received or sent")`` means the
    notebook kernel (or the server hosting it) went away while our cell was
    running. The kernel comes back empty, so the MindGo API globals are gone and
    the run cannot continue without a human reopening the notebook.
    """
    try:
        from websockets.exceptions import ConnectionClosed
    except Exception:  # pragma: no cover - websockets always ships with supermind_mcp
        text = str(exc)
        return "no close frame" in text or "keepalive ping timeout" in text
    return isinstance(exc, ConnectionClosed)


def _kernel_lost_error(
    exc: BaseException,
    *,
    notebook_path: str,
) -> MindgoRemoteExecutionError:
    """Build the actionable failure for a kernel that died mid-execution."""
    return MindgoRemoteExecutionError(
        "The MindGo notebook kernel stopped while a cell was running: the kernel websocket "
        f"closed without a close handshake ({exc}). "
        "The restarted kernel no longer holds the MindGo API globals, so this needs a "
        f"manual restart: open {notebook_path}, run its setup cells, then run the sync "
        "again. Completed windows are already stored and are skipped on the next run."
    )


def _output_lost_error(exc: BaseException) -> MindgoRemoteExecutionError:
    """Build the actionable failure for a cell whose output never arrived."""
    return MindgoRemoteExecutionError(
        "The MindGo kernel finished the cell but its output was lost in transit, so the "
        f"window could not be read ({str(exc)[:300]}). The notebook server silently drops "
        "IOPub messages above iopub_data_rate_limit (1MB/s by default), which happens when "
        "one window returns too much data. Retry the sync, and lower the sync query window "
        "if the same window keeps failing. Completed windows are already stored and are "
        "skipped on the next run."
    )


def _kernel_timeout_error(timeout: float, *, notebook_path: str) -> MindgoRemoteExecutionError:
    """Build the actionable failure for a kernel that never answered."""
    return MindgoRemoteExecutionError(
        f"The MindGo kernel did not answer within {timeout:g}s, so the window was abandoned. "
        "The kernel is most likely hung or recycled; check "
        f"{notebook_path} in the browser, run its setup cells if it restarted, then run the "
        "sync again. Completed windows are already stored and are skipped on the next run."
    )


def _remote_execution_error(
    error: Mapping[str, Any],
    *,
    timeout: float,
    notebook_path: str,
) -> MindgoRemoteExecutionError:
    """Translate a remote cell failure into an actionable error."""
    if _is_kernel_timeout(error):
        # A kernel that stops answering mid-cell is usually a recycled or hung
        # kernel rather than a cell that is genuinely too slow.
        return _kernel_timeout_error(timeout, notebook_path=notebook_path)
    if _is_missing_get_price(error):
        return MindgoRemoteExecutionError(
            "The MindGo kernel does not define get_price: the notebook kernel was restarted "
            "without running its setup cells. Open the notebook, run the cells that import "
            "the MindGo API, then retry. Remote error: " + json.dumps(error, ensure_ascii=False)
        )
    return MindgoRemoteExecutionError(
        "Remote MindGo execution failed: " + json.dumps(error, ensure_ascii=False)
    )


def _is_missing_get_price(error: Mapping[str, Any]) -> bool:
    return str(error.get("ename") or "") == "NameError" and "get_price" in str(
        error.get("evalue") or ""
    )


async def _find_or_create_kernel(api: Any, notebook_path: str) -> str:
    sessions = await api.client.get("/api/sessions")
    _ensure_success(sessions.status_code, "listing Jupyter sessions")
    for session in sessions.json():
        if session.get("path") == notebook_path:
            kernel_id = (session.get("kernel") or {}).get("id")
            if kernel_id:
                return str(kernel_id)

    response = await api.client.post(
        "/api/sessions",
        json={
            "path": notebook_path,
            "type": "notebook",
            "name": notebook_path.rsplit("/", 1)[-1],
            "kernel": {"name": "python3"},
        },
    )
    _ensure_success(response.status_code, "creating Jupyter session")
    kernel_id = (response.json().get("kernel") or {}).get("id")
    if not kernel_id:
        raise MindgoRemoteExecutionError(
            f"Could not create kernel for notebook path: {notebook_path}"
        )
    return str(kernel_id)


def _ensure_success(status_code: int, action: str) -> None:
    message = f"Jupyter API returned HTTP {status_code} while {action}"
    if status_code >= 500:
        # The MindGo notebook server answers 503 while it restarts or culls
        # kernels; retrying with a fresh session recovers from that.
        raise MindgoTransientError(message)
    if status_code >= 400:
        raise MindgoRemoteExecutionError(
            f"{message} - check the MindGo notebook path and access token."
        )


def _normalize_remote_path(path: str) -> str:
    return path.strip().strip("/")


def _extract_marked_json(
    stdout: str,
    *,
    marker_start: str,
    marker_end: str,
    stderr: str = "",
    result: Any = None,
) -> dict[str, Any]:
    start = stdout.find(marker_start)
    end = stdout.find(marker_end, start + len(marker_start))
    if start < 0 or end < 0:
        preview = stdout[-2000:] if stdout else "<empty stdout>"
        detail = f"Could not find MindGo JSON markers in stdout: {preview}"
        if stderr:
            detail += f"; stderr: {stderr[-2000:]}"
        if result is not None:
            detail += f"; result: {str(result)[-2000:]}"
        raise MindgoRemoteExecutionError(detail)
    text = stdout[start + len(marker_start) : end].strip()
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise MindgoRemoteExecutionError("Remote MindGo output JSON must be an object")
    return payload


def _ensure_portable_mcp_importable() -> None:
    portable_mcp_root = _portable_mcp_root()
    if str(portable_mcp_root) not in sys.path:
        sys.path.insert(0, str(portable_mcp_root))


def _portable_mcp_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "docs" / "mindgo" / "mindgo-mcp-portable"
        if (candidate / "supermind_mcp" / "__init__.py").exists():
            return candidate
    raise MindgoRemoteExecutionError("Could not locate bundled supermind_mcp package")
