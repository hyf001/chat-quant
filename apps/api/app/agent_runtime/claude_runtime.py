from __future__ import annotations

import asyncio
import sys
import types
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from datetime import UTC, datetime

try:
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        TextBlock,
        ToolResultBlock,
        ToolUseBlock,
        UserMessage,
        query,
    )
except ModuleNotFoundError:
    @dataclass
    class ClaudeAgentOptions:
        tools: list[str]
        allowed_tools: list[str]
        system_prompt: object
        permission_mode: str
        resume: str | None
        max_turns: int
        model: str
        cwd: str
        include_partial_messages: bool
        setting_sources: list[str]
        skills: list[str]
        plugins: list[dict[str, str]]
        env: dict[str, str]
        disallowed_tools: list[str] | None = None
        thinking: dict[str, object] | None = None
        stderr: Callable[[str], None] | None = None

    @dataclass
    class TextBlock:
        text: str

    @dataclass
    class ToolUseBlock:
        id: str
        name: str
        input: dict[str, object]

    @dataclass
    class ToolResultBlock:
        tool_use_id: str
        content: str
        is_error: bool = False

    @dataclass
    class AssistantMessage:
        content: list[object]
        model: str
        session_id: str
        message_id: str | None = None
        uuid: str | None = None

    @dataclass
    class UserMessage:
        content: list[object]
        uuid: str

    @dataclass
    class SystemMessage:
        content: list[object]
        uuid: str

    @dataclass
    class ResultMessage:
        subtype: str
        duration_ms: int
        duration_api_ms: int
        is_error: bool
        num_turns: int
        session_id: str
        result: str
        uuid: str

    async def query(*_args: object, **_kwargs: object) -> AsyncIterator[object]:
        raise RuntimeError("claude-agent-sdk is not installed")

    def get_session_messages(
        _sdk_session_id: str,
        *,
        directory: str | None = None,
        limit: int | None = None,
    ) -> list[object]:
        del directory, limit
        return []

    fallback_module = types.ModuleType("claude_agent_sdk")
    fallback_module.__path__ = []  # type: ignore[attr-defined]
    fallback_types_module = types.ModuleType("claude_agent_sdk.types")
    for name, value in {
        "AssistantMessage": AssistantMessage,
        "ClaudeAgentOptions": ClaudeAgentOptions,
        "ResultMessage": ResultMessage,
        "TextBlock": TextBlock,
        "ToolResultBlock": ToolResultBlock,
        "ToolUseBlock": ToolUseBlock,
        "UserMessage": UserMessage,
        "SystemMessage": SystemMessage,
        "get_session_messages": get_session_messages,
        "query": query,
    }.items():
        setattr(fallback_module, name, value)
        setattr(fallback_types_module, name, value)
    sys.modules.setdefault("claude_agent_sdk", fallback_module)
    sys.modules.setdefault("claude_agent_sdk.types", fallback_types_module)

from app.agent_runtime.hooks import AgentRuntimeHooks
from app.agent_runtime.prompts import build_system_prompt
from app.agent_runtime.sdk_message_parser import (
    SDKTurnTracker,
    enrich_sdk_event_with_artifacts,
    extract_sdk_session_id,
    parse_sdk_message,
)
from app.agent_runtime.sdk_skill_plugin import SDKSkillPlugin
from app.core.config import Settings
from app.core.logging import get_logger
from app.schema.agent_runtime import (
    AgentExecutionCommand,
    RuntimeErrorCode,
    SDKStreamEnvelope,
)

SDKQuery = Callable[..., AsyncIterator[object]]
logger = get_logger(__name__)
serialize_sdk_message = parse_sdk_message


@dataclass(frozen=True)
class ClaudeAgentOptionsSnapshot:
    model: str
    max_turns: int
    cwd: str
    system_prompt: object
    tools: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    disallowed_tools: tuple[str, ...]
    skills: tuple[str, ...]
    include_partial_messages: bool
    setting_sources: tuple[str, ...]
    env: tuple[tuple[str, str], ...]
    plugins: tuple[dict[str, str], ...]


class ClaudeAgentRuntime:
    def __init__(
        self,
        *,
        settings: Settings,
        sdk_query: SDKQuery = query,
    ) -> None:
        self.settings = settings
        self.sdk_query = sdk_query
        self.hooks = AgentRuntimeHooks()
        self.skill_plugin = SDKSkillPlugin(
            settings.agent_skill_plugin_dir,
            settings.agent_skill_plugin_name,
        )

    async def stream_messages(
        self,
        command: AgentExecutionCommand,
    ) -> AsyncIterator[SDKStreamEnvelope]:
        pre_run_decision = self.hooks.pre_run(command)
        if not pre_run_decision.allowed:
            yield _make_envelope(
                sequence=1,
                chat_session_id=command.chat_session_id,
                sdk_session_id=command.sdk_session_id,
                sdk_event={
                    "type": "runtime_error",
                    "code": (
                        pre_run_decision.code.value
                        if pre_run_decision.code
                        else RuntimeErrorCode.SDK_UNAVAILABLE.value
                    ),
                    "message": pre_run_decision.reason or "agent execution blocked",
                    "retryable": False,
                },
            )
            return

        options = self.build_agent_options(
            command,
            self.skill_plugin.qualify_skill_names(self.skill_plugin.list_skill_names()),
        )

        current_sdk_session_id = command.sdk_session_id
        sdk_stderr_lines: list[str] = []
        saw_effective_event = False
        saw_terminal_event = False
        sequence = 0
        turn_tracker = SDKTurnTracker()

        try:
            def collect_sdk_stderr(line: str) -> None:
                sdk_stderr_lines.append(_redact_text(line, self.settings.agent_api_token))
                if len(sdk_stderr_lines) > 20:
                    del sdk_stderr_lines[:-20]

            sdk_options = self.build_sdk_options(
                command,
                options,
                stderr=collect_sdk_stderr,
            )
            loop = asyncio.get_running_loop()
            first_effective_deadline = loop.time() + self.settings.agent_first_token_timeout_seconds
            execution_deadline = (
                loop.time() + command.deadline_seconds
                if command.deadline_seconds
                else None
            )
            sdk_messages = self.sdk_query(
                prompt=_streaming_user_prompt(command),
                options=sdk_options,
            )

            initial_deadline = _min_deadline(first_effective_deadline, execution_deadline)
            async with asyncio.timeout_at(initial_deadline) as timeout:
                async for sdk_message in sdk_messages:
                    event = enrich_sdk_event_with_artifacts(parse_sdk_message(sdk_message))
                    if _is_effective_agent_event(event) and not saw_effective_event:
                        saw_effective_event = True
                        timeout.reschedule(execution_deadline)

                    event_session_id = extract_sdk_session_id(event)
                    if event_session_id:
                        current_sdk_session_id = event_session_id

                    if event.get("type") == "result_message":
                        saw_terminal_event = True

                    turn_id = turn_tracker.annotate(event)
                    sequence += 1
                    yield _make_envelope(
                        sequence=sequence,
                        chat_session_id=command.chat_session_id,
                        sdk_session_id=current_sdk_session_id,
                        turn_id=turn_id,
                        sdk_event=event,
                    )
        except TimeoutError:
            timeout_code = (
                RuntimeErrorCode.RUN_TIMEOUT
                if saw_effective_event
                else RuntimeErrorCode.FIRST_TOKEN_TIMEOUT
            )
            sequence += 1
            yield _make_envelope(
                sequence=sequence,
                chat_session_id=command.chat_session_id,
                sdk_session_id=current_sdk_session_id,
                turn_id=None,
                sdk_event={
                    "type": "runtime_error",
                    "code": timeout_code.value,
                    "message": _sdk_failure_message(
                        "agent execution timed out"
                        if timeout_code == RuntimeErrorCode.RUN_TIMEOUT
                        else "agent sdk stream timed out before assistant output",
                        sdk_stderr_lines,
                    ),
                    "retryable": True,
                },
            )
        except Exception as exc:
            error_message = _sdk_failure_message(str(exc), sdk_stderr_lines)
            logger.exception(
                "agent sdk call failed",
                extra={
                    "chat_session_id": command.chat_session_id,
                    "error": error_message,
                },
            )
            sequence += 1
            yield _make_envelope(
                sequence=sequence,
                chat_session_id=command.chat_session_id,
                sdk_session_id=current_sdk_session_id,
                turn_id=None,
                sdk_event={
                    "type": "runtime_error",
                    "code": RuntimeErrorCode.SDK_UNAVAILABLE.value,
                    "message": error_message,
                    "retryable": True,
                },
            )
        else:
            if not saw_terminal_event:
                sequence += 1
                yield _make_envelope(
                    sequence=sequence,
                    chat_session_id=command.chat_session_id,
                    sdk_session_id=current_sdk_session_id,
                    turn_id=None,
                    sdk_event={
                        "type": "runtime_error",
                        "code": RuntimeErrorCode.SDK_UNAVAILABLE.value,
                        "message": "agent sdk stream ended without result message",
                        "retryable": True,
                    },
                )

    def build_agent_options(
        self,
        command: AgentExecutionCommand,
        skills: tuple[str, ...],
    ) -> ClaudeAgentOptionsSnapshot:
        system_prompt = build_system_prompt(
            command.scenario,
            command.context,
            user_id=command.user_id,
            project_id=command.project_id,
        )
        tools = _sdk_tools(
            tuple(command.allowed_tools or self.settings.agent_allowed_tools_default),
            skills,
        )
        return ClaudeAgentOptionsSnapshot(
            model=self.settings.agent_model,
            max_turns=self.settings.agent_max_turns,
            cwd=command.project_dir,
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": system_prompt,
            },
            tools=tools,
            allowed_tools=_sdk_allowed_tools(tools),
            disallowed_tools=_sdk_disallowed_tools(tools),
            skills=skills,
            include_partial_messages=self.settings.agent_include_partial_messages,
            setting_sources=("project",),
            env=tuple(_sdk_env(self.settings).items()),
            plugins=self.skill_plugin.sdk_plugin_configs(),
        )

    def build_sdk_options(
        self,
        command: AgentExecutionCommand,
        options: ClaudeAgentOptionsSnapshot,
        stderr: Callable[[str], None] | None = None,
    ) -> ClaudeAgentOptions:
        return ClaudeAgentOptions(
            tools=list(options.tools),
            allowed_tools=list(options.allowed_tools),
            disallowed_tools=list(options.disallowed_tools),
            system_prompt=options.system_prompt,
            permission_mode="dontAsk",
            resume=command.sdk_session_id,
            max_turns=options.max_turns,
            model=options.model,
            cwd=options.cwd,
            include_partial_messages=options.include_partial_messages,
            setting_sources=list(options.setting_sources),
            skills=list(options.skills),
            plugins=[dict(plugin_config) for plugin_config in options.plugins],
            env=dict(options.env),
            thinking=_sdk_thinking_config(self.settings),
            stderr=stderr,
        )


def _make_envelope(
    *,
    sequence: int,
    chat_session_id: str,
    sdk_session_id: str | None,
    sdk_event: dict[str, object],
    turn_id: str | None = None,
) -> SDKStreamEnvelope:
    return SDKStreamEnvelope(
        sequence=sequence,
        chat_session_id=chat_session_id,
        sdk_session_id=sdk_session_id,
        turn_id=turn_id,
        received_at=datetime.now(UTC),
        sdk_event=sdk_event,
    )


def _sdk_env(settings: Settings) -> dict[str, str]:
    env: dict[str, str] = {}
    if settings.agent_base_url:
        env["ANTHROPIC_BASE_URL"] = settings.agent_base_url
    if settings.agent_api_token:
        env["ANTHROPIC_API_KEY"] = settings.agent_api_token
        env["ANTHROPIC_AUTH_TOKEN"] = settings.agent_api_token
    return env


def _sdk_thinking_config(settings: Settings) -> dict[str, object] | None:
    if settings.agent_thinking_type == "disabled":
        return None
    if settings.agent_thinking_type == "enabled":
        return {
            "type": "enabled",
            "budget_tokens": settings.agent_thinking_budget_tokens,
        }
    return {"type": settings.agent_thinking_type}


def _sdk_tools(configured_tools: tuple[str, ...], skills: tuple[str, ...]) -> tuple[str, ...]:
    tools = list(dict.fromkeys(configured_tools))
    if skills and "Skill" not in tools:
        tools.append("Skill")
    return tuple(tools)


def _sdk_allowed_tools(tools: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(tool for tool in tools if tool != "Skill")


def _sdk_disallowed_tools(tools: tuple[str, ...]) -> tuple[str, ...]:
    available = set(tools)
    blocked_tools = ("Write", "Edit", "NotebookEdit", "Read", "WebFetch")
    return tuple(tool for tool in blocked_tools if tool not in available)


def _min_deadline(first_deadline: float, second_deadline: float | None) -> float:
    if second_deadline is None:
        return first_deadline
    return min(first_deadline, second_deadline)


def _is_effective_agent_event(event: dict[str, object]) -> bool:
    event_type = event.get("type")
    if event_type in {
        "assistant_message",
        "result_message",
        "runtime_error",
        "cancelled",
        "tool_use",
        "tool_result",
        "text_delta",
        "thinking_delta",
        "rate_limit_event",
    }:
        return True
    if event_type == "content_block_delta":
        delta = event.get("delta")
        return isinstance(delta, dict) and bool(delta)
    if _extract_tool_use_events(event) or _extract_tool_result_events(event):
        return True
    return bool(_extract_stream_text_deltas(event))


def _extract_stream_text_deltas(event: dict[str, object]) -> list[str]:
    event_type = event.get("type")
    if event_type == "text_delta":
        text = event.get("text")
        return [text] if isinstance(text, str) and text else []
    if event_type != "content_block_delta":
        return []
    delta = event.get("delta")
    if not isinstance(delta, dict):
        return []
    text = delta.get("text")
    return [text] if isinstance(text, str) and text else []


def _extract_tool_use_events(event: dict[str, object]) -> list[dict[str, object]]:
    if event.get("type") == "tool_use":
        return [event]
    content = event.get("content")
    if not isinstance(content, list):
        return []
    tool_events: list[dict[str, object]] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        tool_input = block.get("input")
        command = ""
        if isinstance(tool_input, dict):
            command = str(tool_input.get("command") or "")
        tool_events.append(
            {
                "type": "tool_use",
                "id": str(block.get("id") or ""),
                "message_id": str(event.get("id") or event.get("uuid") or ""),
                "name": str(block.get("name") or ""),
                "command": command,
                "input": tool_input if isinstance(tool_input, dict) else {},
            }
        )
    return tool_events


def _extract_tool_result_events(event: dict[str, object]) -> list[dict[str, object]]:
    if event.get("type") == "tool_result":
        return [event]
    content = event.get("content")
    if not isinstance(content, list):
        return []
    result_events: list[dict[str, object]] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_result":
            continue
        result_events.append(
            {
                "type": "tool_result",
                "tool_use_id": str(block.get("tool_use_id") or ""),
                "content": block.get("content"),
                "is_error": block.get("is_error"),
            }
        )
    return result_events


def _sdk_failure_message(message: str, stderr_lines: list[str]) -> str:
    error_message = message.strip() or "agent sdk call failed"
    stderr_tail = "\n".join(line.strip() for line in stderr_lines if line.strip()).strip()
    if not stderr_tail:
        return error_message
    return f"{error_message}\nSDK stderr:\n{stderr_tail}"


def _redact_text(text: str, secret: str | None) -> str:
    if not secret:
        return text
    return text.replace(secret, "[REDACTED]")


async def _streaming_user_prompt(
    command: AgentExecutionCommand,
) -> AsyncIterator[dict[str, object]]:
    event: dict[str, object] = {
        "type": "user",
        "message": {"role": "user", "content": command.user_prompt},
        "parent_tool_use_id": None,
    }
    if command.sdk_session_id:
        event["session_id"] = command.sdk_session_id
    yield event
