from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_project_create_edit_list_and_delete(tmp_path) -> None:
    local_path = tmp_path / "a-share"
    created = client.post(
        "/api/projects/create",
        json={
            "local_path": str(local_path),
            "name": "A 股策略研究",
            "description": "跟踪策略与回测",
        },
    )

    assert created.status_code == 201
    project = created.json()
    assert project["id"].startswith("project_")
    assert project["local_path"] == str(local_path.resolve())
    assert project["name"] == "A 股策略研究"
    assert local_path.is_dir()

    updated = client.patch(
        f"/api/projects/{project['id']}",
        json={"name": "ETF 轮动研究"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "ETF 轮动研究"

    listed = client.get("/api/projects")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    deleted = client.delete(f"/api/projects/{project['id']}")
    assert deleted.status_code == 204

    listed_after_delete = client.get("/api/projects")
    assert listed_after_delete.json()["total"] == 0


def test_project_open_same_path_returns_same_project(tmp_path) -> None:
    local_path = tmp_path / "existing"
    local_path.mkdir()

    first = client.post("/api/projects/open", json={"local_path": str(local_path)})
    second = client.post("/api/projects/open", json={"local_path": str(local_path / ".")})

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["local_path"] == str(local_path.resolve())


def test_project_resolve_auto_registers_current_directory(tmp_path) -> None:
    response = client.post("/api/projects/resolve", json={"local_path": str(tmp_path)})

    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("project_")
    assert data["local_path"] == str(tmp_path.resolve())


def test_chat_sessions_are_filtered_by_project_query(tmp_path) -> None:
    project_a = client.post(
        "/api/projects/create",
        json={"local_path": str(tmp_path / "project-a")},
    ).json()
    project_b = client.post(
        "/api/projects/create",
        json={"local_path": str(tmp_path / "project-b")},
    ).json()
    client.post("/api/chat-sessions", json={"project_id": project_a["id"], "title": "项目 A 会话"})
    client.post("/api/chat-sessions", json={"project_id": project_b["id"], "title": "项目 B 会话"})

    response = client.get(
        f"/api/chat-sessions?project_id={project_a['id']}",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "项目 A 会话"
