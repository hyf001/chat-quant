from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from datetime import UTC, datetime

from claude_agent_sdk import ClaudeAgentOptions, query

from app.agent_runtime.custom_tools import (
    CHATQ_PYTHON_TOOL_NAME,
    CHATQ_SERVER_NAME,
    CHATQ_STRATEGY_TOOL_NAME,
    build_chatq_mcp_server,
)
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
DEFAULT_SKILL_PLUGIN_DIR = "plugin"
DEFAULT_SKILL_PLUGIN_NAME = "chat-quant"


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
            DEFAULT_SKILL_PLUGIN_DIR,
            DEFAULT_SKILL_PLUGIN_NAME,
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
            timeout_message = (
                "模型执行超过 "
                f"{command.deadline_seconds or self.settings.agent_turn_timeout_seconds} "
                "秒，本轮已中止。"
                if timeout_code == RuntimeErrorCode.RUN_TIMEOUT
                else (
                    "模型在 "
                    f"{self.settings.agent_first_token_timeout_seconds} 秒内没有返回首个有效输出，"
                    "本轮已中止。后台调用可能仍在耗时，请稍后重试，或切换模型/Provider。"
                )
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
                    "message": _sdk_failure_message(timeout_message, sdk_stderr_lines),
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

    def build_sdk_options(
        self,
        command: AgentExecutionCommand,
        skills: tuple[str, ...] | None = None,
        stderr: Callable[[str], None] | None = None,
    ) -> ClaudeAgentOptions:
        if skills is None:
            skills = self.skill_plugin.qualify_skill_names(
                self.skill_plugin.list_skill_names(),
            )
        system_prompt = build_system_prompt(command.context)
        tools = _dedupe_tools(
            tuple(command.allowed_tools or self.settings.agent_available_tools),
        )
        tools = _ensure_skill_tool(tools, skills)
        tools = _dedupe_tools((*tools, CHATQ_STRATEGY_TOOL_NAME, CHATQ_PYTHON_TOOL_NAME))
        return ClaudeAgentOptions(
            tools=list(tools),
            allowed_tools=list(tools),
            disallowed_tools=[],
            mcp_servers={
                CHATQ_SERVER_NAME: build_chatq_mcp_server(command),
            },
            strict_mcp_config=True,
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": system_prompt,
            },
            permission_mode="bypassPermissions",
            resume=command.sdk_session_id,
            max_turns=self.settings.agent_max_turns,
            model=self.settings.agent_model,
            cwd=command.project_dir,
            include_partial_messages=self.settings.agent_include_partial_messages,
            setting_sources=["project"],
            skills=list(skills),
            plugins=[
                dict(plugin_config)
                for plugin_config in self.skill_plugin.sdk_plugin_configs()
            ],
            env=_sdk_env(self.settings),
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


def _dedupe_tools(configured_tools: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(configured_tools))


def _ensure_skill_tool(tools: tuple[str, ...], skills: tuple[str, ...]) -> tuple[str, ...]:
    if not skills or "Skill" in tools:
        return tools
    return (*tools, "Skill")


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
