from __future__ import annotations

import contextlib
import io
import json
from datetime import date
from typing import Any

import pandas as pd
from app.schema.mindgo import MindgoDatasetQueryRequest, MindgoDatasetSyncRequest
from app.service.mindgo.stock_a_adjust_factor.adaptor import (
    STOCK_A_ADJUST_FACTOR_DATASET_ID,
    STOCK_A_ADJUST_FACTOR_MARKER_END,
    STOCK_A_ADJUST_FACTOR_MARKER_START,
    MindgoPartitionedParquetWrite,
    StockAAdjustFactorAdapter,
    normalize_stock_a_adjust_factor,
    stock_a_adjust_factor_remote_code,
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
                "dataset_id": write.dataset_id,
                "partition_values": dict(write.partition_values),
                "path": write.path,
                "rows": json.loads(frame.to_json(orient="records")),
                "start_date": write.request.start_date,
                "end_date": write.request.end_date,
                "order_by": list(write.options.order_by or []),
            }
        )
        return len(frame)


async def test_stock_a_adjust_factor_schema_contract() -> None:
    adapter = StockAAdjustFactorAdapter()

    schema = await adapter.get_schema()

    assert adapter.dataset_id == STOCK_A_ADJUST_FACTOR_DATASET_ID
    assert schema.name == "A股复权因子(日)"
    assert schema.mindgo_function == "query_index"
    assert schema.storage.path.endswith("/stock_a_adjust_factor")
    assert schema.storage.format == "parquet"
    assert schema.storage.partitioned_by == ["trade_day"]
    assert [field.name for field in schema.result_schema] == [
        "symbol",
        "trade_date",
        "name",
        "factor",
    ]
    fields_param = next(param for param in schema.query_params if param.name == "fields")
    field_options = [option.value for option in fields_param.options]
    assert field_options == ["symbol", "trade_date", "name", "factor"]


async def test_stock_a_adjust_factor_query_from_mindgo_returns_dataframe() -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "trade_date": 20260813,
                    "query_id": 1016,
                    "uid": "601827.SH",
                    "股票代码": "601827.SH",
                    "股票简称": "三峰环境",
                    "复权因子": 1.1482,
                },
                {
                    "trade_date": 20260813,
                    "query_id": 1016,
                    "uid": "600117.SH",
                    "股票代码": "600117.SH",
                    "股票简称": "西宁特钢",
                    "复权因子": 1.0,
                },
            ]
        }
    )
    adapter = StockAAdjustFactorAdapter(runner)  # type: ignore[arg-type]

    frame = await adapter.query_from_mindgo(
        MindgoDatasetQueryRequest(params={"baseDay": "2026-08-13"})
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame["trade_date"].tolist() == ["20260813", "20260813"]
    assert frame.iloc[0].to_dict() == {
        "symbol": "601827.SH",
        "trade_date": "20260813",
        "name": "三峰环境",
        "factor": 1.1482,
    }
    assert frame.iloc[1]["factor"] == 1.0
    assert runner.calls[0]["marker_start"] == STOCK_A_ADJUST_FACTOR_MARKER_START
    assert runner.calls[0]["marker_end"] == STOCK_A_ADJUST_FACTOR_MARKER_END
    assert '"baseDay": "2026-08-13"' in runner.calls[0]["code"]
    assert '"1016"' in runner.calls[0]["code"]


def test_stock_a_adjust_factor_remote_code_uses_query_index_title_from_date() -> None:
    code = stock_a_adjust_factor_remote_code({"baseDay": "2026-08-14"})
    raw = {
        "total": 1,
        "titles": [
            {"key": "40000000", "label": "股票代码", "from": "0"},
            {"key": "40000006", "label": "股票简称", "from": "0"},
            {"key": "40000000_factor", "label": "复权因子", "from": "20260813"},
        ],
        "data": [
            {
                "40000000": "601827.SH",
                "40000006": "三峰环境",
                "40000000_factor": 1.1482,
            }
        ],
    }

    class FakeResponse:
        def json(self) -> dict[str, Any]:
            return raw

    class FakeArsenalAPI:
        def post(self, path: str, *, files: dict[str, tuple[None, str]]) -> FakeResponse:
            assert path == "/babel/api/query_index"
            assert files["queryId"] == (None, "1016")
            assert files["baseDay"] == (None, "20260814")
            return FakeResponse()

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code, {"get_arsenal_api": lambda pod: FakeArsenalAPI()})  # noqa: S102

    output = stdout.getvalue()
    payload_text = output.split(STOCK_A_ADJUST_FACTOR_MARKER_START)[1].split(
        STOCK_A_ADJUST_FACTOR_MARKER_END
    )[0]
    payload = json.loads(payload_text)

    assert payload["data"] == [
        {
            "股票代码": "601827.SH",
            "股票简称": "三峰环境",
            "复权因子": 1.1482,
            "trade_date": "20260813",
            "query_id": "1016",
        }
    ]


def test_normalize_stock_a_adjust_factor_accepts_dataframe_and_aliases() -> None:
    frame = normalize_stock_a_adjust_factor(
        pd.DataFrame(
            [
                {
                    "date": "2026-08-13",
                    "同花顺代码": "000001.SZ",
                    "证券简称": "平安银行",
                    "复权因子(日)": 1.2345,
                    "query_id": 1016,
                }
            ]
        )
    )

    assert frame.to_dict(orient="records") == [
        {
            "symbol": "000001.SZ",
            "trade_date": "20260813",
            "name": "平安银行",
            "factor": 1.2345,
        }
    ]


async def test_stock_a_adjust_factor_sync_writes_daily_partitions(tmp_path) -> None:
    runner = FakeMindgoRunner(
        {
            "data": [
                {
                    "trade_date": "20260813",
                    "股票代码": "000001.SZ",
                    "股票简称": "平安银行",
                    "复权因子": 1.2,
                },
                {
                    "trade_date": "20260814",
                    "股票代码": "000002.SZ",
                    "股票简称": "万科A",
                    "复权因子": 1.3,
                },
            ]
        }
    )
    writer = FakeMindgoSyncWriter()
    adapter = StockAAdjustFactorAdapter(
        runner,  # type: ignore[arg-type]
        sync_writer=writer,
        storage_root=tmp_path,
    )

    result = await adapter.sync(
        MindgoDatasetSyncRequest(
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
    assert {call["dataset_id"] for call in writer.calls} == {STOCK_A_ADJUST_FACTOR_DATASET_ID}
    assert {tuple(call["order_by"]) for call in writer.calls} == {("trade_date", "symbol")}
