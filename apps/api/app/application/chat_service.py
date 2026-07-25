from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime
from app.agent_runtime.sdk_session_store import InMemoryAgentSessionStore
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.agent_runtime.sdk_transcript_store import ClaudeSDKTranscriptReader
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.contracts.agent_runtime import (
    AgentScenario,
    AgentTurnCommand,
    ChatHistoryMessage,
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
        session_store: InMemoryAgentSessionStore,
        stream_relay: InMemoryStreamRelay,
        transcript_reader: ClaudeSDKTranscriptReader | None = None,
    ) -> None:
        self.runtime = runtime
        self.session_store = session_store
        self.stream_relay = stream_relay
        self.transcript_reader = transcript_reader or ClaudeSDKTranscriptReader()
        self._running_tasks: dict[str, asyncio.Task[None]] = {}

    async def handle_user_message(self, request: ChatMessageRequest) -> ChatMessageAccepted:
        chat_session_id = request.chat_session_id or f"chat_{uuid4().hex}"
        user_message_id = f"msg_user_{uuid4().hex}"
        existing = self.session_store.get_session(chat_session_id)
        title = _title_from_prompt(request.message)
        session = self.session_store.ensure_session(
            chat_session_id=chat_session_id,
            sdk_session_id=existing.sdk_session_id if existing is not None else None,
            title=existing.title if existing is not None else title,
        )
        self.session_store.append_message(
            chat_session_id,
            ChatHistoryMessage(
                message_id=user_message_id,
                role="user",
                content=request.message,
                created_at=datetime.now(UTC),
            ),
        )
        context = ChatSessionContext(
            recent_messages=self.session_store.list_messages(chat_session_id)[-8:],
            summary=session.summary,
            related_assets=list(session.assets),
        )
        command = AgentTurnCommand(
            user_id=request.user_id,
            project_id=request.project_id,
            chat_session_id=chat_session_id,
            user_message_id=user_message_id,
            scenario=request.scenario
            or infer_scenario(request.message, has_history=existing is not None),
            context=context,
            working_dir=f"{get_settings().agent_workdir_root}/{chat_session_id}",
            sdk_session_id=existing.sdk_session_id if existing is not None else None,
            request_id=f"req_{uuid4().hex}",
            deadline_seconds=get_settings().agent_turn_timeout_seconds,
            user_prompt=request.message,
        )
        stream_after = self.stream_relay.latest_sequence(chat_session_id)
        self._running_tasks[chat_session_id] = asyncio.create_task(self._run_agent_turn(command))
        return ChatMessageAccepted(
            chat_session_id=chat_session_id,
            user_message_id=user_message_id,
            sdk_session_id=command.sdk_session_id,
            stream_url=f"/api/chat/{chat_session_id}/stream?after={stream_after}",
        )

    def get_session_detail(self, chat_session_id: str) -> ChatSessionDetail | None:
        session = self.session_store.get_session(chat_session_id)
        if session is None:
            return None
        sdk_messages = self._read_sdk_messages(session.sdk_session_id)
        return ChatSessionDetail(
            chat_session_id=session.chat_session_id,
            sdk_session_id=session.sdk_session_id,
            title=session.title,
            summary=session.summary,
            messages=list(session.messages),
            sdk_messages=sdk_messages,
            envelopes=self.stream_relay.list_envelopes(chat_session_id),
            assets=list(session.assets),
        )

    async def cancel_session_turn(self, chat_session_id: str, reason: str) -> bool:
        exists = self.session_store.get_session(chat_session_id) is not None
        await self.runtime.cancel_session_turn(chat_session_id, reason)
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

    def _read_sdk_messages(self, sdk_session_id: str | None) -> list[dict[str, object]]:
        if sdk_session_id is None:
            return []
        try:
            return self.transcript_reader.get_messages(sdk_session_id)
        except FileNotFoundError:
            return []
        except (RuntimeError, ValueError) as exc:
            logger.warning(
                "failed to read sdk transcript",
                extra={"sdk_session_id": sdk_session_id, "error": str(exc)},
            )
            return []

    async def _run_agent_turn(self, command: AgentTurnCommand) -> None:
        try:
            await self.runtime.run_turn(command)
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


stream_relay = InMemoryStreamRelay()
session_store = InMemoryAgentSessionStore()
runtime = ClaudeAgentRuntime(
    settings=get_settings(),
    stream_relay=stream_relay,
    session_store=session_store,
)
chat_application_service = ChatApplicationService(
    runtime,
    session_store,
    stream_relay,
)
