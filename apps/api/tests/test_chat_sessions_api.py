from __future__ import annotations

from pathlib import Path

import pytest
from app.main import app
from app.service.chat_session import service as chat_session_service
from claude_agent_sdk.types import AssistantMessage, TextBlock, UserMessage
from fastapi.testclient import TestClient

client = TestClient(app)
_project_counter = 0


def _create_project(name: str = "workspace") -> dict[str, object]:
    global _project_counter
    _project_counter += 1
    local_path = Path("/tmp/chatq/test-chat-sessions") / f"{name}-{_project_counter}"
    local_path.mkdir(parents=True, exist_ok=True)
    response = client.post("/api/projects/open", json={"local_path": str(local_path)})
    assert response.status_code == 200
    return response.json()


@pytest.fixture(autouse=True)
def reset_m1_state(monkeypatch):
    transcripts: dict[str, list[object]] = {}

    transcripts["sdk_001"] = [
        UserMessage(content="帮我分析 600519 最近走势", uuid="msg_user_1"),
        AssistantMessage(
            content=[TextBlock(text="已分析 600519。")],
            model="claude-test",
            session_id="sdk_001",
            uuid="msg_assistant_1",
        ),
    ]

    def fake_get_session_messages(
        session_id: str, directory: str | None = None, limit: int | None = None, offset: int = 0
    ) -> list[object]:
        assert directory is not None
        assert offset == 0
        messages = transcripts.get(session_id, [])
        return messages[-limit:] if limit else messages

    monkeypatch.setattr(
        chat_session_service, "sdk_get_session_messages", fake_get_session_messages
    )


def test_create_session_with_initial_prompt_only_creates_chat_session():
    project = _create_project("workspace-a")
    response = client.post(
        "/api/chat-sessions",
        json={
            "project_id": project["id"],
            "initial_prompt": "帮我分析 600519 最近走势",
            "symbols": ["600519"],
            "tags": ["白酒"],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("chat_")
    assert data["title"] == "帮我分析 600519 最近走势"
    assert data["sdk_session_id"] is None
    assert data["symbols"] == ["600519"]


def test_detail_reads_messages_from_claude_agent_sdk_get_session_messages():
    project = _create_project("workspace-a")
    created = client.post(
        "/api/chat-sessions",
        json={"project_id": project["id"], "title": "已有 SDK 会话"},
    ).json()
    patched = client.patch(
        f"/api/chat-sessions/{created['id']}",
        json={"sdk_session_id": "sdk_001"},
    )
    assert patched.status_code == 200

    detail = client.get(f"/api/chat-sessions/{created['id']}")
    assert detail.status_code == 200
    detail_data = detail.json()
    assert len(detail_data["messages"]) == 2
    assert detail_data["messages"][0]["role"] == "user"


def test_list_sessions_filters_by_project_and_query():
    project_b = _create_project("workspace-b")
    project_c = _create_project("workspace-c")
    first = client.post(
        "/api/chat-sessions",
        json={
            "project_id": project_b["id"],
            "title": "均线策略复盘",
            "kind": "strategy",
            "tags": ["ma"],
        },
    )
    assert first.status_code == 201
    second = client.post(
        "/api/chat-sessions",
        json={"project_id": project_c["id"], "title": "均线策略复盘"},
    )
    assert second.status_code == 201

    response = client.get(
        f"/api/chat-sessions?project_id={project_b['id']}&query=均线&kind=strategy",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "均线策略复盘"


def test_send_message_is_owned_by_m2_runtime():
    project = _create_project("workspace-d")
    created = client.post(
        "/api/chat-sessions",
        json={"project_id": project["id"], "title": "追问测试"},
    ).json()

    response = client.post(
        f"/api/chat-sessions/{created['id']}/messages",
        json={"content": "更稳一点，回撤小一些"},
    )

    assert response.status_code == 501
    assert "M2 Claude Agent Runtime" in response.json()["detail"]


def test_link_asset_is_idempotent_and_updates_snapshot():
    project = _create_project("workspace-e")
    created = client.post(
        "/api/chat-sessions",
        json={"project_id": project["id"], "title": "回测资产"},
    ).json()

    first = client.post(
        f"/api/chat-sessions/{created['id']}/assets",
        json={
            "asset_type": "backtest_run",
            "asset_id": "bt_001",
            "relation_type": "result",
            "display_snapshot": {"title": "V1 回测", "annual_return_pct": 12.5},
        },
    )
    second = client.post(
        f"/api/chat-sessions/{created['id']}/assets",
        json={
            "asset_type": "backtest_run",
            "asset_id": "bt_001",
            "relation_type": "result",
            "display_snapshot": {"title": "V1 回测完成", "annual_return_pct": 13.2},
        },
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    assert second.json()["display_snapshot"]["annual_return_pct"] == 13.2


def test_session_detail_and_asset_link_are_not_user_scoped():
    project = _create_project("workspace-local")
    created = client.post(
        "/api/chat-sessions",
        json={"project_id": project["id"], "title": "本地会话"},
    ).json()

    detail = client.get(f"/api/chat-sessions/{created['id']}")
    link = client.post(
        f"/api/chat-sessions/{created['id']}/assets",
        json={"asset_type": "strategy_version", "asset_id": "stv_1", "relation_type": "created"},
    )

    assert detail.status_code == 200
    assert link.status_code == 201
