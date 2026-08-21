import json
import logging
from pathlib import Path

import app.core.config as config_module
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


def test_config_file_path_ignores_current_working_directory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    project_config = tmp_path / "config.json"
    project_config.write_text('{"api_port": 19999}\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(config_module, "DEFAULT_CONFIG_FILE_PATH", Path("config.json"))

    assert config_module.config_file_path() != project_config.resolve(strict=False)


def test_relative_database_path_resolves_from_config_file_directory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config_dir = tmp_path / "runtime"
    project_dir = tmp_path / "project"
    config_dir.mkdir()
    project_dir.mkdir()
    config_file = config_dir / "config.json"
    config_file.write_text(
        json.dumps(
            {
                "database_path": "data/custom-chat-quant.db",
                "api_port": 18001,
                "web_port": 15174,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(config_module, "DEFAULT_CONFIG_FILE_PATH", config_file)
    monkeypatch.chdir(project_dir)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.config_file_path == config_file.resolve(strict=False)
    assert settings.database_path == (config_dir / "data/custom-chat-quant.db").resolve(
        strict=False
    )


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
    assert payload["settings"]["mindgo"]["jupyter_url"] is None
    assert payload["settings"]["mindgo"]["jupyter_token"] is None
    assert payload["settings"]["mindgo"]["notebook_path"] == "deepsolo_v3/少标的分时实时.ipynb"
    assert payload["settings"]["mindgo"]["timeout_seconds"] == 120
    assert payload["settings"]["mindgo"]["storage_root"] == "data/mindgo/parquet"
    assert payload["settings"]["market_data"]["market_data_dataset"]["dataset_id"] == ""
    assert payload["settings"]["market_data"]["market_data_dataset"]["open_field"] == ""
    assert "openinterest_field" not in payload["settings"]["market_data"]["market_data_dataset"]
    assert payload["settings"]["market_data"]["benchmark_dataset"]["dataset_id"] == ""
    assert payload["settings"]["market_data"]["benchmark_dataset"]["symbol_field"] == ""
    assert payload["settings"]["market_data"]["benchmark_dataset"]["close_field"] == ""
    assert "symbol" not in payload["settings"]["market_data"]["benchmark_dataset"]
    assert payload["settings"]["system"]["job_runtime_creation_tick_minutes"] == 1
    assert payload["settings"]["system"]["job_runtime_dispatch_interval_seconds"] == 30
    assert payload["settings"]["system"]["job_runtime_dispatch_limit"] == 20
    assert payload["settings"]["system"]["job_runtime_max_concurrent_instances"] == 20
    assert "available_tools" in payload["settings"]["agent"]
    assert "allowed_tools_default" not in payload["settings"]["agent"]
    assert any(field["key"] == "agent_provider_id" for field in payload["fields"])
    assert any(field["key"] == "agent_model" for field in payload["fields"])
    assert any(field["key"] == "agent_available_tools" for field in payload["fields"])
    tool_field = next(
        field for field in payload["fields"] if field["key"] == "agent_available_tools"
    )
    assert "Bash" in tool_field["options"]
    assert "Read" in tool_field["options"]


def test_config_api_updates_mindgo_settings(client: TestClient) -> None:
    response = client.put(
        "/api/config",
        json={
            "settings": {
                "mindgo": {
                    "jupyter_url": "https://supermind.example/notebook/user/test",
                    "jupyter_token": "token-1",
                    "notebook_path": "research/data.ipynb",
                    "kernel_id": "kernel-1",
                    "timeout_seconds": 90,
                    "storage_root": "/tmp/chatq-mindgo",
                }
            }
        },
    )

    assert response.status_code == 200
    updated = response.json()["settings"]["mindgo"]
    assert updated["jupyter_url"] == "https://supermind.example/notebook/user/test"
    assert updated["jupyter_token"] == "token-1"
    assert updated["notebook_path"] == "research/data.ipynb"
    assert updated["kernel_id"] == "kernel-1"
    assert updated["timeout_seconds"] == 90
    assert updated["storage_root"] == "/tmp/chatq-mindgo"
    assert get_settings().mindgo_jupyter_url == "https://supermind.example/notebook/user/test"
    assert get_settings().mindgo_jupyter_token == "token-1"
    assert get_settings().mindgo_notebook_path == "research/data.ipynb"
    assert get_settings().mindgo_storage_root == "/tmp/chatq-mindgo"


def test_config_api_updates_market_data_dataset_settings(client: TestClient) -> None:
    response = client.put(
        "/api/config",
        json={
            "settings": {
                "market_data": {
                    "market_data_dataset": {
                        "dataset_id": "ds_market",
                        "symbol_field": "ts_code",
                        "datetime_field": "trade_date",
                        "open_field": "open_px",
                        "high_field": "high_px",
                        "low_field": "low_px",
                        "close_field": "close_px",
                        "volume_field": "vol",
                    },
                    "benchmark_dataset": {
                        "dataset_id": "ds_index",
                        "symbol_field": "index_code",
                        "datetime_field": "trade_date",
                        "close_field": "close_px",
                    },
                },
            }
        },
    )

    assert response.status_code == 200
    updated = response.json()["settings"]
    assert updated["market_data"]["market_data_dataset"]["dataset_id"] == "ds_market"
    assert updated["market_data"]["market_data_dataset"]["open_field"] == "open_px"
    assert "openinterest_field" not in updated["market_data"]["market_data_dataset"]
    assert updated["market_data"]["benchmark_dataset"]["dataset_id"] == "ds_index"
    assert "symbol" not in updated["market_data"]["benchmark_dataset"]
    assert updated["market_data"]["benchmark_dataset"]["symbol_field"] == "index_code"
    assert get_settings().market_data_dataset["symbol_field"] == "ts_code"
    assert get_settings().benchmark_dataset["symbol_field"] == "index_code"
    assert get_settings().benchmark_dataset["close_field"] == "close_px"


def test_config_api_migrates_legacy_backtest_market_dataset(
    tmp_path: Path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "chat-quant.db"
    connection = config_module.sqlite3.connect(database_path)
    try:
        connection.execute(
            "CREATE TABLE app_settings (scope TEXT, namespace TEXT, key TEXT, value_json TEXT)"
        )
        connection.execute(
            "INSERT INTO app_settings VALUES ('global', 'backtest', 'backtest_market_dataset', ?)",
            [
                json.dumps(
                    {
                        "dataset_id": "ds_market",
                        "symbol_field": "ts_code",
                        "datetime_field": "trade_date",
                        "open_field": "open_px",
                        "high_field": "high_px",
                        "low_field": "low_px",
                        "close_field": "close_px",
                        "volume_field": "vol",
                    }
                )
            ],
        )
        connection.commit()
    finally:
        connection.close()
    config_file = tmp_path / "config.json"
    config_file.write_text(
        json.dumps({"database_path": str(database_path)}),
        encoding="utf-8",
    )
    monkeypatch.setattr(config_module, "DEFAULT_CONFIG_FILE_PATH", config_file)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.market_data_dataset["dataset_id"] == "ds_market"
    assert settings.market_data_dataset["symbol_field"] == "ts_code"


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


def test_config_api_updates_job_runtime_settings(client: TestClient) -> None:
    response = client.put(
        "/api/config",
        json={
            "settings": {
                "system": {
                    "job_runtime_creation_tick_minutes": 5,
                    "job_runtime_dispatch_interval_seconds": 10,
                    "job_runtime_dispatch_limit": 7,
                    "job_runtime_max_concurrent_instances": 3,
                }
            }
        },
    )

    assert response.status_code == 200
    updated = response.json()["settings"]["system"]
    assert updated["job_runtime_creation_tick_minutes"] == 5
    assert updated["job_runtime_dispatch_interval_seconds"] == 10
    assert updated["job_runtime_dispatch_limit"] == 7
    assert updated["job_runtime_max_concurrent_instances"] == 3
    settings = get_settings()
    assert settings.job_runtime_creation_tick_minutes == 5
    assert settings.job_runtime_dispatch_interval_seconds == 10
    assert settings.job_runtime_dispatch_limit == 7
    assert settings.job_runtime_max_concurrent_instances == 3


def test_app_restart_applies_job_runtime_settings(client: TestClient) -> None:
    response = client.put(
        "/api/config",
        json={
            "settings": {
                "system": {
                    "job_runtime_creation_tick_minutes": 6,
                    "job_runtime_dispatch_interval_seconds": 11,
                    "job_runtime_dispatch_limit": 8,
                    "job_runtime_max_concurrent_instances": 4,
                }
            }
        },
    )
    assert response.status_code == 200

    with TestClient(create_app()) as fresh_client:
        worker = fresh_client.app.state.job_runtime_worker

        assert worker._creation_tick_minutes == 6
        assert worker._dispatch_interval_seconds == 11
        assert worker._dispatch_limit == 8
        assert worker._max_concurrent_instances == 4


def test_config_api_updates_single_setting_without_touching_other_groups(
    client: TestClient,
) -> None:
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
