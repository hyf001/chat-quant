import asyncio
import shlex
from pathlib import Path

import pytest
from app.agent_runtime.custom_tools.chatq_python import handle_chatq_python_tool
from app.schema.agent_runtime import AgentExecutionCommand


def test_chatq_python_runs_inline_code(tmp_path: Path) -> None:
    asyncio.run(_run_inline_code_assertions(tmp_path))


def test_chatq_python_runs_inside_service_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fail_if_subprocess_is_used(*args: object, **kwargs: object) -> None:
        raise AssertionError("chatq-python should execute in the service process")

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fail_if_subprocess_is_used)

    asyncio.run(_run_inline_code_assertions(tmp_path))


def test_chatq_python_runs_project_code_file(tmp_path: Path) -> None:
    asyncio.run(_run_project_code_file_assertions(tmp_path))


def test_chatq_python_rejects_code_file_outside_project(tmp_path: Path) -> None:
    asyncio.run(_run_outside_project_code_file_assertions(tmp_path))


def test_chatq_python_rejects_relative_code_file(tmp_path: Path) -> None:
    asyncio.run(_run_relative_code_file_assertions(tmp_path))


async def _run_inline_code_assertions(project_dir: Path) -> None:
    result = await handle_chatq_python_tool(
        _command(project_dir),
        {"command": 'run --code "print(1 + 1)"'},
    )

    assert result.is_error is False
    assert "Python execution completed." in result.text
    assert "stdout:\n2" in result.text


async def _run_project_code_file_assertions(project_dir: Path) -> None:
    source_file = project_dir / "script.py"
    source_file.write_text("print('from-file')\n", encoding="utf-8")

    result = await handle_chatq_python_tool(
        _command(project_dir),
        {"command": f"run --code-file {shlex.quote(str(source_file))}"},
    )

    assert result.is_error is False
    assert "Python execution completed." in result.text
    assert "stdout:\nfrom-file" in result.text


async def _run_outside_project_code_file_assertions(project_dir: Path) -> None:
    outside_file = project_dir.parent / "outside.py"
    outside_file.write_text("print('outside')\n", encoding="utf-8")

    result = await handle_chatq_python_tool(
        _command(project_dir),
        {"command": f"run --code-file {shlex.quote(str(outside_file))}"},
    )

    assert result.is_error is True
    assert "CHATQ_PYTHON_CODE_FILE_OUTSIDE_PROJECT" in result.text


async def _run_relative_code_file_assertions(project_dir: Path) -> None:
    source_file = project_dir / "relative.py"
    source_file.write_text("print('relative')\n", encoding="utf-8")

    result = await handle_chatq_python_tool(
        _command(project_dir),
        {"command": "run --code-file relative.py"},
    )

    assert result.is_error is True
    assert "CHATQ_PYTHON_CODE_FILE_NOT_ABSOLUTE" in result.text


def _command(project_dir: Path) -> AgentExecutionCommand:
    return AgentExecutionCommand(
        project_id="project_test",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(project_dir),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="执行 Python",
    )
