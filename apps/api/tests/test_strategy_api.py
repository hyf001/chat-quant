import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.usefixtures("project_test")


def test_create_strategy_returns_draft_first_version(client: TestClient) -> None:
    response = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["strategy_id"].startswith("str_")
    assert set(data) == {"strategy_id"}


def test_create_strategy_rejects_missing_project(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["project_id"] = "project_missing"

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "PROJECT_NOT_FOUND"


def test_create_strategy_rejects_chatq_param_default_type_mismatch(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = payload["source_code"].replace(
        '"default": 20',
        '"default": "20"',
        1,
    )

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_rejects_request_custom_params(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["custom_params"] = [
        {
            "name_cn": "短期均线周期",
            "name_en": "fast_period",
            "type": "integer",
            "default": 20,
            "required": True,
        }
    ]

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_rejects_external_data_access(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = f"import akshare as ak\n{payload['source_code']}"

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error_code"] == "STRATEGY_EXTERNAL_DATA_ACCESS"
    assert detail["issues"][0]["detail"]["module"] == "akshare"


def test_create_strategy_rejects_missing_trading_method(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = "\n".join(
        [
            "import backtrader as bt",
            "",
            "class GeneratedStrategy(bt.Strategy):",
            "    def __init__(self):",
            "        self.close = self.datas[0].close",
        ]
    )

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_NO_TRADING_METHOD"


def test_update_metadata_does_not_create_new_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.patch(
        f"/api/strategies/{created['strategy_id']}",
        json={
            "name": "稳健均线策略",
            "description": "保留同一策略逻辑，只更新展示元数据",
            "tags": ["沪深300", "稳健版", "沪深300"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "稳健均线策略"
    assert data["tags"] == ["沪深300", "稳健版"]
    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["name"] == "稳健均线策略"


def test_create_strategy_version_switches_current_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90, strategy_mode="multi_symbol"),
    )

    assert response.status_code == 201
    version = response.json()
    assert version["strategy_id"] == created["strategy_id"]
    assert version["version"] == 2
    assert version["strategy_mode"] == "multi_symbol"
    assert version["custom_params"][0]["default"] == 30
    assert version["custom_params"][1]["default"] == 90

    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == version["id"]

    strategies = client.get("/api/strategies?project_id=project_test").json()
    assert strategies[0]["strategy_version_id"] == version["id"]
    assert strategies[0]["version"] == 2
    assert strategies[0]["strategy_mode"] == "multi_symbol"
    assert "strategy_config" not in strategies[0]
    assert strategies[0]["custom_params"][0]["default"] == 30


def test_create_strategy_version_rejects_request_custom_params(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    payload = strategy_version_payload(fast_period=30, slow_period=90)
    payload["custom_params"] = [
        {
            "name_cn": "短期均线周期",
            "name_en": "fast_period",
            "type": "integer",
            "default": 30,
            "required": True,
        }
    ]

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_version_smoke_failure_is_blocked_without_switching(
    client: TestClient,
) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    first_version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]
    payload = strategy_version_payload()
    payload["source_code"] = "\n".join(
        [
            "import backtrader as bt",
            "",
            "class GeneratedStrategy(bt.Strategy):",
            "    def next(self):",
            "        raise RuntimeError('boom')",
        ]
    )

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_SMOKE_RUN_FAILED"
    versions = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()
    assert [version["id"] for version in versions] == [first_version["id"]]
    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == first_version["id"]


def test_switch_current_version_can_select_existing_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    first_version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]
    second_version = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90, strategy_mode="multi_symbol"),
    ).json()

    response = client.patch(
        f"/api/strategies/{created['strategy_id']}/current-version",
        json={"strategy_version_id": first_version["id"]},
    )

    assert response.status_code == 200
    summary = response.json()
    assert summary["strategy_version_id"] == first_version["id"]
    assert summary["version"] == 1
    assert summary["strategy_mode"] == "single_symbol"

    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == first_version["id"]

    strategies = client.get("/api/strategies?project_id=project_test").json()
    assert strategies[0]["strategy_version_id"] == first_version["id"]
    assert strategies[0]["version"] == 1
    assert strategies[0]["strategy_version_id"] != second_version["id"]


def test_list_strategy_versions_returns_all_versions(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90),
    )

    response = client.get(f"/api/strategies/{created['strategy_id']}/versions")

    assert response.status_code == 200
    versions = response.json()
    assert [version["version"] for version in versions] == [1, 2]
    assert [version["strategy_mode"] for version in versions] == ["single_symbol", "single_symbol"]
    assert versions[0]["source_code"]
    assert "strategy_config" not in versions[0]


def test_get_strategy_version_by_id(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]

    response = client.get(f"/api/strategy-versions/{version['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == version["id"]
    assert response.json()["strategy_id"] == created["strategy_id"]


def test_create_strategy_version_rejects_deleted_strategy(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    client.delete(f"/api/strategies/{created['strategy_id']}")

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90),
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error_code"] == "STRATEGY_DELETED"


def test_deleted_strategy_is_hidden_from_list(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.delete(f"/api/strategies/{created['strategy_id']}")

    assert response.status_code == 200
    assert client.get("/api/strategies?project_id=project_test").json() == []


def strategy_create_payload(
    *,
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
    strategy_mode: str = "single_symbol",
) -> dict[str, object]:
    return {
        "project_id": "project_test",
        "name": "均线突破策略",
        "description": "短期均线上穿长期均线买入，下穿卖出",
        "source_code": "\n".join(
            [
                "import backtrader as bt",
                "",
                "class GeneratedStrategy(bt.Strategy):",
                "    @classmethod",
                "    def chatq_params(cls):",
                "        return [",
                chatq_param_source("fast_period", "integer", fast_period, "短期均线周期"),
                chatq_param_source("slow_period", "integer", slow_period, "长期均线周期"),
                chatq_param_source(
                    "volatility_filter",
                    "string",
                    volatility_filter,
                    "波动过滤",
                ),
                "        ]",
                "",
                "    def __init__(self):",
                "        close = self.datas[0].close",
                "        self.fast_ma = bt.ind.SMA(close, period=self.p.fast_period)",
                "        self.slow_ma = bt.ind.SMA(close, period=self.p.slow_period)",
                "",
                "    def next(self):",
                "        if not self.position and self.fast_ma[0] > self.slow_ma[0]:",
                "            self.order_target_percent(target=0.95)",
                "        elif self.position and self.fast_ma[0] < self.slow_ma[0]:",
                "            self.order_target_percent(target=0)",
            ]
        ),
        "strategy_mode": strategy_mode,
        "risk_notes": ["历史回测不代表未来收益，不构成投资建议"],
    }


def strategy_version_payload(
    *,
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
    strategy_mode: str = "single_symbol",
) -> dict[str, object]:
    payload = strategy_create_payload(
        fast_period=fast_period,
        slow_period=slow_period,
        volatility_filter=volatility_filter,
        strategy_mode=strategy_mode,
    )
    payload.pop("name")
    payload.pop("description")
    payload.pop("project_id")
    return payload


def chatq_param_source(
    name: str,
    param_type: str,
    default: object,
    label: str,
) -> str:
    return (
        "            "
        f'{{"name": {name!r}, "type": {param_type!r}, '
        f'"default": {default!r}, "label": {label!r}}},'
    )
