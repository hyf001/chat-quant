from __future__ import annotations

from types import SimpleNamespace

from app.db.session import get_session_factory
from app.schema.chat_session import sdk_messages_to_response
from app.service.chat_session import ChatSessionService
from claude_agent_sdk.types import AssistantMessage, TextBlock, UserMessage


def test_chat_session_service_directly_calls_claude_sdk_get_session_messages(monkeypatch):
    import asyncio

    asyncio.run(_run_direct_sdk_get_session_messages_test(monkeypatch))


def test_chat_session_service_derives_sdk_directory_from_project_home(monkeypatch):
    import asyncio

    asyncio.run(_run_derived_sdk_directory_test(monkeypatch))


def test_sdk_session_message_wrappers_are_converted_to_api_messages() -> None:
    responses = sdk_messages_to_response(
        [
            SimpleNamespace(
                type="user",
                uuid="msg_user",
                session_id="sdk_real",
                message={"role": "user", "content": "你好"},
            ),
            SimpleNamespace(
                type="assistant",
                uuid="msg_assistant",
                session_id="sdk_real",
                message={
                    "role": "assistant",
                    "content": [{"type": "text", "text": "你好，我可以帮你分析股票。"}],
                },
            ),
        ]
    )

    assert [message.role for message in responses] == ["user", "assistant"]
    assert responses[0].content[0].text == "你好"
    assert responses[1].content[0].text == "你好，我可以帮你分析股票。"


async def _run_direct_sdk_get_session_messages_test(monkeypatch):
    calls: list[str] = []

    def fake_get_session_messages(
        session_id: str, directory: str | None = None, limit: int | None = None, offset: int = 0
    ) -> list[object]:
        calls.append("get_session_messages")
        assert session_id == "sdk_real"
        assert directory == "/tmp/chatq"
        assert limit == 10
        assert offset == 0
        return [
            UserMessage(content="分析贵州茅台", uuid="msg_user"),
            AssistantMessage(
                content=[TextBlock(text="已分析")],
                model="claude-test",
                session_id=session_id,
                uuid="msg_assistant",
            ),
        ]

    from app.service.chat_session import service as chat_session_sdk_service

    monkeypatch.setattr(
        chat_session_sdk_service, "sdk_get_session_messages", fake_get_session_messages
    )

    async with get_session_factory()() as db:
        chat_session_service = ChatSessionService(db, claude_agent_cwd="/tmp/chatq")
        session = await chat_session_service.create_chat_session(
            user_id="user_a",
            project_id="project_a",
            title="SDK 直连",
        )
        updated_session = await chat_session_service.update_chat_session(
            session.id,
            user_id="user_a",
            sdk_session_id="sdk_real",
        )
        _, history_messages, _ = await chat_session_service.get_chat_session_detail(
            session.id,
            user_id="user_a",
            message_limit=10,
        )

    assert calls == ["get_session_messages"]
    assert updated_session.sdk_session_id == "sdk_real"
    assert history_messages[0].uuid == "msg_user"


async def _run_derived_sdk_directory_test(monkeypatch):
    calls: list[str] = []

    def fake_get_session_messages(
        session_id: str, directory: str | None = None, limit: int | None = None, offset: int = 0
    ) -> list[object]:
        del limit, offset
        calls.append(directory or "")
        assert session_id == "sdk_real"
        return []

    from app.service.chat_session import service as chat_session_sdk_service

    monkeypatch.setattr(
        chat_session_sdk_service, "sdk_get_session_messages", fake_get_session_messages
    )

    async with get_session_factory()() as db:
        chat_session_service = ChatSessionService(db, project_home="/tmp/chatq/projects")
        session = await chat_session_service.create_chat_session(
            user_id="user_a",
            project_id="project_a",
            chat_session_id="conv_real",
            title="SDK 目录",
        )
        await chat_session_service.update_chat_session(
            session.id,
            user_id="user_a",
            sdk_session_id="sdk_real",
        )
        await chat_session_service.get_chat_session_detail(session.id, user_id="user_a")

    assert calls == ["/tmp/chatq/projects/project_a"]
