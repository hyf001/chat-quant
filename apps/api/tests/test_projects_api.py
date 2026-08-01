from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_project_create_edit_list_and_delete() -> None:
    created = client.post(
        "/api/projects",
        headers={"X-User-Id": "user_project_a"},
        json={"name": "A 股策略研究", "description": "跟踪策略与回测"},
    )

    assert created.status_code == 201
    project = created.json()
    assert project["id"].startswith("project_")
    assert project["name"] == "A 股策略研究"

    updated = client.patch(
        f"/api/projects/{project['id']}",
        headers={"X-User-Id": "user_project_a"},
        json={"name": "ETF 轮动研究"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "ETF 轮动研究"

    listed = client.get("/api/projects", headers={"X-User-Id": "user_project_a"})
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    deleted = client.delete(
        f"/api/projects/{project['id']}",
        headers={"X-User-Id": "user_project_a"},
    )
    assert deleted.status_code == 204

    listed_after_delete = client.get("/api/projects", headers={"X-User-Id": "user_project_a"})
    assert listed_after_delete.json()["total"] == 0


def test_project_access_is_user_scoped() -> None:
    created = client.post(
        "/api/projects",
        headers={"X-User-Id": "owner"},
        json={"name": "私有项目"},
    ).json()

    response = client.patch(
        f"/api/projects/{created['id']}",
        headers={"X-User-Id": "intruder"},
        json={"name": "越权编辑"},
    )

    assert response.status_code == 403


def test_chat_sessions_are_filtered_by_project_header() -> None:
    client.post(
        "/api/chat-sessions",
        headers={"X-User-Id": "project_filter_user", "X-Project-Id": "project_a"},
        json={"title": "项目 A 会话"},
    )
    client.post(
        "/api/chat-sessions",
        headers={"X-User-Id": "project_filter_user", "X-Project-Id": "project_b"},
        json={"title": "项目 B 会话"},
    )

    response = client.get(
        "/api/chat-sessions",
        headers={"X-User-Id": "project_filter_user", "X-Project-Id": "project_a"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "项目 A 会话"
