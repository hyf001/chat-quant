from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from typing import Any

import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_daily_price.adaptor import (
    STOCK_A_DAILY_PRICE_MARKER_END,
    STOCK_A_DAILY_PRICE_MARKER_START,
    STOCK_A_DAILY_PRICE_SOURCE_ID,
    DuckDBParquetMindgoSyncWriter,
    MindgoPartitionedParquetWrite,
    StockADailyPriceAdapter,
    mindgo_parquet_partition_path,
    normalize_stock_a_daily_price,
    stock_a_daily_price_remote_code,
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


async def test_stock_a_daily_price_schema_contract() -> None:
    adapter = StockADailyPriceAdapter()

    schema = await adapter.get_source_schema()

    assert adapter.source_id == STOCK_A_DAILY_PRICE_SOURCE_ID
    assert schema.name == "A股历史行情数据(日)"
    assert schema.mindgo_function == "query_index"
    assert schema.storage.path.endswith("/stock_a_daily_price")
    assert schema.storage.format == "parquet"
    assert schema.storage.partitioned_by == ["trade_day"]
    assert [param.name for param in schema.query_params][:2] == [
        "baseDay",
        "fields",
    ]
    assert [field.name for field in schema.result_schema[:4]] == [
        "symbol",
        "trade_date",
        "name",
        "open",
    ]
    result_field_names = [field.name for field in schema.result_schema]
    assert "uid" not in result_field_names
    assert "query_id" not in result_field_names
    fields_param = next(param for param in schema.query_params if param.name == "fields")
    field_options = [option.value for option in fields_param.options]
    assert "uid" not in field_options
    assert "query_id" not in field_options


async def test_stock_a_daily_price_query_from_mindgo_returns_dataframe() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "trade_date": 20260813,
                    "query_id": 1015,
                    "uid": "601827.SH",
                    "开盘价:不复权": 8.78,
                    "成交量(日)": 13275200.0,
                    "成交额(日)": 112309808.0,
                    "最高价:不复权": 8.78,
                    "换手(日)": 0.794,
                    "股票代码": "601827.SH",
                    "股票简称": "三峰环境",
                    "最低价:不复权": 8.36,
                    "收盘价:不复权": 8.38,
                },
                {
                    "trade_date": 20260813,
                    "query_id": 1015,
                    "uid": "600117.SH",
                    "开盘价:不复权": 2.26,
                    "成交量(日)": 14055710.0,
                    "成交额(日)": 31957520.0,
                    "最高价:不复权": 2.3,
                    "换手(日)": 0.4318,
                    "股票代码": "600117.SH",
                    "股票简称": "西宁特钢",
                    "最低价:不复权": 2.24,
                    "收盘价:不复权": 2.3,
                },
            ]
        }
    )
    adapter = StockADailyPriceAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(
            params={
                "baseDay": "2026-08-13",
                "fields": ["open", "close"],
            }
        )
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame["trade_date"].tolist() == ["20260813", "20260813"]
    assert frame.iloc[0]["symbol"] == "601827.SH"
    assert frame.iloc[0]["name"] == "三峰环境"
    assert frame.iloc[0]["open"] == 8.78
    assert frame.iloc[1]["close"] == 2.3
    assert runner.calls[0]["marker_start"] == STOCK_A_DAILY_PRICE_MARKER_START
    assert runner.calls[0]["marker_end"] == STOCK_A_DAILY_PRICE_MARKER_END
    assert '"baseDay": "2026-08-13"' in runner.calls[0]["code"]
    assert '"1015"' in runner.calls[0]["code"]


def test_stock_a_daily_price_remote_code_embeds_query_index_contract() -> None:
    code = stock_a_daily_price_remote_code(
        {
            "baseDay": "2026-08-13",
        }
    )

    assert 'api.post(' in code
    assert '"/babel/api/query_index"' in code
    assert '"queryId": (None, QUERY_ID)' in code
    assert '"baseDay": (None, base_day.replace("-", ""))' in code
    assert 'get_open_api("public")' not in code
    assert "open_api.get_llminfo()" not in code
    assert "retried_after_token_refresh" not in code
    assert "title_trade_date(titles) or base_day" in code
    assert "MINDGO_STOCK_A_DAILY_PRICE_JSON_START" in code


def test_stock_a_daily_price_remote_code_uses_query_index_title_from_date() -> None:
    code = stock_a_daily_price_remote_code({"baseDay": "2026-08-14"})
    raw = {
        "total": 1,
        "titles": [
            {"key": "40000000", "label": "股票代码", "from": "0"},
            {"key": "40000006", "label": "股票简称", "from": "0"},
            {"key": "40000014_b94e8445", "label": "开盘价:不复权", "from": "20260813"},
            {"key": "40000009_b94e8445", "label": "收盘价:不复权", "from": "20260813"},
        ],
        "data": [
            {
                "40000000": "601827.SH",
                "40000006": "三峰环境",
                "40000014_b94e8445": 8.37,
                "40000009_b94e8445": 8.6,
            }
        ],
    }

    class FakeResponse:
        def json(self) -> dict[str, Any]:
            return raw

    class FakeArsenalAPI:
        def post(self, path: str, *, files: dict[str, tuple[None, str]]) -> FakeResponse:
            assert path == "/babel/api/query_index"
            assert files["queryId"] == (None, "1015")
            assert files["baseDay"] == (None, "20260814")
            return FakeResponse()

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code, {"get_arsenal_api": lambda pod: FakeArsenalAPI()})  # noqa: S102

    text = stdout.getvalue()
    start = text.index(STOCK_A_DAILY_PRICE_MARKER_START) + len(
        STOCK_A_DAILY_PRICE_MARKER_START
    )
    end = text.index(STOCK_A_DAILY_PRICE_MARKER_END, start)
    payload = json.loads(text[start:end].strip())

    assert payload["data"][0]["trade_date"] == "20260813"
    assert payload["data"][0]["股票代码"] == "601827.SH"
    assert payload["data"][0]["收盘价:不复权"] == 8.6


def test_normalize_stock_a_daily_price_maps_query_1015_columns_to_standard_columns() -> None:
    raw = [
        {
            "trade_date": 20260813,
            "query_id": 1015,
            "uid": "601827.SH",
            "开盘价:不复权": 8.78,
            "成交量(日)": 13275200.0,
            "成交额(日)": 112309808.0,
            "最高价:不复权": 8.78,
            "换手(日)": 0.794,
            "股票代码": "601827.SH",
            "股票简称": "三峰环境",
            "最低价:不复权": 8.36,
            "收盘价:不复权": 8.38,
        }
    ]

    frame = normalize_stock_a_daily_price(raw)

    assert frame[
        [
            "symbol",
            "trade_date",
            "name",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "turnover",
            "turnover_rate",
        ]
    ].to_dict(orient="records") == [
        {
            "symbol": "601827.SH",
            "trade_date": "20260813",
            "name": "三峰环境",
            "open": 8.78,
            "high": 8.78,
            "low": 8.36,
            "close": 8.38,
            "volume": 13275200.0,
            "turnover": 112309808.0,
            "turnover_rate": 0.794,
        },
    ]
    assert "amplitude" not in frame.columns
    assert "change" not in frame.columns
    assert "uid" not in frame.columns
    assert "query_id" not in frame.columns


async def test_stock_a_daily_price_sync_writes_daily_partitions_with_storage_protocol() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {"股票代码": "601827.SH", "trade_date": 20260813, "收盘价:不复权": 8.38},
                {"股票代码": "600117.SH", "trade_date": 20260813, "收盘价:不复权": 2.3},
            ]
        }
    )
    writer = FakeMindgoSyncWriter()
    adapter = StockADailyPriceAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=writer,
        storage_root="/tmp/mindgo-test/parquet",
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2026, 8, 14),
            end_date=date(2026, 8, 14),
            params={"fields": ["close"]},
        )
    )

    assert result.status == "success"
    assert result.elapsed_ms >= 0
    assert result.synced_count == 2
    assert writer.calls[0]["source_id"] == STOCK_A_DAILY_PRICE_SOURCE_ID
    assert writer.calls[0]["partition_values"] == {"trade_day": "20260813"}
    assert writer.calls[0]["path"].as_posix().endswith(
        "/stock_a_daily_price/trade_day=20260813/data.parquet"
    )
    assert writer.calls[0]["start_date"] == date(2026, 8, 14)
    assert writer.calls[0]["end_date"] == date(2026, 8, 14)
    assert writer.calls[0]["order_by"] == ["trade_date", "symbol"]
    assert '"baseDay": "2026-08-14"' in runner.calls[0]["code"]


async def test_stock_a_daily_price_sync_imports_multiple_days_to_duckdb_parquet(
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
            if '"baseDay": "2026-08-13"' in code:
                return {
                    "data": [
                        {"股票代码": "601827.SH", "trade_date": 20260813, "收盘价:不复权": 8.38},
                    ]
                }
            return {
                "data": [
                    {"股票代码": "600117.SH", "trade_date": 20260814, "收盘价:不复权": 2.3},
                ]
            }

    parquet_root = tmp_path / "mindgo" / "parquet"
    store = DuckDBParquetStore()
    adapter = StockADailyPriceAdapter(  # type: ignore[arg-type]
        DailyMindgoRunner(),
        sync_writer=DuckDBParquetMindgoSyncWriter(store),
        storage=MindgoSourceStorage(parquet_root),
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2026, 8, 13),
            end_date=date(2026, 8, 14),
            params={"fields": ["close"]},
        )
    )

    assert result.synced_count == 2
    first_path = mindgo_parquet_partition_path(
        parquet_root,
        STOCK_A_DAILY_PRICE_SOURCE_ID,
        {"trade_day": "20260813"},
    )
    second_path = mindgo_parquet_partition_path(
        parquet_root,
        STOCK_A_DAILY_PRICE_SOURCE_ID,
        {"trade_day": "20260814"},
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
                parquet_root / STOCK_A_DAILY_PRICE_SOURCE_ID / "trade_day=*" / "data.parquet"
            )
        },
    )

    assert frame.to_dict(orient="records") == [
        {"symbol": "601827.SH", "trade_date": "20260813", "close": 8.38},
        {"symbol": "600117.SH", "trade_date": "20260814", "close": 2.3},
    ]
