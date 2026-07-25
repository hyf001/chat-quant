from collections.abc import AsyncIterator

from app.api.routes.chat import get_chat_application_service
from app.application.chat_service import ChatApplicationService
from app.core.config import Settings
from app.agent_runtime.claude_runtime import ClaudeAgentRuntime
from app.agent_runtime.sdk_session_store import InMemoryAgentSessionStore
from app.agent_runtime.sdk_stream_relay import InMemoryStreamRelay
from app.main import app
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from fastapi.testclient import TestClient


async def fake_sdk_query(*, prompt: str, options: object | None = None) -> AsyncIterator[object]:
    del options
    session_id = "sdk_api_1"
    yield AssistantMessage(
        content=[TextBlock(text=f"收到：{prompt}")],
        model="claude-sonnet-4",
        message_id="sdk_api_msg_1",
        session_id=session_id,
    )
    yield ResultMessage(
        subtype="success",
        duration_ms=1,
        duration_api_ms=1,
        is_error=False,
        num_turns=1,
        session_id=session_id,
        result="API 流式回合完成。",
        uuid="sdk_api_result_1",
    )


stream_relay = InMemoryStreamRelay()
session_store = InMemoryAgentSessionStore()
runtime = ClaudeAgentRuntime(
    settings=Settings(),
    stream_relay=stream_relay,
    session_store=session_store,
    sdk_query=fake_sdk_query,
)
test_service = ChatApplicationService(runtime, session_store, stream_relay)
app.dependency_overrides[get_chat_application_service] = lambda: test_service
client = TestClient(app)


def test_chat_message_returns_stream_url_and_sse_events() -> None:
    response = client.post(
        "/api/chat/messages",
        json={"message": "帮我用均线策略做一个简单回测", "project_id": "project_1"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["chat_session_id"].startswith("chat_")
    assert data["sdk_session_id"] is None
    assert data["stream_url"].startswith(f"/api/chat/{data['chat_session_id']}/stream")

    stream_response = client.get(data["stream_url"])

    assert stream_response.status_code == 200
    assert "event: sdk" in stream_response.text
    assert "result_message" in stream_response.text


def test_conversation_detail_contains_messages_and_envelopes() -> None:
    response = client.post(
        "/api/chat/messages",
        json={"message": "筛选最近成交活跃的股票", "project_id": "project_1"},
    )
    chat_session_id = response.json()["chat_session_id"]

    detail_response = client.get(f"/api/chat/conversations/{chat_session_id}")

    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["chat_session_id"] == chat_session_id
    assert len(detail["messages"]) == 2
    assert len(detail["envelopes"]) >= 2
