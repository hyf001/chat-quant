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


def test_mindgo_dataset_storage_summarizes_partitions(tmp_path) -> None:
    storage = MindgoDatasetStorage(tmp_path)
    storage.partition_path(
        "stock_a_daily_price",
        {"trade_day": "20260814"},
    ).parent.mkdir(parents=True)
    storage.partition_path(
        "stock_a_daily_price",
        {"trade_day": "20260814"},
    ).write_text("not parquet")
    storage.partition_path(
        "stock_a_daily_price",
        {"trade_day": "20260813"},
    ).parent.mkdir(parents=True)
    storage.partition_path(
        "stock_a_daily_price",
        {"trade_day": "20260813"},
    ).write_text("not parquet")

    summary = storage.partition_summary("stock_a_daily_price", ["trade_day"])

    assert summary.min_partition == "20260813"
    assert summary.max_partition == "20260814"
    assert summary.partition_count == 2


def test_mindgo_dataset_storage_returns_empty_partition_summary(tmp_path) -> None:
    storage = MindgoDatasetStorage(tmp_path)

    summary = storage.partition_summary("stock_a_daily_price", ["trade_day"])

    assert summary.min_partition is None
    assert summary.max_partition is None
    assert summary.partition_count == 0
