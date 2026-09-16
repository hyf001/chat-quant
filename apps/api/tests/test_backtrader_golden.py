"""Golden baseline for the shared backtrader host.

冻结 ``metrics`` / ``trades`` / ``curves`` / ``candles`` / ``daily_positions`` 的数字快照，
用于保证抽取共享宿主（``service/chatq_engine``）后回测行为零漂移。

设置 ``GOLDEN_DUMP=1`` 可以把当前快照打印出来做对比（重构前 / 重构后）。
"""

from __future__ import annotations

import json
import os
from datetime import date

import pytest
from fastapi.testclient import TestClient
from tests.test_strategy_api import strategy_create_payload

pytestmark = pytest.mark.usefixtures("project_test")

GOLDEN: dict[str, object] = {
    "backtest_engine": "backtrader",
    "backtest_status": "succeeded",
    "benchmark": {
        "last_point": {"date": "2024-04-30", "normalized_value": "15.5934", "value": "4396.9424"},
        "point_count": 121,
        "symbol": "000300.SH",
        "total_return_pct": "15.5934",
    },
    "curve_values": {
        "drawdown": [
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "-0.0002",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
            "0.0000",
        ],
        "equity": [
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "100000.0000",
            "99999.7874",
            "100000.8503",
            "100001.9142",
            "100002.9792",
            "100004.0453",
            "100005.1124",
            "100006.1806",
            "100007.2499",
            "100008.3202",
            "100009.3916",
            "100010.4641",
            "100012.0744",
            "100013.6871",
            "100015.3022",
            "100016.9198",
            "100018.5398",
            "100020.1622",
            "100021.7871",
            "100023.4144",
            "100025.0441",
            "100026.6763",
            "100028.3110",
            "100029.9481",
            "100031.5876",
            "100033.2296",
            "100034.8741",
            "100036.5210",
            "100038.1704",
            "100039.8223",
            "100041.4766",
            "100043.1334",
            "100044.7928",
            "100046.4546",
            "100048.1189",
            "100049.7857",
            "100051.4550",
            "100053.1268",
            "100054.8011",
            "100056.4779",
            "100058.1572",
            "100059.8391",
            "100061.5235",
            "100063.2104",
            "100064.8998",
            "100066.5918",
            "100068.2863",
            "100069.9833",
            "100071.6829",
            "100073.3851",
            "100075.0898",
            "100076.7970",
            "100078.5068",
            "100080.2192",
            "100081.9342",
            "100083.6517",
            "100085.3718",
            "100087.0944",
            "100088.8197",
            "100090.5476",
            "100092.2780",
            "100094.0110",
        ],
    },
    "daily_positions": {
        "count": 121,
        "first": {
            "cash": "100000.0000",
            "daily_pnl": "0.0000",
            "date": "2024-01-01",
            "positions": [],
            "total_value": "100000.0000",
        },
        "last": {
            "cash": "98936.9209",
            "daily_pnl": "1.7330",
            "date": "2024-04-30",
            "positions": [
                {
                    "close_price": "115.7090",
                    "market_value": "1157.0901",
                    "size": "10.000000",
                    "symbol": "600519.SH",
                    "unrealized_pnl": "95.0730",
                }
            ],
            "total_value": "100094.0110",
        },
    },
    "data_source": {
        "benchmark_dataset": {
            "dataset_id": "ds_backtest_benchmark",
            "dataset_name": "backtest_benchmark_prices",
            "field_mapping": {"close": "close", "datetime": "date", "symbol": "symbol"},
        },
        "market_data_dataset": {
            "dataset_id": "ds_backtest_market",
            "dataset_name": "backtest_market_prices",
            "field_mapping": {
                "close": "close",
                "datetime": "date",
                "high": "high",
                "low": "low",
                "open": "open",
                "symbol": "symbol",
                "volume": "volume",
            },
        },
        "mode": "dataset",
        "symbols": ["600519.SH"],
    },
    "market_data": [
        {
            "candle_count": 121,
            "first_candle": {
                "close": "100.1000",
                "date": "2024-01-01",
                "high": "101.1010",
                "low": "99.0000",
                "open": "100.0000",
                "symbol": "600519.SH",
                "volume": "1000000.000000",
            },
            "last_candle": {
                "close": "115.7090",
                "date": "2024-04-30",
                "high": "116.8661",
                "low": "114.3804",
                "open": "115.5357",
                "symbol": "600519.SH",
                "volume": "1000120.000000",
            },
            "symbol": "600519.SH",
        }
    ],
    "metrics": {
        "annual_return_pct": "0.2862",
        "final_value": "100094.0110",
        "initial_value": "100000.0000",
        "max_drawdown_duration_days": 60,
        "max_drawdown_end": "2024-03-01",
        "max_drawdown_pct": "-0.0002",
        "max_drawdown_start": "2024-01-01",
        "sharpe_ratio": "75.9935",
        "total_return_pct": "0.0940",
        "total_trades": 0,
        "win_rate_pct": None,
    },
    "summary": "策略回测完成：总收益 0.0940%，最大回撤 -0.0002%，交易 0 笔。",
    "trades": [
        {
            "commission": "1.0620",
            "metadata": {"basis": "backtrader_order_execution"},
            "pnl": None,
            "pnl_pct": None,
            "price": "106.2017",
            "side": "buy",
            "size": "10.000000",
            "status": "opened",
            "symbol": "600519.SH",
            "trade_datetime": "2024-03-01T00:00:00",
            "value": "1062.0171",
        }
    ],
    "warnings": [],
}


@pytest.fixture(autouse=True)
def configured_backtest_datasets(client: TestClient, project_test: None) -> None:
    market_values = _price_values_sql("600519.SH", close_start=100.0)
    benchmark_values = _price_values_sql("000300.SH", close_start=3800.0)
    response = client.post(
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
    assert response.status_code == 201, response.json()
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
    assert benchmark_response.status_code == 201, benchmark_response.json()
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
    assert config_response.status_code == 200, config_response.json()


def test_backtest_engine_matches_golden_snapshot(client: TestClient) -> None:
    created = client.post("/api/strategies", json=strategy_create_payload()).json()
    response = client.post(
        f"/api/strategies/{created['strategy_id']}/backtest",
        json=_backtest_payload(),
    )

    assert response.status_code == 200, response.json()
    snapshot = _snapshot(response.json())

    if os.environ.get("GOLDEN_DUMP"):
        print("GOLDEN_DUMP_BEGIN")
        print(json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2))
        print("GOLDEN_DUMP_END")
        return

    assert GOLDEN, "golden snapshot is empty; run with GOLDEN_DUMP=1 to regenerate"
    assert snapshot == GOLDEN


def _snapshot(payload: dict[str, object]) -> dict[str, object]:
    result = payload["result"]
    backtest = payload["backtest"]
    curves = {
        curve["curve_type"]: [point["value"] for point in curve["points"]]
        for curve in result["curves"]
    }
    market_data = result["market_data"]
    daily_positions = result["daily_positions"]
    benchmark = result["benchmark"]
    return {
        "backtest_status": backtest["status"],
        "backtest_engine": backtest["execution_engine"],
        "summary": result["summary"],
        "metrics": result["metrics"],
        "trades": [
            {key: value for key, value in trade.items() if key not in _VOLATILE_TRADE_KEYS}
            for trade in result["trades"]
        ],
        "curve_values": curves,
        "market_data": [
            {
                "symbol": series["symbol"],
                "candle_count": len(series["candles"]),
                "first_candle": series["candles"][0],
                "last_candle": series["candles"][-1],
            }
            for series in market_data
        ],
        "daily_positions": {
            "count": len(daily_positions),
            "first": daily_positions[0],
            "last": daily_positions[-1],
        },
        "benchmark": None
        if benchmark is None
        else {
            "symbol": benchmark["symbol"],
            "total_return_pct": benchmark["total_return_pct"],
            "point_count": len(benchmark["points"]),
            "last_point": benchmark["points"][-1],
        },
        "warnings": result["warnings"],
        "data_source": result["data_source"],
    }


_VOLATILE_TRADE_KEYS = {"id", "strategy_backtest_id"}


def _backtest_payload() -> dict[str, object]:
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
