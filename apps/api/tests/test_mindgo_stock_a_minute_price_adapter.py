from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from typing import Any

import app.service.datasource.mindgo.stock_a_minute_price.adaptor as minute_adaptor
import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_minute_price.adaptor import (
    STOCK_A_MINUTE_PRICE_MARKER_END,
    STOCK_A_MINUTE_PRICE_MARKER_START,
    STOCK_A_MINUTE_PRICE_SOURCE_ID,
    DuckDBParquetMindgoSyncWriter,
    MindgoPartitionedParquetWrite,
    StockAMinutePriceAdapter,
    mindgo_parquet_partition_path,
    normalize_stock_a_minute_price,
    stock_a_minute_price_remote_code,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage
from app.storage import DuckDBParquetStore


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
                "order_by": list(write.options.order_by or []),
            }
        )
        return len(frame)


async def test_stock_a_minute_price_schema_contract() -> None:
    adapter = StockAMinutePriceAdapter()

    schema = await adapter.get_source_schema()

    assert adapter.source_id == STOCK_A_MINUTE_PRICE_SOURCE_ID
    assert schema.name == "A股股票分钟行情数据"
    assert schema.name_en == "a_stock_minute_price"
    assert schema.category_path == ["A股", "股票", "分钟", "行情数据"]
    assert schema.category_path_en == ["a", "stock", "minute", "price"]
    assert schema.mindgo_function == "get_price"
    assert schema.storage.path.endswith("/a_stock_minute_price")
    assert schema.storage.partitioned_by == ["trade_day"]
    assert schema.sync.supports_query_window is True
    assert [field.name for field in schema.result_schema] == [
        "symbol",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    assert [param.name for param in schema.query_params[:3]] == [
        "securities",
        "start_date",
        "end_date",
    ]


def test_stock_a_minute_price_uses_snapshot_info_for_security_options(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        minute_adaptor,
        "_snapshot_info_frame",
        lambda: pd.DataFrame(
            [
                {"symbol": "000001.SZ", "name": "平安银行"},
                {"symbol": "600519.SH", "name": "贵州茅台"},
                {"symbol": "000001.SZ", "name": "平安银行"},
            ]
        ),
    )

    schema = minute_adaptor.stock_a_minute_price_schema()
    securities_param = next(param for param in schema.query_params if param.name == "securities")

    assert securities_param.default == ["000001.SZ", "600519.SH"]
    assert [(option.label, option.value) for option in securities_param.options] == [
        ("平安银行 000001.SZ", "000001.SZ"),
        ("贵州茅台 600519.SH", "600519.SH"),
    ]
    assert minute_adaptor._query_params(MindgoSourceQueryRequest(params={}))["securities"] == [
        "000001.SZ",
        "600519.SH",
    ]


async def test_stock_a_minute_price_query_normalizes_dict_result() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "symbol": "000001.SZ",
                    "trade_date": "2023-02-01 10:58:00",
                    "open": 14.57,
                    "high": 14.58,
                    "low": 14.56,
                    "close": 14.57,
                    "volume": 773700.0,
                    "turnover": 11230980.0,
                    "turnover_rate": 0.01,
                    "is_paused": 0.0,
                }
            ]
        }
    )
    adapter = StockAMinutePriceAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(
            params={
                "securities": ["000001.SZ"],
                "start_date": "2023-02-01 10:58",
                "end_date": "2023-02-01 10:59",
                "fields": ["close"],
            }
        )
    )

    assert frame.iloc[0]["symbol"] == "000001.SZ"
    assert frame.iloc[0]["trade_date"] == "2023-02-01 10:58:00"
    assert frame.iloc[0]["close"] == 14.57
    assert runner.calls[0]["marker_start"] == STOCK_A_MINUTE_PRICE_MARKER_START
    assert runner.calls[0]["marker_end"] == STOCK_A_MINUTE_PRICE_MARKER_END
    assert '"fre_step": "1m"' not in runner.calls[0]["code"]
    assert 'fre_step="1m"' in runner.calls[0]["code"]


def test_stock_a_minute_price_remote_code_calls_get_price_with_minute_frequency() -> None:
    code = stock_a_minute_price_remote_code(
        {
            "securities": ["000001.SZ", "600519.SH"],
            "start_date": "2023-02-01 10:57",
            "end_date": "2023-02-01 10:59",
            "fields": ["close", "volume"],
            "fq": "none",
            "skip_paused": True,
            "bar_count": 3,
        }
    )
    calls: list[dict[str, Any]] = []

    def fake_get_price(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return {
            "000001.SZ": pd.DataFrame(
                {"close": [14.57], "volume": [100.0]},
                index=pd.to_datetime(["2023-02-01 10:59:00"]),
            )
        }

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code, {"get_price": fake_get_price})  # noqa: S102

    text = stdout.getvalue()
    start = text.index(STOCK_A_MINUTE_PRICE_MARKER_START) + len(STOCK_A_MINUTE_PRICE_MARKER_START)
    end = text.index(STOCK_A_MINUTE_PRICE_MARKER_END, start)
    payload = json.loads(text[start:end].strip())

    assert calls[0]["args"] == (["000001.SZ", "600519.SH"],)
    assert calls[0]["kwargs"]["fre_step"] == "1m"
    assert calls[0]["kwargs"]["fq"] is None
    assert calls[0]["kwargs"]["skip_paused"] is True
    assert calls[0]["kwargs"]["is_panel"] is False
    assert payload["data"][0]["trade_date"] == "2023-02-01 10:59:00"
    assert payload["data"][0]["symbol"] == "000001.SZ"


def test_normalize_stock_a_minute_price_preserves_panel_timestamps() -> None:
    raw = {
        "close": pd.DataFrame(
            {
                "000001.SZ": [14.57, 14.59],
                "600519.SH": [1822.0, 1821.0],
            },
            index=pd.to_datetime(["2023-02-01 10:58:00", "2023-02-01 10:59:00"]),
        ),
        "volume": pd.DataFrame(
            {
                "000001.SZ": [100.0, 200.0],
                "600519.SH": [300.0, 400.0],
            },
            index=pd.to_datetime(["2023-02-01 10:58:00", "2023-02-01 10:59:00"]),
        ),
    }

    frame = normalize_stock_a_minute_price(raw)

    assert frame[["symbol", "trade_date", "close", "volume"]].to_dict(orient="records") == [
        {
            "symbol": "000001.SZ",
            "trade_date": "2023-02-01 10:58:00",
            "close": 14.57,
            "volume": 100.0,
        },
        {
            "symbol": "600519.SH",
            "trade_date": "2023-02-01 10:58:00",
            "close": 1822.0,
            "volume": 300.0,
        },
        {
            "symbol": "000001.SZ",
            "trade_date": "2023-02-01 10:59:00",
            "close": 14.59,
            "volume": 200.0,
        },
        {
            "symbol": "600519.SH",
            "trade_date": "2023-02-01 10:59:00",
            "close": 1821.0,
            "volume": 400.0,
        },
    ]


async def test_stock_a_minute_price_sync_writes_trade_day_partitions() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "symbol": "000001.SZ",
                    "trade_date": "2023-02-01 10:59:00",
                    "close": 14.57,
                },
                {
                    "symbol": "000001.SZ",
                    "trade_date": "2023-02-02 09:31:00",
                    "close": 14.60,
                },
            ]
        }
    )
    writer = FakeMindgoSyncWriter()
    adapter = StockAMinutePriceAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=writer,
        storage_root="/tmp/mindgo-test/parquet",
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2023, 2, 1),
            end_date=date(2023, 2, 2),
            params={"securities": ["000001.SZ"], "fields": ["close"]},
        )
    )

    assert result.status == "success"
    assert result.synced_count == 2
    assert [call["partition_values"] for call in writer.calls] == [
        {"trade_day": "20230201"},
        {"trade_day": "20230202"},
    ]
    assert (
        writer.calls[0]["path"]
        .as_posix()
        .endswith("/a_stock_minute_price/trade_day=20230201/data.parquet")
    )
    assert writer.calls[0]["order_by"] == ["trade_date", "symbol"]
    assert '"fre_step": "1m"' not in runner.calls[0]["code"]
    assert '"start_date": "2023-02-01"' in runner.calls[0]["code"]
    assert '"end_date": "2023-02-02"' in runner.calls[0]["code"]


async def test_stock_a_minute_price_sync_writes_parquet(tmp_path) -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "symbol": "000001.SZ",
                    "trade_date": "2023-02-01 10:59:00",
                    "close": 14.57,
                }
            ]
        }
    )
    parquet_root = tmp_path / "mindgo" / "parquet"
    store = DuckDBParquetStore()
    adapter = StockAMinutePriceAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=DuckDBParquetMindgoSyncWriter(store),
        storage=MindgoSourceStorage(parquet_root),
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2023, 2, 1),
            end_date=date(2023, 2, 1),
            params={"securities": ["000001.SZ"], "fields": ["close"]},
        )
    )

    assert result.synced_count == 1
    path = mindgo_parquet_partition_path(
        parquet_root,
        STOCK_A_MINUTE_PRICE_SOURCE_ID,
        {"trade_day": "20230201"},
    )
    assert path.exists()
    frame = store.query(
        "SELECT symbol, trade_date, close FROM read_parquet($path)",
        params={"path": str(path)},
    )
    assert frame.to_dict(orient="records") == [
        {
            "symbol": "000001.SZ",
            "trade_date": "2023-02-01 10:59:00",
            "close": 14.57,
        }
    ]
