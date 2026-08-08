import asyncio
from pathlib import Path

import pytest
from app.agent_runtime.custom_tools import build_chatq_mcp_server
from app.agent_runtime.custom_tools.chatq_python import CHATQ_PYTHON_TOOL_NAME
from app.agent_runtime.custom_tools.chatq_strategy import (
    CHATQ_STRATEGY_TOOL_NAME,
    handle_chatq_strategy_tool,
)
from app.schema.agent_runtime import AgentExecutionCommand
from tests.test_strategy_api import strategy_create_payload

pytestmark = pytest.mark.usefixtures("project_test")


def test_chatq_strategy_operator_creates_and_lists_strategy(tmp_path: Path) -> None:
    asyncio.run(_run_create_and_list_strategy_assertions(tmp_path))


def test_chatq_strategy_help_returns_cli_text() -> None:
    asyncio.run(_run_help_assertions())


def test_chatq_strategy_rejects_project_id_argument() -> None:
    asyncio.run(_run_project_id_rejection_assertions())


def test_chatq_strategy_handler_returns_source_validation_issues(tmp_path: Path) -> None:
    asyncio.run(_run_source_validation_error_assertions(tmp_path))


def test_update_strategy_can_update_metadata_and_create_version(tmp_path: Path) -> None:
    asyncio.run(_run_update_strategy_with_version_assertions(tmp_path))


def test_chatq_strategy_mcp_server_uses_native_server() -> None:
    server_config = build_chatq_mcp_server(_command())

    assert CHATQ_STRATEGY_TOOL_NAME == "mcp__chatq__strategy"
    assert CHATQ_PYTHON_TOOL_NAME == "mcp__chatq__python"
    assert server_config["type"] == "sdk"
    assert server_config["name"] == "chatq"
    assert server_config["instance"] is not None


async def _run_create_and_list_strategy_assertions(project_dir: Path) -> None:
    command = _command(project_dir)
    payload = strategy_create_payload()
    source_file = project_dir / "strategy_tool_create.py"
    source_file.write_text(payload["source_code"], encoding="utf-8")

    result = await handle_chatq_strategy_tool(
        command,
        {
            "command": (
                "strategy create --name 均线突破策略 --description 测试策略 "
                "--source-file strategy_tool_create.py --mode single_symbol"
            )
        },
    )

    assert result.is_error is False
    assert "策略已创建：均线突破策略" in result.text
    strategy_id_line = next(
        line for line in result.text.splitlines() if line.startswith("strategy_id: ")
    )
    strategy_id = strategy_id_line.removeprefix("strategy_id: ")

    listed = await handle_chatq_strategy_tool(command, {"command": "strategy list"})

    assert listed.is_error is False
    assert "Strategies:" in listed.text
    assert strategy_id in listed.text


async def _run_help_assertions() -> None:
    result = await handle_chatq_strategy_tool(_command(), {"command": "--help"})

    assert result.is_error is False
    assert result.text.startswith("usage: chatq-strategy")
    assert "--project-path" not in result.text
    assert "--project-id" not in result.text


async def _run_project_id_rejection_assertions() -> None:
    result = await handle_chatq_strategy_tool(
        _command(),
        {"command": "strategy list --project-id project_test"},
    )

    assert result.is_error is True
    assert "unrecognized arguments: --project-id project_test" in result.text


async def _run_source_validation_error_assertions(project_dir: Path) -> None:
    source_file = project_dir / "invalid_strategy.py"
    source_file.write_text("class GeneratedStrategy:\n    pass\n", encoding="utf-8")
    result = await handle_chatq_strategy_tool(
        _command(project_dir),
        {
            "command": (
                "strategy create --name 无效策略 "
                "--source-file invalid_strategy.py --mode single_symbol"
            ),
        },
    )

    assert result.is_error is True
    assert "Error:" in result.text
    assert "STRATEGY_PROTOCOL_INVALID" in result.text


async def _run_update_strategy_with_version_assertions(project_dir: Path) -> None:
    command = _command(project_dir)
    payload = strategy_create_payload()
    source_file = project_dir / "strategy_tool_update.py"
    source_file.write_text(payload["source_code"], encoding="utf-8")
    created = await handle_chatq_strategy_tool(
        command,
        {"command": "strategy create --name 均线策略 --source-file strategy_tool_update.py"},
    )
    strategy_id_line = next(
        line for line in created.text.splitlines() if line.startswith("strategy_id: ")
    )
    strategy_id = strategy_id_line.removeprefix("strategy_id: ")
    updated_source = payload["source_code"].replace('"default": 20', '"default": 30', 1)
    source_file.write_text(updated_source, encoding="utf-8")

    result = await handle_chatq_strategy_tool(
        command,
        {
            "command": (
                f"strategy modify --strategy-id {strategy_id} --name 新版均线策略 "
                "--source-file strategy_tool_update.py --risk-note 调整短期均线周期"
            )
        },
    )

    assert result.is_error is False
    assert "策略已更新" in result.text
    assert "strategy_version_id: stv_" in result.text


def _command(project_dir: Path | None = None) -> AgentExecutionCommand:
    return AgentExecutionCommand(
        project_id="project_test",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(project_dir or Path.cwd()),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="创建策略",
    )
