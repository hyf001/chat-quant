from __future__ import annotations

from pathlib import Path

from app.service.notebook.runtime import NotebookRuntimeRecord, _server_response
from fastapi.testclient import TestClient


def test_notebook_server_response_includes_same_origin_proxy_url() -> None:
    record = NotebookRuntimeRecord(
        runtime_id="nb_test",
        project_id="project_test",
        project_path="/tmp/chatq-test-project",
        root_dir="/tmp/chatq-test-project/notebook",
        ipython_dir="/tmp/chatq-runtime/ipython-nb_test",
        host="127.0.0.1",
        port=18888,
        token="token-test",
        pid=123,
        process_group_id=123,
        started_at="2026-09-04T00:00:00",
        updated_at="2026-09-04T00:00:00",
        status="running",
    )

    response = _server_response(record, status="running")

    assert response.base_url == "http://127.0.0.1:18888"
    assert response.proxy_base_url == "/api/notebooks/project_test/proxy"
    assert response.url == "/api/notebooks/project_test/proxy/tree?token=token-test"


def test_notebook_file_create_rename_and_delete(
    client: TestClient,
    tmp_path: Path,
) -> None:
    project = _create_project(client, tmp_path)
    notebook_dir = Path(project["local_path"]) / "notebook"

    create_response = client.post(
        f"/api/notebooks/{project['id']}/files",
        json={"name": "analysis"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "analysis.ipynb"
    assert (notebook_dir / "analysis.ipynb").is_file()

    rename_response = client.patch(
        f"/api/notebooks/{project['id']}/files",
        json={"path": "analysis.ipynb", "name": "renamed"},
    )

    assert rename_response.status_code == 200
    renamed = rename_response.json()
    assert renamed["name"] == "renamed.ipynb"
    assert not (notebook_dir / "analysis.ipynb").exists()
    assert (notebook_dir / "renamed.ipynb").is_file()

    delete_response = client.request(
        "DELETE",
        f"/api/notebooks/{project['id']}/files",
        json={"path": "renamed.ipynb"},
    )

    assert delete_response.status_code == 204
    assert not (notebook_dir / "renamed.ipynb").exists()


def test_notebook_file_rename_rejects_existing_name(
    client: TestClient,
    tmp_path: Path,
) -> None:
    project = _create_project(client, tmp_path)
    for name in ("one", "two"):
        response = client.post(f"/api/notebooks/{project['id']}/files", json={"name": name})
        assert response.status_code == 201

    response = client.patch(
        f"/api/notebooks/{project['id']}/files",
        json={"path": "one.ipynb", "name": "two"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Notebook file already exists"


def test_notebook_file_operations_reject_paths_outside_notebook_dir(
    client: TestClient,
    tmp_path: Path,
) -> None:
    project = _create_project(client, tmp_path)
    outside = Path(project["local_path"]) / "outside.ipynb"
    outside.write_text("{}", encoding="utf-8")

    response = client.request(
        "DELETE",
        f"/api/notebooks/{project['id']}/files",
        json={"path": "../outside.ipynb"},
    )

    assert response.status_code == 422
    assert outside.exists()


def _create_project(client: TestClient, tmp_path: Path) -> dict[str, object]:
    project_dir = tmp_path / "project"
    response = client.post(
        "/api/projects/create",
        json={"local_path": str(project_dir), "name": "Notebook Project"},
    )
    assert response.status_code == 201
    return response.json()
