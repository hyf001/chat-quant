from app.core.config import get_settings
from fastapi.testclient import TestClient


def test_config_api_returns_structured_settings(client: TestClient) -> None:
    response = client.get("/api/config")

    assert response.status_code == 200
    payload = response.json()
    assert payload["bootstrap"]["database_path"].endswith("chat-quant.db")
    assert payload["settings"]["agent"]["model"] == "claude-sonnet-4"
    assert payload["settings"]["agent"]["thinking"]["type"] == "disabled"
    assert any(field["key"] == "agent_model" for field in payload["fields"])


def test_config_api_updates_sqlite_backed_settings(client: TestClient) -> None:
    current = client.get("/api/config").json()
    settings = current["settings"]
    settings["agent"]["model"] = "claude-test-model"
    settings["agent"]["max_turns"] = 3
    settings["paths"]["project_home"] = "custom/projects"

    response = client.put("/api/config", json={"settings": settings})

    assert response.status_code == 200
    updated = response.json()["settings"]
    assert updated["agent"]["model"] == "claude-test-model"
    assert updated["agent"]["max_turns"] == 3
    assert updated["paths"]["project_home"] == "custom/projects"
    assert get_settings().agent_model == "claude-test-model"
    assert get_settings().project_home == "custom/projects"
