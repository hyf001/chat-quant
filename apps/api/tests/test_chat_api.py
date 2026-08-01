import asyncio
from collections.abc import AsyncIterator
from pathlib import Path
from types import SimpleNamespace

from app.agent_runtime.claude_runtime import ClaudeAgentRuntime
from app.api.v1 import chat_api as chat_api_module
from app.core.config import Settings
from app.db.session import get_session_factory
from app.main import app
from app.schema.agent_runtime import ChatMessageRequest
from app.service.chat import ChatApplicationService
from app.service.chat import service as chat_service
from app.service.chat_session import chat_session_service
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

TEST_PROJECT_HOME = "/tmp/chatq/test-projects"


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
    settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
    sdk_query=fake_sdk_query,
)
test_service = ChatApplicationService(runtime)
chat_api_module.chat_application_service = test_service
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


def test_first_answer_uses_sdk_session_title_when_available(monkeypatch: MonkeyPatch) -> None:
    asyncio.run(_run_first_answer_sdk_title_assertions(monkeypatch))


def test_first_answer_fallback_title_is_not_overwritten_by_follow_up(
    monkeypatch: MonkeyPatch,
) -> None:
    asyncio.run(_run_first_answer_fallback_title_follow_up_assertions(monkeypatch))


def test_precreated_empty_session_title_is_finalized_after_first_answer(
    monkeypatch: MonkeyPatch,
) -> None:
    asyncio.run(_run_precreated_empty_session_title_assertions(monkeypatch))


def test_agent_detail_reads_sdk_messages_from_m1_index_after_refresh(
    monkeypatch: MonkeyPatch,
) -> None:
    asyncio.run(_run_agent_detail_refresh_assertions(monkeypatch))


def test_chat_message_creates_project_directory(tmp_path: Path) -> None:
    asyncio.run(_run_project_directory_creation_assertions(tmp_path))


async def _run_project_directory_creation_assertions(tmp_path: Path) -> None:
    project_home = tmp_path / "projects"
    chat_session_id = "conv_project_dir_creation"
    project_id = "project_dir_creation"
    isolated_runtime = ClaudeAgentRuntime(
        settings=Settings(_env_file=None, PROJECT_HOME=str(project_home)),
        sdk_query=fake_sdk_query,
    )
    isolated_service = ChatApplicationService(isolated_runtime)

    await isolated_service.handle_user_message(
        ChatMessageRequest(
            message="你好",
            chat_session_id=chat_session_id,
            project_id=project_id,
        )
    )

    assert (project_home / project_id).is_dir()
    assert not (project_home / chat_session_id).exists()


async def _run_m1_index_sync_assertions() -> None:
    isolated_runtime = ClaudeAgentRuntime(
        settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
        sdk_query=fake_sdk_query,
    )
    isolated_service = ChatApplicationService(isolated_runtime)
    async with get_session_factory()() as db:
        chat_sessions = chat_session_service(db)
        accepted = await isolated_service.handle_user_message(
            ChatMessageRequest(
                chat_session_id="conv_index_sync",
                message="同步 SDK session",
                project_id="project_1",
            ),
            chat_sessions,
        )
        _ = [
            envelope
            async for envelope in isolated_service.stream_chat_session(
                accepted.chat_session_id,
                chat_sessions,
            )
        ]

        session, _ = await chat_sessions.get_context(
            "conv_index_sync",
            user_id="local_user",
        )

    assert session.sdk_session_id == "sdk_api_1"
    assert session.snippet == "同步 SDK session"


async def _run_first_answer_sdk_title_assertions(monkeypatch: MonkeyPatch) -> None:
    from app.service.chat_session import service as chat_session_sdk_service

    calls: list[tuple[str, str | None]] = []

    def fake_get_session_info(session_id: str, directory: str | None = None) -> object:
        calls.append((session_id, directory))
        return SimpleNamespace(custom_title="SDK 生成的会话名称", summary="SDK 摘要")

    monkeypatch.setattr(
        chat_session_sdk_service,
        "sdk_get_session_info",
        fake_get_session_info,
    )
    isolated_service = ChatApplicationService(
        ClaudeAgentRuntime(
            settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
            sdk_query=fake_sdk_query,
        )
    )
    async with get_session_factory()() as db:
        chat_sessions = chat_session_service(db)
        accepted = await isolated_service.handle_user_message(
            ChatMessageRequest(
                chat_session_id="conv_sdk_title_sync",
                message="帮我分析一下贵州茅台最近走势",
                project_id="project_1",
            ),
            chat_sessions,
        )
        _ = [
            envelope
            async for envelope in isolated_service.stream_chat_session(
                accepted.chat_session_id,
                chat_sessions,
            )
        ]
        session, _ = await chat_sessions.get_context(
            "conv_sdk_title_sync",
            user_id="local_user",
        )

    assert calls == [("sdk_api_1", "data/projects/project_1")]
    assert session.title == "SDK 生成的会话名称"


async def _run_first_answer_fallback_title_follow_up_assertions(
    monkeypatch: MonkeyPatch,
) -> None:
    from app.service.chat_session import service as chat_session_sdk_service

    calls: list[str] = []

    def fake_get_session_info(session_id: str, directory: str | None = None) -> None:
        del directory
        calls.append(session_id)
        return None

    monkeypatch.setattr(
        chat_session_sdk_service,
        "sdk_get_session_info",
        fake_get_session_info,
    )
    isolated_service = ChatApplicationService(
        ClaudeAgentRuntime(
            settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
            sdk_query=fake_sdk_query,
        )
    )
    async with get_session_factory()() as db:
        chat_sessions = chat_session_service(db)
        first = await isolated_service.handle_user_message(
            ChatMessageRequest(
                chat_session_id="conv_first_title_fallback",
                message="请帮我筛选最近成交量持续放大的科技股并说明原因",
                project_id="project_1",
            ),
            chat_sessions,
        )
        _ = [
            envelope
            async for envelope in isolated_service.stream_chat_session(
                first.chat_session_id,
                chat_sessions,
            )
        ]
        second = await isolated_service.handle_user_message(
            ChatMessageRequest(
                chat_session_id=first.chat_session_id,
                message="继续分析估值和风险",
                project_id="project_1",
            ),
            chat_sessions,
        )
        _ = [
            envelope
            async for envelope in isolated_service.stream_chat_session(
                second.chat_session_id,
                chat_sessions,
            )
        ]
        session, _ = await chat_sessions.get_context(
            "conv_first_title_fallback",
            user_id="local_user",
        )

    assert calls == ["sdk_api_1"]
    assert session.title == "请帮我筛选最近成交量持续放大的科技股并说"


async def _run_precreated_empty_session_title_assertions(monkeypatch: MonkeyPatch) -> None:
    from app.service.chat_session import service as chat_session_sdk_service

    def fake_get_session_info(session_id: str, directory: str | None = None) -> None:
        del session_id, directory
        return None

    def fake_get_session_messages(
        session_id: str,
        directory: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[object]:
        del session_id, directory, limit, offset
        return [
            SimpleNamespace(type="user", message={"role": "user", "content": "查看当前路径"}),
            SimpleNamespace(
                type="assistant",
                message={"role": "assistant", "content": "我来看看当前路径的内容。"},
            ),
        ]

    monkeypatch.setattr(
        chat_session_sdk_service,
        "sdk_get_session_info",
        fake_get_session_info,
    )
    monkeypatch.setattr(
        chat_session_sdk_service,
        "sdk_get_session_messages",
        fake_get_session_messages,
    )
    isolated_service = ChatApplicationService(
        ClaudeAgentRuntime(
            settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
            sdk_query=fake_sdk_query,
        )
    )
    async with get_session_factory()() as db:
        chat_sessions = chat_session_service(db)
        await chat_sessions.create_chat_session(
            user_id="local_user",
            project_id="project_1",
            chat_session_id="conv_precreated_empty",
            title="新的量化会话",
        )

        accepted = await isolated_service.handle_user_message(
            ChatMessageRequest(
                chat_session_id="conv_precreated_empty",
                message="查看当前路径",
                project_id="project_1",
            ),
            chat_sessions,
        )
        _ = [
            envelope
            async for envelope in isolated_service.stream_chat_session(
                accepted.chat_session_id,
                chat_sessions,
            )
        ]
        session, _ = await chat_sessions.get_context(
            "conv_precreated_empty",
            user_id="local_user",
        )

    assert session.title == "查看当前路径"


async def _run_agent_detail_refresh_assertions(monkeypatch: MonkeyPatch) -> None:
    def fake_get_session_messages(
        session_id: str,
        directory: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[object]:
        del limit, offset
        assert session_id == "sdk_refresh_1"
        assert directory.endswith("/project_1")
        return [
            SimpleNamespace(
                type="user",
                uuid="sdk_user_1",
                promptId="sdk_prompt_1",
                session_id=session_id,
                message={"role": "user", "content": "刷新后也要看到我"},
            ),
            SimpleNamespace(
                type="assistant",
                uuid="sdk_assistant_1",
                parentUuid="sdk_user_1",
                session_id=session_id,
                message={
                    "role": "assistant",
                    "content": [{"type": "text", "text": "这是 SDK session store 里的回复。"}],
                },
            ),
        ]

    monkeypatch.setattr(
        chat_service,
        "sdk_get_session_messages",
        fake_get_session_messages,
    )

    async with get_session_factory()() as db:
        chat_sessions = chat_session_service(db)
        await chat_sessions.create_chat_session(
            user_id="local_user",
            project_id="project_1",
            chat_session_id="conv_refresh_history",
            title="刷新历史",
        )
        await chat_sessions.update_chat_session(
            "conv_refresh_history",
            user_id="local_user",
            sdk_session_id="sdk_refresh_1",
        )
        fresh_service = ChatApplicationService(
            ClaudeAgentRuntime(
                settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
                sdk_query=fake_sdk_query,
            )
        )

        detail = await fresh_service.get_session_detail(
            "conv_refresh_history",
            chat_sessions,
            user_id="local_user",
        )

        assert detail is not None
        assert detail.sdk_session_id == "sdk_refresh_1"
        assert [envelope.sdk_event["type"] for envelope in detail.sdk_messages] == [
            "user_message",
            "assistant_message",
        ]
        assert [envelope.turn_id for envelope in detail.sdk_messages] == [
            "sdk_prompt_1",
            "sdk_prompt_1",
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
        settings=Settings(_env_file=None, PROJECT_HOME=TEST_PROJECT_HOME),
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
