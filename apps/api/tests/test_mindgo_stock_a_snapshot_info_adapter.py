from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from typing import Any

import pandas as pd
from app.schema.mindgo import MindgoSourceQueryRequest, MindgoSourceSyncRequest
from app.service.datasource.mindgo.stock_a_snapshot_info.adaptor import (
    STOCK_A_SNAPSHOT_INFO_MARKER_END,
    STOCK_A_SNAPSHOT_INFO_MARKER_START,
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
    DuckDBParquetMindgoSnapshotSyncWriter,
    MindgoSnapshotParquetWrite,
    StockASnapshotInfoAdapter,
    mindgo_parquet_snapshot_path,
    normalize_stock_a_snapshot_info,
    stock_a_snapshot_info_remote_code,
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


class FakeMindgoSnapshotSyncWriter:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def write(
        self,
        write: MindgoSnapshotParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        self.calls.append(
            {
                "source_id": write.source_id,
                "path": write.path,
                "rows": json.loads(frame.to_json(orient="records")),
                "start_date": write.request.start_date,
                "end_date": write.request.end_date,
                "order_by": list(write.options.order_by or []),
            }
        )
        return len(frame)


async def test_stock_a_snapshot_info_schema_contract() -> None:
    adapter = StockASnapshotInfoAdapter()

    schema = await adapter.get_source_schema()

    assert adapter.source_id == STOCK_A_SNAPSHOT_INFO_SOURCE_ID
    assert schema.name == "A股股票信息维表"
    assert schema.name_zh == "A股股票信息维表"
    assert schema.name_en == "a_stock_snapshot_info"
    assert schema.category_path == ["A股", "股票", "快照", "信息维表"]
    assert schema.category_path_en == ["a", "stock", "snapshot", "info"]
    assert schema.mindgo_function == "query_index"
    assert schema.storage.path.endswith("/a_stock_snapshot_info/data.parquet")
    assert schema.storage.format == "parquet"
    assert schema.storage.partitioned_by == []
    assert schema.storage.min_partition is None
    assert schema.storage.max_partition is None
    assert schema.storage.partition_count == 0
    assert [param.name for param in schema.query_params] == ["baseDay", "fields"]
    assert [field.name for field in schema.result_schema] == ["symbol", "name"]


async def test_a_stock_snapshot_info_query_from_mindgo_returns_dataframe() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "query_id": 1018,
                    "序号": 1,
                    "股票代码": "601827.SH",
                    "股票简称": "三峰环境",
                },
                {
                    "query_id": 1018,
                    "序号": 2,
                    "股票代码": "600117.SH",
                    "股票简称": "西宁特钢",
                },
            ]
        }
    )
    adapter = StockASnapshotInfoAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(params={"baseDay": "2026-08-13"})
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame.to_dict(orient="records") == [
        {"symbol": "601827.SH", "name": "三峰环境"},
        {"symbol": "600117.SH", "name": "西宁特钢"},
    ]
    assert runner.calls[0]["marker_start"] == STOCK_A_SNAPSHOT_INFO_MARKER_START
    assert runner.calls[0]["marker_end"] == STOCK_A_SNAPSHOT_INFO_MARKER_END
    assert '"baseDay": "2026-08-13"' in runner.calls[0]["code"]
    assert '"1018"' in runner.calls[0]["code"]


def test_stock_a_snapshot_info_remote_code_uses_query_index_1018() -> None:
    code = stock_a_snapshot_info_remote_code({"baseDay": "2026-08-14"})
    raw = {
        "total": 1,
        "titles": [
            {"key": "1", "label": "序号", "from": "0"},
            {"key": "40000000", "label": "股票代码", "from": "0"},
            {"key": "40000006", "label": "股票简称", "from": "0"},
        ],
        "data": [
            {
                "1": 1,
                "40000000": "601827.SH",
                "40000006": "三峰环境",
            }
        ],
    }

    class FakeResponse:
        def json(self) -> dict[str, Any]:
            return raw

    class FakeArsenalAPI:
        def post(self, path: str, *, files: dict[str, tuple[None, str]]) -> FakeResponse:
            assert path == "/babel/api/query_index"
            assert files["queryId"] == (None, "1018")
            assert files["baseDay"] == (None, "20260814")
            return FakeResponse()

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code, {"get_arsenal_api": lambda pod: FakeArsenalAPI()})  # noqa: S102

    output = stdout.getvalue()
    payload_text = output.split(STOCK_A_SNAPSHOT_INFO_MARKER_START)[1].split(
        STOCK_A_SNAPSHOT_INFO_MARKER_END
    )[0]
    payload = json.loads(payload_text)

    assert payload["data"] == [{"序号": 1, "股票代码": "601827.SH", "股票简称": "三峰环境"}]


def test_normalize_stock_a_snapshot_info_maps_query_1018_columns_to_standard_columns() -> None:
    frame = normalize_stock_a_snapshot_info(
        [
            {
                "序号": 1,
                "股票代码": "601827.SH",
                "股票简称": "三峰环境",
            }
        ]
    )

    assert frame.to_dict(orient="records") == [
        {"symbol": "601827.SH", "name": "三峰环境"},
    ]


async def test_a_stock_snapshot_info_sync_writes_single_snapshot_path() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {"股票代码": "601827.SH", "股票简称": "三峰环境"},
                {"股票代码": "600117.SH", "股票简称": "西宁特钢"},
            ]
        }
    )
    writer = FakeMindgoSnapshotSyncWriter()
    adapter = StockASnapshotInfoAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=writer,
        storage_root="/tmp/mindgo-test/parquet",
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2026, 8, 13),
            end_date=date(2026, 8, 14),
        )
    )

    assert result.status == "success"
    assert result.elapsed_ms >= 0
    assert result.synced_count == 2
    assert len(writer.calls) == 1
    assert writer.calls[0]["source_id"] == STOCK_A_SNAPSHOT_INFO_SOURCE_ID
    assert writer.calls[0]["path"].as_posix().endswith(
        "/a_stock_snapshot_info/data.parquet"
    )
    assert writer.calls[0]["start_date"] == date(2026, 8, 13)
    assert writer.calls[0]["end_date"] == date(2026, 8, 14)
    assert writer.calls[0]["order_by"] == ["symbol"]
    assert '"baseDay": "2026-08-14"' in runner.calls[0]["code"]


async def test_a_stock_snapshot_info_sync_imports_to_duckdb_parquet(tmp_path) -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {"股票代码": "601827.SH", "股票简称": "三峰环境"},
                {"股票代码": "600117.SH", "股票简称": "西宁特钢"},
            ]
        }
    )
    parquet_root = tmp_path / "mindgo" / "parquet"
    store = DuckDBParquetStore()
    adapter = StockASnapshotInfoAdapter(  # type: ignore[arg-type]
        runner,
        sync_writer=DuckDBParquetMindgoSnapshotSyncWriter(store),
        storage=MindgoSourceStorage(parquet_root),
    )

    result = await adapter.sync(
        MindgoSourceSyncRequest(
            start_date=date(2026, 8, 14),
            end_date=date(2026, 8, 14),
        )
    )

    assert result.synced_count == 2
    snapshot_path = mindgo_parquet_snapshot_path(
        parquet_root,
        STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
    )
    assert snapshot_path.exists()

    frame = store.query(
        """
        SELECT symbol, name
        FROM read_parquet($path)
        ORDER BY symbol
        """,
        params={"path": str(snapshot_path)},
    )

    assert frame.to_dict(orient="records") == [
        {"symbol": "600117.SH", "name": "西宁特钢"},
        {"symbol": "601827.SH", "name": "三峰环境"},
    ]
