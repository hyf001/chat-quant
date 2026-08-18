import logging
from datetime import date
from decimal import Decimal

import pytest
from app.schema.backtest import StrategyBacktestConfig
from fastapi.testclient import TestClient
from tests.test_strategy_api import strategy_create_payload, strategy_version_payload

pytestmark = pytest.mark.usefixtures("project_test")


@pytest.fixture(autouse=True)
def configured_backtest_datasets(client: TestClient, project_test: None) -> None:
    market_values = _price_values_sql("600519.SH", close_start=100.0)
    benchmark_values = _price_values_sql("000300.SH", close_start=3800.0)
    market_response = client.post(
        "/api/datasets",
        json={
            "id": "ds_backtest_market",
            "name": "backtest_market_prices",
            "description": "回测行情测试数据",
            "category_path": ["CN", "股票", "日频", "回测行情"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW backtest_market_prices AS "
                "SELECT * FROM (VALUES "
                f"{market_values}"
                ") AS t(symbol, date, open, high, low, close, volume)"
            ),
        },
    )
    assert market_response.status_code == 201
    benchmark_response = client.post(
        "/api/datasets",
        json={
            "id": "ds_backtest_benchmark",
            "name": "backtest_benchmark_prices",
            "description": "回测基准测试数据",
            "category_path": ["CN", "指数", "日频", "回测基准"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW backtest_benchmark_prices AS "
                "SELECT * FROM (VALUES "
                f"{benchmark_values}"
                ") AS t(symbol, date, open, high, low, close, volume)"
            ),
        },
    )
    assert benchmark_response.status_code == 201
    config_response = client.put(
        "/api/config",
        json={
            "settings": {
                "backtest": {
                    "market_dataset": {
                        "dataset_id": "ds_backtest_market",
                        "symbol_field": "symbol",
                        "datetime_field": "date",
                        "open_field": "open",
                        "high_field": "high",
                        "low_field": "low",
                        "close_field": "close",
                        "volume_field": "volume",
                    },
                    "benchmark_dataset": {
                        "dataset_id": "ds_backtest_benchmark",
                        "symbol_field": "symbol",
                        "datetime_field": "date",
                        "close_field": "close",
                    },
                }
            }
        },
    )
    assert config_response.status_code == 200


def create_strategy(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    )
    assert response.status_code == 201
    return response.json()


def create_backtest_payload() -> dict[str, object]:
    return {
        "project_id": "project_test",
        "config": {
            "strategy_mode": "single_symbol",
            "asset_class": "stock",
            "symbols": ["600519.SH"],
            "market": "CN",
            "symbol_source": "manual",
            "benchmark_symbol": "000300.SH",
            "start_date": "2024-01-01",
            "end_date": "2024-04-30",
            "initial_cash": "100000",
            "commission": "0.001",
            "slippage": "0.0002",
            "rebalance_frequency": "none",
            "position_sizing": "fixed_percent",
            "allow_short": False,
            "risk_control_enabled": False,
            "params": {"fast_period": 20, "slow_period": 60, "volatility_filter": "medium"},
        },
    }


def test_backtest_config_defaults_to_sse50_and_past_year() -> None:
    today = date.today()
    config = StrategyBacktestConfig()

    assert config.benchmark_symbol == "000016.SH"
    assert today <= config.end_date <= date.today()
    assert config.start_date == _one_year_before(config.end_date)


def test_strategy_backtest_protocol_is_documented(client: TestClient) -> None:
    response = client.get("/api/strategy-backtest/protocol")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "chatq_backtrader_strategy_v2"
    assert data["base_class"] == "backtrader.Strategy"
    assert data["source_format"] == (
        "A single Python source string defining one backtrader.Strategy subclass"
    )


def test_backtest_strategy_returns_backtest_result(client: TestClient, caplog) -> None:
    created = create_strategy(client)
    caplog.set_level(logging.INFO, logger="app.service.backtest.service")

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["backtest"]["status"] == "succeeded"
    assert data["backtest"]["id"].startswith("sbt_")
    assert data["backtest"]["execution_engine"] == "backtrader"
    assert data["backtest"]["config"]["strategy_mode"] == "single_symbol"
    assert data["backtest"]["config"]["symbols"] == ["600519.SH"]
    assert data["result"]["protocol"] == "chatq_backtrader_strategy_v2"
    assert data["result"]["engine"] == "backtrader"
    assert data["result"]["data_source"]["mode"] == "dataset"
    assert data["result"]["data_source"]["market_dataset"]["dataset_id"] == "ds_backtest_market"
    assert data["result"]["market_data"][0]["symbol"] == "600519.SH"
    assert data["result"]["market_data"][0]["candles"][0]["open"]
    assert data["result"]["trades"][0]["side"] in {"buy", "sell"}
    assert data["result"]["benchmark"]["symbol"] == "000300.SH"
    assert data["result"]["benchmark"]["points"][0]["normalized_value"] == "0.0000"
    assert data["result"]["daily_positions"][0]["cash"]
    assert data["result"]["daily_positions"][0]["total_value"]
    assert "positions" in data["result"]["daily_positions"][0]
    assert Decimal(data["result"]["metrics"]["final_value"]) > Decimal("0")
    assert data["result"]["metrics"]["annual_return_pct"] is not None
    assert {curve["curve_type"] for curve in data["result"]["curves"]} == {
        "equity",
        "drawdown",
    }

    detail = client.get(f"/api/backtests/{data['backtest']['id']}").json()
    assert detail["result"]["id"] == data["result"]["id"]
    assert [
        record.message
        for record in caplog.records
        if record.name == "app.service.backtest.service"
        and record.backtest_id == data["backtest"]["id"]
    ] == [
        "strategy backtest created",
        "strategy backtest started",
        "strategy backtest succeeded",
    ]


def test_create_rejects_non_backtrader_strategy(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = "class GeneratedStrategy:\n    pass\n"

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_PROTOCOL_INVALID"


def test_backtest_can_target_specific_strategy_version(client: TestClient) -> None:
    created = create_strategy(client)
    versions = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()
    client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90),
    )

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json={
            **create_backtest_payload(),
            "strategy_version_id": versions[0]["id"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["backtest"]["strategy_version_id"] == versions[0]["id"]


def test_backtest_rejects_strategy_mode_mismatch(client: TestClient) -> None:
    response = client.post(
        "/api/strategies",
        json=strategy_create_payload(strategy_mode="multi_symbol"),
    )
    assert response.status_code == 201
    created = response.json()

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_MODE_MISMATCH"


def test_list_backtest_records(client: TestClient) -> None:
    created = create_strategy(client)
    backtest = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    ).json()["backtest"]

    response = client.get("/api/backtests")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [backtest["id"]]


def _one_year_before(value: date) -> date:
    try:
        return value.replace(year=value.year - 1)
    except ValueError:
        return value.replace(year=value.year - 1, day=28)


def _price_values_sql(symbol: str, *, close_start: float) -> str:
    close = close_start
    rows: list[str] = []
    current = date(2024, 1, 1)
    for index in range(121):
        open_price = close
        close = close * (1.001 + (0.0005 if index > 70 else 0))
        high = max(open_price, close) * 1.01
        low = min(open_price, close) * 0.99
        rows.append(
            (
                f"('{symbol}', DATE '{current.isoformat()}', "
                f"{open_price:.6f}, {high:.6f}, {low:.6f}, {close:.6f}, {1000000 + index})"
            )
        )
        current = date.fromordinal(current.toordinal() + 1)
    return ", ".join(rows)
