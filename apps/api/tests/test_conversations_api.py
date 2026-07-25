from __future__ import annotations

import pytest
from app.api.dependencies import get_m1_services, make_in_memory_m1_services
from app.domain.chat_sessions import services as chat_session_services
from app.main import app
from claude_agent_sdk.types import AssistantMessage, TextBlock, UserMessage
from fastapi.testclient import TestClient

client = TestClient(app)


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
        assert directory is None
        assert offset == 0
        messages = transcripts.get(session_id, [])
        return messages[-limit:] if limit else messages

    monkeypatch.setattr(
        chat_session_services, "sdk_get_session_messages", fake_get_session_messages
    )
    app.state.m1_services = make_in_memory_m1_services()
    app.dependency_overrides[get_m1_services] = lambda: app.state.m1_services


def test_create_session_with_initial_prompt_only_creates_chat_session():
    response = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_a", "X-Project-Id": "workspace_a"},
        json={
            "initial_prompt": "帮我分析 600519 最近走势",
            "symbols": ["600519"],
            "tags": ["白酒"],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("conv_")
    assert data["title"] == "帮我分析 600519 最近走势"
    assert data["sdk_session_id"] is None
    assert data["symbols"] == ["600519"]


def test_detail_reads_messages_from_claude_agent_sdk_get_session_messages():
    created = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_a", "X-Project-Id": "workspace_a"},
        json={"title": "已有 SDK 会话"},
    ).json()
    patched = client.patch(
        f"/api/conversations/{created['id']}",
        headers={"X-User-Id": "user_a"},
        json={"sdk_session_id": "sdk_001"},
    )
    assert patched.status_code == 200

    detail = client.get(
        f"/api/conversations/{created['id']}",
        headers={"X-User-Id": "user_a"},
    )
    assert detail.status_code == 200
    detail_data = detail.json()
    assert len(detail_data["messages"]) == 2
    assert detail_data["messages"][0]["role"] == "user"


def test_list_sessions_filters_by_user_and_query():
    first = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_b", "X-Project-Id": "workspace_b"},
        json={"title": "均线策略复盘", "kind": "strategy", "tags": ["ma"]},
    )
    assert first.status_code == 201
    second = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_c", "X-Project-Id": "workspace_c"},
        json={"title": "均线策略复盘"},
    )
    assert second.status_code == 201

    response = client.get(
        "/api/conversations?query=均线&kind=strategy",
        headers={"X-User-Id": "user_b"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "均线策略复盘"


def test_send_message_is_owned_by_m2_runtime():
    created = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_d", "X-Project-Id": "workspace_d"},
        json={"title": "追问测试"},
    ).json()

    response = client.post(
        f"/api/conversations/{created['id']}/messages",
        headers={"X-User-Id": "user_d"},
        json={"content": "更稳一点，回撤小一些"},
    )

    assert response.status_code == 501
    assert "M2 Claude Agent Runtime" in response.json()["detail"]


def test_link_asset_is_idempotent_and_updates_snapshot():
    created = client.post(
        "/api/conversations",
        headers={"X-User-Id": "user_e", "X-Project-Id": "workspace_e"},
        json={"title": "回测资产"},
    ).json()

    first = client.post(
        f"/api/conversations/{created['id']}/assets",
        headers={"X-User-Id": "user_e"},
        json={
            "asset_type": "backtest_run",
            "asset_id": "bt_001",
            "relation_type": "result",
            "display_snapshot": {"title": "V1 回测", "annual_return_pct": 12.5},
        },
    )
    second = client.post(
        f"/api/conversations/{created['id']}/assets",
        headers={"X-User-Id": "user_e"},
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


def test_user_cannot_read_or_link_another_users_session():
    created = client.post(
        "/api/conversations",
        headers={"X-User-Id": "owner", "X-Project-Id": "workspace_owner"},
        json={"title": "私有会话"},
    ).json()

    detail = client.get(
        f"/api/conversations/{created['id']}",
        headers={"X-User-Id": "intruder"},
    )
    link = client.post(
        f"/api/conversations/{created['id']}/assets",
        headers={"X-User-Id": "intruder"},
        json={"asset_type": "code_artifact", "asset_id": "code_1", "relation_type": "created"},
    )

    assert detail.status_code == 403
    assert link.status_code == 403
