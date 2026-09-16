"""出口脱敏：训练期响应递归断言不含 symbol / name / 真实日期（设计方案 §9.2）。"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest
from app.service.training import masking

SENSITIVE_KEYS = ("symbol", "name", "trade_date", "date", "datetime")


def assert_masked(payload: object, path: str = "$") -> None:
    """递归断言：训练期响应里不允许出现任何敏感字段。"""
    leaks = masking.find_leaks(payload)
    assert leaks == [], f"训练期响应泄露了敏感字段: {leaks} ({path})"


def test_assert_masked_detects_nested_leak() -> None:
    assert_masked({"session": {"id": "trn_1"}, "bars": [{"i": 0, "o": 1.0}]})
    with pytest.raises(AssertionError):
        assert_masked({"session": {"symbol": "600000.SH"}})
    with pytest.raises(AssertionError):
        assert_masked({"bars": [{"i": 0}, {"trade_date": "2024-01-01"}]})


def test_bar_payload_only_exposes_index_and_prices() -> None:
    bar = SimpleNamespace(
        trade_date=date(2024, 1, 2),
        open=10.0,
        high=11.0,
        low=9.0,
        close=10.5,
        volume=1234.0,
    )

    payload = masking.bar_payload(7, bar)

    assert payload == {"i": 7, "o": 10.0, "h": 11.0, "l": 9.0, "c": 10.5, "v": 1234.0}
    assert_masked(payload)


def test_revealed_bar_payload_adds_real_date_only() -> None:
    bar = SimpleNamespace(
        trade_date=date(2024, 1, 2),
        open=10.0,
        high=11.0,
        low=9.0,
        close=10.5,
        volume=1234.0,
    )

    payload = masking.revealed_bar_payload(7, bar)

    assert payload["i"] == 7
    assert payload["date"] == "2024-01-02"
    assert payload["o"] == 10.0


def test_scrub_mapping_strips_sensitive_keys_recursively() -> None:
    scrubbed = masking.scrub_mapping(
        {
            "symbol": "600000.SH",
            "name": "浦发银行",
            "bars": [{"date": "2024-01-02", "close": 10.5, "nested": {"datetime": "x"}}],
            "keep": {"cash": 1000},
        }
    )

    assert scrubbed == {"bars": [{"close": 10.5, "nested": {}}], "keep": {"cash": 1000}}
    assert_masked(scrubbed)


def test_marker_payload_maps_fills_to_bs_markers() -> None:
    markers = masking.marker_payload(
        [
            {"i": 181, "side": "buy"},
            {"i": 190, "side": "sell"},
        ]
    )

    assert markers == [
        {"i": 181, "side": "buy", "text": "B"},
        {"i": 190, "side": "sell", "text": "S"},
    ]
    assert_masked(markers)
