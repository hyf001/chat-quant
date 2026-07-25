from __future__ import annotations

import asyncio
from uuid import uuid4

from claude_agent_sdk import get_session_messages as sdk_get_session_messages

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime, serialize_sdk_message
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.core.config import get_settings
from app.core.logging import get_logger
from app.domain.chat_sessions.models import AssetLink
from app.domain.chat_sessions.services import ChatSessionService
from app.schemas.contracts.agent_runtime import (
    AgentScenario,
    AgentTurnCommand,
    AgentTurnResult,
    AssetReference,
    ChatMessageAccepted,
    ChatMessageRequest,
    ChatSessionContext,
    ChatSessionDetail,
)

logger = get_logger(__name__)


class ChatApplicationService:
    def __init__(
        self,
        runtime: ClaudeAgentRuntime,
        stream_relay: InMemoryStreamRelay,
    ) -> None:
        self.runtime = runtime
        self.stream_relay = stream_relay
        self._running_tasks: dict[str, asyncio.Task[None]] = {}

    async def handle_user_message(
        self,
        request: ChatMessageRequest,
        chat_sessions: ChatSessionService | None = None,
    ) -> ChatMessageAccepted:
        chat_session_id = request.chat_session_id or f"chat_{uuid4().hex}"
        user_message_id = f"msg_user_{uuid4().hex}"
        title = _title_from_prompt(request.message)
        indexed_session = (
            await chat_sessions.ensure_chat_session(
                chat_session_id=chat_session_id,
                user_id=request.user_id,
                project_id=request.project_id,
                title=title,
                initial_prompt=request.message,
            )
            if chat_sessions is not None
            else None
        )
        sdk_session_id = indexed_session.sdk_session_id if indexed_session is not None else None
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
        command = AgentTurnCommand(
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
            working_dir=f"{get_settings().agent_workdir_root}/{chat_session_id}",
            sdk_session_id=sdk_session_id,
            request_id=f"req_{uuid4().hex}",
            deadline_seconds=get_settings().agent_turn_timeout_seconds,
            user_prompt=request.message,
        )
        stream_after = self.stream_relay.latest_sequence(chat_session_id)
        self._running_tasks[chat_session_id] = asyncio.create_task(
            self._run_agent_turn(command, chat_sessions)
        )
        return ChatMessageAccepted(
            chat_session_id=chat_session_id,
            user_message_id=user_message_id,
            sdk_session_id=command.sdk_session_id,
            stream_url=f"/api/chat/sessions/{chat_session_id}/stream?after={stream_after}",
        )

    def get_session_detail(self, chat_session_id: str) -> ChatSessionDetail | None:
        envelopes = self.stream_relay.list_envelopes(chat_session_id)
        if not envelopes and not self.is_turn_running(chat_session_id):
            return None
        sdk_session_id = _latest_sdk_session_id(envelopes)
        sdk_messages = self._read_sdk_messages(chat_session_id, sdk_session_id)
        return ChatSessionDetail(
            chat_session_id=chat_session_id,
            sdk_session_id=sdk_session_id,
            title="Chat-Quant 分析会话",
            sdk_messages=sdk_messages,
            envelopes=envelopes,
        )

    async def cancel_session_turn(self, chat_session_id: str, reason: str) -> bool:
        envelopes = self.stream_relay.list_envelopes(chat_session_id)
        exists = self.is_turn_running(chat_session_id) or bool(envelopes)
        if exists:
            await self.runtime.cancel_session_turn(
                chat_session_id,
                reason,
                sdk_session_id=_latest_sdk_session_id(envelopes),
            )
        task = self._running_tasks.get(chat_session_id)
        if task is not None and not task.done():
            task.cancel()
        logger.info(
            "chat session cancellation requested",
            extra={"chat_session_id": chat_session_id, "found": exists},
        )
        return exists

    def is_turn_running(self, chat_session_id: str) -> bool:
        task = self._running_tasks.get(chat_session_id)
        return task is not None and not task.done()

    def _read_sdk_messages(
        self,
        chat_session_id: str,
        sdk_session_id: str | None,
    ) -> list[dict[str, object]]:
        if sdk_session_id is None:
            return []
        try:
            messages = sdk_get_session_messages(
                sdk_session_id,
                directory=f"{get_settings().agent_workdir_root}/{chat_session_id}",
            )
            return [serialize_sdk_message(message) for message in messages]
        except FileNotFoundError:
            return []
        except (RuntimeError, ValueError) as exc:
            logger.warning(
                "failed to read sdk messages",
                extra={"sdk_session_id": sdk_session_id, "error": str(exc)},
            )
            return []

    async def _run_agent_turn(
        self,
        command: AgentTurnCommand,
        chat_sessions: ChatSessionService | None = None,
    ) -> None:
        try:
            result = await self.runtime.run_turn(command)
            if chat_sessions is not None:
                await _sync_chat_session_index(chat_sessions, command, result)
        except asyncio.CancelledError:
            logger.info(
                "agent turn task cancelled",
                extra={"chat_session_id": command.chat_session_id},
            )
            raise
        except Exception:
            logger.exception(
                "agent turn task failed unexpectedly",
                extra={"chat_session_id": command.chat_session_id},
            )
            raise
        finally:
            self._running_tasks.pop(command.chat_session_id, None)


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
    command: AgentTurnCommand,
    result: AgentTurnResult,
) -> None:
    try:
        await chat_sessions.update_chat_session(
            command.chat_session_id,
            user_id=command.user_id,
            snippet=command.user_prompt[:160],
            summary=_summary_from_prompt(command.user_prompt),
            sdk_session_id=result.sdk_session_id,
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


stream_relay = InMemoryStreamRelay()
runtime = ClaudeAgentRuntime(
    settings=get_settings(),
    stream_relay=stream_relay,
)
chat_application_service = ChatApplicationService(
    runtime,
    stream_relay,
)


def _latest_sdk_session_id(envelopes: list[object]) -> str | None:
    for envelope in reversed(envelopes):
        sdk_session_id = getattr(envelope, "sdk_session_id", None)
        if isinstance(sdk_session_id, str) and sdk_session_id:
            return sdk_session_id
    return None
