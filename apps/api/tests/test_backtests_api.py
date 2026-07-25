from decimal import Decimal

from fastapi.testclient import TestClient
from tests.test_strategy_api import strategy_package


def create_strategy(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    )
    assert response.status_code == 201
    return response.json()


def create_backtest_payload() -> dict[str, object]:
    return {
        "chat_session_id": "conv_demo",
        "config": {
            "symbols": ["000300.SH"],
            "market": "CN",
            "benchmark_symbol": "000300.SH",
            "start_date": "2024-01-01",
            "end_date": "2024-04-30",
            "initial_cash": "100000",
            "commission": "0.001",
            "slippage": "0.0002",
            "params": {"fast_period": 20, "slow_period": 60, "volatility_filter": "medium"},
        },
    }


def test_strategy_backtest_protocol_is_documented(client: TestClient) -> None:
    response = client.get("/api/strategy-backtest/protocol")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "chatq_backtrader_strategy_v1"
    assert data["base_class"] == "backtrader.Strategy"
    assert data["entrypoint_format"] == "<relative_python_file.py>:<StrategyClassName>"


def test_backtest_strategy_returns_backtest_result(client: TestClient) -> None:
    created = create_strategy(client)

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["backtest"]["status"] == "succeeded"
    assert data["backtest"]["id"].startswith("sbt_")
    assert data["backtest"]["execution_engine"] == "backtrader"
    assert data["backtest"]["config_hash"].startswith("sha256:")
    assert data["backtest"]["config"]["symbols"] == ["000300.SH"]
    assert data["result"]["protocol"] == "chatq_backtrader_strategy_v1"
    assert data["result"]["engine"] == "backtrader"
    assert Decimal(data["result"]["metrics"]["final_value"]) > Decimal("0")
    assert data["result"]["metrics"]["annual_return_pct"] is not None
    assert {curve["curve_type"] for curve in data["result"]["curves"]} == {
        "equity",
        "drawdown",
    }

    detail = client.get(f"/api/backtests/{data['backtest']['id']}").json()
    assert detail["result"]["id"] == data["result"]["id"]


def test_execute_rejects_non_backtrader_strategy(client: TestClient) -> None:
    package = strategy_package()
    package["code_files"] = [
        {"path": "strategy.py", "content": "class GeneratedStrategy:\n    pass\n"}
    ]
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": package},
    ).json()
    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["backtest"]["status"] == "failed"
    assert data["backtest"]["failure_code"] == "STRATEGY_PROTOCOL_INVALID"


def test_list_backtest_records(client: TestClient) -> None:
    created = create_strategy(client)
    backtest = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    ).json()["backtest"]

    response = client.get("/api/backtests")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [backtest["id"]]
