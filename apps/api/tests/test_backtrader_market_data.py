from types import SimpleNamespace

import pandas as pd
from app.service.backtest.backtrader import (
    _fetch_cn_index_history,
    _fetch_cn_stock_history,
    _normalize_ohlcv_frame,
)


def test_normalize_ohlcv_frame_accepts_english_columns() -> None:
    frame = _normalize_ohlcv_frame(
        pd.DataFrame(
            [
                {
                    "date": "2024-01-02",
                    "open": "10",
                    "high": "11",
                    "low": "9",
                    "close": "10.5",
                    "volume": "1000",
                }
            ]
        )
    )

    assert list(frame.columns) == ["open", "high", "low", "close", "volume", "openinterest"]
    assert frame.index[0].date().isoformat() == "2024-01-02"
    assert frame.iloc[0]["close"] == 10.5


def test_normalize_ohlcv_frame_accepts_amount_as_volume() -> None:
    frame = _normalize_ohlcv_frame(
        pd.DataFrame(
            [
                {
                    "date": "2024-01-02",
                    "open": "10",
                    "high": "11",
                    "low": "9",
                    "close": "10.5",
                    "amount": "1000",
                }
            ]
        )
    )

    assert frame.iloc[0]["volume"] == 1000


def test_fetch_cn_stock_history_falls_back_to_tx_source() -> None:
    def failing_hist(**_: object) -> pd.DataFrame:
        raise ConnectionError("remote closed")

    def tx_hist(**_: object) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "date": "2024-01-02",
                    "open": 10,
                    "high": 11,
                    "low": 9,
                    "close": 10.5,
                    "volume": 1000,
                }
            ]
        )

    ak = SimpleNamespace(
        stock_zh_a_hist=failing_hist,
        stock_zh_a_hist_tx=tx_hist,
        stock_zh_a_daily=failing_hist,
    )

    frame = _fetch_cn_stock_history(
        ak=ak,
        symbol="600519.SH",
        normalized_symbol="600519",
        start_date="20240101",
        end_date="20240110",
        adjust="qfq",
    )

    assert not frame.empty
    assert list(frame.columns) == ["date", "open", "high", "low", "close", "volume"]


def test_fetch_cn_index_history_falls_back_to_tx_source() -> None:
    def failing_hist(**_: object) -> pd.DataFrame:
        raise ConnectionError("eastmoney closed")

    def tx_hist(**_: object) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "date": "2024-01-02",
                    "open": 10,
                    "high": 11,
                    "low": 9,
                    "close": 10.5,
                    "amount": 1000,
                }
            ]
        )

    ak = SimpleNamespace(
        index_zh_a_hist=failing_hist,
        stock_zh_index_daily_tx=tx_hist,
    )

    frame = _fetch_cn_index_history(
        ak=ak,
        symbol="000300.SH",
        normalized_symbol="000300",
        start_date="20240101",
        end_date="20240110",
    )

    assert not frame.empty
    assert list(frame.columns) == ["date", "open", "high", "low", "close", "amount"]
