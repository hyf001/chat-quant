from datetime import date
from decimal import Decimal

import pandas as pd
import pytest
from app.core.logging import clear_log_entries
from app.schema.backtest import StrategyBacktestConfig
from fastapi.testclient import TestClient
from tests.test_strategy_api import strategy_create_payload, strategy_version_payload

pytestmark = pytest.mark.usefixtures("project_test")


@pytest.fixture(autouse=True)
def fake_akshare_market_data(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.service.backtest import backtrader

    def fake_fetch_akshare_history(**_: object) -> pd.DataFrame:
        dates = pd.date_range("2024-01-01", "2024-04-30", freq="D")
        rows = []
        close = 100.0
        for index, current_date in enumerate(dates):
            open_price = close
            close = close * (1.001 + (0.0005 if index > 70 else 0))
            rows.append(
                {
                    "日期": current_date.date().isoformat(),
                    "开盘": open_price,
                    "收盘": close,
                    "最高": max(open_price, close) * 1.01,
                    "最低": min(open_price, close) * 0.99,
                    "成交量": 1000000 + index,
                }
            )
        return pd.DataFrame(rows)

    monkeypatch.setattr(backtrader, "_fetch_akshare_history", fake_fetch_akshare_history)


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


def test_backtest_strategy_returns_backtest_result(client: TestClient) -> None:
    created = create_strategy(client)
    clear_log_entries()

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
    assert data["result"]["data_source"]["mode"] == "akshare_ohlcv"
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
    logs = client.get("/api/logs?category=business&limit=20").json()["items"]
    assert [
        item["message"]
        for item in logs
        if item["logger"] == "app.service.backtest.service"
        and item["backtest_id"] == data["backtest"]["id"]
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
