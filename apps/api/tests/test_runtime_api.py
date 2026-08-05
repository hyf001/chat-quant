from app.main import create_app
from fastapi.testclient import TestClient


def test_runtime_health_returns_runtime_probe() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/api/runtime/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["python_version"]
    assert isinstance(data["packages"], dict)
    assert "project_home_writable" not in data
