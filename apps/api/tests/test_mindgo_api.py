from __future__ import annotations

import pandas as pd
from app.service.datasource.mindgo import service as mindgo_service
from app.service.datasource.mindgo.index_a_daily_price.adaptor import index_a_daily_price_schema
from app.service.datasource.mindgo.jupyter_runner import _portable_mcp_root
from app.service.datasource.mindgo.stock_a_adjust_factor.adaptor import stock_a_adjust_factor_schema
from app.service.datasource.mindgo.stock_a_daily_price.adaptor import stock_a_daily_price_schema
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.adaptor import (
    stock_a_daily_valuation_metrics_schema,
)
from app.service.datasource.mindgo.stock_a_minute_price.adaptor import (
    stock_a_minute_price_schema,
)
from app.service.datasource.mindgo.stock_a_snapshot_info.adaptor import (
    stock_a_snapshot_info_schema,
)
from fastapi.testclient import TestClient


def test_mindgo_api_lists_first_source(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources")

    assert response.status_code == 200
    payload = response.json()
    assert payload["sources"][0]["id"] == "a_stock_daily_price"
    assert payload["sources"][1]["id"] == "a_stock_daily_adjust_factor"
    assert payload["sources"][2]["id"] == "a_stock_daily_valuation_metrics"
    assert payload["sources"][3]["id"] == "a_index_daily_price"
    assert payload["sources"][4]["id"] == "a_stock_snapshot_info"
    assert payload["sources"][5]["id"] == "a_stock_minute_price"
    assert payload["sources"][0]["category_path_en"] == [
        "a",
        "stock",
        "daily",
        "price",
    ]
    assert payload["sources"][0]["storage"] == {
        "path": "data/mindgo/parquet/a_stock_daily_price",
        "format": "parquet",
        "partitioned_by": ["trade_day"],
        "min_partition": None,
        "max_partition": None,
        "partition_count": 0,
    }


def test_mindgo_api_returns_stock_daily_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_stock_daily_price/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股股票日行情数据"
    assert payload["name_zh"] == "A股股票日行情数据"
    assert payload["name_en"] == "a_stock_daily_price"
    assert payload["category_path"] == ["A股", "股票", "日", "行情数据"]
    assert payload["category_path_en"] == ["a", "stock", "daily", "price"]
    assert "sync_table_name" not in payload
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_stock_daily_price"
    assert payload["storage"]["format"] == "parquet"
    assert payload["storage"]["partitioned_by"] == ["trade_day"]
    assert payload["storage"]["min_partition"] is None
    assert payload["storage"]["max_partition"] is None
    assert payload["storage"]["partition_count"] == 0
    assert payload["result_schema"][0]["name"] == "symbol"


def test_mindgo_api_returns_stock_adjust_factor_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_stock_daily_adjust_factor/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股股票日复权因子"
    assert payload["name_zh"] == "A股股票日复权因子"
    assert payload["name_en"] == "a_stock_daily_adjust_factor"
    assert payload["category_path"] == ["A股", "股票", "日", "复权因子"]
    assert payload["category_path_en"] == [
        "a",
        "stock",
        "daily",
        "adjust_factor",
    ]
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_stock_daily_adjust_factor"
    assert payload["storage"]["format"] == "parquet"
    assert payload["storage"]["partitioned_by"] == ["trade_day"]
    assert [field["name"] for field in payload["result_schema"]] == [
        "symbol",
        "trade_date",
        "name",
        "factor",
    ]


def test_mindgo_api_returns_index_daily_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_index_daily_price/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股指数日行情数据"
    assert payload["name_zh"] == "A股指数日行情数据"
    assert payload["name_en"] == "a_index_daily_price"
    assert payload["category_path"] == ["A股", "指数", "日", "行情数据"]
    assert payload["category_path_en"] == ["a", "index", "daily", "price"]
    assert payload["mindgo_function"] == "get_price"
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_index_daily_price"
    assert payload["storage"]["format"] == "parquet"
    assert payload["storage"]["partitioned_by"] == ["trade_day"]
    assert [field["name"] for field in payload["result_schema"]] == [
        "symbol",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    securities_param = next(
        param for param in payload["query_params"] if param["name"] == "securities"
    )
    assert securities_param["default"][:3] == ["000300.SH", "000905.SH", "000852.SH"]
    assert securities_param["options"][:3] == [
        {"label": "沪深300 000300.SH", "value": "000300.SH"},
        {"label": "中证500 000905.SH", "value": "000905.SH"},
        {"label": "中证1000 000852.SH", "value": "000852.SH"},
    ]


def test_mindgo_api_returns_stock_valuation_metrics_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_stock_daily_valuation_metrics/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股股票日估值指标"
    assert payload["name_zh"] == "A股股票日估值指标"
    assert payload["name_en"] == "a_stock_daily_valuation_metrics"
    assert payload["category_path"] == ["A股", "股票", "日", "估值指标"]
    assert payload["category_path_en"] == ["a", "stock", "daily", "valuation_metrics"]
    assert payload["mindgo_function"] == "get_fundamentals"
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_stock_daily_valuation_metrics"
    assert payload["storage"]["format"] == "parquet"
    assert payload["storage"]["partitioned_by"] == ["trade_day"]
    assert [field["name"] for field in payload["result_schema"][:7]] == [
        "symbol",
        "trade_date",
        "report_date",
        "stat_date",
        "pe_lyr",
        "pe_mrq",
        "pe_ttm",
    ]


def test_mindgo_api_returns_stock_snapshot_info_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_stock_snapshot_info/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股股票信息维表"
    assert payload["name_zh"] == "A股股票信息维表"
    assert payload["name_en"] == "a_stock_snapshot_info"
    assert payload["category_path"] == ["A股", "股票", "快照", "信息维表"]
    assert payload["category_path_en"] == ["a", "stock", "snapshot", "info"]
    assert payload["mindgo_function"] == "query_index"
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_stock_snapshot_info/data.parquet"
    assert payload["storage"]["format"] == "parquet"
    assert payload["storage"]["partitioned_by"] == []
    assert [field["name"] for field in payload["result_schema"]] == ["symbol", "name"]


def test_mindgo_api_returns_stock_minute_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/sources/a_stock_minute_price/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股股票分钟行情数据"
    assert payload["name_en"] == "a_stock_minute_price"
    assert payload["category_path"] == ["A股", "股票", "分钟", "行情数据"]
    assert payload["category_path_en"] == ["a", "stock", "minute", "price"]
    assert payload["mindgo_function"] == "get_price"
    assert payload["storage"]["path"] == "data/mindgo/parquet/a_stock_minute_price"
    assert payload["storage"]["partitioned_by"] == ["trade_day"]
    assert [field["name"] for field in payload["result_schema"][:6]] == [
        "symbol",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
    ]


def test_mindgo_sync_supports_stock_minute_price(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_minute_price"

        async def get_source_schema(self):
            return stock_a_minute_price_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_minute_price/sync",
        json={
            "trigger_start_date": "2023-02-01",
            "trigger_end_date": "2023-02-01",
            "trigger_time": "18:00:00",
            "write_mode": "overwrite",
            "query_window": {"start_offset_days": -1, "end_offset_days": 0},
            "params": {"securities": ["000001.SZ"], "fields": ["close"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["instance"]["job_type"] == "mindgo.a_stock_minute_price.sync"
    assert payload["instance"]["payload"]["start_date"] == "2023-01-31"
    assert payload["instance"]["payload"]["end_date"] == "2023-02-01"
    assert payload["instance"]["payload"]["params"] == {
        "securities": ["000001.SZ"],
        "fields": ["close"],
    }


def test_mindgo_jupyter_runner_finds_bundled_supermind_mcp() -> None:
    assert (_portable_mcp_root() / "supermind_mcp" / "__init__.py").exists()


def test_mindgo_query_uses_default_connection(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_daily_price"

        async def get_source_schema(self):
            return stock_a_daily_price_schema()

        async def query_from_mindgo(self, request):
            return pd.DataFrame(
                [{"symbol": "000001.SZ", "trade_date": "20260813", "close": 10.0}]
            )

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_daily_price/query",
        json={
            "params": {
                "baseDay": "2026-08-13",
            }
        },
    )

    assert response.status_code == 200
    assert response.json()["rows"] == [
        {"symbol": "000001.SZ", "trade_date": "20260813", "close": 10.0}
    ]


def test_mindgo_connection_test_reports_runner_failure(
    client: TestClient,
    monkeypatch,
) -> None:
    class FailingRunner:
        async def run_json(self, code, *, marker_start, marker_end, timeout_seconds=None):
            raise RuntimeError("boom")

    monkeypatch.setattr(
        mindgo_service,
        "_runner_from_connection",
        lambda connection: FailingRunner(),
    )
    client.put(
        "/api/config",
        json={
            "settings": {
                "mindgo": {
                    "jupyter_url": "https://supermind.example/notebook/user/test",
                    "jupyter_token": "token-1",
                }
            }
        },
    )

    response = client.post("/api/mindgo/test", json={})

    assert response.status_code == 200
    assert response.json() == {"ok": False, "message": "连接失败：boom"}


def test_mindgo_connection_test_requires_configured_token(client: TestClient) -> None:
    client.put(
        "/api/config",
        json={
            "settings": {
                "mindgo": {"jupyter_url": "https://supermind.example/notebook/user/test"}
            }
        },
    )

    response = client.post("/api/mindgo/test", json={})

    assert response.status_code == 200
    assert response.json() == {"ok": False, "message": "请填写访问 Token"}


def test_mindgo_connection_test_runs_immediate_probe(
    client: TestClient,
    monkeypatch,
) -> None:
    captured = {}

    class FakeRunner:
        async def run_json(self, code, *, marker_start, marker_end, timeout_seconds=None):
            assert "MINDGO_CONNECTION_TEST_JSON_START" in code
            assert marker_start == "MINDGO_CONNECTION_TEST_JSON_START"
            assert marker_end == "MINDGO_CONNECTION_TEST_JSON_END"
            return {"ok": True}

    monkeypatch.setattr(
        mindgo_service,
        "_runner_from_connection",
        lambda connection: captured.setdefault("connection", connection) and FakeRunner(),
    )
    client.put(
        "/api/config",
        json={
            "settings": {
                "mindgo": {
                    "jupyter_url": "https://supermind.example/notebook/user/test",
                    "jupyter_token": "token-1",
                }
            }
        },
    )

    response = client.post("/api/mindgo/test", json={})

    assert response.status_code == 200
    assert response.json() == {"ok": True, "message": "MindGo Jupyter 连接可用"}
    assert captured["connection"].url == "https://supermind.example/notebook/user/test"
    assert captured["connection"].token == "token-1"


def test_mindgo_query_paginates_dataframe_rows(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_daily_price"

        async def get_source_schema(self):
            return stock_a_daily_price_schema()

        async def query_from_mindgo(self, request):
            return pd.DataFrame(
                [
                    {"symbol": "000001.SZ", "trade_date": "20260813", "close": 10.0},
                    {"symbol": "000002.SZ", "trade_date": "20260813", "close": 11.0},
                    {"symbol": "000003.SZ", "trade_date": "20260813", "close": 12.0},
                ]
            )

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_daily_price/query",
        json={"params": {}, "page": 2, "page_size": 2},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["total_pages"] == 2
    assert payload["rows"] == [
        {"symbol": "000003.SZ", "trade_date": "20260813", "close": 12.0}
    ]


def test_mindgo_sync_runs_immediate_import(
    client: TestClient,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: (_ for _ in ()).throw(
            AssertionError("sync endpoint should only create job instances")
        ),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_daily_price/sync",
        json={
            "trigger_start_date": "2026-08-13",
            "trigger_end_date": "2026-08-15",
            "trigger_time": "10:30:15",
            "write_mode": "skip",
            "params": {"fields": ["close"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["instances"]) == 3
    assert payload["instance"] == payload["instances"][0]
    assert [instance["payload"]["start_date"] for instance in payload["instances"]] == [
        "2026-08-13",
        "2026-08-14",
        "2026-08-15",
    ]
    assert [instance["payload"]["end_date"] for instance in payload["instances"]] == [
        "2026-08-13",
        "2026-08-14",
        "2026-08-15",
    ]
    assert [instance["scheduled_for"][:10] for instance in payload["instances"]] == [
        "2026-08-13",
        "2026-08-14",
        "2026-08-15",
    ]
    assert {instance["scheduled_for"][11:19] for instance in payload["instances"]} == {
        "10:30:15"
    }
    assert {instance["payload"]["write_mode"] for instance in payload["instances"]} == {"skip"}
    assert {instance["trigger_type"] for instance in payload["instances"]} == {"manual"}


def test_mindgo_sync_supports_stock_adjust_factor(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_daily_adjust_factor"

        async def get_source_schema(self):
            return stock_a_adjust_factor_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_daily_adjust_factor/sync",
        json={
            "trigger_start_date": "2026-08-13",
            "trigger_end_date": "2026-08-13",
            "trigger_time": "10:30:15",
            "write_mode": "overwrite",
            "params": {"fields": ["factor"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["instance"]["job_type"] == "mindgo.a_stock_daily_adjust_factor.sync"
    assert payload["instance"]["payload"]["params"] == {"fields": ["factor"]}


def test_mindgo_sync_supports_stock_valuation_metrics(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_daily_valuation_metrics"

        async def get_source_schema(self):
            return stock_a_daily_valuation_metrics_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_daily_valuation_metrics/sync",
        json={
            "trigger_start_date": "2026-08-13",
            "trigger_end_date": "2026-08-13",
            "trigger_time": "10:30:15",
            "write_mode": "overwrite",
            "params": {"fields": ["pe_ttm", "pb_mrq"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["instance"]["job_type"] == "mindgo.a_stock_daily_valuation_metrics.sync"
    assert payload["instance"]["payload"]["params"] == {"fields": ["pe_ttm", "pb_mrq"]}


def test_mindgo_sync_supports_stock_snapshot_info(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_stock_snapshot_info"

        async def get_source_schema(self):
            return stock_a_snapshot_info_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_stock_snapshot_info/sync",
        json={
            "trigger_start_date": "2026-08-13",
            "trigger_end_date": "2026-08-13",
            "trigger_time": "10:30:15",
            "write_mode": "overwrite",
            "params": {},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["instance"]["job_type"] == "mindgo.a_stock_snapshot_info.sync"
    assert payload["instance"]["payload"]["params"] == {}


def test_mindgo_sync_supports_index_daily_price(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_index_daily_price"

        async def get_source_schema(self):
            return index_a_daily_price_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_index_daily_price/sync",
        json={
            "trigger_start_date": "2023-04-03",
            "trigger_end_date": "2023-04-03",
            "trigger_time": "10:30:15",
            "write_mode": "overwrite",
            "params": {"securities": ["000905.SH"], "fields": ["close"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["instance"]["job_type"] == "mindgo.a_index_daily_price.sync"
    assert payload["instance"]["payload"]["params"] == {
        "securities": ["000905.SH"],
        "fields": ["close"],
    }


def test_mindgo_sync_applies_query_window_offsets_to_index_daily_price(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        source_id = "a_index_daily_price"

        async def get_source_schema(self):
            return index_a_daily_price_schema()

        async def query_from_mindgo(self, request):
            raise AssertionError("query_from_mindgo should not run")

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_source",
        lambda source_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/sources/a_index_daily_price/sync",
        json={
            "trigger_start_date": "2023-04-03",
            "trigger_end_date": "2023-04-05",
            "trigger_time": "10:30:15",
            "write_mode": "overwrite",
            "query_window": {"start_offset_days": -2, "end_offset_days": 0},
            "params": {"securities": ["000905.SH"]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["instances"]) == 3
    assert [instance["scheduled_for"][:10] for instance in payload["instances"]] == [
        "2023-04-03",
        "2023-04-04",
        "2023-04-05",
    ]
    assert [instance["payload"]["start_date"] for instance in payload["instances"]] == [
        "2023-04-01",
        "2023-04-02",
        "2023-04-03",
    ]
    assert [instance["payload"]["end_date"] for instance in payload["instances"]] == [
        "2023-04-03",
        "2023-04-04",
        "2023-04-05",
    ]
    assert {
        instance["payload"]["query_window"]["start_offset_days"]
        for instance in payload["instances"]
    } == {-2}
