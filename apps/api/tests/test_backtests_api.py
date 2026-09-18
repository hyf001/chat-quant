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
    signal_response = client.post(
        "/api/datasets",
        json={
            "id": "ds_chatq_signal_index",
            "name": "chatq_signal_index_prices",
            "description": "策略可读指数信号测试数据",
            "category_path": ["CN", "指数", "日频", "策略信号"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW chatq_signal_index_prices AS "
                "SELECT * FROM (VALUES "
                f"{_price_values_sql('399006.SZ', close_start=100.0)}"
                ") AS t(symbol, date, open, high, low, close, volume)"
            ),
        },
    )
    assert signal_response.status_code == 201
    config_response = client.put(
        "/api/config",
        json={
            "settings": {
                "market_data": {
                    "market_data_dataset": {
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
    assert response.status_code == 201, response.json()
    return response.json()


def create_backtest_payload() -> dict[str, object]:
    return {
        "project_id": "project_test",
        "config": {
            "strategy_mode": "single_symbol",
            "asset_class": "stock",
            "symbols": ["600519.SH"],
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


def test_backtest_config_defaults_to_sse50_and_past_year() -> None:
    today = date.today()
    config = StrategyBacktestConfig()

    assert config.benchmark_symbol == "000016.SH"
    assert config.commission == Decimal("0.0005")
    assert today <= config.end_date <= date.today()
    assert config.start_date == _one_year_before(config.end_date)


def test_strategy_backtest_protocol_is_documented(client: TestClient) -> None:
    response = client.get("/api/strategy-backtest/protocol")

    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["name"] == "chatq_signal_strategy_v1"
    assert data["base_class"] is None
    assert "chatq_params/chatq_init/chatq_next" in data["source_format"]


@pytest.mark.parametrize("execution_mode", [None, "next_open", "current_close"])
def test_backtest_market_order_execution_mode(
    client: TestClient, execution_mode: str | None,
) -> None:
    strategy_payload = strategy_create_payload()
    expected_mode = execution_mode or "next_open"
    strategy_payload["source_code"] = "\n".join([
        "def chatq_params(): return []",
        "def chatq_init(context):",
        f"    assert context['execution_mode'] == {expected_mode!r}",
        "    return {}",
        "def chatq_next(context, state):",
        f"    assert context['execution_mode'] == {expected_mode!r}",
        "    if state.get('submitted'): return {'actions': [], 'state': state}",
        "    return {'actions': [{'action': 'buy', 'symbol': context['symbols'][0],",
        "                         'size': 10}], 'state': {'submitted': True}}",
    ])
    created = client.post("/api/strategies", json=strategy_payload)
    assert created.status_code == 201, created.json()
    payload = create_backtest_payload()
    payload["config"].update({"params": {}, "slippage": "0"})
    if execution_mode is not None:
        payload["config"]["execution_mode"] = execution_mode
    response = client.post(
        f"/api/strategies/{created.json()['strategy_id']}/backtest", json=payload,
    )
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["backtest"]["status"] == "succeeded", data
    trades = data["result"]["trades"]
    assert len(trades) == 1
    candles = data["result"]["market_data"][0]["candles"]
    candle = candles[0 if execution_mode == "current_close" else 1]
    assert trades[0]["trade_datetime"][:10] == candle["date"]
    price_field = "close" if execution_mode == "current_close" else "open"
    assert float(trades[0]["price"]) == pytest.approx(float(candle[price_field]))
    detail = client.get(f"/api/backtests/{data['backtest']['id']}").json()
    assert detail["backtest"]["config"]["execution_mode"] == (execution_mode or "next_open")


def test_backtest_rejects_unsupported_execution_mode(client: TestClient) -> None:
    created = create_strategy(client)
    payload = create_backtest_payload()
    payload["config"]["execution_mode"] = "invalid"
    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest", json=payload,
    )
    assert response.status_code == 422


def test_backtest_strategy_returns_backtest_result(client: TestClient, caplog) -> None:
    created = create_strategy(client)
    caplog.set_level(logging.INFO, logger="app.service.backtest.service")

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    )

    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["backtest"]["status"] == "succeeded"
    assert data["backtest"]["id"].startswith("sbt_")
    assert data["backtest"]["execution_engine"] == "backtrader"
    assert data["backtest"]["config"]["strategy_mode"] == "single_symbol"
    assert data["backtest"]["config"]["symbols"] == ["600519.SH"]
    assert data["result"]["protocol"] == "chatq_signal_strategy_v1"
    assert data["result"]["engine"] == "backtrader"
    assert data["result"]["data_source"]["mode"] == "dataset"
    assert (
        data["result"]["data_source"]["market_data_dataset"]["dataset_id"]
        == "ds_backtest_market"
    )
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


def test_backtest_strategy_can_query_exposed_dataset_with_chatq_sql(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/strategies",
        json={
            **strategy_create_payload(),
            "name": "外部指数信号策略",
            "source_code": "\n".join(
                [
                    "from app.service.strategy.protocol import "
                    "ChatQBarContext, ChatQInitContext, ChatQNextResult, ChatQState",
                    "",
                    "def chatq_init(context: ChatQInitContext) -> ChatQState:",
                    "    frame = context['chatq'].sql(",
                    '        "SELECT date, close FROM chatq_signal_index_prices "',
                    "        \"WHERE symbol = '399006.SZ' ORDER BY date\"",
                    "    )",
                    "    signal_dates = {",
                    "        value.date().isoformat() if hasattr(value, 'date')",
                    "        else value.isoformat() if hasattr(value, 'isoformat')",
                    "        else str(value)",
                    "        for value in frame.loc[frame['close'] > 100.5, 'date']",
                    "    }",
                    "    return {'signal_dates': sorted(signal_dates)}",
                    "",
                    "def chatq_next("
                    "context: ChatQBarContext, state: ChatQState"
                    ") -> ChatQNextResult:",
                    "    symbol = context['symbols'][0]",
                    "    today = context['datetime'][:10]",
                    "    position = context['positions'].get(symbol, {'size': 0})",
                    "    if position['size'] == 0 and today in state['signal_dates']:",
                    "        return {'actions': ["
                    "{'action': 'buy', 'symbol': symbol, 'size': 10}"
                    "], 'state': state}",
                    "    if position['size'] > 0 and today not in state['signal_dates']:",
                    "        return {'actions': ["
                    "{'action': 'close', 'symbol': symbol}"
                    "], 'state': state}",
                    "    return {'actions': [], 'state': state}",
                ]
            ),
        },
    )
    assert response.status_code == 201, response.json()
    created = response.json()

    backtest_payload = create_backtest_payload()
    backtest_payload["config"]["params"] = {}
    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=backtest_payload,
    )

    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["backtest"]["status"] == "succeeded"
    assert data["result"]["trades"][0]["side"] == "buy"


def test_create_rejects_missing_chatq_protocol(client: TestClient) -> None:
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


def test_rerun_backtest_updates_existing_record(client: TestClient) -> None:
    created = create_strategy(client)
    original = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=create_backtest_payload(),
    ).json()
    backtest_id = original["backtest"]["id"]
    original_result_id = original["result"]["id"]

    payload = create_backtest_payload()
    payload["config"]["initial_cash"] = "200000"
    response = client.patch(
        f"/api/backtests/{backtest_id}/rerun",
        json={"config": payload["config"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["backtest"]["id"] == backtest_id
    assert data["backtest"]["config"]["initial_cash"] == "200000"
    assert data["backtest"]["result_id"] != original_result_id
    assert data["result"]["id"] == data["backtest"]["result_id"]
    records = client.get("/api/backtests").json()
    assert [record["id"] for record in records] == [backtest_id]


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
            
                f"('{symbol}', DATE '{current.isoformat()}', "
                f"{open_price:.6f}, {high:.6f}, {low:.6f}, {close:.6f}, {1000000 + index})"
            
        )
        current = date.fromordinal(current.toordinal() + 1)
    return ", ".join(rows)
