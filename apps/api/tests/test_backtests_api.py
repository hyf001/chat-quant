from decimal import Decimal

from app.domain.backtests.service import backtest_service
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def setup_function() -> None:
    backtest_service.reset()


def create_payload() -> dict[str, object]:
    return {
        "chat_session_id": "conv_demo",
        "strategy_version_id": "stv_ma_cross_v1",
        "symbols": ["000300.SH"],
        "market": "CN",
        "benchmark_symbol": "000300.SH",
        "start_date": "2024-01-01",
        "end_date": "2024-04-30",
        "initial_cash": "100000",
        "commission": "0.001",
        "slippage": "0.0002",
        "params": {"fast_period": 20, "slow_period": 60},
    }


def test_create_backtest_run_returns_pending_run_with_config_hash() -> None:
    response = client.post("/api/backtests", json=create_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("bt_")
    assert data["status"] == "pending"
    assert data["config_hash"].startswith("sha256:")
    assert data["config"]["symbols"] == ["000300.SH"]


def test_run_backtest_persists_result_trades_and_curves() -> None:
    created = client.post("/api/backtests", json=create_payload()).json()

    response = client.post(f"/api/backtests/{created['id']}/run", json={"mode": "sync"})

    assert response.status_code == 200
    data = response.json()
    assert data["run"]["status"] == "succeeded"
    assert data["result"]["metrics"]["annual_return_pct"] is not None
    assert Decimal(data["result"]["metrics"]["max_drawdown_pct"]) <= 0
    assert len(data["trades"]) > 0
    assert {curve["curve_type"] for curve in data["curves"]} == {"equity", "drawdown"}


def test_rerun_with_override_creates_child_and_compare_returns_metrics_table() -> None:
    created = client.post("/api/backtests", json=create_payload()).json()
    first = client.post(f"/api/backtests/{created['id']}/run", json={"mode": "sync"}).json()

    rerun_response = client.post(
        f"/api/backtests/{created['id']}/rerun",
        json={
            "run_immediately": True,
            "override_config": {"initial_cash": "200000", "params": {"fast_period": 25}},
        },
    )

    assert rerun_response.status_code == 201
    second = rerun_response.json()
    assert second["run"]["parent_backtest_run_id"] == created["id"]
    assert second["run"]["config"]["initial_cash"] == "200000"
    assert second["run"]["status"] == "succeeded"

    compare_response = client.post(
        "/api/backtests/compare",
        json={
            "base_backtest_run_id": first["run"]["id"],
            "backtest_run_ids": [first["run"]["id"], second["run"]["id"]],
        },
    )

    assert compare_response.status_code == 200
    comparison = compare_response.json()
    assert len(comparison["metrics_table"]) == 2
    assert len(comparison["equity_series"]) == 2
    assert comparison["differences"]


def test_create_rejects_invalid_strategy_params() -> None:
    payload = create_payload()
    payload["params"] = {"fast_period": 60, "slow_period": 20}

    response = client.post("/api/backtests", json=payload)

    assert response.status_code == 422
    assert "fast_period" in response.json()["detail"]


def test_list_strategy_backtests_uses_documented_route() -> None:
    created = client.post("/api/backtests", json=create_payload()).json()

    response = client.get("/api/strategy-versions/stv_ma_cross_v1/backtests")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [created["id"]]
