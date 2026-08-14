from __future__ import annotations

import pytest
from app.service.mindgo.storage import MindgoDatasetStorage, mindgo_dataset_partition_path


def test_mindgo_dataset_storage_builds_dataset_partition_path() -> None:
    storage = MindgoDatasetStorage("/tmp/mindgo-root")

    path = storage.partition_path(
        "stock_a_daily_price",
        {"trade_day": "20260813"},
    )

    assert (
        path.as_posix()
        == "/tmp/mindgo-root/stock_a_daily_price/trade_day=20260813/data.parquet"
    )


def test_mindgo_dataset_partition_path_rejects_unsafe_segments() -> None:
    with pytest.raises(ValueError):
        mindgo_dataset_partition_path(
            "/tmp/mindgo-root",
            "../stock_a_daily_price",
            {"trade_day": "20260813"},
        )
