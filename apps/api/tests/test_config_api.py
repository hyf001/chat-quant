import logging

from app.core.config import get_settings
from app.main import create_app
from fastapi.testclient import TestClient


def test_cross_origin_requests_are_allowed() -> None:
    with TestClient(create_app()) as fresh_client:
        response = fresh_client.options(
            "/api/projects",
            headers={
                "Origin": "http://example.test",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://example.test"


def test_config_api_returns_structured_settings(client: TestClient) -> None:
    response = client.get("/api/config")

    assert response.status_code == 200
    payload = response.json()
    assert payload["bootstrap"]["database_path"].endswith("chat-quant.db")
    assert payload["bootstrap"]["api_host"] == "127.0.0.1"
    assert payload["bootstrap"]["api_port"] == 18000
    assert payload["bootstrap"]["web_host"] == "127.0.0.1"
    assert payload["bootstrap"]["web_port"] == 15173
    assert "identity" not in payload["settings"]
    assert "paths" not in payload["settings"]
    assert payload["settings"]["agent"]["provider_id"] == "provider_anthropic_default"
    assert payload["settings"]["agent"]["model"] == "claude-sonnet-4"
    assert payload["settings"]["agent"]["thinking"]["type"] == "disabled"
    assert "available_tools" in payload["settings"]["agent"]
    assert "allowed_tools_default" not in payload["settings"]["agent"]
    assert any(field["key"] == "agent_provider_id" for field in payload["fields"])
    assert any(field["key"] == "agent_model" for field in payload["fields"])
    assert any(field["key"] == "agent_available_tools" for field in payload["fields"])
    tool_field = next(field for field in payload["fields"] if field["key"] == "agent_available_tools")
    assert "Bash" in tool_field["options"]
    assert "Read" in tool_field["options"]


def test_config_api_updates_sqlite_backed_settings(client: TestClient) -> None:
    current = client.get("/api/config").json()
    settings = current["settings"]
    settings["agent"]["model"] = "claude-test-model"
    settings["agent"]["max_turns"] = 3
    settings["agent"]["available_tools"] = ["Bash", "Read"]

    response = client.put("/api/config", json={"settings": settings})

    assert response.status_code == 200
    updated = response.json()["settings"]
    assert updated["agent"]["model"] == "claude-test-model"
    assert updated["agent"]["max_turns"] == 3
    assert updated["agent"]["available_tools"] == ["Bash", "Read"]
    assert get_settings().agent_model == "claude-test-model"
    assert get_settings().agent_available_tools == ["Bash", "Read"]


def test_config_api_updates_single_setting_without_touching_other_groups(client: TestClient) -> None:
    response = client.put("/api/config", json={"settings": {"agent": {"max_turns": 7}}})

    assert response.status_code == 200
    updated = response.json()["settings"]
    assert updated["agent"]["max_turns"] == 7
    assert updated["logging"]["level"] == "INFO"
    assert get_settings().agent_max_turns == 7
    assert get_settings().log_level == "INFO"


def test_config_api_applies_logging_level_immediately(client: TestClient) -> None:
    response = client.put("/api/config", json={"settings": {"logging": {"level": "ERROR"}}})

    assert response.status_code == 200
    assert response.json()["settings"]["logging"]["level"] == "ERROR"
    assert logging.getLogger().level == logging.ERROR
    assert logging.getLogger("app").level == logging.ERROR


def test_config_api_rejects_unknown_agent_provider(client: TestClient) -> None:
    current = client.get("/api/config").json()
    settings = current["settings"]
    settings["agent"]["provider_id"] = "provider_missing"

    response = client.put("/api/config", json={"settings": settings})

    assert response.status_code == 422
