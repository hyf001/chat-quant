from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from claude_agent_sdk import get_session_messages as sdk_get_session_messages

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime
from app.agent_runtime.sdk_message_parser import extract_sdk_session_id, parse_sdk_message
from app.core.config import get_settings
from app.core.logging import get_logger
from app.domain.chat_sessions.models import AssetLink
from app.domain.chat_sessions.repositories import ChatSessionNotFoundError
from app.domain.chat_sessions.services import ChatSessionAccessError, ChatSessionService
from app.schemas.contracts.agent_runtime import (
    AgentExecutionCommand,
    AgentScenario,
    AssetReference,
    ChatMessageAccepted,
    ChatMessageRequest,
    ChatSessionContext,
    ChatSessionDetail,
    SDKStreamEnvelope,
)

logger = get_logger(__name__)


@dataclass
class ChatExecutionState:
    title: str
    working_dir: str
    sdk_session_id: str | None = None


class ChatApplicationService:
    def __init__(self, runtime: ClaudeAgentRuntime) -> None:
        self.runtime = runtime
        self._pending_executions: dict[str, AgentExecutionCommand] = {}
        self._session_state: dict[str, ChatExecutionState] = {}

    async def handle_user_message(
        self,
        request: ChatMessageRequest,
        chat_sessions: ChatSessionService | None = None,
    ) -> ChatMessageAccepted:
        chat_session_id = request.chat_session_id or f"chat_{uuid4().hex}"
        user_message_id = f"msg_user_{uuid4().hex}"
        title = _title_from_prompt(request.message)
        ensured_session = (
            await chat_sessions.ensure_chat_session_with_status(
                chat_session_id=chat_session_id,
                user_id=request.user_id,
                project_id=request.project_id,
                title=title,
                initial_prompt=request.message,
            )
            if chat_sessions is not None
            else None
        )
        indexed_session = ensured_session.session if ensured_session is not None else None
        if indexed_session is not None:
            sdk_session_id = indexed_session.sdk_session_id
        else:
            state = self._session_state.get(chat_session_id)
            sdk_session_id = state.sdk_session_id if state is not None else None
        asset_links: list[AssetLink] = []
        if chat_sessions is not None and indexed_session is not None:
            _, asset_links = await chat_sessions.get_context(
                indexed_session.id,
                user_id=request.user_id,
            )
        context = ChatSessionContext(
            summary=indexed_session.summary if indexed_session is not None else None,
            related_assets=[_asset_reference_from_link(link) for link in asset_links],
        )
        working_dir = f"{self.runtime.settings.agent_workdir_root}/{chat_session_id}"
        command = AgentExecutionCommand(
            user_id=request.user_id,
            project_id=request.project_id,
            chat_session_id=chat_session_id,
            user_message_id=user_message_id,
            scenario=request.scenario
            or infer_scenario(
                request.message,
                has_history=sdk_session_id is not None,
            ),
            context=context,
            working_dir=working_dir,
            sdk_session_id=sdk_session_id,
            should_finalize_initial_title=indexed_session is not None
            and indexed_session.sdk_session_id is None,
            request_id=f"req_{uuid4().hex}",
            deadline_seconds=self.runtime.settings.agent_turn_timeout_seconds,
            user_prompt=request.message,
        )
        Path(command.working_dir).mkdir(parents=True, exist_ok=True)
        self._pending_executions[chat_session_id] = command
        self._session_state[chat_session_id] = ChatExecutionState(
            title=title,
            working_dir=working_dir,
            sdk_session_id=sdk_session_id,
        )
        return ChatMessageAccepted(
            chat_session_id=chat_session_id,
            user_message_id=user_message_id,
            sdk_session_id=command.sdk_session_id,
            stream_url=f"/api/chat/sessions/{chat_session_id}/stream",
        )

    async def get_session_detail(
        self,
        chat_session_id: str,
        chat_sessions: ChatSessionService | None = None,
        *,
        user_id: str | None = None,
    ) -> ChatSessionDetail | None:
        state = self._session_state.get(chat_session_id)
        pending = self._pending_executions.get(chat_session_id)
        session = None
        assets: list[AssetLink] = []
        if chat_sessions is not None and user_id is not None:
            try:
                session, assets = await chat_sessions.get_context(
                    chat_session_id,
                    user_id=user_id,
                )
            except ChatSessionNotFoundError:
                if state is None and pending is None:
                    return None
            except ChatSessionAccessError:
                raise
        if state is None and pending is None and session is None:
            return None

        sdk_session_id = (
            session.sdk_session_id
            if session is not None
            else state.sdk_session_id
            if state is not None
            else pending.sdk_session_id
        )
        sdk_messages = self._read_sdk_messages(chat_session_id, sdk_session_id)
        return ChatSessionDetail(
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            title=(
                session.title
                if session is not None
                else state.title
                if state is not None
                else "Chat-Quant 分析会话"
            ),
            summary=session.summary if session is not None else None,
            sdk_messages=sdk_messages,
            envelopes=[],
            assets=[_asset_reference_from_link(link) for link in assets],
        )

    async def stream_chat_session(
        self,
        chat_session_id: str,
        chat_sessions: ChatSessionService | None = None,
        *,
        user_id: str | None = None,
    ) -> AsyncIterator[SDKStreamEnvelope]:
        command = self._pending_executions.pop(chat_session_id, None)
        if command is None:
            state = self._session_state.get(chat_session_id)
            sdk_session_id = state.sdk_session_id if state is not None else None
            if sdk_session_id is None and chat_sessions is not None and user_id is not None:
                try:
                    session, _ = await chat_sessions.get_context(
                        chat_session_id,
                        user_id=user_id,
                    )
                    sdk_session_id = session.sdk_session_id
                except Exception:
                    sdk_session_id = None
            if sdk_session_id is None:
                return
            for envelope in self._read_sdk_messages(chat_session_id, sdk_session_id):
                yield envelope
            return

        latest_sdk_session_id = command.sdk_session_id
        session_index_synced = False
        async for envelope in self.runtime.stream_messages(command):
            event_session_id = envelope.sdk_session_id or extract_sdk_session_id(envelope.sdk_event)
            if event_session_id:
                latest_sdk_session_id = event_session_id
                state = self._session_state.get(chat_session_id)
                if state is not None:
                    state.sdk_session_id = event_session_id
            if (
                chat_sessions is not None
                and not session_index_synced
                and envelope.sdk_event.get("type")
                in {"result_message", "runtime_error", "cancelled"}
            ):
                await _sync_chat_session_index(
                    chat_sessions,
                    command,
                    latest_sdk_session_id,
                    envelope.sdk_event,
                )
                session_index_synced = True
            yield envelope

        if chat_sessions is not None and not session_index_synced:
            await _sync_chat_session_index(
                chat_sessions,
                command,
                latest_sdk_session_id,
                None,
            )

    async def cancel_session(self, chat_session_id: str, reason: str) -> bool:
        removed = self._pending_executions.pop(chat_session_id, None)
        exists = removed is not None or chat_session_id in self._session_state
        logger.info(
            "chat session cancellation requested",
            extra={"chat_session_id": chat_session_id, "reason": reason, "found": exists},
        )
        return exists

    def _read_sdk_messages(
        self,
        chat_session_id: str,
        sdk_session_id: str | None,
    ) -> list[SDKStreamEnvelope]:
        if sdk_session_id is None:
            return []
        try:
            messages = sdk_get_session_messages(
                sdk_session_id,
                directory=f"{self.runtime.settings.agent_workdir_root}/{chat_session_id}",
            )
            return [
                SDKStreamEnvelope(
                    sequence=index,
                    chat_session_id=chat_session_id,
                    sdk_session_id=extract_sdk_session_id(event) or sdk_session_id,
                    received_at=_now(),
                    sdk_event=event,
                )
                for index, event in enumerate(
                    (parse_sdk_message(message) for message in messages),
                    start=1,
                )
            ]
        except FileNotFoundError:
            return []
        except (RuntimeError, ValueError) as exc:
            logger.warning(
                "failed to read sdk messages",
                extra={"sdk_session_id": sdk_session_id, "error": str(exc)},
            )
            return []


def infer_scenario(message: str, has_history: bool = False) -> AgentScenario:
    lowered = message.lower()
    if has_history and any(word in lowered for word in ("再", "继续", "优化", "follow", "again")):
        return AgentScenario.FOLLOW_UP
    if any(word in lowered for word in ("回测", "backtest", "收益", "回撤")):
        return AgentScenario.BACKTEST
    if any(word in lowered for word in ("策略", "strategy", "均线", "买入", "卖出")):
        return AgentScenario.STRATEGY_BUILD
    if any(word in lowered for word in ("选股", "筛选", "screen")):
        return AgentScenario.SCREENING
    return AgentScenario.CHAT_ANALYSIS


def _title_from_prompt(prompt: str) -> str:
    stripped = prompt.strip()
    if not stripped:
        return "新的分析会话"
    return stripped[:24]


async def _sync_chat_session_index(
    chat_sessions: ChatSessionService,
    command: AgentExecutionCommand,
    sdk_session_id: str | None,
    terminal_event: dict[str, object] | None,
) -> None:
    try:
        title: str | None = None
        del terminal_event
        if command.should_finalize_initial_title:
            title = chat_sessions.initial_answer_title(
                command.chat_session_id,
                initial_prompt=command.user_prompt,
                sdk_session_id=sdk_session_id,
            )
        await chat_sessions.update_chat_session(
            command.chat_session_id,
            user_id=command.user_id,
            title=title,
            snippet=command.user_prompt[:160],
            summary=_summary_from_prompt(command.user_prompt),
            sdk_session_id=sdk_session_id,
        )
    except Exception:
        logger.exception(
            "failed to sync chat session index",
            extra={"chat_session_id": command.chat_session_id},
        )


def _summary_from_prompt(prompt: str) -> str:
    return f"最近请求：{prompt.strip()[:80]}"


def _asset_reference_from_link(link: AssetLink) -> AssetReference:
    return AssetReference(
        asset_type=str(link.asset_type),
        asset_id=link.asset_id,
        sdk_message_uuid=link.sdk_message_uuid,
        sdk_tool_use_id=link.sdk_tool_use_id,
    )


def _now() -> datetime:
    return datetime.now(UTC)


runtime = ClaudeAgentRuntime(
    settings=get_settings(),
)
chat_application_service = ChatApplicationService(runtime)
