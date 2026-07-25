import asyncio
import json
from collections.abc import AsyncIterator

from app.agent_runtime.bash_command_policy import (
    CommandContext,
    load_default_policy,
    resolve_allowed_commands,
    validate_bash_command,
)
from app.agent_runtime.claude_runtime import ClaudeAgentRuntime, serialize_sdk_message
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.core.config import Settings
from app.schemas.contracts.agent_runtime import AgentScenario, AgentTurnCommand, RuntimeErrorCode
from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    StreamEvent,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)


def test_policy_rejects_strategy_backtest_cli_commands() -> None:
    policy = load_default_policy()
    allowed = resolve_allowed_commands(policy, AgentScenario.BACKTEST)

    decision = validate_bash_command(
        "chatq backtest get --chat-session-id chat_1 --sdk-session-id sdk_1 "
        "--project-id project_1 --json",
        allowed,
        CommandContext(chat_session_id="chat_1", sdk_session_id="sdk_1", project_id="project_1"),
    )

    assert not decision.allowed
    assert decision.code == RuntimeErrorCode.COMMAND_NOT_ALLOWED


def test_policy_blocks_shell_control_operator() -> None:
    policy = load_default_policy()
    allowed = resolve_allowed_commands(policy, AgentScenario.CHAT_ANALYSIS)

    decision = validate_bash_command(
        "chatq artifact save-code --json; rm -rf /tmp/anything",
        allowed,
        CommandContext(chat_session_id="chat_1", sdk_session_id="sdk_1", project_id="project_1"),
    )

    assert not decision.allowed
    assert decision.code == RuntimeErrorCode.TOOL_PERMISSION_DENIED


def test_runtime_runs_turn_and_publishes_sdk_envelopes() -> None:
    asyncio.run(_run_runtime_turn_assertions())


def test_runtime_preserves_stream_event_inner_type() -> None:
    asyncio.run(_run_stream_event_type_assertions())


def test_runtime_extracts_session_id_from_system_event_data() -> None:
    asyncio.run(_run_system_event_session_id_assertions())


def test_sdk_options_omit_thinking_by_default_for_compatible_agent_api() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=InMemoryStreamRelay(),
        sdk_query=fake_sdk_query,
    )
    command = AgentTurnCommand(
        user_id="user_1",
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        scenario=AgentScenario.CHAT_ANALYSIS,
        working_dir="/tmp/chatq/sdk-sessions/chat_1",
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )
    options = runtime.build_agent_options(command, (), ())

    sdk_options = runtime.build_sdk_options(command, options, ())

    assert sdk_options.tools == ["Bash"]
    assert sdk_options.allowed_tools == []
    assert sdk_options.permission_mode == "default"
    assert sdk_options.thinking is None


def test_sdk_env_maps_configured_token_to_claude_code_api_key() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(
            _env_file=None,
            ANTHROPIC_BASE_URL="https://api.example.test",
            ANTHROPIC_AUTH_TOKEN="secret_token",
        ),
        stream_relay=InMemoryStreamRelay(),
        sdk_query=fake_sdk_query,
    )
    command = AgentTurnCommand(
        user_id="user_1",
        project_id="project_1",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        scenario=AgentScenario.CHAT_ANALYSIS,
        working_dir="/tmp/chatq/sdk-sessions/chat_1",
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="你好",
    )

    options = runtime.build_agent_options(command, (), ())

    assert dict(options.env) == {
        "ANTHROPIC_API_KEY": "secret_token",
        "ANTHROPIC_AUTH_TOKEN": "secret_token",
        "ANTHROPIC_BASE_URL": "https://api.example.test",
    }


def test_runtime_first_token_timeout_publishes_runtime_error() -> None:
    asyncio.run(_run_first_token_timeout_assertions())


def test_runtime_includes_sdk_stderr_in_runtime_error() -> None:
    asyncio.run(_run_sdk_stderr_error_assertions())


async def _run_runtime_turn_assertions() -> None:
    stream_relay = InMemoryStreamRelay()
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=stream_relay,
        sdk_query=fake_sdk_query,
    )

    result = await runtime.run_turn(
        AgentTurnCommand(
            user_id="user_1",
            project_id="project_1",
            chat_session_id="chat_1",
            user_message_id="msg_1",
            scenario=AgentScenario.CHAT_ANALYSIS,
            working_dir="/tmp/chatq/sdk-sessions/chat_1",
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="分析贵州茅台最近走势",
        )
    )

    envelopes = stream_relay.list_envelopes("chat_1")
    assert result.error_code is None
    assert result.sdk_session_id is not None
    assert result.assistant_message
    assert [envelope.sequence for envelope in envelopes] == [1, 2, 3, 4]
    assert result.sdk_tool_uses[0].chatq_command == "chatq artifact save-code"


async def _run_stream_event_type_assertions() -> None:
    stream_relay = InMemoryStreamRelay()
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=stream_relay,
        sdk_query=fake_stream_event_sdk_query,
    )

    result = await runtime.run_turn(
        AgentTurnCommand(
            user_id="user_1",
            project_id="project_1",
            chat_session_id="chat_stream_1",
            user_message_id="msg_1",
            scenario=AgentScenario.CHAT_ANALYSIS,
            working_dir="/tmp/chatq/sdk-sessions/chat_stream_1",
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    envelopes = stream_relay.list_envelopes("chat_stream_1")
    assert result.error_code is None
    assert result.assistant_message == "你好"
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
    stream_relay = InMemoryStreamRelay()
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=stream_relay,
        sdk_query=fake_system_only_sdk_query,
    )

    result = await runtime.run_turn(
        AgentTurnCommand(
            user_id="user_1",
            project_id="project_1",
            chat_session_id="chat_system_1",
            user_message_id="msg_1",
            scenario=AgentScenario.CHAT_ANALYSIS,
            working_dir="/tmp/chatq/sdk-sessions/chat_system_1",
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    envelopes = stream_relay.list_envelopes("chat_system_1")
    assert result.sdk_session_id == "e7939275-7f1a-4958-823b-eafb4e2b3434"
    assert envelopes[0].sdk_session_id == result.sdk_session_id
    assert envelopes[-1].sdk_event["type"] == "runtime_error"
    assert envelopes[-1].sdk_event["message"] == "agent sdk stream ended without assistant output"


async def _run_first_token_timeout_assertions() -> None:
    stream_relay = InMemoryStreamRelay()
    settings = Settings(_env_file=None)
    settings.agent_first_token_timeout_seconds = 0.01  # type: ignore[assignment]
    runtime = ClaudeAgentRuntime(
        settings=settings,
        stream_relay=stream_relay,
        sdk_query=fake_hanging_after_system_sdk_query,
    )

    result = await runtime.run_turn(
        AgentTurnCommand(
            user_id="user_1",
            project_id="project_1",
            chat_session_id="chat_timeout_1",
            user_message_id="msg_1",
            scenario=AgentScenario.CHAT_ANALYSIS,
            working_dir="/tmp/chatq/sdk-sessions/chat_timeout_1",
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
            deadline_seconds=1,
        )
    )

    envelopes = stream_relay.list_envelopes("chat_timeout_1")
    assert result.error_code == RuntimeErrorCode.FIRST_TOKEN_TIMEOUT
    assert result.sdk_session_id == "sdk_real_1"
    assert envelopes[-1].sdk_event["type"] == "runtime_error"
    assert envelopes[-1].sdk_event["code"] == RuntimeErrorCode.FIRST_TOKEN_TIMEOUT


async def _run_sdk_stderr_error_assertions() -> None:
    stream_relay = InMemoryStreamRelay()
    runtime = ClaudeAgentRuntime(
        settings=Settings(_env_file=None, ANTHROPIC_AUTH_TOKEN="secret_token"),
        stream_relay=stream_relay,
        sdk_query=fake_stderr_error_sdk_query,
    )

    result = await runtime.run_turn(
        AgentTurnCommand(
            user_id="user_1",
            project_id="project_1",
            chat_session_id="chat_stderr_1",
            user_message_id="msg_1",
            scenario=AgentScenario.CHAT_ANALYSIS,
            working_dir="/tmp/chatq/sdk-sessions/chat_stderr_1",
            sdk_session_id=None,
            request_id="req_1",
            user_prompt="你好",
        )
    )

    envelopes = stream_relay.list_envelopes("chat_stderr_1")
    assert result.error_code == RuntimeErrorCode.SDK_UNAVAILABLE
    assert "SDK stderr:" in result.error_message
    assert "unsupported --thinking disabled" in result.error_message
    assert "secret_token" not in result.error_message
    assert envelopes[-1].sdk_event["type"] == "runtime_error"


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
        "chatq artifact save-code --chat-session-id chat_1 --project-id project_1 "
        "--request-id req_1 --json"
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
