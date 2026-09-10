from __future__ import annotations

import contextlib
import io
import json
from datetime import date, datetime
from typing import Any

import app.service.datasource.mindgo.stock_a_minute_price.adaptor as minute_adaptor
import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_minute_price.adaptor import (
    STOCK_A_MINUTE_PRICE_MARKER_END,
    STOCK_A_MINUTE_PRICE_MARKER_START,
    STOCK_A_MINUTE_PRICE_SOURCE_ID,
    STOCK_A_MINUTE_PRICE_WINDOW_MINUTES,
    DuckDBParquetMindgoSyncWriter,
    MindgoPartitionedParquetWrite,
    StockAMinutePriceAdapter,
    minute_price_frame_from_payload,
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


def run_remote_code(params: dict[str, Any], get_price: Any) -> dict[str, Any]:
    """Execute the generated remote cell locally and return its JSON payload."""
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(stock_a_minute_price_remote_code(params), {"get_price": get_price})  # noqa: S102

    text = stdout.getvalue()
    start = text.index(STOCK_A_MINUTE_PRICE_MARKER_START) + len(STOCK_A_MINUTE_PRICE_MARKER_START)
    end = text.index(STOCK_A_MINUTE_PRICE_MARKER_END, start)
    return json.loads(text[start:end].strip())


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


async def test_stock_a_minute_price_query_decodes_parquet_payload() -> None:
    payload = run_remote_code(
        {
            "securities": ["000001.SZ"],
            "start_date": "2023-02-01 10:58",
            "end_date": "2023-02-01 10:59",
            "fields": ["close"],
            "fq": "none",
            "skip_paused": False,
            "bar_count": 0,
        },
        lambda *args, **kwargs: {
            "000001.SZ": pd.DataFrame(
                {"close": [14.57]},
                index=pd.to_datetime(["2023-02-01 10:58:00"]),
            )
        },
    )
    runner = FakeMindgoRunner(payload)
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


def test_stock_a_minute_price_remote_code_returns_parquet_payload() -> None:
    calls: list[dict[str, Any]] = []

    def fake_get_price(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return {
            "000001.SZ": pd.DataFrame(
                {"close": [14.57], "volume": [100.0]},
                index=pd.to_datetime(["2023-02-01 10:59:00"]),
            )
        }

    payload = run_remote_code(
        {
            "securities": ["000001.SZ", "600519.SH"],
            "start_date": "2023-02-01 10:57",
            "end_date": "2023-02-01 10:59",
            "fields": ["close", "volume"],
            "fq": "none",
            "skip_paused": True,
            "bar_count": 3,
        },
        fake_get_price,
    )

    assert calls[0]["args"] == (["000001.SZ", "600519.SH"],)
    assert calls[0]["kwargs"]["fre_step"] == "1m"
    assert calls[0]["kwargs"]["fq"] is None
    assert calls[0]["kwargs"]["skip_paused"] is True
    assert calls[0]["kwargs"]["is_panel"] is False
    assert payload["rows"] == 1
    assert payload["data_b64"]

    frame = minute_price_frame_from_payload(payload)

    assert list(frame.columns) == [
        "symbol",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    assert frame.iloc[0]["symbol"] == "000001.SZ"
    assert frame.iloc[0]["trade_date"] == "2023-02-01 10:59:00"
    assert frame.iloc[0]["close"] == 14.57
    assert frame.iloc[0]["volume"] == 100.0
    assert pd.isna(frame.iloc[0]["open"])


def test_stock_a_minute_price_remote_code_converts_panel_frames() -> None:
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

    payload = run_remote_code(
        {
            "securities": ["000001.SZ", "600519.SH"],
            "fields": ["close", "volume"],
            "fq": "none",
            "skip_paused": False,
            "bar_count": 0,
            "start_date": "2023-02-01 10:58",
            "end_date": "2023-02-01 10:59",
        },
        lambda *args, **kwargs: raw,
    )

    frame = minute_price_frame_from_payload(payload)
    records = frame[["symbol", "trade_date", "close", "volume"]].to_dict(orient="records")
    records.sort(key=lambda record: (record["trade_date"], record["symbol"]))

    assert records == [
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


def test_minute_windows_slice_the_session_into_configured_windows() -> None:
    windows = minute_adaptor._minute_windows(date(2023, 2, 1))

    assert STOCK_A_MINUTE_PRICE_WINDOW_MINUTES == 20
    assert len(windows) == 12
    assert windows[0] == (datetime(2023, 2, 1, 9, 30), datetime(2023, 2, 1, 9, 49, 59))
    assert windows[5] == (datetime(2023, 2, 1, 11, 10), datetime(2023, 2, 1, 11, 29, 59))
    assert windows[6] == (datetime(2023, 2, 1, 13, 0), datetime(2023, 2, 1, 13, 19, 59))
    assert windows[-1] == (datetime(2023, 2, 1, 14, 40), datetime(2023, 2, 1, 14, 59, 59))


def _single_symbol_payload(symbol: str = "000001.SZ") -> dict[str, Any]:
    return run_remote_code(
        {
            "securities": [symbol],
            "fields": ["close"],
            "fq": "none",
            "skip_paused": False,
            "bar_count": 0,
        },
        lambda *args, **kwargs: {
            symbol: pd.DataFrame(
                {"close": [14.57]},
                index=pd.to_datetime(["2023-02-01 10:59:00"]),
            )
        },
    )


async def test_stock_a_minute_price_sync_writes_window_files(monkeypatch) -> None:
    monkeypatch.setattr(minute_adaptor, "_snapshot_info_securities", lambda: ["000001.SZ"])
    runner = FakeMindgoRunner(_single_symbol_payload())
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
    assert result.synced_count == 24
    assert sorted({call["partition_values"]["trade_day"] for call in writer.calls}) == [
        "20230201",
        "20230202",
    ]
    assert len({call["path"].name for call in writer.calls}) == 12
    assert {call["path"].name for call in writer.calls} >= {
        "093000_094959.parquet",
        "111000_112959.parquet",
        "130000_131959.parquet",
        "144000_145959.parquet",
    }
    assert writer.calls[0]["order_by"] == ["trade_date", "symbol"]
    assert '"start_date": "2023-02-01 09:30:00"' in runner.calls[0]["code"]
    assert '"end_date": "2023-02-01 09:49:59"' in runner.calls[0]["code"]
    assert '"fre_step": "1m"' not in runner.calls[0]["code"]
    assert '["000001.SZ"]' in runner.calls[0]["code"]


async def test_stock_a_minute_price_sync_writes_parquet(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(minute_adaptor, "_snapshot_info_securities", lambda: ["000001.SZ"])
    runner = FakeMindgoRunner(_single_symbol_payload())
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
            params={"fields": ["close"]},
        )
    )

    assert result.synced_count == 12
    partition_dir = parquet_root / STOCK_A_MINUTE_PRICE_SOURCE_ID / "trade_day=20230201"
    files = sorted(partition_dir.glob("*.parquet"))
    assert len(files) == 12
    assert (partition_dir / "093000_094959.parquet").exists()

    frame = store.query(
        "SELECT symbol, trade_date, close FROM read_parquet($glob)",
        params={"glob": str(partition_dir / "*.parquet")},
    )
    assert frame["symbol"].unique().tolist() == ["000001.SZ"]
    assert set(frame["trade_date"]) == {"2023-02-01 10:59:00"}
    assert set(frame["close"]) == {14.57}
