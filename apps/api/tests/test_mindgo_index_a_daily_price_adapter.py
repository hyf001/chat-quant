from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from typing import Any

import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.index_a_daily_price.adaptor import (
    INDEX_A_DAILY_PRICE_MARKER_END,
    INDEX_A_DAILY_PRICE_MARKER_START,
    INDEX_A_DAILY_PRICE_SOURCE_ID,
    DuckDBParquetMindgoSyncWriter,
    IndexADailyPriceAdapter,
    MindgoPartitionedParquetWrite,
    index_a_daily_price_remote_code,
    mindgo_parquet_partition_path,
    normalize_index_a_daily_price,
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
                "start_date": write.request.start_date,
                "end_date": write.request.end_date,
                "order_by": list(write.options.order_by or []),
            }
        )
        return len(frame)


async def test_index_a_daily_price_schema_contract() -> None:
    adapter = IndexADailyPriceAdapter()

    schema = await adapter.get_source_schema()

    assert adapter.source_id == INDEX_A_DAILY_PRICE_SOURCE_ID
    assert schema.name == "A股指数日行情数据"
    assert schema.category_path == ["指数", "指数行情数据"]
    assert schema.mindgo_function == "get_price"
    assert schema.storage.path.endswith("/index_a_daily_price")
    assert schema.storage.format == "parquet"
    assert schema.storage.partitioned_by == ["trade_day"]
    assert schema.sync.supports_query_window is True
    assert schema.sync.min_start_offset_days == -20000
    assert schema.sync.max_end_offset_days == 0
    assert [param.name for param in schema.query_params[:4]] == [
        "securities",
        "start_date",
        "end_date",
        "fields",
    ]
    assert [field.name for field in schema.result_schema] == [
        "symbol",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    securities_param = next(param for param in schema.query_params if param.name == "securities")
    assert securities_param.default == [
        "000300.SH",
        "000905.SH",
        "000852.SH",
        "000016.SH",
        "000001.SH",
        "399001.SZ",
        "399006.SZ",
        "000688.SH",
    ]
    assert [option.label for option in securities_param.options[:3]] == [
        "沪深300 000300.SH",
        "中证500 000905.SH",
        "中证1000 000852.SH",
    ]
    fields_param = next(param for param in schema.query_params if param.name == "fields")
    assert fields_param.default == ["open", "high", "low", "close", "volume"]
    assert [option.value for option in fields_param.options] == [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]


async def test_index_a_daily_price_query_from_mindgo_returns_dataframe() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "symbol": "000905.SH",
                    "trade_date": 20230403,
                    "open": 6403.54,
                    "close": 6413.8073,
                    "volume": 123.0,
                },
                {
                    "symbol": "000300.SH",
                    "trade_date": 20230403,
                    "open": 4087.12,
                    "close": 4090.5676,
                    "volume": 456.0,
                },
            ]
        }
    )
    adapter = IndexADailyPriceAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(
            params={
                "securities": ["000905.SH", "000300.SH"],
                "start_date": "2023-04-03",
                "end_date": "2023-04-03",
                "fields": ["open", "close", "volume"],
            }
        )
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame["trade_date"].tolist() == ["20230403", "20230403"]
    assert frame.iloc[0]["symbol"] == "000905.SH"
    assert frame.iloc[0]["close"] == 6413.8073
    assert frame.iloc[1]["close"] == 4090.5676
    assert runner.calls[0]["marker_start"] == INDEX_A_DAILY_PRICE_MARKER_START
    assert runner.calls[0]["marker_end"] == INDEX_A_DAILY_PRICE_MARKER_END
    assert '"securities": ["000905.SH", "000300.SH"]' in runner.calls[0]["code"]
    assert "get_price(" in runner.calls[0]["code"]


def test_index_a_daily_price_remote_code_calls_get_price() -> None:
    code = index_a_daily_price_remote_code(
        {
            "securities": ["000905.SH", "000300.SH"],
            "start_date": "2023-04-03",
            "end_date": "2023-04-03",
            "fields": ["open", "close"],
            "skip_paused": False,
        }
    )

    calls = []

    def fake_get_price(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return pd.DataFrame(
            {"open": [6403.54], "close": [6413.8073]},
            index=pd.to_datetime(["2023-04-03"]),
        )

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code, {"get_price": fake_get_price})  # noqa: S102

    text = stdout.getvalue()
    start = text.index(INDEX_A_DAILY_PRICE_MARKER_START) + len(
        INDEX_A_DAILY_PRICE_MARKER_START
    )
    end = text.index(INDEX_A_DAILY_PRICE_MARKER_END, start)
    payload = json.loads(text[start:end].strip())

    assert calls[0]["args"] == (["000905.SH", "000300.SH"],)
    assert calls[0]["kwargs"]["fre_step"] == "1d"
    assert calls[0]["kwargs"]["fq"] == "pre"
    assert calls[0]["kwargs"]["is_panel"] is False
    assert calls[0]["kwargs"]["skip_paused"] is False
    assert payload["data"][0]["trade_date"] == "20230403"
    assert payload["data"][0]["close"] == 6413.8073


def test_normalize_index_a_daily_price_maps_panel_dict_to_standard_rows() -> None:
    raw = {
        "close": pd.DataFrame(
            {
                "000905.SH": [6413.8073],
                "000300.SH": [4090.5676],
            },
            index=pd.to_datetime(["2023-04-03"]),
        ),
        "volume": pd.DataFrame(
            {
                "000905.SH": [100.0],
                "000300.SH": [200.0],
            },
            index=pd.to_datetime(["2023-04-03"]),
        ),
    }

    frame = normalize_index_a_daily_price(raw)

    assert frame[["symbol", "trade_date", "close", "volume"]].to_dict(
        orient="records"
    ) == [
        {
            "symbol": "000905.SH",
            "trade_date": "20230403",
            "close": 6413.8073,
            "volume": 100.0,
        },
        {
            "symbol": "000300.SH",
            "trade_date": "20230403",
            "close": 4090.5676,
            "volume": 200.0,
        },
    ]


async def test_index_a_daily_price_sync_writes_daily_partitions_with_storage_protocol() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {"symbol": "000905.SH", "trade_date": 20230403, "close": 6413.8073},
                {"symbol": "000300.SH", "trade_date": 20230403, "close": 4090.5676},
            ]
        }
    )
    writer = FakeMindgoSyncWriter()
    adapter = IndexADailyPriceAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=writer,
        storage_root="/tmp/mindgo-test/parquet",
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2023, 4, 3),
            end_date=date(2023, 4, 3),
            params={"securities": ["000905.SH", "000300.SH"], "fields": ["close"]},
        )
    )

    assert result.status == "success"
    assert result.elapsed_ms >= 0
    assert result.synced_count == 2
    assert writer.calls[0]["source_id"] == INDEX_A_DAILY_PRICE_SOURCE_ID
    assert writer.calls[0]["partition_values"] == {"trade_day": "20230403"}
    assert writer.calls[0]["path"].as_posix().endswith(
        "/index_a_daily_price/trade_day=20230403/data.parquet"
    )
    assert writer.calls[0]["order_by"] == ["trade_date", "symbol"]
    assert '"start_date": "2023-04-03"' in runner.calls[0]["code"]
    assert '"end_date": "2023-04-03"' in runner.calls[0]["code"]


async def test_index_a_daily_price_sync_imports_multiple_days_to_duckdb_parquet(
    tmp_path,
) -> None:
    class DailyMindgoRunner:
        def __init__(self) -> None:
            self.calls: list[str] = []

        async def run_json(
            self,
            code: str,
            *,
            marker_start: str,
            marker_end: str,
            timeout_seconds: float | None = None,
        ) -> dict[str, Any]:
            self.calls.append(code)
            return {
                "data": [
                    {"symbol": "000905.SH", "trade_date": 20230403, "close": 6413.8073},
                    {"symbol": "000905.SH", "trade_date": 20230404, "close": 6408.8994},
                ]
            }

    runner = DailyMindgoRunner()
    parquet_root = tmp_path / "mindgo" / "parquet"
    store = DuckDBParquetStore()
    adapter = IndexADailyPriceAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=DuckDBParquetMindgoSyncWriter(store),
        storage=MindgoSourceStorage(parquet_root),
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2023, 4, 3),
            end_date=date(2023, 4, 4),
            params={"securities": ["000905.SH"], "fields": ["close"]},
        )
    )

    assert result.synced_count == 2
    assert len(runner.calls) == 1
    assert '"start_date": "2023-04-03"' in runner.calls[0]
    assert '"end_date": "2023-04-04"' in runner.calls[0]
    first_path = mindgo_parquet_partition_path(
        parquet_root,
        INDEX_A_DAILY_PRICE_SOURCE_ID,
        {"trade_day": "20230403"},
    )
    second_path = mindgo_parquet_partition_path(
        parquet_root,
        INDEX_A_DAILY_PRICE_SOURCE_ID,
        {"trade_day": "20230404"},
    )
    assert first_path.exists()
    assert second_path.exists()

    frame = store.query(
        """
        SELECT symbol, trade_date, close
        FROM read_parquet($path)
        ORDER BY trade_date, symbol
        """,
        params={
            "path": str(
                parquet_root / INDEX_A_DAILY_PRICE_SOURCE_ID / "trade_day=*" / "data.parquet"
            )
        },
    )

    assert frame.to_dict(orient="records") == [
        {"symbol": "000905.SH", "trade_date": "20230403", "close": 6413.8073},
        {"symbol": "000905.SH", "trade_date": "20230404", "close": 6408.8994},
    ]
