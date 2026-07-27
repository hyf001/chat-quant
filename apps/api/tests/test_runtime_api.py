from pathlib import Path

from app.core.config import get_settings
from app.main import create_app
from fastapi.testclient import TestClient


def test_runtime_health_returns_runtime_probe(monkeypatch, tmp_path: Path) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("PROJECT_HOME", str(tmp_path / "projects"))
    app = create_app()

    try:
        with TestClient(app) as client:
            response = client.get("/api/runtime/health")
    finally:
        get_settings.cache_clear()

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["python_version"]
    assert isinstance(data["packages"], dict)
    assert data["project_home_writable"] is True
