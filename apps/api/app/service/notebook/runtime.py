from __future__ import annotations

import asyncio
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.core.config import get_settings
from app.core.logging import get_logger
from app.schema.notebook import (
    NotebookServerResponse,
    NotebookServerStatusResponse,
    NotebookSessionResponse,
)

logger = get_logger(__name__)

NOTEBOOK_DIR_NAME = "notebook"
RUNTIME_DIR_NAME = "notebook-runtime"
REGISTRY_FILE_NAME = "notebook-runtimes.json"
MANAGED_ENV = "CHATQ_MANAGED_NOTEBOOK"
READY_TIMEOUT_SECONDS = 20.0


class NotebookRuntimeError(RuntimeError):
    pass


@dataclass(frozen=True)
class NotebookRuntimeRecord:
    runtime_id: str
    project_id: str
    project_path: str
    root_dir: str
    ipython_dir: str
    host: str
    port: int
    token: str
    pid: int
    process_group_id: int | None
    started_at: str
    updated_at: str
    status: str

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def url(self) -> str:
        return f"{self.base_url}/tree?token={self.token}"


class NotebookRuntimeManager:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._records: dict[str, NotebookRuntimeRecord] = {}
        self._processes: dict[str, subprocess.Popen[bytes]] = {}

    async def cleanup_stale_runtimes(self) -> None:
        async with self._lock:
            records = self._read_registry()
            if not records:
                return
            stale_count = 0
            for record in records:
                if _is_pid_running(record.pid) and _record_matches_process(record):
                    stale_count += 1
                    logger.info(
                        "stopping stale notebook runtime",
                        extra={
                            "project_id": record.project_id,
                            "runtime_id": record.runtime_id,
                            "pid": record.pid,
                        },
                    )
                    _terminate_record(record)
            self._write_registry([])
            if stale_count:
                logger.info("stale notebook runtime cleanup finished", extra={"count": stale_count})

    async def ensure_server(self, *, project_id: str, project_path: str) -> NotebookServerResponse:
        async with self._lock:
            current = self._records.get(project_id)
            if current is not None and _is_pid_running(current.pid):
                return _server_response(current, status="running")
            if current is not None:
                self._records.pop(project_id, None)
                self._processes.pop(project_id, None)
                self._persist_active_records()

            record, process = self._start_server(project_id=project_id, project_path=project_path)
            self._records[project_id] = record
            self._processes[project_id] = process
            self._persist_active_records()

        try:
            await asyncio.to_thread(_wait_until_ready, record)
        except NotebookRuntimeError:
            await self.stop_server(project_id=project_id)
            raise
        return _server_response(record, status="running")

    async def server_status(self, *, project_id: str) -> NotebookServerStatusResponse:
        async with self._lock:
            record = self._records.get(project_id)
            if record is None or not _is_pid_running(record.pid):
                return NotebookServerStatusResponse(project_id=project_id, status="stopped")
            return NotebookServerStatusResponse(
                project_id=project_id,
                status="running",
                url=record.url,
                base_url=record.base_url,
                root_dir=record.root_dir,
                pid=record.pid,
                runtime_id=record.runtime_id,
            )

    async def ensure_session(
        self,
        *,
        project_id: str,
        relative_path: str,
        name: str,
    ) -> NotebookSessionResponse:
        async with self._lock:
            record = self._records.get(project_id)
            if record is None or not _is_pid_running(record.pid):
                raise NotebookRuntimeError("Jupyter Notebook is not running")
        return await asyncio.to_thread(
            _ensure_jupyter_session,
            record,
            relative_path,
            name,
        )

    async def stop_server(self, *, project_id: str) -> None:
        async with self._lock:
            record = self._records.pop(project_id, None)
            process = self._processes.pop(project_id, None)
            if record is not None:
                _terminate_record(record, process=process)
            self._persist_active_records()

    async def stop_all(self) -> None:
        async with self._lock:
            for project_id, record in list(self._records.items()):
                _terminate_record(record, process=self._processes.get(project_id))
            self._records.clear()
            self._processes.clear()
            self._write_registry([])

    def _start_server(
        self,
        *,
        project_id: str,
        project_path: str,
    ) -> tuple[NotebookRuntimeRecord, subprocess.Popen[bytes]]:
        project_dir = Path(project_path).expanduser().resolve(strict=True)
        root_dir = project_dir / NOTEBOOK_DIR_NAME
        root_dir.mkdir(parents=True, exist_ok=True)
        runtime_id = f"nb_{uuid4().hex[:16]}"
        ipython_dir = _prepare_ipython_startup(runtime_id)
        host = "127.0.0.1"
        port = _reserve_port(host)
        token = uuid4().hex
        runtime_dir = _runtime_dir()
        runtime_dir.mkdir(parents=True, exist_ok=True)
        log_file = runtime_dir / f"{runtime_id}.log"

        env = os.environ.copy()
        env.update(
            {
                MANAGED_ENV: "1",
                "CHATQ_PROJECT_ID": project_id,
                "CHATQ_NOTEBOOK_RUNTIME_ID": runtime_id,
                "CHATQ_NOTEBOOK_ROOT": str(root_dir),
                "IPYTHONDIR": str(ipython_dir),
                "MPLCONFIGDIR": str(ipython_dir / "matplotlib"),
            }
        )
        command = [
            sys.executable,
            "-m",
            "notebook",
            "--no-browser",
            f"--ServerApp.ip={host}",
            f"--ServerApp.port={port}",
            f"--ServerApp.token={token}",
            "--ServerApp.password=",
            f"--ServerApp.root_dir={root_dir}",
            "--ServerApp.open_browser=False",
            "--ServerApp.allow_origin=*",
            "--ServerApp.disable_check_xsrf=True",
            "--ServerApp.tornado_settings="
            '{"headers":{"Content-Security-Policy":"frame-ancestors *"}}',
        ]
        start_kwargs: dict[str, Any] = {}
        if os.name == "posix":
            start_kwargs["preexec_fn"] = os.setsid
        elif os.name == "nt":
            start_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        handle = None
        try:
            handle = log_file.open("ab")
            process = subprocess.Popen(
                command,
                cwd=str(root_dir),
                env=env,
                stdout=handle,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                close_fds=os.name == "posix",
                **start_kwargs,
            )
        except OSError as exc:
            raise NotebookRuntimeError(f"failed to start Jupyter Notebook: {exc}") from exc
        finally:
            if handle is not None:
                handle.close()

        process_group_id = _process_group_id(process.pid)
        now = _now_iso()
        return (
            NotebookRuntimeRecord(
                runtime_id=runtime_id,
                project_id=project_id,
                project_path=str(project_dir),
                root_dir=str(root_dir),
                ipython_dir=str(ipython_dir),
                host=host,
                port=port,
                token=token,
                pid=process.pid,
                process_group_id=process_group_id,
                started_at=now,
                updated_at=now,
                status="running",
            ),
            process,
        )

    def _persist_active_records(self) -> None:
        self._write_registry(list(self._records.values()))

    def _read_registry(self) -> list[NotebookRuntimeRecord]:
        path = _registry_path()
        if not path.exists():
            return []
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        records = payload.get("runtimes") if isinstance(payload, dict) else None
        if not isinstance(records, list):
            return []
        parsed: list[NotebookRuntimeRecord] = []
        for item in records:
            if not isinstance(item, dict):
                continue
            try:
                parsed.append(NotebookRuntimeRecord(**item))
            except TypeError:
                continue
        return parsed

    def _write_registry(self, records: list[NotebookRuntimeRecord]) -> None:
        path = _registry_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"runtimes": [asdict(record) for record in records]}
        tmp_path = path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(path)


def _server_response(
    record: NotebookRuntimeRecord,
    *,
    status: str,
) -> NotebookServerResponse:
    return NotebookServerResponse(
        project_id=record.project_id,
        status=status,  # type: ignore[arg-type]
        url=record.url,
        base_url=record.base_url,
        token=record.token,
        root_dir=record.root_dir,
        pid=record.pid,
        runtime_id=record.runtime_id,
    )


def _runtime_dir() -> Path:
    return get_settings().database_path.expanduser().resolve(strict=False).parent / RUNTIME_DIR_NAME


def _registry_path() -> Path:
    return _runtime_dir() / REGISTRY_FILE_NAME


def _reserve_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def _prepare_ipython_startup(runtime_id: str) -> Path:
    ipython_dir = _runtime_dir() / f"ipython-{runtime_id}"
    startup_dir = ipython_dir / "profile_default" / "startup"
    startup_dir.mkdir(parents=True, exist_ok=True)
    startup_file = startup_dir / "00-chatq-python-api.py"
    startup_file.write_text(
        "\n".join(
            [
                "from types import SimpleNamespace",
                "from app.service.dataset.python_api import (",
                "    describe_dataset,",
                "    list_datasets,",
                "    preview_dataset,",
                "    query_dataset,",
                ")",
                "from app.service.stock_pool.python_api import (",
                "    add_pool_stocks,",
                "    get_stock_pool,",
                "    list_pool_stocks,",
                "    list_stock_pools,",
                "    stock_pool_symbols,",
                "    stock_pool_symbols_by_tag,",
                "    stock_pool_tags,",
                ")",
                "chatq = SimpleNamespace(",
                "    list_datasets=list_datasets,",
                "    describe_dataset=describe_dataset,",
                "    preview_dataset=preview_dataset,",
                "    query_dataset=query_dataset,",
                "    add_pool_stocks=add_pool_stocks,",
                "    list_stock_pools=list_stock_pools,",
                "    get_stock_pool=get_stock_pool,",
                "    list_pool_stocks=list_pool_stocks,",
                "    stock_pool_symbols=stock_pool_symbols,",
                "    stock_pool_tags=stock_pool_tags,",
                "    stock_pool_symbols_by_tag=stock_pool_symbols_by_tag,",
                ")",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return ipython_dir


def _wait_until_ready(record: NotebookRuntimeRecord) -> None:
    deadline = time.monotonic() + READY_TIMEOUT_SECONDS
    url = f"{record.base_url}/api?token={record.token}"
    while time.monotonic() < deadline:
        if not _is_pid_running(record.pid):
            raise NotebookRuntimeError("Jupyter Notebook exited before it became ready")
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status < 500:
                    return
        except (OSError, urllib.error.URLError):
            time.sleep(0.25)
    raise NotebookRuntimeError("Jupyter Notebook did not become ready in time")


def _ensure_jupyter_session(
    record: NotebookRuntimeRecord,
    relative_path: str,
    name: str,
) -> NotebookSessionResponse:
    sessions = _request_jupyter_json(record, "/api/sessions")
    if isinstance(sessions, list):
        for session in sessions:
            if not isinstance(session, dict) or session.get("path") != relative_path:
                continue
            kernel = session.get("kernel") if isinstance(session.get("kernel"), dict) else {}
            return NotebookSessionResponse(
                path=relative_path,
                session_id=_string_or_none(session.get("id")),
                kernel_id=_string_or_none(kernel.get("id")),
                kernel_name=_string_or_none(kernel.get("name")),
            )

    payload = {
        "path": relative_path,
        "type": "notebook",
        "name": name,
        "kernel": {"name": "python3"},
    }
    try:
        session = _request_jupyter_json(record, "/api/sessions", method="POST", body=payload)
    except NotebookRuntimeError:
        sessions = _request_jupyter_json(record, "/api/sessions")
        if not isinstance(sessions, list):
            raise
        for session in sessions:
            if isinstance(session, dict) and session.get("path") == relative_path:
                break
        else:
            raise
    if not isinstance(session, dict):
        raise NotebookRuntimeError("Jupyter Notebook returned an invalid session response")

    kernel = session.get("kernel") if isinstance(session.get("kernel"), dict) else {}
    return NotebookSessionResponse(
        path=relative_path,
        session_id=_string_or_none(session.get("id")),
        kernel_id=_string_or_none(kernel.get("id")),
        kernel_name=_string_or_none(kernel.get("name")),
    )


def _request_jupyter_json(
    record: NotebookRuntimeRecord,
    path: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> Any:
    query = urllib.parse.urlencode({"token": record.token})
    url = f"{record.base_url}{path}?{query}"
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise NotebookRuntimeError(f"Jupyter Notebook request failed: {exc.code} {detail}") from exc
    except OSError as exc:
        raise NotebookRuntimeError(f"Jupyter Notebook request failed: {exc}") from exc
    if not payload:
        return None
    try:
        return json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise NotebookRuntimeError("Jupyter Notebook returned invalid JSON") from exc


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _terminate_record(
    record: NotebookRuntimeRecord,
    *,
    process: subprocess.Popen[bytes] | None = None,
) -> None:
    if not _is_pid_running(record.pid):
        _cleanup_runtime_files(record)
        return
    if os.name == "posix":
        target = record.process_group_id or record.pid
        with _suppress_process_errors():
            os.killpg(target, signal.SIGTERM)
        if not _wait_for_exit(record.pid, timeout_seconds=5):
            with _suppress_process_errors():
                os.killpg(target, signal.SIGKILL)
        _cleanup_runtime_files(record)
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(record.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        _cleanup_runtime_files(record)
        return
    if process is not None:
        process.terminate()
    else:
        with _suppress_process_errors():
            os.kill(record.pid, signal.SIGTERM)
    _cleanup_runtime_files(record)


def _wait_for_exit(pid: int, *, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if not _is_pid_running(pid):
            return True
        time.sleep(0.1)
    return not _is_pid_running(pid)


def _is_pid_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _record_matches_process(record: NotebookRuntimeRecord) -> bool:
    command = _process_command(record.pid)
    if not command:
        return False
    return (
        record.root_dir in command
        and str(record.port) in command
        and ("notebook" in command or "jupyter" in command)
    )


def _process_command(pid: int) -> str:
    if os.name == "posix":
        completed = subprocess.run(
            ["ps", "-p", str(pid), "-o", "command="],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        return completed.stdout.strip()
    return ""


def _cleanup_runtime_files(record: NotebookRuntimeRecord) -> None:
    with _suppress_process_errors():
        shutil.rmtree(record.ipython_dir, ignore_errors=True)


def _process_group_id(pid: int) -> int | None:
    if os.name != "posix":
        return None
    try:
        return os.getpgid(pid)
    except OSError:
        return None


class _suppress_process_errors:
    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> bool:
        return exc_type in {ProcessLookupError, PermissionError, OSError}


def _now_iso() -> str:
    return datetime.now().isoformat()


notebook_runtime_manager = NotebookRuntimeManager()
