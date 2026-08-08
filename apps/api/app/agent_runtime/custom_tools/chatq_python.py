from __future__ import annotations

import argparse
import io
import json
import shlex
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.schema.agent_runtime import AgentExecutionCommand
from app.service.python_execution import (
    PythonExecutionError,
    PythonExecutionResult,
    execute_python_code,
)

CHATQ_PYTHON_SERVER_NAME = "chatq"
CHATQ_PYTHON_MCP_TOOL_NAME = "python"
CHATQ_PYTHON_TOOL_NAME = f"mcp__{CHATQ_PYTHON_SERVER_NAME}__{CHATQ_PYTHON_MCP_TOOL_NAME}"
CHATQ_PYTHON_TIMEOUT_SECONDS = 10
CHATQ_PYTHON_MAX_TIMEOUT_SECONDS = 60


class ChatqPythonCommandRequest(BaseModel):
    command: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class ToolExecutionError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


@dataclass(frozen=True)
class ToolTextResult:
    text: str
    is_error: bool = False


def build_chatq_python_tool_schema() -> dict[str, object]:
    return {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": (
                    "chatq-python style command line. For example: "
                    "run --code 'print(1 + 1)' or "
                    "run --code-file /absolute/path/inside/current/project/script.py"
                ),
            },
        },
        "required": ["command"],
        "additionalProperties": False,
    }


async def handle_chatq_python_tool(
    command: AgentExecutionCommand,
    args: dict[str, Any],
) -> ToolTextResult:
    try:
        request = ChatqPythonCommandRequest.model_validate(args)
        return await execute_chatq_python_command(command, request.command)
    except ValidationError as exc:
        return ToolTextResult(
            _format_cli_error(
                "chatq_python input is invalid",
                detail=_jsonable(exc.errors()),
            ),
            is_error=True,
        )
    except PythonExecutionError as exc:
        return ToolTextResult(_format_cli_error(exc.message, _error_detail(exc)), True)
    except ToolExecutionError as exc:
        return ToolTextResult(_format_cli_error(exc.message, _error_detail(exc)), True)


async def execute_chatq_python_command(
    command: AgentExecutionCommand,
    command_line: str,
) -> ToolTextResult:
    try:
        argv = shlex.split(command_line)
    except ValueError as exc:
        return ToolTextResult(_format_cli_error(f"Failed to parse command: {exc}"), True)
    return await execute_chatq_python_argv(command, argv)


async def execute_chatq_python_argv(
    command: AgentExecutionCommand,
    argv: list[str],
) -> ToolTextResult:
    parser = build_command_parser()
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            args = parser.parse_args(argv)
    except SystemExit as exc:
        output = stdout.getvalue() or stderr.getvalue()
        code = exc.code if isinstance(exc.code, int) else 1
        return ToolTextResult(output.rstrip(), code != 0)

    result = await run_cli_command(command, args)
    is_error = result.timed_out or result.exit_code != 0
    return ToolTextResult(format_cli_result(args, result), is_error)


def build_command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chatq-python",
        description="Run Python code through the Chat-Quant Python execution service.",
    )
    subparsers = parser.add_subparsers(dest="command_group", required=True)
    run = subparsers.add_parser("run", help="Run Python code in the current agent project.")
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--code", help="Python source code to execute.")
    source.add_argument(
        "--code-file",
        help="Absolute path to a Python file under the current agent project directory.",
    )
    run.add_argument("--stdin", default=None, help="Optional stdin text passed to the program.")
    run.add_argument(
        "--timeout",
        type=int,
        default=CHATQ_PYTHON_TIMEOUT_SECONDS,
        help=f"Execution timeout in seconds, max {CHATQ_PYTHON_MAX_TIMEOUT_SECONDS}.",
    )
    run.add_argument("--json", action="store_true", help="Return a JSON result.")
    return parser


async def run_cli_command(
    command: AgentExecutionCommand,
    args: argparse.Namespace,
) -> PythonExecutionResult:
    if args.command_group != "run":
        raise ToolExecutionError(
            "CHATQ_PYTHON_COMMAND_UNSUPPORTED",
            f"Unsupported command: {args.command_group}",
        )
    timeout_seconds = _validate_timeout(args.timeout)
    project_dir = _resolve_project_dir(command.project_dir)
    code_file = _resolve_code_file_before_service(project_dir, args.code_file)
    return await execute_python_code(
        project_dir=project_dir,
        code=args.code,
        code_file=code_file,
        stdin=args.stdin,
        timeout_seconds=timeout_seconds,
    )


def _validate_timeout(timeout_seconds: int) -> int:
    if timeout_seconds < 1 or timeout_seconds > CHATQ_PYTHON_MAX_TIMEOUT_SECONDS:
        raise ToolExecutionError(
            "CHATQ_PYTHON_TIMEOUT_INVALID",
            f"timeout must be between 1 and {CHATQ_PYTHON_MAX_TIMEOUT_SECONDS} seconds",
            detail={"timeout": timeout_seconds},
        )
    return timeout_seconds


def _resolve_project_dir(project_dir: str) -> Path:
    try:
        return Path(project_dir).expanduser().resolve(strict=True)
    except FileNotFoundError as exc:
        raise ToolExecutionError(
            "CHATQ_PYTHON_PROJECT_DIR_NOT_FOUND",
            "Current agent project directory was not found",
            detail={"project_dir": project_dir},
        ) from exc


def _resolve_code_file_before_service(project_dir: Path, code_file: str | None) -> Path | None:
    if code_file is None:
        return None
    candidate = Path(code_file).expanduser()
    if not candidate.is_absolute():
        raise ToolExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_ABSOLUTE",
            "Python code file must be an absolute path",
            detail={"code_file": code_file},
        )
    try:
        resolved_code_file = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ToolExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_FOUND",
            "Python code file was not found",
            detail={"code_file": code_file},
        ) from exc
    if not resolved_code_file.is_file():
        raise ToolExecutionError(
            "CHATQ_PYTHON_CODE_FILE_NOT_FOUND",
            "Python code file is not a regular file",
            detail={"code_file": code_file},
        )
    if not resolved_code_file.is_relative_to(project_dir):
        raise ToolExecutionError(
            "CHATQ_PYTHON_CODE_FILE_OUTSIDE_PROJECT",
            "Python code file must be under the current agent project directory",
            detail={
                "code_file": str(resolved_code_file),
                "project_dir": str(project_dir),
            },
        )
    return resolved_code_file


def format_cli_result(args: argparse.Namespace, result: PythonExecutionResult) -> str:
    payload = {
        "ok": not result.timed_out and result.exit_code == 0,
        "operator": "python run",
        "data": {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exit_code,
            "duration_ms": result.duration_ms,
            "timed_out": result.timed_out,
            "code_file": result.code_file,
            "output_truncated": result.output_truncated,
        },
    }
    if getattr(args, "json", False):
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if result.timed_out:
        header = "Python execution timed out."
    elif result.exit_code == 0:
        header = "Python execution completed."
    else:
        header = "Python execution failed."
    lines = [
        header,
        f"exit_code: {result.exit_code}",
        f"duration_ms: {result.duration_ms}",
        f"code_file: {result.code_file}",
    ]
    if result.output_truncated:
        lines.append("output_truncated: true")
    if result.stdout:
        lines.extend(["stdout:", result.stdout.rstrip()])
    if result.stderr:
        lines.extend(["stderr:", result.stderr.rstrip()])
    return "\n".join(lines)


def _format_cli_error(message: str, detail: object | None = None) -> str:
    lines = [f"Error: {message}"]
    if detail:
        lines.append(json.dumps(detail, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(lines)


def _error_detail(exc: PythonExecutionError | ToolExecutionError) -> dict[str, object]:
    return {
        "error_code": exc.error_code,
        **exc.detail,
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)
