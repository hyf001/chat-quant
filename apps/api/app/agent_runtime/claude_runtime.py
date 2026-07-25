from __future__ import annotations

import sys
import types
from collections.abc import AsyncIterator, Callable
from dataclasses import asdict, dataclass, is_dataclass
from uuid import uuid4

try:
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        PermissionResultAllow,
        PermissionResultDeny,
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
        system_prompt: str
        permission_mode: str
        resume: str | None
        max_turns: int
        model: str
        cwd: str
        can_use_tool: object
        include_partial_messages: bool
        setting_sources: list[str]
        skills: list[str]
        env: dict[str, str]
        thinking: dict[str, object] | None = None

    @dataclass
    class PermissionResultAllow:
        message: str | None = None

    @dataclass
    class PermissionResultDeny:
        message: str
        interrupt: bool = False

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
        "PermissionResultAllow": PermissionResultAllow,
        "PermissionResultDeny": PermissionResultDeny,
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

from app.agent_runtime.bash_command_policy import (
    BashCommand,
    CommandContext,
    load_default_policy,
    resolve_allowed_commands,
    validate_bash_command,
)
from app.agent_runtime.hooks import AgentRuntimeHooks
from app.agent_runtime.prompts import build_system_prompt
from app.agent_runtime.sdk_session_store import AgentSession, InMemoryAgentSessionStore
from app.agent_runtime.sdk_skill_workspace import SDKSkillWorkspace
from app.agent_runtime.sdk_skills import select_available_sdk_skills
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.agent_runtime.tool_call_logger import ToolCallLogger
from app.core.config import Settings
from app.schemas.contracts.agent_runtime import (
    AgentTurnCommand,
    AgentTurnResult,
    GeneratedArtifact,
    RuntimeErrorCode,
    SDKMessageRef,
    SDKStreamEnvelope,
    SDKToolUseRef,
)

SDKQuery = Callable[..., AsyncIterator[object]]


@dataclass(frozen=True)
class ClaudeAgentOptionsSnapshot:
    model: str
    max_turns: int
    cwd: str
    system_prompt: str
    allowed_tools: tuple[str, ...]
    skills: tuple[str, ...]
    include_partial_messages: bool
    setting_sources: tuple[str, ...]
    env: tuple[tuple[str, str], ...]


class ClaudeAgentRuntime:
    def __init__(
        self,
        *,
        settings: Settings,
        stream_relay: InMemoryStreamRelay,
        session_store: InMemoryAgentSessionStore,
        sdk_query: SDKQuery = query,
    ) -> None:
        self.settings = settings
        self.stream_relay = stream_relay
        self.session_store = session_store
        self.sdk_query = sdk_query
        self.policy = load_default_policy()
        self.hooks = AgentRuntimeHooks()
        self.tool_logger = ToolCallLogger()
        self.skill_workspace = SDKSkillWorkspace(settings.agent_project_skill_dir)

    async def run_turn(
        self,
        command: AgentTurnCommand,
        stream_sink: InMemoryStreamRelay | None = None,
    ) -> AgentTurnResult:
        sink = stream_sink or self.stream_relay
        pre_run_decision = self.hooks.pre_run(command)
        if not pre_run_decision.allowed:
            return _failed_result(command, pre_run_decision.code, pre_run_decision.reason)

        project_skill_dir = self.skill_workspace.prepare(command.working_dir)
        available_skills = self.skill_workspace.list_skill_names(project_skill_dir)
        session = self.resume_session(command.chat_session_id, command.sdk_session_id)
        allowed_commands = resolve_allowed_commands(self.policy, command.scenario)
        skill_selection = select_available_sdk_skills(
            command.scenario,
            command.sdk_skill_names,
            available_skills,
        )
        options = self.build_agent_options(command, skill_selection.names, allowed_commands)
        assistant_parts: list[str] = []
        message_refs: list[SDKMessageRef] = []
        tool_uses: dict[str, SDKToolUseRef] = {}
        envelopes: list[SDKStreamEnvelope] = []
        result_message_id: str | None = None
        result_subtype: str | None = None
        persisted_assistant_message = False

        try:
            sdk_options = self.build_sdk_options(command, options, allowed_commands)
            async for sdk_message in self.sdk_query(
                prompt=_streaming_user_prompt(command),
                options=sdk_options,
            ):
                event = serialize_sdk_message(sdk_message)
                if event.get("type") == "stream_event":
                    inner_event = event.get("event")
                    if isinstance(inner_event, dict):
                        event = {
                            **inner_event,
                            "type": "stream_event",
                            "uuid": event.get("uuid"),
                            "session_id": event.get("session_id"),
                            "parent_tool_use_id": event.get("parent_tool_use_id"),
                        }
                event = self.enrich_sdk_event_with_artifacts(event)

                event_session_id = event.get("session_id")
                if isinstance(event_session_id, str) and event_session_id:
                    session.sdk_session_id = event_session_id

                event_tool_context = CommandContext(
                    chat_session_id=command.chat_session_id,
                    sdk_session_id=event_session_id
                    if isinstance(event_session_id, str)
                    else command.sdk_session_id,
                    project_id=command.project_id,
                )

                should_publish_original_event = True
                for tool_event in _extract_tool_use_events(event):
                    decision = self.hooks.pre_tool_use(
                        tool_event,
                        allowed_commands,
                        event_tool_context,
                    )
                    if not decision.allowed:
                        blocked_event = {
                            "type": "tool_result",
                            "tool_use_id": str(tool_event.get("id") or ""),
                            "content": decision.reason or "tool use blocked",
                            "is_error": True,
                            "error_code": str(decision.code.value if decision.code else ""),
                        }
                        envelopes.append(
                            sink.publish(
                                command.chat_session_id,
                                session.sdk_session_id,
                                blocked_event,
                            )
                        )
                        should_publish_original_event = False
                        continue
                    tool_ref = self.tool_logger.from_tool_use(
                        event=tool_event,
                        chat_session_id=command.chat_session_id,
                        sdk_session_id=session.sdk_session_id,
                    )
                    if tool_ref is not None:
                        tool_uses[tool_ref.sdk_tool_use_id] = tool_ref

                for tool_result_event in _extract_tool_result_events(event):
                    tool_use_id = str(tool_result_event.get("tool_use_id") or "")
                    if tool_use_id in tool_uses:
                        tool_uses[tool_use_id] = self.tool_logger.merge_tool_result(
                            tool_uses[tool_use_id],
                            tool_result_event,
                        )

                if event.get("type") == "assistant_message":
                    message_id = str(
                        event.get("id") or event.get("uuid") or f"sdk_msg_{uuid4().hex}"
                    )
                    text_parts = _extract_text_blocks(event)
                    assistant_parts.extend(text_parts)
                    assistant_text = "\n\n".join(part for part in text_parts if part).strip()
                    if assistant_text:
                        self.session_store.append_sdk_message(
                            chat_session_id=command.chat_session_id,
                            message_id=message_id,
                            role="assistant",
                            content=assistant_text,
                        )
                        persisted_assistant_message = True
                    message_refs.append(
                        SDKMessageRef(
                            sdk_message_uuid=message_id,
                            chat_session_id=command.chat_session_id,
                            sdk_session_id=session.sdk_session_id,
                            message_type="assistant_message",
                            role="assistant",
                        )
                    )

                if event.get("type") == "result_message":
                    result_message_id = str(event.get("id") or event.get("uuid") or "")
                    result_subtype = str(event.get("subtype") or "")
                    result_text = str(event.get("result") or "")
                    if result_text:
                        assistant_parts.append(result_text)
                        if not persisted_assistant_message:
                            self.session_store.append_sdk_message(
                                chat_session_id=command.chat_session_id,
                                message_id=result_message_id or f"sdk_result_{uuid4().hex}",
                                role="assistant",
                                content=result_text,
                            )
                            persisted_assistant_message = True

                if should_publish_original_event:
                    envelopes.append(
                        sink.publish(command.chat_session_id, session.sdk_session_id, event)
                    )
        except TimeoutError:
            return self._publish_failed_turn(
                command,
                RuntimeErrorCode.RUN_TIMEOUT,
                "agent turn timed out",
                retryable=True,
                sink=sink,
            )
        except Exception as exc:
            return self._publish_failed_turn(
                command,
                RuntimeErrorCode.SDK_UNAVAILABLE,
                str(exc),
                retryable=True,
                sink=sink,
            )

        assistant_message = "\n\n".join(part for part in assistant_parts if part).strip()
        if assistant_message and not persisted_assistant_message:
            self.session_store.append_sdk_message(
                chat_session_id=command.chat_session_id,
                message_id=result_message_id or f"sdk_result_{uuid4().hex}",
                role="assistant",
                content=assistant_message,
            )
        self.session_store.update_summary(
            command.chat_session_id,
            _build_summary(command.user_prompt),
        )
        self.session_store.add_envelope_assets(command.chat_session_id, envelopes)

        return AgentTurnResult(
            chat_session_id=command.chat_session_id,
            user_message_id=command.user_message_id,
            sdk_session_id=session.sdk_session_id,
            sdk_result_message_id=result_message_id,
            sdk_result_subtype=result_subtype,
            assistant_message=assistant_message,
            generated_artifacts=_generated_artifacts(envelopes),
            sdk_message_refs=message_refs,
            sdk_tool_uses=list(tool_uses.values()),
        )

    def resume_session(self, chat_session_id: str, sdk_session_id: str | None) -> AgentSession:
        return self.session_store.ensure_session(
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            title="Chat-Quant 分析会话",
        )

    async def cancel_session_turn(self, chat_session_id: str, reason: str) -> None:
        cancelled = self.session_store.cancel(chat_session_id)
        self.stream_relay.publish(
            chat_session_id,
            self.session_store.get_session(chat_session_id).sdk_session_id if cancelled else None,
            {"type": "cancelled", "reason": reason},
        )

    def build_agent_options(
        self,
        command: AgentTurnCommand,
        skills: tuple[str, ...],
        allowed_commands: tuple[object, ...],
    ) -> ClaudeAgentOptionsSnapshot:
        system_prompt = build_system_prompt(
            command.scenario,
            command.context,
            allowed_commands,  # type: ignore[arg-type]
        )
        allowed_tools = tuple(command.allowed_tools or self.settings.agent_allowed_tools_default)
        return ClaudeAgentOptionsSnapshot(
            model=self.settings.agent_model,
            max_turns=self.settings.agent_max_turns,
            cwd=command.working_dir,
            system_prompt=system_prompt,
            allowed_tools=allowed_tools,
            skills=skills,
            include_partial_messages=self.settings.agent_include_partial_messages,
            setting_sources=("project",),
            env=tuple(_sdk_env(self.settings).items()),
        )

    def build_sdk_options(
        self,
        command: AgentTurnCommand,
        options: ClaudeAgentOptionsSnapshot,
        allowed_commands: tuple[BashCommand, ...],
    ) -> ClaudeAgentOptions:
        permission_context = CommandContext(
            chat_session_id=command.chat_session_id,
            sdk_session_id=command.sdk_session_id,
            project_id=command.project_id,
        )

        async def can_use_tool(
            tool_name: str,
            tool_input: dict[str, object],
            _context: object,
        ) -> PermissionResultAllow | PermissionResultDeny:
            if tool_name != "Bash":
                return PermissionResultDeny(
                    message="Chat-Quant M2 only permits Bash for whitelisted chatq commands.",
                    interrupt=False,
                )
            bash_command = str(tool_input.get("command") or "")
            decision = validate_bash_command(bash_command, allowed_commands, permission_context)
            if decision.allowed:
                return PermissionResultAllow()
            return PermissionResultDeny(
                message=decision.reason or "Command is not allowed by Chat-Quant policy.",
                interrupt=False,
            )

        return ClaudeAgentOptions(
            tools=list(options.allowed_tools),
            allowed_tools=[],
            system_prompt=options.system_prompt,
            permission_mode="default",
            resume=command.sdk_session_id,
            max_turns=options.max_turns,
            model=options.model,
            cwd=options.cwd,
            can_use_tool=can_use_tool,
            include_partial_messages=options.include_partial_messages,
            setting_sources=list(options.setting_sources),
            skills=list(options.skills),
            env=dict(options.env),
            thinking=_sdk_thinking_config(self.settings),
        )

    def enrich_sdk_event_with_artifacts(self, event: dict[str, object]) -> dict[str, object]:
        artifacts = _extract_artifacts_from_event(event)
        if artifacts and "artifacts" not in event:
            return {**event, "artifacts": artifacts}
        return event

    def _publish_failed_turn(
        self,
        command: AgentTurnCommand,
        code: RuntimeErrorCode,
        message: str,
        *,
        retryable: bool,
        sink: InMemoryStreamRelay,
    ) -> AgentTurnResult:
        session = self.session_store.get_session(command.chat_session_id)
        self.session_store.append_sdk_message(
            chat_session_id=command.chat_session_id,
            message_id=f"sdk_error_{uuid4().hex}",
            role="assistant",
            content=f"运行失败：{message}",
        )
        sink.publish(
            command.chat_session_id,
            session.sdk_session_id if session else command.sdk_session_id,
            {
                "type": "runtime_error",
                "code": code.value,
                "message": message,
                "retryable": retryable,
            },
        )
        return _failed_result(command, code, message, retryable=retryable)


def _extract_text_blocks(event: dict[str, object]) -> list[str]:
    content = event.get("content")
    if not isinstance(content, list):
        return []
    blocks: list[str] = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            blocks.append(str(block.get("text") or ""))
    return blocks


def _sdk_env(settings: Settings) -> dict[str, str]:
    env: dict[str, str] = {}
    if settings.agent_base_url:
        env["ANTHROPIC_BASE_URL"] = settings.agent_base_url
    if settings.agent_api_token:
        env["ANTHROPIC_AUTH_TOKEN"] = settings.agent_api_token
    return env


def _sdk_thinking_config(settings: Settings) -> dict[str, object]:
    if settings.agent_thinking_type == "enabled":
        return {
            "type": "enabled",
            "budget_tokens": settings.agent_thinking_budget_tokens,
        }
    return {"type": settings.agent_thinking_type}


async def _streaming_user_prompt(command: AgentTurnCommand) -> AsyncIterator[dict[str, object]]:
    event: dict[str, object] = {
        "type": "user",
        "message": {"role": "user", "content": command.user_prompt},
        "parent_tool_use_id": None,
    }
    if command.sdk_session_id:
        event["session_id"] = command.sdk_session_id
    yield event


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


def serialize_sdk_message(message: object) -> dict[str, object]:
    data = _to_jsonable(message)
    message_type = _sdk_type_name(message)
    if message_type:
        data.setdefault("type", message_type)
    if data.get("message_id") and not data.get("id"):
        data["id"] = data["message_id"]
    data = _normalize_sdk_content_blocks(data)
    return data


def _sdk_type_name(message: object) -> str:
    name = message.__class__.__name__
    mapping = {
        "AssistantMessage": "assistant_message",
        "UserMessage": "user_message",
        "SystemMessage": "system_message",
        "ResultMessage": "result_message",
        "StreamEvent": "stream_event",
        "RateLimitEvent": "rate_limit_event",
    }
    return mapping.get(name, name)


def _to_jsonable(value: object) -> dict[str, object]:
    if is_dataclass(value):
        converted = asdict(value)
    elif hasattr(value, "model_dump"):
        converted = value.model_dump(mode="json")  # type: ignore[union-attr]
    elif isinstance(value, dict):
        converted = value
    else:
        converted = {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    normalized = _normalize_json_value(converted)
    if isinstance(normalized, dict):
        return normalized
    return {"value": normalized}


def _normalize_json_value(value: object) -> object:
    if is_dataclass(value):
        return _normalize_json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _normalize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    return str(value)


def _normalize_sdk_content_blocks(event: dict[str, object]) -> dict[str, object]:
    content = event.get("content")
    if not isinstance(content, list):
        return event
    return {
        **event,
        "content": [
            _normalize_sdk_content_block(block) if isinstance(block, dict) else block
            for block in content
        ],
    }


def _normalize_sdk_content_block(block: dict[str, object]) -> dict[str, object]:
    if "type" in block:
        return block
    if "text" in block:
        return {"type": "text", **block}
    if "id" in block and "name" in block and "input" in block:
        return {"type": "tool_use", **block}
    if "tool_use_id" in block:
        return {"type": "tool_result", **block}
    if "thinking" in block:
        return {"type": "thinking", **block}
    return block


def _extract_artifacts_from_event(event: dict[str, object]) -> list[dict[str, object]]:
    artifacts: list[dict[str, object]] = []
    for tool_result in _extract_tool_result_events(event):
        content = tool_result.get("content")
        if not isinstance(content, str):
            continue
        parsed = _parse_json_object(content)
        if parsed is None:
            continue
        parsed_artifacts = parsed.get("artifacts")
        if not isinstance(parsed_artifacts, list):
            continue
        for artifact in parsed_artifacts:
            if isinstance(artifact, dict):
                artifacts.append(artifact)
    return artifacts


def _parse_json_object(value: str) -> dict[str, object] | None:
    import json

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _generated_artifacts(envelopes: list[SDKStreamEnvelope]) -> list[GeneratedArtifact]:
    artifacts: list[GeneratedArtifact] = []
    seen: set[tuple[str, str]] = set()
    for envelope in envelopes:
        event_artifacts = envelope.sdk_event.get("artifacts")
        if not isinstance(event_artifacts, list):
            continue
        for artifact in event_artifacts:
            if not isinstance(artifact, dict):
                continue
            artifact_type = str(artifact.get("type") or "artifact")
            artifact_id = str(artifact.get("id") or artifact.get("uri") or "")
            if not artifact_id or (artifact_type, artifact_id) in seen:
                continue
            seen.add((artifact_type, artifact_id))
            artifacts.append(
                GeneratedArtifact(
                    artifact_type=artifact_type,
                    artifact_id=artifact_id,
                    title=str(artifact.get("title") or "") or None,
                    uri=str(artifact.get("uri") or "") or None,
                )
            )
    return artifacts


def _build_summary(user_prompt: str) -> str:
    prompt = user_prompt.strip()
    if len(prompt) <= 72:
        return prompt
    return f"{prompt[:72]}..."


def _failed_result(
    command: AgentTurnCommand,
    code: RuntimeErrorCode | None,
    message: str | None,
    retryable: bool = False,
) -> AgentTurnResult:
    return AgentTurnResult(
        chat_session_id=command.chat_session_id,
        user_message_id=command.user_message_id,
        error_code=code,
        error_message=message,
        retryable=retryable,
    )
