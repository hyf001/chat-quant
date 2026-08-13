from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MINDGO_NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"
DEFAULT_MINDGO_AUTH_SCHEME = "Bearer"


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


class MindgoJupyterRunner:
    def __init__(self, config: MindgoJupyterConfig) -> None:
        self._config = config

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

        from supermind_mcp.config import resolve_config
        from supermind_mcp.jupyter_api import JupyterAPI
        from supermind_mcp.jupyter_ws import execute_code_ws

        token = (self._config.token or "").strip()
        if not token:
            raise MindgoRemoteExecutionError("Jupyter token is not available")
        config = resolve_config(
            url=self._config.url,
            token=token,
            auth_scheme=self._config.auth_scheme,
        )
        async with JupyterAPI(config) as api:
            kernel_id = self._config.kernel_id or await _find_or_create_kernel(
                api,
                _normalize_remote_path(self._config.notebook_path),
            )
            execution = await execute_code_ws(
                kernel_id,
                code,
                url=self._config.url,
                token=token,
                auth_scheme=self._config.auth_scheme,
                timeout=timeout_seconds or self._config.timeout_seconds,
            )

        if execution.error:
            raise MindgoRemoteExecutionError(
                "Remote MindGo execution failed: " + json.dumps(execution.error, ensure_ascii=False)
            )

        stdout = "".join(execution.stdout)
        return _extract_marked_json(stdout, marker_start=marker_start, marker_end=marker_end)


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
    if status_code >= 400:
        raise MindgoRemoteExecutionError(f"Jupyter API returned HTTP {status_code} while {action}")


def _normalize_remote_path(path: str) -> str:
    return path.strip().strip("/")


def _extract_marked_json(
    stdout: str,
    *,
    marker_start: str,
    marker_end: str,
) -> dict[str, Any]:
    start = stdout.find(marker_start)
    end = stdout.find(marker_end, start + len(marker_start))
    if start < 0 or end < 0:
        preview = stdout[-2000:] if stdout else "<empty stdout>"
        raise MindgoRemoteExecutionError(f"Could not find MindGo JSON markers in stdout: {preview}")
    text = stdout[start + len(marker_start) : end].strip()
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise MindgoRemoteExecutionError("Remote MindGo output JSON must be an object")
    return payload


def _ensure_portable_mcp_importable() -> None:
    root = Path(__file__).resolve().parents[5]
    portable_mcp_root = root / "docs" / "mindgo" / "mindgo-mcp-portable"
    if str(portable_mcp_root) not in sys.path:
        sys.path.insert(0, str(portable_mcp_root))

