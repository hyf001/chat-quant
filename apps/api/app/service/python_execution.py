from __future__ import annotations

import asyncio
import contextlib
import io
import os
import runpy
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from types import FrameType
from uuid import uuid4

MAX_OUTPUT_CHARS = 65536
_PYTHON_EXECUTOR = ThreadPoolExecutor(max_workers=4, thread_name_prefix="chatq-python")
_PYTHON_EXECUTION_LOCK = threading.Lock()
_STDIO_LOCAL = threading.local()
_STDIO_PROXY_LOCK = threading.Lock()


@dataclass(frozen=True)
class PythonExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: int
    timed_out: bool
    code_file: str
    output_truncated: bool = False


class PythonExecutionError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


async def execute_python_code(
    *,
    project_dir: Path,
    code: str | None,
    code_file: Path | None,
    stdin: str | None = None,
    timeout_seconds: int = 10,
) -> PythonExecutionResult:
    resolved_project_dir = project_dir.expanduser().resolve(strict=True)
    if code is None and code_file is None:
        raise PythonExecutionError(
            "CHATQ_PYTHON_SOURCE_REQUIRED",
            "Either code or code_file is required",
        )
    if code is not None and code_file is not None:
        raise PythonExecutionError(
            "CHATQ_PYTHON_SOURCE_CONFLICT",
            "Pass code or code_file, not both",
        )

    execution_file = (
        _write_inline_code(resolved_project_dir, code)
        if code is not None
        else _resolve_project_code_file(resolved_project_dir, code_file)
    )
    return await _run_python_file(
        resolved_project_dir,
        execution_file,
        stdin=stdin,
        timeout_seconds=timeout_seconds,
    )


def _write_inline_code(project_dir: Path, code: str | None) -> Path:
    if code is None or not code.strip():
        raise PythonExecutionError("CHATQ_PYTHON_CODE_EMPTY", "Python code is empty")
    run_dir = project_dir / ".chatq" / "python-runs" / uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=False)
    code_file = run_dir / "main.py"
    code_file.write_text(code, encoding="utf-8")
    return code_file


def _resolve_project_code_file(project_dir: Path, code_file: Path | None) -> Path:
    if code_file is None:
        raise PythonExecutionError(
            "CHATQ_PYTHON_CODE_FILE_REQUIRED",
            "Python code file is required",
        )
    if not code_file.is_absolute():
        raise PythonExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_ABSOLUTE",
            "Python code file must be an absolute path",
            detail={"code_file": str(code_file)},
        )
    try:
        resolved_code_file = code_file.expanduser().resolve(strict=True)
    except FileNotFoundError as exc:
        raise PythonExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_FOUND",
            "Python code file was not found",
            detail={"code_file": str(code_file)},
        ) from exc
    if not resolved_code_file.is_file():
        raise PythonExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_FOUND",
            "Python code file is not a regular file",
            detail={"code_file": str(code_file)},
        )
    if not resolved_code_file.is_relative_to(project_dir):
        raise PythonExecutionError(
            "CHATQ_PYTHON_CODE_FILE_OUTSIDE_PROJECT",
            "Python code file must be under the current agent project directory",
            detail={
                "code_file": str(resolved_code_file),
                "project_dir": str(project_dir),
            },
        )
    return resolved_code_file


async def _run_python_file(
    project_dir: Path,
    code_file: Path,
    *,
    stdin: str | None,
    timeout_seconds: int,
) -> PythonExecutionResult:
    started_at = time.monotonic()
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(
        _PYTHON_EXECUTOR,
        _run_python_file_in_process,
        project_dir,
        code_file,
        stdin,
        timeout_seconds,
    )
    try:
        execution = await asyncio.wait_for(future, timeout=timeout_seconds + 1)
    except TimeoutError:
        execution = _InProcessExecution(
            stdout="",
            stderr="Python execution timed out while running inside the Chat-Quant service.\n",
            exit_code=-1,
            timed_out=True,
        )

    duration_ms = round((time.monotonic() - started_at) * 1000)
    stdout, stdout_truncated = _truncate_output(execution.stdout)
    stderr, stderr_truncated = _truncate_output(execution.stderr)
    return PythonExecutionResult(
        stdout=stdout,
        stderr=stderr,
        exit_code=execution.exit_code,
        duration_ms=duration_ms,
        timed_out=execution.timed_out,
        code_file=str(code_file),
        output_truncated=stdout_truncated or stderr_truncated,
    )


@dataclass(frozen=True)
class _InProcessExecution:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


def _run_python_file_in_process(
    project_dir: Path,
    code_file: Path,
    stdin: str | None,
    timeout_seconds: int,
) -> _InProcessExecution:
    stdout = io.StringIO()
    stderr = io.StringIO()
    started_at = time.monotonic()

    _ensure_stdio_proxies()
    with _PYTHON_EXECUTION_LOCK:
        old_cwd = Path.cwd()
        old_sys_path = list(sys.path)
        old_argv = sys.argv[:]
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_trace = sys.gettrace()
        try:
            os.chdir(project_dir)
            sys.path.insert(0, str(project_dir))
            sys.argv = [str(code_file)]
            _STDIO_LOCAL.stdin = io.StringIO(stdin or "")
            _STDIO_LOCAL.stdout = stdout
            _STDIO_LOCAL.stderr = stderr
            sys.settrace(_build_timeout_trace(started_at, timeout_seconds))
            try:
                runpy.run_path(str(code_file), run_name="__main__")
                return _InProcessExecution(
                    stdout=stdout.getvalue(),
                    stderr=stderr.getvalue(),
                    exit_code=0,
                    timed_out=False,
                )
            except _PythonExecutionTimeout:
                return _InProcessExecution(
                    stdout=stdout.getvalue(),
                    stderr=stderr.getvalue(),
                    exit_code=-1,
                    timed_out=True,
                )
            except SystemExit as exc:
                return _InProcessExecution(
                    stdout=stdout.getvalue(),
                    stderr=stderr.getvalue(),
                    exit_code=_system_exit_code(exc),
                    timed_out=False,
                )
            except BaseException:
                traceback.print_exc()
                return _InProcessExecution(
                    stdout=stdout.getvalue(),
                    stderr=stderr.getvalue(),
                    exit_code=1,
                    timed_out=False,
                )
        finally:
            sys.settrace(old_trace)
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.argv = old_argv
            sys.path[:] = old_sys_path
            _clear_thread_stdio()
            with contextlib.suppress(FileNotFoundError):
                os.chdir(old_cwd)


class _ThreadLocalTextIO:
    def __init__(self, name: str, fallback: object) -> None:
        self._name = name
        self._fallback = fallback

    @property
    def encoding(self) -> str | None:
        return getattr(self._target, "encoding", None)

    @property
    def errors(self) -> str | None:
        return getattr(self._target, "errors", None)

    @property
    def _target(self) -> object:
        return getattr(_STDIO_LOCAL, self._name, self._fallback)

    def write(self, value: str) -> int:
        return self._target.write(value)

    def flush(self) -> None:
        self._target.flush()

    def read(self, *args: object, **kwargs: object) -> str:
        return self._target.read(*args, **kwargs)

    def readline(self, *args: object, **kwargs: object) -> str:
        return self._target.readline(*args, **kwargs)

    def isatty(self) -> bool:
        return self._target.isatty()

    def writable(self) -> bool:
        return self._target.writable()

    def readable(self) -> bool:
        return self._target.readable()

    def __getattr__(self, name: str) -> object:
        return getattr(self._target, name)


def _ensure_stdio_proxies() -> None:
    with _STDIO_PROXY_LOCK:
        if not isinstance(sys.stdin, _ThreadLocalTextIO):
            sys.stdin = _ThreadLocalTextIO("stdin", sys.stdin)
        if not isinstance(sys.stdout, _ThreadLocalTextIO):
            sys.stdout = _ThreadLocalTextIO("stdout", sys.stdout)
        if not isinstance(sys.stderr, _ThreadLocalTextIO):
            sys.stderr = _ThreadLocalTextIO("stderr", sys.stderr)


def _clear_thread_stdio() -> None:
    for name in ("stdin", "stdout", "stderr"):
        with contextlib.suppress(AttributeError):
            delattr(_STDIO_LOCAL, name)


class _PythonExecutionTimeout(Exception):
    pass


def _build_timeout_trace(started_at: float, timeout_seconds: int):
    def trace(frame: FrameType, event: str, arg: object):
        del frame, event, arg
        if time.monotonic() - started_at > timeout_seconds:
            raise _PythonExecutionTimeout()
        return trace

    return trace


def _system_exit_code(exc: SystemExit) -> int:
    if exc.code is None:
        return 0
    if isinstance(exc.code, int):
        return exc.code
    print(exc.code, file=sys.stderr)
    return 1


def _truncate_output(text: str) -> tuple[str, bool]:
    if len(text) <= MAX_OUTPUT_CHARS:
        return text, False
    return text[:MAX_OUTPUT_CHARS], True
