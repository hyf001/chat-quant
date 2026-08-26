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


def test_project_visualization_html_serves_project_html(tmp_path) -> None:
    local_path = tmp_path / "viz-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    html_file = local_path / "reports" / "chart.html"
    html_file.parent.mkdir(parents=True)
    html_file.write_text("<!doctype html><title>chart</title>", encoding="utf-8")

    response = client.get(
        f"/api/projects/{project['id']}/visualization-html/reports/chart.html"
    )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert response.text == "<!doctype html><title>chart</title>"


def test_project_visualization_html_rejects_non_html_and_path_escape(tmp_path) -> None:
    local_path = tmp_path / "viz-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()

    non_html = client.get(f"/api/projects/{project['id']}/visualization-html/report.txt")
    escaped = client.get(f"/api/projects/{project['id']}/visualization-html/../secret.html")

    assert non_html.status_code == 422
    assert escaped.status_code == 404


def test_project_files_lists_root_directory_with_metadata(tmp_path) -> None:
    local_path = tmp_path / "files-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    (local_path / "reports").mkdir()
    (local_path / "strategy.py").write_text("print('ok')\n", encoding="utf-8")
    (local_path / "README.md").write_text("# Readme\n", encoding="utf-8")
    (local_path / ".git").mkdir()
    (local_path / "node_modules").mkdir()

    response = client.get(f"/api/projects/{project['id']}/files")

    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == project["id"]
    assert data["root_name"] == project["name"]
    assert data["current_path"] == ""
    assert data["parent_path"] is None
    assert [item["name"] for item in data["items"]] == [
        "reports",
        "README.md",
        "strategy.py",
    ]
    assert data["items"][0]["type"] == "directory"
    assert data["items"][0]["size"] is None
    assert data["items"][1]["extension"] == "md"
    assert data["items"][2]["size"] == len("print('ok')\n")
    assert ".git" not in [item["name"] for item in data["items"]]
    assert "node_modules" not in [item["name"] for item in data["items"]]


def test_project_files_lists_nested_directory_and_parent_path(tmp_path) -> None:
    local_path = tmp_path / "files-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    nested = local_path / "reports" / "daily"
    nested.mkdir(parents=True)
    (nested / "chart.html").write_text("<title>chart</title>", encoding="utf-8")

    response = client.get(f"/api/projects/{project['id']}/files?path=reports/daily")

    assert response.status_code == 200
    data = response.json()
    assert data["current_path"] == "reports/daily"
    assert data["parent_path"] == "reports"
    assert data["items"][0]["name"] == "chart.html"
    assert data["items"][0]["relative_path"] == "reports/daily/chart.html"
    assert data["items"][0]["extension"] == "html"


def test_project_files_rejects_path_escape_and_non_directory(tmp_path) -> None:
    local_path = tmp_path / "files-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    (local_path / "strategy.py").write_text("print('ok')\n", encoding="utf-8")
    (tmp_path / "secret").mkdir()

    escaped = client.get(f"/api/projects/{project['id']}/files?path=../secret")
    file_path = client.get(f"/api/projects/{project['id']}/files?path=strategy.py")

    assert escaped.status_code == 404
    assert file_path.status_code == 404


def test_project_file_content_reads_utf8_text_file(tmp_path) -> None:
    local_path = tmp_path / "files-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    source_file = local_path / "reports" / "strategy.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('hello')\n", encoding="utf-8")

    response = client.get(
        f"/api/projects/{project['id']}/files/content",
        params={"path": "reports/strategy.py"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "strategy.py"
    assert data["relative_path"] == "reports/strategy.py"
    assert data["extension"] == "py"
    assert data["content"] == "print('hello')\n"
    assert data["truncated"] is False


def test_project_file_content_rejects_binary_and_path_escape(tmp_path) -> None:
    local_path = tmp_path / "files-project"
    project = client.post("/api/projects/create", json={"local_path": str(local_path)}).json()
    (local_path / "data.bin").write_bytes(b"\xff\xfe\x00")
    (tmp_path / "secret.txt").write_text("secret", encoding="utf-8")

    binary = client.get(
        f"/api/projects/{project['id']}/files/content",
        params={"path": "data.bin"},
    )
    escaped = client.get(
        f"/api/projects/{project['id']}/files/content",
        params={"path": "../secret.txt"},
    )

    assert binary.status_code == 422
    assert escaped.status_code == 404


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
