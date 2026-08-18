import pandas as pd
import pytest
from app.service.backtest.execution import StrategyBacktestError
from app.service.backtest.market_data import (
    _normalize_dataset_benchmark_frame,
    _normalize_dataset_market_frame,
)


def test_normalize_dataset_market_frame_accepts_mapped_columns() -> None:
    frame = _normalize_dataset_market_frame(
        pd.DataFrame(
            [
                {
                    "datetime": "2024-01-02",
                    "open": "10",
                    "high": "11",
                    "low": "9",
                    "close": "10.5",
                    "volume": "1000",
                    "openinterest": 0,
                }
            ]
        ),
        symbol="600519.SH",
    )

    assert list(frame.columns) == ["open", "high", "low", "close", "volume", "openinterest"]
    assert frame.index[0].date().isoformat() == "2024-01-02"
    assert frame.iloc[0]["close"] == 10.5


def test_normalize_dataset_market_frame_rejects_missing_columns() -> None:
    with pytest.raises(StrategyBacktestError) as raised:
        _normalize_dataset_market_frame(
            pd.DataFrame([{"datetime": "2024-01-02", "close": 10.5}]),
            symbol="600519.SH",
        )

    assert raised.value.error_code == "BACKTEST_DATASET_FORMAT_INVALID"
    assert "open" in raised.value.detail["missing_columns"]


def test_normalize_dataset_benchmark_frame_accepts_close_series() -> None:
    frame = _normalize_dataset_benchmark_frame(
        pd.DataFrame(
            [
                {
                    "datetime": "2024-01-02",
                    "close": "3800.5",
                }
            ]
        ),
        symbol="000300.SH",
    )

    assert list(frame.columns) == ["close"]
    assert frame.index[0].date().isoformat() == "2024-01-02"
    assert frame.iloc[0]["close"] == 3800.5
