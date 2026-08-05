import asyncio
import json
from collections.abc import AsyncIterator
from pathlib import Path

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime, serialize_sdk_message
from app.core.config import Settings
from app.schema.agent_runtime import (
    AgentExecutionCommand,
    RuntimeErrorCode,
)
from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    StreamEvent,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)


def test_runtime_streams_sdk_envelopes() -> None:
    asyncio.run(_run_runtime_stream_assertions())


def test_runtime_preserves_stream_event_inner_type() -> None:
    asyncio.run(_run_stream_event_type_assertions())


def test_runtime_extracts_session_id_from_system_event_data() -> None:
    asyncio.run(_run_system_event_session_id_assertions())


def test_sdk_options_omit_thinking_by_default_for_compatible_agent_api() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_sdk_query,
    )
    command = AgentExecutionCommand(
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(Path.cwd()),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )
    options = runtime.build_agent_options(command, ())

    sdk_options = runtime.build_sdk_options(command, options)

    assert sdk_options.tools == ["Bash"]
    assert sdk_options.allowed_tools == ["Bash"]
    assert sdk_options.permission_mode == "dontAsk"
    assert sdk_options.thinking is None
    assert sdk_options.plugins == [
        {
            "type": "local",
            "path": str((Path.cwd() / "plugin").resolve()),
        }
    ]


def test_runtime_system_prompt_omits_user_and_project_id() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_sdk_query,
    )
    command = AgentExecutionCommand(
        project_id="project_prompt_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(Path.cwd()),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )

    options = runtime.build_agent_options(command, ())

    assert isinstance(options.system_prompt, dict)
    system_prompt = options.system_prompt["append"]
    assert "当前项目上下文：" in system_prompt
    assert "当前工作目录就是本地项目目录" in system_prompt
    assert "user_id" not in system_prompt
    assert "project_prompt_1" not in system_prompt


def test_runtime_uses_plugin_namespaced_skills_without_copying_into_cwd(tmp_path) -> None:
    plugin_dir = tmp_path / "plugin"
    skill_dir = plugin_dir / "skills" / "financial_data_query"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Financial Data Query\n", encoding="utf-8")
    custom_skill_dir = plugin_dir / "skills" / "custom_local_skill"
    custom_skill_dir.mkdir()
    (custom_skill_dir / "SKILL.md").write_text("# Custom Local Skill\n", encoding="utf-8")
    project_dir = tmp_path / "user-project"
    project_dir.mkdir()
    runtime = ClaudeAgentRuntime(
        settings=Settings(_env_file=None, AGENT_SKILL_PLUGIN_DIR=str(plugin_dir)),
        sdk_query=fake_sdk_query,
    )
    command = AgentExecutionCommand(
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(project_dir),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )

    options = runtime.build_agent_options(
        command,
        runtime.skill_plugin.qualify_skill_names(runtime.skill_plugin.list_skill_names()),
    )
    sdk_options = runtime.build_sdk_options(command, options)

    assert sdk_options.cwd == str(project_dir)
    assert sdk_options.plugins == [{"type": "local", "path": str(plugin_dir)}]
    assert sdk_options.tools == ["Bash", "Skill"]
    assert sdk_options.skills == [
        "chat-quant:custom_local_skill",
        "chat-quant:financial_data_query",
    ]
    assert not (project_dir / ".claude" / "skills").exists()


def test_sdk_options_delegate_permissions_to_sdk_rules_without_hooks() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_sdk_query,
    )
    command = AgentExecutionCommand(
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(Path.cwd()),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )
    options = runtime.build_agent_options(
        command,
        ("chat-quant:financial_data_query",),
    )
    sdk_options = runtime.build_sdk_options(command, options)

    assert sdk_options.tools == ["Bash", "Skill"]
    assert sdk_options.allowed_tools == ["Bash"]
    assert "Skill" not in sdk_options.allowed_tools
    assert not hasattr(sdk_options, "hooks") or sdk_options.hooks is None


def test_sdk_env_maps_configured_token_to_claude_code_api_key() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(
            _env_file=None,
            ANTHROPIC_BASE_URL="https://api.example.test",
            ANTHROPIC_AUTH_TOKEN="secret_token",
        ),
        sdk_query=fake_sdk_query,
    )
    command = AgentExecutionCommand(
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(Path.cwd()),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )

    options = runtime.build_agent_options(command, ())

    assert dict(options.env) == {
        "ANTHROPIC_API_KEY": "secret_token",
        "ANTHROPIC_AUTH_TOKEN": "secret_token",
        "ANTHROPIC_BASE_URL": "https://api.example.test",
    }


def test_runtime_first_token_timeout_publishes_runtime_error() -> None:
    asyncio.run(_run_first_token_timeout_assertions())


def test_runtime_includes_sdk_stderr_in_runtime_error() -> None:
    asyncio.run(_run_sdk_stderr_error_assertions())


async def _collect_stream(
    runtime: ClaudeAgentRuntime,
    command: AgentExecutionCommand,
):
    return [envelope async for envelope in runtime.stream_messages(command)]


async def _run_runtime_stream_assertions() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_sdk_query,
    )

    envelopes = await _collect_stream(
        runtime,
        AgentExecutionCommand(
            project_id="project_1",
            chat_session_id="chat_1",
            user_message_id="msg_1",
            project_dir=str(Path.cwd()),
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="分析贵州茅台最近走势",
        )
    )

    assert [envelope.sequence for envelope in envelopes] == [1, 2, 3, 4]
    assert envelopes[0].sdk_session_id == "sdk_query_1"
    assert envelopes[-1].sdk_event["type"] == "result_message"


async def _run_stream_event_type_assertions() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_stream_event_sdk_query,
    )

    envelopes = await _collect_stream(
        runtime,
        AgentExecutionCommand(
            project_id="project_1",
            chat_session_id="chat_stream_1",
            user_message_id="msg_1",
            project_dir=str(Path.cwd()),
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    assert [envelope.sdk_event["type"] for envelope in envelopes] == [
        "content_block_delta",
        "content_block_delta",
        "result_message",
    ]
    assert envelopes[0].sdk_event["delta"] == {
        "type": "thinking_delta",
        "thinking": "先理解问题",
    }
    assert envelopes[1].sdk_event["delta"] == {"type": "text_delta", "text": "你好"}


async def _run_system_event_session_id_assertions() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_system_only_sdk_query,
    )

    envelopes = await _collect_stream(
        runtime,
        AgentExecutionCommand(
            project_id="project_1",
            chat_session_id="chat_system_1",
            user_message_id="msg_1",
            project_dir=str(Path.cwd()),
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    assert envelopes[0].sdk_session_id == "e7939275-7f1a-4958-823b-eafb4e2b3434"
    assert envelopes[-1].sdk_event["type"] == "runtime_error"
    assert envelopes[-1].sdk_event["message"] == "agent sdk stream ended without result message"


async def _run_first_token_timeout_assertions() -> None:
    settings = Settings(_env_file=None)
    settings.agent_first_token_timeout_seconds = 0.01  # type: ignore[assignment]
    runtime = ClaudeAgentRuntime(
        settings=settings,
        sdk_query=fake_hanging_after_system_sdk_query,
    )

    envelopes = await _collect_stream(
        runtime,
        AgentExecutionCommand(
            project_id="project_1",
            chat_session_id="chat_timeout_1",
            user_message_id="msg_1",
            project_dir=str(Path.cwd()),
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
            deadline_seconds=1,
        )
    )

    assert envelopes[-1].sdk_event["type"] == "runtime_error"
    assert envelopes[-1].sdk_event["code"] == RuntimeErrorCode.FIRST_TOKEN_TIMEOUT
    assert envelopes[-1].sdk_session_id == "sdk_real_1"


async def _run_sdk_stderr_error_assertions() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(_env_file=None, ANTHROPIC_AUTH_TOKEN="secret_token"),
        sdk_query=fake_stderr_error_sdk_query,
    )

    envelopes = await _collect_stream(
        runtime,
        AgentExecutionCommand(
            project_id="project_1",
            chat_session_id="chat_stderr_1",
            user_message_id="msg_1",
            project_dir=str(Path.cwd()),
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    assert envelopes[-1].sdk_event["type"] == "runtime_error"
    assert envelopes[-1].sdk_event["code"] == RuntimeErrorCode.SDK_UNAVAILABLE
    assert "SDK stderr:" in envelopes[-1].sdk_event["message"]
    assert "unsupported --thinking disabled" in envelopes[-1].sdk_event["message"]
    assert "secret_token" not in envelopes[-1].sdk_event["message"]


def test_sdk_message_serializer_preserves_standard_content_block_semantics() -> None:
    event = serialize_sdk_message(
        AssistantMessage(
            content=[
                TextBlock(text="hello"),
                ToolUseBlock(
                    id="toolu_1",
                    name="Bash",
                    input={"command": "chatq backtest get --json"},
                ),
            ],
            model="claude-sonnet-4",
            message_id="msg_1",
            session_id="sdk_1",
        )
    )

    assert event["type"] == "assistant_message"
    assert event["id"] == "msg_1"
    assert event["content"] == [
        {"type": "text", "text": "hello"},
        {
            "type": "tool_use",
            "id": "toolu_1",
            "name": "Bash",
            "input": {"command": "chatq backtest get --json"},
        },
    ]


async def fake_sdk_query(*, prompt: str, options: object | None = None) -> AsyncIterator[object]:
    del options
    session_id = "sdk_query_1"
    tool_use_id = "toolu_1"
    command = (
        "chatq strategy create --project-id project_1 --request-id req_1 --json"
    )
    yield AssistantMessage(
        content=[TextBlock(text=f"我已收到你的问题：{prompt}")],
        model="claude-sonnet-4",
        message_id="sdk_msg_1",
        session_id=session_id,
    )
    yield AssistantMessage(
        content=[ToolUseBlock(id=tool_use_id, name="Bash", input={"command": command})],
        model="claude-sonnet-4",
        message_id="sdk_msg_2",
        session_id=session_id,
    )
    yield UserMessage(
        content=[
            ToolResultBlock(
                tool_use_id=tool_use_id,
                content=json.dumps(
                    {
                        "ok": True,
                        "request_id": "req_1",
                        "data": {},
                        "artifacts": [
                            {
                                "type": "runtime_trace",
                                "id": "artifact_1",
                                "title": "M2 SDK query trace",
                            }
                        ],
                        "warnings": [],
                        "error": None,
                    },
                    ensure_ascii=False,
                ),
            )
        ],
        uuid="sdk_user_1",
    )
    yield ResultMessage(
        subtype="success",
        duration_ms=1,
        duration_api_ms=1,
        is_error=False,
        num_turns=1,
        session_id=session_id,
        result="已完成 SDK 标准 query 流式回合。",
        uuid="sdk_result_1",
    )


async def fake_stream_event_sdk_query(
    *,
    prompt: str,
    options: object | None = None,
) -> AsyncIterator[object]:
    del prompt, options
    session_id = "sdk_stream_1"
    yield StreamEvent(
        uuid="stream_event_1",
        session_id=session_id,
        event={
            "type": "content_block_delta",
            "delta": {"type": "thinking_delta", "thinking": "先理解问题"},
        },
    )
    yield StreamEvent(
        uuid="stream_event_2",
        session_id=session_id,
        event={
            "type": "content_block_delta",
            "delta": {"type": "text_delta", "text": "你好"},
        },
    )
    yield ResultMessage(
        subtype="success",
        duration_ms=1,
        duration_api_ms=1,
        is_error=False,
        num_turns=1,
        session_id=session_id,
        result="",
        uuid="sdk_stream_result_1",
    )


async def fake_system_only_sdk_query(
    *,
    prompt: str,
    options: object | None = None,
) -> AsyncIterator[object]:
    del prompt, options
    yield {
        "type": "system_message",
        "subtype": "init",
        "data": {
            "type": "system",
            "subtype": "init",
            "session_id": "e7939275-7f1a-4958-823b-eafb4e2b3434",
        },
    }


async def fake_hanging_after_system_sdk_query(
    *,
    prompt: str,
    options: object | None = None,
) -> AsyncIterator[object]:
    del prompt, options
    yield {
        "type": "system_message",
        "subtype": "status",
        "data": {
            "status": "requesting",
            "session_id": "sdk_real_1",
        },
    }
    await asyncio.sleep(60)


async def fake_stderr_error_sdk_query(
    *,
    prompt: str,
    options: object | None = None,
) -> AsyncIterator[object]:
    del prompt
    stderr = getattr(options, "stderr", None)
    if stderr is not None:
        stderr("Error: unsupported --thinking disabled with token secret_token")
    raise RuntimeError("Command failed with exit code 1")
    yield {}
