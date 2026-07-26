import asyncio
from collections.abc import AsyncIterator
from pathlib import Path
from types import SimpleNamespace

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime
from app.api.dependencies import get_m1_services, make_in_memory_m1_services
from app.api.routes.chat import get_chat_application_service
from app.application import chat_service as chat_service_module
from app.application.chat_service import ChatApplicationService
from app.core.config import Settings
from app.main import app
from app.schemas.contracts.agent_runtime import ChatMessageRequest
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from fastapi.testclient import TestClient
from pytest import MonkeyPatch


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


runtime = ClaudeAgentRuntime(
    settings=Settings(),
    sdk_query=fake_sdk_query,
)
test_service = ChatApplicationService(runtime)
app.dependency_overrides[get_chat_application_service] = lambda: test_service
app.dependency_overrides[get_m1_services] = lambda: make_in_memory_m1_services()
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
    assert data["stream_url"].startswith(
        f"/api/chat/sessions/{data['chat_session_id']}/stream"
    )

    stream_response = client.get(data["stream_url"])

    assert stream_response.status_code == 200
    assert "event: sdk" in stream_response.text
    assert "result_message" in stream_response.text


def test_chat_session_detail_does_not_use_live_envelope_cache() -> None:
    response = client.post(
        "/api/chat/messages",
        json={"message": "筛选最近成交活跃的股票", "project_id": "project_1"},
    )
    chat_session_id = response.json()["chat_session_id"]

    detail_response = client.get(f"/api/chat/sessions/{chat_session_id}")

    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["chat_session_id"] == chat_session_id
    assert detail["messages"] == []
    assert detail["envelopes"] == []


def test_follow_up_message_reuses_sdk_session_after_streaming() -> None:
    first_response = client.post(
        "/api/chat/messages",
        json={"message": "先分析一下", "project_id": "project_1"},
    )
    chat_session_id = first_response.json()["chat_session_id"]
    first_stream_response = client.get(first_response.json()["stream_url"])
    assert first_stream_response.status_code == 200

    second_response = client.post(
        "/api/chat/messages",
        json={
            "chat_session_id": chat_session_id,
            "message": "继续",
            "project_id": "project_1",
        },
    )

    assert second_response.status_code == 200
    assert "after=" not in second_response.json()["stream_url"]


def test_follow_up_message_does_not_resume_generated_sdk_placeholder() -> None:
    asyncio.run(_run_no_placeholder_resume_assertions())


def test_chat_message_syncs_sdk_session_id_to_m1_index() -> None:
    asyncio.run(_run_m1_index_sync_assertions())


def test_agent_detail_reads_sdk_messages_from_m1_index_after_refresh(
    monkeypatch: MonkeyPatch,
) -> None:
    asyncio.run(_run_agent_detail_refresh_assertions(monkeypatch))


def test_chat_message_creates_agent_working_directory(tmp_path: Path) -> None:
    asyncio.run(_run_working_directory_creation_assertions(tmp_path))


async def _run_working_directory_creation_assertions(tmp_path: Path) -> None:
    workdir_root = tmp_path / "sdk-sessions"
    chat_session_id = "conv_workdir_creation"
    isolated_runtime = ClaudeAgentRuntime(
        settings=Settings(AGENT_WORKDIR_ROOT=str(workdir_root)),
        sdk_query=fake_sdk_query,
    )
    isolated_service = ChatApplicationService(isolated_runtime)

    await isolated_service.handle_user_message(
        ChatMessageRequest(message="你好", chat_session_id=chat_session_id)
    )

    assert (workdir_root / chat_session_id).is_dir()


async def _run_m1_index_sync_assertions() -> None:
    isolated_runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=fake_sdk_query,
    )
    isolated_service = ChatApplicationService(isolated_runtime)
    m1_services = make_in_memory_m1_services()

    accepted = await isolated_service.handle_user_message(
        ChatMessageRequest(
            chat_session_id="conv_index_sync",
            message="同步 SDK session",
            project_id="project_1",
        ),
        m1_services.chat_sessions,
    )
    _ = [
        envelope
        async for envelope in isolated_service.stream_chat_session(
            accepted.chat_session_id,
            m1_services.chat_sessions,
        )
    ]

    session, _ = await m1_services.chat_sessions.get_context(
        "conv_index_sync",
        user_id="local_user",
    )

    assert session.sdk_session_id == "sdk_api_1"
    assert session.snippet == "同步 SDK session"


async def _run_agent_detail_refresh_assertions(monkeypatch: MonkeyPatch) -> None:
    def fake_get_session_messages(
        session_id: str,
        directory: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[object]:
        del limit, offset
        assert session_id == "sdk_refresh_1"
        assert directory.endswith("/conv_refresh_history")
        return [
            SimpleNamespace(
                type="user",
                uuid="sdk_user_1",
                session_id=session_id,
                message={"role": "user", "content": "刷新后也要看到我"},
            ),
            SimpleNamespace(
                type="assistant",
                uuid="sdk_assistant_1",
                session_id=session_id,
                message={
                    "role": "assistant",
                    "content": [{"type": "text", "text": "这是 SDK session store 里的回复。"}],
                },
            ),
        ]

    monkeypatch.setattr(
        chat_service_module,
        "sdk_get_session_messages",
        fake_get_session_messages,
    )

    m1_services = make_in_memory_m1_services()
    await m1_services.chat_sessions.create_chat_session(
        user_id="local_user",
        project_id="project_1",
        chat_session_id="conv_refresh_history",
        title="刷新历史",
    )
    await m1_services.chat_sessions.update_chat_session(
        "conv_refresh_history",
        user_id="local_user",
        sdk_session_id="sdk_refresh_1",
    )
    fresh_service = ChatApplicationService(
        ClaudeAgentRuntime(settings=Settings(), sdk_query=fake_sdk_query)
    )

    detail = await fresh_service.get_session_detail(
        "conv_refresh_history",
        m1_services.chat_sessions,
        user_id="local_user",
    )

    assert detail is not None
    assert detail.sdk_session_id == "sdk_refresh_1"
    assert [envelope.sdk_event["type"] for envelope in detail.sdk_messages] == [
        "user_message",
        "assistant_message",
    ]
    assert detail.sdk_messages[0].sdk_event["content"] == "刷新后也要看到我"
    assert detail.sdk_messages[1].sdk_event["content"] == [
        {"type": "text", "text": "这是 SDK session store 里的回复。"}
    ]
    assert detail.messages == []
    assert detail.envelopes == []


async def _run_no_placeholder_resume_assertions() -> None:
    captured_resume_values: list[str | None] = []

    async def sdk_query_without_session_id(
        *,
        prompt: str,
        options: object | None = None,
    ) -> AsyncIterator[object]:
        del prompt
        captured_resume_values.append(getattr(options, "resume", None))
        yield {"type": "result_message", "result": "完成。", "uuid": "sdk_result_no_session"}

    isolated_runtime = ClaudeAgentRuntime(
        settings=Settings(),
        sdk_query=sdk_query_without_session_id,
    )
    isolated_service = ChatApplicationService(isolated_runtime)

    first = await isolated_service.handle_user_message(
        ChatMessageRequest(message="第一轮", chat_session_id="conv_without_sdk_session")
    )
    _ = [envelope async for envelope in isolated_service.stream_chat_session(first.chat_session_id)]
    second = await isolated_service.handle_user_message(
        ChatMessageRequest(message="第二轮", chat_session_id=first.chat_session_id)
    )
    _ = [
        envelope
        async for envelope in isolated_service.stream_chat_session(second.chat_session_id)
    ]

    assert captured_resume_values == [None, None]
