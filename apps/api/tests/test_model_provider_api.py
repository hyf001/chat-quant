from app.core.config import get_settings
from app.schema.model_provider import ProviderModelResponse
from app.service import model_provider as model_provider_service
from fastapi.testclient import TestClient
from pytest import LogCaptureFixture, MonkeyPatch


def test_model_provider_api_lists_default_provider_and_models(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        model_provider_service,
        "fetch_anthropic_models",
        _fake_fetch_models,
    )
    providers_response = client.get("/api/model-providers")

    assert providers_response.status_code == 200
    providers = providers_response.json()["providers"]
    assert providers[0]["id"] == "provider_anthropic_default"
    assert providers[0]["name"] == "Anthropic"
    assert providers[0]["has_api_key"] is False

    models_response = client.get("/api/model-providers/provider_anthropic_default/models")

    assert models_response.status_code == 200
    model_ids = [model["id"] for model in models_response.json()["models"]]
    assert "claude-sonnet-4" in model_ids


def test_model_provider_can_be_created_and_selected(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        model_provider_service,
        "fetch_anthropic_models",
        _fake_fetch_models,
    )
    create_response = client.post(
        "/api/model-providers",
        json={
            "name": "Internal Anthropic Gateway",
            "base_url": "https://anthropic-gateway.local",
            "api_key": "secret-token",
            "enabled": True,
        },
    )

    assert create_response.status_code == 201
    provider = create_response.json()
    assert provider["has_api_key"] is True
    assert "api_key" not in provider

    key_response = client.get(f"/api/model-providers/{provider['id']}/api-key")
    assert key_response.status_code == 200
    assert key_response.json()["api_key"] == "secret-token"

    current = client.get("/api/config").json()
    settings = current["settings"]
    settings["agent"]["provider_id"] = provider["id"]
    settings["agent"]["model"] = "claude-gateway-model"
    update_response = client.put("/api/config", json={"settings": settings})

    assert update_response.status_code == 200
    get_settings.cache_clear()
    resolved = get_settings()
    assert resolved.agent_provider_id == provider["id"]
    assert resolved.agent_model == "claude-gateway-model"
    assert resolved.agent_base_url == "https://anthropic-gateway.local"
    assert resolved.agent_api_token == "secret-token"


def test_active_model_provider_cannot_be_deleted(client: TestClient) -> None:
    response = client.delete("/api/model-providers/provider_anthropic_default")

    assert response.status_code == 409


def test_model_provider_save_requires_model_endpoint(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    def failing_fetch_models(*, base_url: str | None, api_key: str | None) -> list[object]:
        del base_url, api_key
        raise model_provider_service.ProviderModelFetchError("model endpoint failed")

    monkeypatch.setattr(
        model_provider_service,
        "fetch_anthropic_models",
        failing_fetch_models,
    )

    response = client.post(
        "/api/model-providers",
        json={
            "name": "Broken Gateway",
            "base_url": "https://broken.local",
            "api_key": "secret-token",
            "enabled": True,
        },
    )

    assert response.status_code == 502


def test_model_provider_model_fetch_failure_is_logged(
    client: TestClient,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    def failing_fetch_models(*, base_url: str | None, api_key: str | None) -> list[object]:
        del base_url, api_key
        raise model_provider_service.ProviderModelFetchError("model endpoint timed out")

    monkeypatch.setattr(
        model_provider_service,
        "fetch_anthropic_models",
        failing_fetch_models,
    )

    with caplog.at_level("WARNING", logger="app.service.model_provider"):
        response = client.get("/api/model-providers/provider_anthropic_default/models")

    assert response.status_code == 502
    record = next(
        item
        for item in caplog.records
        if item.message == "model provider model list fetch failed"
    )
    assert record.provider_id == "provider_anthropic_default"
    assert record.operation == "list_models"
    assert record.error == "model endpoint timed out"


def test_anthropic_provider_model_fetch_falls_back_for_deepseek_anthropic_base_url(
    monkeypatch: MonkeyPatch,
) -> None:
    requested_base_urls: list[str | None] = []

    def fetch_models(*, base_url: str | None, api_key: str | None) -> list[ProviderModelResponse]:
        del api_key
        requested_base_urls.append(base_url)
        if base_url == "https://api.deepseek.com/anthropic":
            raise model_provider_service.ProviderModelFetchError("Model list request failed: HTTP 404")
        return [ProviderModelResponse(id="deepseek-v4-flash", name="deepseek-v4-flash")]

    monkeypatch.setattr(
        model_provider_service,
        "_fetch_models_from_endpoint",
        fetch_models,
    )

    models = model_provider_service.fetch_anthropic_models(
        base_url="https://api.deepseek.com/anthropic",
        api_key="secret-token",
    )

    assert requested_base_urls == [
        "https://api.deepseek.com/anthropic",
        "https://api.deepseek.com",
    ]
    assert models[0].id == "deepseek-v4-flash"


def _fake_fetch_models(
    *,
    base_url: str | None,
    api_key: str | None,
) -> list[ProviderModelResponse]:
    del base_url, api_key
    return [
        ProviderModelResponse(id="claude-sonnet-4", name="claude-sonnet-4"),
        ProviderModelResponse(id="claude-gateway-model", name="claude-gateway-model"),
    ]
