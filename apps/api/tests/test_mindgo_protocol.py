from datetime import date

import pandas as pd
import pytest
from app.schema.mindgo import (
    MindgoFieldSpec,
    MindgoParameterSpec,
    MindgoSourceQueryRequest,
    MindgoSourceSchema,
    MindgoSourceStorageSpec,
    MindgoSourceSyncQueryWindow,
    MindgoSourceSyncRequest,
    MindgoSourceSyncResult,
)
from pydantic import ValidationError


def test_mindgo_source_schema_protocol_supports_result_schema() -> None:
    schema = MindgoSourceSchema(
        name="股票日行情数据(A股)",
        category_path=["股票", "A股", "行情数据(A股)"],
        description="A股股票日频行情数据",
        mindgo_function="get_price",
        storage=MindgoSourceStorageSpec(
            path="data/mindgo/parquet/stock_a_daily_price",
            format="parquet",
            partitioned_by=["trade_day"],
        ),
        query_params=[
            MindgoParameterSpec(
                name="securities",
                label="股票代码",
                value_type="string[]",
                required=True,
                validation={"min_items": 1, "max_items": 100},
            ),
        ],
        result_schema=[
            MindgoFieldSpec(
                name="symbol",
                label="股票代码",
                value_type="string",
                required=True,
            ),
            MindgoFieldSpec(
                name="trade_date",
                label="交易日",
                value_type="date",
                required=True,
            ),
        ],
    )

    assert schema.name == "股票日行情数据(A股)"
    assert schema.storage.path == "data/mindgo/parquet/stock_a_daily_price"
    assert schema.storage.partitioned_by == ["trade_day"]
    assert schema.storage.min_partition is None
    assert schema.storage.max_partition is None
    assert schema.storage.partition_count == 0
    assert schema.result_schema[0].name == "symbol"


def test_mindgo_query_and_sync_payload_contracts() -> None:
    query_request = MindgoSourceQueryRequest(
        params={"securities": ["000001.SZ"], "fq": "pre"},
        page=2,
        page_size=20,
    )
    sync_request = MindgoSourceSyncRequest(
        start_date="2023-02-01",
        end_date="2023-02-03",
        params={"securities": ["000001.SZ"]},
    )

    assert query_request.params["fq"] == "pre"
    assert query_request.page == 2
    assert sync_request.start_date == date(2023, 2, 1)
    assert sync_request.end_date == date(2023, 2, 3)
    assert sync_request.query_window == MindgoSourceSyncQueryWindow()
    assert sync_request.params["securities"] == ["000001.SZ"]


def test_mindgo_sync_request_requires_date_range() -> None:
    with pytest.raises(ValidationError):
        MindgoSourceSyncRequest(params={"securities": ["000001.SZ"]})


def test_mindgo_sync_request_requires_ordered_date_range() -> None:
    with pytest.raises(ValidationError):
        MindgoSourceSyncRequest(
            start_date=date(2023, 2, 3),
            end_date=date(2023, 2, 1),
            params={"securities": ["000001.SZ"]},
        )


def test_mindgo_sync_result_contract() -> None:
    result = MindgoSourceSyncResult(status="success", elapsed_ms=123, synced_count=10)

    assert result.status == "success"
    assert result.elapsed_ms == 123
    assert result.synced_count == 10


async def test_mindgo_source_adapter_query_entries_return_dataframes() -> None:
    class FakeMindgoSourceAdapter:
        source_id = "stock_a_daily_price"

        async def get_source_schema(self) -> MindgoSourceSchema:
            return MindgoSourceSchema(
                name="股票日行情数据(A股)",
                category_path=["股票", "A股", "行情数据(A股)"],
                mindgo_function="get_price",
                storage=MindgoSourceStorageSpec(
                    path="data/mindgo/parquet/stock_a_daily_price",
                    format="parquet",
                    partitioned_by=["trade_day"],
                ),
                query_params=[],
                result_schema=[],
            )

        async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
            return pd.DataFrame(
                [{"symbol": "000001.SZ", "trade_date": "2023-02-01", "close": 14.7}]
            )

        async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
            return MindgoSourceSyncResult(status="success", elapsed_ms=12, synced_count=1)

    adapter = FakeMindgoSourceAdapter()
    frame = await adapter.query_from_mindgo(
        MindgoSourceQueryRequest(params={"securities": ["000001.SZ"]})
    )

    assert isinstance(frame, pd.DataFrame)
    assert frame.iloc[0]["symbol"] == "000001.SZ"
