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
from app.agent_runtime.sdk_session_store import InMemoryAgentSessionStore
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.core.config import Settings
from app.schemas.contracts.agent_runtime import AgentScenario, AgentTurnCommand, RuntimeErrorCode
from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
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


def test_sdk_options_disable_thinking_by_default_for_compatible_agent_api() -> None:
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=InMemoryStreamRelay(),
        session_store=InMemoryAgentSessionStore(),
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
    assert sdk_options.thinking == {"type": "disabled"}


async def _run_runtime_turn_assertions() -> None:
    stream_relay = InMemoryStreamRelay()
    session_store = InMemoryAgentSessionStore()
    runtime = ClaudeAgentRuntime(
        settings=Settings(),
        stream_relay=stream_relay,
        session_store=session_store,
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
