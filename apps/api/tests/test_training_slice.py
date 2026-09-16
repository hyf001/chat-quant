"""切片正确性：warmup / 训练段长度、末端对齐、除权过滤、只喂训练段（设计方案 §9.2）。"""

from __future__ import annotations

import random

import pytest
from app.service.training.slice_loader import (
    TrainingSliceError,
    load_slice_window,
    load_training_slice,
)
from fastapi.testclient import TestClient


def test_slice_is_random_length_and_anchored_to_dataset_end(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400)])
    _create_adjust_factor_dataset(client, [])

    training_slice = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=180,
        rng=random.Random(7),
    )

    assert training_slice.warmup_bars == 180
    assert 60 <= training_slice.training_bars <= 180
    assert len(training_slice.bars) == 180 + training_slice.training_bars
    assert len(training_slice.warmup) == 180
    assert len(training_slice.training) == training_slice.training_bars
    # 终点贴到数据末端
    assert training_slice.slice_end == training_slice.bars[-1].trade_date
    assert training_slice.bars[-1].trade_date == _dates(400)[-1]
    # warmup 与训练段连续不重叠
    assert training_slice.warmup[-1].trade_date < training_slice.training[0].trade_date
    # 只把训练段喂给 backtrader
    assert len(training_slice.training_frame()) == training_slice.training_bars


def test_slice_rejects_window_with_ex_dividend(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400)])
    # 窗口内因子发生变化（除权除息）
    _create_adjust_factor_dataset(
        client,
        [("600000.SH", _dates(400)[200], 1.0), ("600000.SH", _dates(400)[210], 2.0)],
    )

    with pytest.raises(TrainingSliceError) as raised:
        load_training_slice(
            warmup_bars=180,
            training_bars_min=60,
            training_bars_max=60,
            rng=random.Random(1),
        )

    assert raised.value.error_code == "TRAINING_SLICE_UNAVAILABLE"


def test_slice_accepts_window_without_factor_change(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400)])
    # 除权发生在窗口之前，不影响末端切片
    _create_adjust_factor_dataset(
        client,
        [
            ("600000.SH", _dates(400)[10], 1.0),
            ("600000.SH", _dates(400)[20], 2.0),
        ],
    )

    training_slice = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=60,
        rng=random.Random(1),
    )

    assert training_slice.symbol == "600000.SH"
    assert training_slice.training_bars == 60


def test_slice_reports_unavailable_without_enough_bars(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 100)])
    _create_adjust_factor_dataset(client, [])

    with pytest.raises(TrainingSliceError) as raised:
        load_training_slice(
            warmup_bars=180,
            training_bars_min=60,
            training_bars_max=60,
            rng=random.Random(1),
        )

    assert raised.value.error_code == "TRAINING_SLICE_UNAVAILABLE"


def test_slice_window_reload_matches_original(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400)])
    _create_adjust_factor_dataset(client, [])
    original = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=60,
        rng=random.Random(3),
    )

    reloaded = load_slice_window(
        symbol=original.symbol,
        slice_start=original.slice_start,
        slice_end=original.slice_end,
        warmup_bars=original.warmup_bars,
    )

    assert reloaded.training_bars == original.training_bars
    assert [bar.trade_date for bar in reloaded.bars] == [
        bar.trade_date for bar in original.bars
    ]


def test_slice_prefers_symbol_without_ex_dividend(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400), ("600001.SH", 400)])
    _create_adjust_factor_dataset(
        client,
        [("600000.SH", _dates(400)[200], 1.0), ("600000.SH", _dates(400)[210], 2.0)],
    )

    training_slice = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=60,
        rng=random.Random(5),
    )

    assert training_slice.symbol == "600001.SH"


def test_slice_excludes_st_symbols_when_asked(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400)])
    _create_adjust_factor_dataset(client, [])
    _create_snapshot_dataset(client, [("600000.SH", "*ST测试")])

    # 唯一的候选是 ST：打开开关就出不了题（前端提示重新出题 / 关掉开关）
    with pytest.raises(TrainingSliceError) as raised:
        load_training_slice(
            warmup_bars=180,
            training_bars_min=60,
            training_bars_max=60,
            exclude_st=True,
            rng=random.Random(1),
        )

    assert raised.value.error_code == "TRAINING_SLICE_UNAVAILABLE"
    assert raised.value.detail["exclude_st"] is True

    # 关掉开关就照常出题
    kept = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=60,
        exclude_st=False,
        rng=random.Random(1),
    )
    assert kept.symbol == "600000.SH"


def test_slice_picks_non_st_symbol_when_st_filter_is_on(client: TestClient) -> None:
    _create_price_dataset(client, [("600000.SH", 400), ("600001.SH", 400)])
    _create_adjust_factor_dataset(client, [])
    _create_snapshot_dataset(client, [("600000.SH", "ST测试"), ("600001.SH", "正常标的")])

    for seed in (1, 2, 3):
        training_slice = load_training_slice(
            warmup_bars=180,
            training_bars_min=60,
            training_bars_max=60,
            exclude_st=True,
            rng=random.Random(seed),
        )
        assert training_slice.symbol == "600001.SH"


def test_slice_keeps_st_symbols_when_snapshot_dataset_is_missing(client: TestClient) -> None:
    """快照数据集不在时不阻塞出题：ST 过滤退化成不过滤。"""
    _create_price_dataset(client, [("600000.SH", 400)])
    _create_adjust_factor_dataset(client, [])

    training_slice = load_training_slice(
        warmup_bars=180,
        training_bars_min=60,
        training_bars_max=60,
        exclude_st=True,
        rng=random.Random(1),
    )

    assert training_slice.symbol == "600000.SH"


def _create_snapshot_dataset(client: TestClient, rows: list[tuple[str, str]]) -> None:
    values = ", ".join(f"('{symbol}', '{name}')" for symbol, name in rows)
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_snapshot",
            "name": "a_stock_snapshot_info",
            "description": "训练标的名称测试数据",
            "category_path": ["A股", "股票", "快照", "信息维表"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_snapshot_info AS "
                "SELECT * FROM (VALUES "
                f"{values}"
                ") AS t(symbol, name)"
            ),
        },
    )
    assert response.status_code == 201, response.json()


def _dates(count: int) -> list:
    from datetime import date, timedelta

    start = date(2024, 1, 1)
    return [start + timedelta(days=index) for index in range(count)]


def _create_price_dataset(client: TestClient, symbols: list[tuple[str, int]]) -> None:
    rows: list[str] = []
    for symbol, count in symbols:
        for index, current in enumerate(_dates(count)):
            close = 10.0 + index * 0.05
            open_price = close - 0.02
            high = close * 1.01
            low = close * 0.99
            rows.append(
                f"('{symbol}', '{current.isoformat()}', '测试标的', "
                f"{open_price:.6f}, {high:.6f}, {low:.6f}, {close:.6f}, {100000 + index})"
            )
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_slice",
            "name": "a_stock_daily_price_unadjusted",
            "description": "训练切片测试数据",
            "category_path": ["CN", "股票", "日频", "训练行情"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_unadjusted AS "
                "SELECT * FROM (VALUES "
                f"{', '.join(rows)}"
                ") AS t(symbol, trade_date, name, open, high, low, close, volume)"
            ),
        },
    )
    assert response.status_code == 201, response.json()


def _create_adjust_factor_dataset(
    client: TestClient,
    rows: list[tuple[str, object, float]],
) -> None:
    values = ", ".join(
        f"('{symbol}', '{value.isoformat()}', '测试标的', {factor})"
        for symbol, value, factor in rows
    )
    if not values:
        values = "('__none__', '2024-01-01', '无', 1.0)"
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_adjust_factor",
            "name": "a_stock_daily_adjust_factor",
            "description": "训练复权因子测试数据",
            "category_path": ["CN", "股票", "日频", "复权因子"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_daily_adjust_factor AS "
                "SELECT * FROM (VALUES "
                f"{values}"
                ") AS t(symbol, trade_date, name, factor)"
            ),
        },
    )
    assert response.status_code == 201, response.json()
