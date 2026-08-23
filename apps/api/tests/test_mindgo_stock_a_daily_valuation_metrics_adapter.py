from __future__ import annotations

import contextlib
import io
import json
import types
from datetime import date
from typing import Any

import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.adaptor import (
    STOCK_A_VALUATION_METRICS_MARKER_END,
    STOCK_A_VALUATION_METRICS_MARKER_START,
    STOCK_A_VALUATION_METRICS_SOURCE_ID,
    MindgoPartitionedParquetWrite,
    StockAValuationMetricsAdapter,
    normalize_stock_a_daily_valuation_metrics,
    stock_a_daily_valuation_metrics_remote_code,
)


class FakeMindgoRunner:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.calls: list[dict[str, Any]] = []

    async def run_json(
        self,
        code: str,
        *,
        marker_start: str,
        marker_end: str,
        timeout_seconds: float | None = None,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "code": code,
                "marker_start": marker_start,
                "marker_end": marker_end,
                "timeout_seconds": timeout_seconds,
            }
        )
        return self.payload


class FakeMindgoSyncWriter:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def write(
        self,
        write: MindgoPartitionedParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        self.calls.append(
            {
                "source_id": write.source_id,
                "partition_values": dict(write.partition_values),
                "path": write.path,
                "rows": json.loads(frame.to_json(orient="records")),
                "start_date": write.request.start_date,
                "end_date": write.request.end_date,
                "order_by": list(write.options.order_by or []),
            }
        )
        return len(frame)


async def test_stock_a_daily_valuation_metrics_schema_contract() -> None:
    adapter = StockAValuationMetricsAdapter()

    schema = await adapter.get_source_schema()

    assert adapter.source_id == STOCK_A_VALUATION_METRICS_SOURCE_ID
    assert schema.name == "A股股票日估值指标"
    assert schema.name_zh == "A股股票日估值指标"
    assert schema.name_en == "a_stock_daily_valuation_metrics"
    assert schema.category_path == ["A股", "股票", "日", "估值指标"]
    assert schema.category_path_en == ["a", "stock", "daily", "valuation_metrics"]
    assert schema.mindgo_function == "get_fundamentals"
    assert schema.storage.path.endswith("/a_stock_daily_valuation_metrics")
    assert schema.storage.format == "parquet"
    assert schema.storage.partitioned_by == ["trade_day"]
    assert [field.name for field in schema.result_schema[:8]] == [
        "symbol",
        "trade_date",
        "report_date",
        "stat_date",
        "pe_lyr",
        "pe_mrq",
        "pe_ttm",
        "fore_pe_his",
    ]
    assert [field.name for field in schema.result_schema[-4:]] == [
        "total_shares",
        "float_shares",
        "ashare_total_shares",
        "ashare_float_shares",
    ]
    fields_param = next(param for param in schema.query_params if param.name == "fields")
    assert fields_param.options[0].value == "symbol"
    assert fields_param.options[-1].value == "ashare_float_shares"


async def test_a_stock_daily_valuation_metrics_query_from_mindgo_returns_dataframe() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "asharevalue_symbol": "300002.SZ",
                    "asharevalue_date": "2023-02-01",
                    "asharevalue_report_date": "2022-10-25",
                    "asharevalue_stat_date": "2022-09-30",
                    "asharevalue_pe_lyr": 27.1838,
                    "asharevalue_pe_ttm": 18.8137,
                    "asharevalue_pb_mrq": 1.25,
                    "asharevalue_total_mv": 10452620000.0,
                },
                {
                    "symbol": "300013.SZ",
                    "date": 20230201,
                    "pe_lyr": -11.201,
                    "pe_ttm": -13.1445,
                    "pb_mrq": 2.5,
                    "total_mv_ashare": 2121764000.0,
                },
            ]
        }
    )
    adapter = StockAValuationMetricsAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(params={"date": "2023-02-01"})
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame["trade_date"].tolist() == ["20230201", "20230201"]
    assert frame.iloc[0]["symbol"] == "300002.SZ"
    assert frame.iloc[0]["report_date"] == "20221025"
    assert frame.iloc[0]["stat_date"] == "20220930"
    assert frame.iloc[0]["pe_lyr"] == 27.1838
    assert frame.iloc[1]["total_mv_object"] == 2121764000.0
    assert runner.calls[0]["marker_start"] == STOCK_A_VALUATION_METRICS_MARKER_START
    assert runner.calls[0]["marker_end"] == STOCK_A_VALUATION_METRICS_MARKER_END
    assert '"date": "2023-02-01"' in runner.calls[0]["code"]
    assert "get_fundamentals" in runner.calls[0]["code"]


def test_stock_a_daily_valuation_metrics_remote_code_queries_asharevalue() -> None:
    code = stock_a_daily_valuation_metrics_remote_code(
        {"date": "2023-02-01", "fields": ["pe_lyr", "pb_mrq"]}
    )
    assert "getattr" not in code
    assert "import sys" not in code
    assert (
        "query(asharevalue.symbol, asharevalue.date, "
        "asharevalue.pe_lyr, asharevalue.pb_mrq)"
    ) in code
    assert "emit_payload(payload)" in code
    assert "__mindgo_payload_path" not in code

    class FakeField:
        def __init__(self, name: str) -> None:
            self.name = name

    class FakeAshareValue:
        symbol = FakeField("symbol")
        date = FakeField("date")
        pe_lyr = FakeField("pe_lyr")
        pb_mrq = FakeField("pb_mrq")

    captured: dict[str, Any] = {}

    def fake_query(*fields: FakeField) -> list[str]:
        captured["fields"] = [field.name for field in fields]
        return captured["fields"]

    def fake_get_fundamentals(query_object: list[str], *, date: str) -> pd.DataFrame:
        captured["query_object"] = query_object
        captured["date"] = date
        return pd.DataFrame(
            [
                {
                    "asharevalue_symbol": "300002.SZ",
                    "asharevalue_date": "2023-02-01",
                    "asharevalue_pe_lyr": 27.1838,
                    "asharevalue_pb_mrq": 1.25,
                }
            ]
        )

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(  # noqa: S102
            code,
            {
                "asharevalue": FakeAshareValue,
                "get_fundamentals": fake_get_fundamentals,
                "query": fake_query,
                "time": types.SimpleNamespace(sleep=lambda seconds: None),
            },
        )

    output = stdout.getvalue()
    payload_text = output.split(STOCK_A_VALUATION_METRICS_MARKER_START)[1].split(
        STOCK_A_VALUATION_METRICS_MARKER_END
    )[0]
    payload = json.loads(payload_text)

    assert captured["fields"] == ["symbol", "date", "pe_lyr", "pb_mrq"]
    assert captured["date"] == "20230201"
    assert payload["data"] == [
        {
            "asharevalue_symbol": "300002.SZ",
            "asharevalue_date": "2023-02-01",
            "asharevalue_pe_lyr": 27.1838,
            "asharevalue_pb_mrq": 1.25,
        }
    ]


def test_normalize_stock_a_daily_valuation_metrics_accepts_dataframe_and_aliases() -> None:
    frame = normalize_stock_a_daily_valuation_metrics(
        pd.DataFrame(
            [
                {
                    "asharevalue_symbol": "000001.SZ",
                    "asharevalue_date": "2026-08-13",
                    "asharevalue_pe_ttm": 6.615,
                    "asharevalue_pb_mrq": 0.456,
                    "asharevalue_ev2_to_ebitda": 4.2,
                    "asharevalue_total_mv_ashare": 1000.0,
                }
            ]
        )
    )

    assert frame.to_dict(orient="records")[0] | {
        "symbol": "000001.SZ",
        "trade_date": "20260813",
        "pe_ttm": 6.615,
        "pb_mrq": 0.456,
        "ev2_to_ebitda": 4.2,
        "total_mv_object": 1000.0,
    } == frame.to_dict(orient="records")[0]


async def test_a_stock_daily_valuation_metrics_sync_writes_daily_partitions(tmp_path) -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "asharevalue_symbol": "000001.SZ",
                    "asharevalue_date": "2026-08-13",
                    "asharevalue_pe_ttm": 6.6,
                },
                {
                    "asharevalue_symbol": "000002.SZ",
                    "asharevalue_date": "2026-08-14",
                    "asharevalue_pe_ttm": 7.7,
                },
            ]
        }
    )
    writer = FakeMindgoSyncWriter()
    adapter = StockAValuationMetricsAdapter(
        runner,  # type: ignore[arg-type]
        sync_writer=writer,
        storage_root=tmp_path,
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2026, 8, 13),
            end_date=date(2026, 8, 13),
        )
    )

    assert result.status == "success"
    assert result.synced_count == 2
    assert [call["partition_values"] for call in writer.calls] == [
        {"trade_day": "20260813"},
        {"trade_day": "20260814"},
    ]
    assert {call["source_id"] for call in writer.calls} == {STOCK_A_VALUATION_METRICS_SOURCE_ID}
    assert {tuple(call["order_by"]) for call in writer.calls} == {("trade_date", "symbol")}
