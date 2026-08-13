from __future__ import annotations

from datetime import date

import pandas as pd
from app.schema.mindgo import MindgoDatasetSyncResult
from app.service.mindgo import service as mindgo_service
from app.service.mindgo.stock_a_daily_price import stock_a_daily_price_schema
from fastapi.testclient import TestClient


def test_mindgo_api_lists_first_dataset(client: TestClient) -> None:
    response = client.get("/api/mindgo/datasets")

    assert response.status_code == 200
    payload = response.json()
    assert payload["datasets"][0]["id"] == "stock_a_daily_price"
    assert payload["datasets"][0]["actions"] == ["get_schema", "query", "sync"]


def test_mindgo_api_returns_stock_daily_schema(client: TestClient) -> None:
    response = client.get("/api/mindgo/datasets/stock_a_daily_price/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "A股历史行情数据(日)"
    assert payload["category_path"] == ["股票", "A股", "行情数据(A股)"]
    assert payload["result_schema"][0]["name"] == "symbol"


def test_mindgo_query_uses_default_connection(
    client: TestClient,
    monkeypatch,
) -> None:
    class FakeAdapter:
        dataset_id = "stock_a_daily_price"

        async def get_schema(self):
            return stock_a_daily_price_schema()

        async def query(self, request):
            return pd.DataFrame(
                [{"symbol": "000001.SZ", "trade_date": "20260813", "close": 10.0}]
            )

        async def sync(self, request):
            raise AssertionError("sync should not run")

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_dataset",
        lambda dataset_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/datasets/stock_a_daily_price/query",
        json={
            "params": {
                "start_date": "2026-08-13",
                "end_date": "2026-08-13",
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
        dataset_id = "stock_a_daily_price"

        async def get_schema(self):
            return stock_a_daily_price_schema()

        async def query(self, request):
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
        "_adapter_for_dataset",
        lambda dataset_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/datasets/stock_a_daily_price/query",
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
    class FakeAdapter:
        dataset_id = "stock_a_daily_price"

        async def get_schema(self):
            raise AssertionError("schema should not run")

        async def query(self, request):
            raise AssertionError("query should not run")

        async def sync(self, request):
            assert request.start_date == date(2026, 8, 13)
            assert request.end_date == date(2026, 8, 13)
            return MindgoDatasetSyncResult(status="success", elapsed_ms=21, synced_count=2)

    monkeypatch.setattr(
        mindgo_service,
        "_adapter_for_dataset",
        lambda dataset_id, allow_missing_runner=False: FakeAdapter(),
    )

    response = client.post(
        "/api/mindgo/datasets/stock_a_daily_price/sync",
        json={
            "start_date": "2026-08-13",
            "end_date": "2026-08-13",
            "params": {"fields": ["close"]},
        },
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success", "elapsed_ms": 21, "synced_count": 2}
