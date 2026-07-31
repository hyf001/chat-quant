from fastapi.testclient import TestClient


def test_create_strategy_returns_draft_first_version(client: TestClient) -> None:
    response = client.post(
        "/api/strategies",
        json={
            "package": strategy_package(),
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["strategy_id"].startswith("str_")
    assert data["entrypoint"] == "strategy.py:GeneratedStrategy"


def test_create_strategy_rejects_default_param_outside_schema(client: TestClient) -> None:
    package = strategy_package()
    package["default_params"]["fast_period"] = 1

    response = client.post(
        "/api/strategies",
        json={"package": package},
    )

    assert response.status_code == 422


def test_update_metadata_does_not_create_new_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"package": strategy_package()},
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


def test_deleted_strategy_is_hidden_from_list(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"package": strategy_package()},
    ).json()

    response = client.delete(f"/api/strategies/{created['strategy_id']}")

    assert response.status_code == 200
    assert client.get("/api/strategies").json() == []


def strategy_package(
    *,
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
) -> dict[str, object]:
    return {
        "name": "均线突破策略",
        "description": "短期均线上穿长期均线买入，下穿卖出",
        "entrypoint": "strategy.py:GeneratedStrategy",
        "python_file": {
            "path": "strategy.py",
            "content": "\n".join(
                [
                    "import backtrader as bt",
                    "",
                    "class GeneratedStrategy(bt.Strategy):",
                    "    params = (",
                    "        ('fast_period', 20),",
                    "        ('slow_period', 60),",
                    "        ('volatility_filter', 'medium'),",
                    "    )",
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
        },
        "params_schema": {
            "fast_period": {
                "type": "integer",
                "title": "短期均线周期",
                "default": fast_period,
                "minimum": 2,
                "maximum": 250,
                "ui": {"control": "number", "unit": "日"},
            },
            "slow_period": {
                "type": "integer",
                "title": "长期均线周期",
                "default": slow_period,
                "minimum": 5,
                "maximum": 500,
                "ui": {"control": "number", "unit": "日"},
            },
            "volatility_filter": {
                "type": "string",
                "title": "波动过滤",
                "enum": ["off", "medium", "strong"],
                "default": volatility_filter,
                "ui": {"control": "select"},
            },
        },
        "default_params": {
            "fast_period": fast_period,
            "slow_period": slow_period,
            "volatility_filter": volatility_filter,
        },
        "risk_notes": ["历史回测不代表未来收益，不构成投资建议"],
    }
