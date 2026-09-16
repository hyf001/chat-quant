"""双击已揭示的日线看当日分时：接口语义 + 出口脱敏（设计方案 §5.7）。"""

from __future__ import annotations

from datetime import date

import pytest
from fastapi.testclient import TestClient
from tests.test_training_api import (
    SYMBOL,
    TRAINING_BARS,
    WARMUP_BARS,
    _create_adjust_factor_dataset,
    _create_price_dataset,
    _create_session,
    _create_snapshot_dataset,
    _dates,
    _reveal,
    _stop_engine,
)
from tests.test_training_masking import assert_masked

pytestmark = pytest.mark.usefixtures("project_test")

PRICE_BARS = 400
MINUTE_SOURCE_ID = "a_stock_minute_price"
#: 切片是 400 根价格的末端 240 根：切片第 i 根 ↔ 价格序列第 160 + i 根。
SLICE_OFFSET = PRICE_BARS - (WARMUP_BARS + TRAINING_BARS)
FIRST_TRAINING_BAR = WARMUP_BARS


@pytest.fixture(autouse=True)
def training_datasets(client: TestClient) -> None:
    _create_price_dataset(client)
    _create_adjust_factor_dataset(client)
    _create_snapshot_dataset(client)


def test_intraday_returns_revealed_day_minutes(client: TestClient) -> None:
    trade_day = _slice_date(FIRST_TRAINING_BAR)
    _create_minute_dataset(
        client,
        [
            (f"{trade_day.isoformat()} 09:31:00", 10.10, 1000.0),
            (f"{trade_day.isoformat()} 09:32:00", 10.20, 2000.0),
            (f"{trade_day.isoformat()} 09:33:00", 10.05, 1500.0),
        ],
    )
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200

    response = _intraday(client, session_id, seq=FIRST_TRAINING_BAR)

    assert response.status_code == 200, response.json()
    payload = response.json()
    assert_masked(payload)
    assert payload["available"] is True
    assert payload["session_id"] == session_id
    assert payload["seq"] == FIRST_TRAINING_BAR
    assert payload["bar"]["i"] == FIRST_TRAINING_BAR
    # 分时点只有时刻与价格：交易日只用来查数据，不进响应体
    assert payload["points"] == [
        {"t": "09:31", "p": 10.1, "v": 1000.0},
        {"t": "09:32", "p": 10.2, "v": 2000.0},
        {"t": "09:33", "p": 10.05, "v": 1500.0},
    ]
    # 基准是切片里前一根的 close（分时涨跌幅的昨收口径）
    assert float(payload["prev_close"]) == pytest.approx(_slice_close(FIRST_TRAINING_BAR - 1))
    assert trade_day.isoformat() not in response.text
    _stop_engine(session_id)


def test_intraday_only_accepts_revealed_bars(client: TestClient) -> None:
    session_id = _create_session(client)

    # 展示段是开局就给的前提：第 0 根与展示段最后一根都可看（只是没数据）
    assert _intraday(client, session_id, seq=0).status_code == 200
    assert _intraday(client, session_id, seq=WARMUP_BARS - 1).status_code == 200

    blocked = _intraday(client, session_id, seq=FIRST_TRAINING_BAR)
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["error_code"] == "TRAINING_INTRADAY_NOT_REVEALED"

    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200
    assert _intraday(client, session_id, seq=FIRST_TRAINING_BAR).status_code == 200
    assert _intraday(client, session_id, seq=FIRST_TRAINING_BAR + 1).status_code == 409
    assert _intraday(client, session_id, seq=PRICE_BARS).status_code == 409
    _stop_engine(session_id)


def test_intraday_survives_engine_recycle_and_early_finish(client: TestClient) -> None:
    trade_day = _slice_date(FIRST_TRAINING_BAR)
    _create_minute_dataset(client, [(f"{trade_day.isoformat()} 09:31:00", 10.10, 1000.0)])
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200

    # 引擎被回收（进程内句柄没了）时按窗口重装切片，仍旧给得出同一天的分时
    _stop_engine(session_id)
    reloaded = _intraday(client, session_id, seq=FIRST_TRAINING_BAR)
    assert reloaded.status_code == 200, reloaded.json()
    assert reloaded.json()["points"] == [{"t": "09:31", "p": 10.1, "v": 1000.0}]

    # 提前收局后仍然只覆盖已揭示的那一根
    finished = client.post(f"/api/training/sessions/{session_id}/finish")
    assert finished.status_code == 200, finished.json()
    assert _intraday(client, session_id, seq=FIRST_TRAINING_BAR).status_code == 200
    assert _intraday(client, session_id, seq=FIRST_TRAINING_BAR + 1).status_code == 409


def test_intraday_reports_unavailable_when_minutes_are_missing(client: TestClient) -> None:
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200

    # 分时数据集还没接入（默认这一局就没有分钟视图）：按"没有分时"返回，不报错
    missing_dataset = _intraday(client, session_id, seq=FIRST_TRAINING_BAR)
    assert missing_dataset.status_code == 200, missing_dataset.json()
    payload = missing_dataset.json()
    assert_masked(payload)
    assert payload["available"] is False
    assert payload["points"] == []
    assert payload["bar"]["i"] == FIRST_TRAINING_BAR

    # 数据集接入了，但这一根当天没有分钟数据
    another_day = _slice_date(0)
    _create_minute_dataset(client, [(f"{another_day.isoformat()} 09:31:00", 10.10, 1000.0)])
    empty_day = _intraday(client, session_id, seq=FIRST_TRAINING_BAR)
    assert empty_day.status_code == 200, empty_day.json()
    assert empty_day.json()["available"] is False
    assert empty_day.json()["points"] == []
    _stop_engine(session_id)


def test_intraday_requires_an_existing_session(client: TestClient) -> None:
    response = _intraday(client, "trn_missing", seq=0)

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "TRAINING_SESSION_NOT_FOUND"


def test_intraday_rejects_negative_seq(client: TestClient) -> None:
    session_id = _create_session(client)

    response = _intraday(client, session_id, seq=-1)

    assert response.status_code == 422
    _stop_engine(session_id)


# -- helpers ---------------------------------------------------------------


def _intraday(client: TestClient, session_id: str, *, seq: int):
    return client.get(
        f"/api/training/sessions/{session_id}/intraday",
        params={"seq": seq},
    )


def _slice_date(index: int) -> date:
    """切片第 ``index`` 根对应的交易日（价格序列与 test_training_api 同源）。"""
    return _dates(PRICE_BARS)[SLICE_OFFSET + index]


def _slice_close(index: int) -> float:
    return 10.0 + (SLICE_OFFSET + index + 1) * 0.05


def _create_minute_dataset(
    client: TestClient,
    rows: list[tuple[str, float, float]],
) -> None:
    values = ", ".join(
        f"('{SYMBOL}', '{stamp}', {price}, {volume})" for stamp, price, volume in rows
    )
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_minute",
            "name": MINUTE_SOURCE_ID,
            "description": "训练分时测试数据",
            "category_path": ["CN", "股票", "分钟", "训练分时"],
            "exposed_to_agent": False,
            "create_sql": (
                f"CREATE VIEW {MINUTE_SOURCE_ID} AS "
                "SELECT * FROM (VALUES "
                f"{values}"
                ") AS t(symbol, trade_date, close, volume)"
            ),
        },
    )
    assert response.status_code == 201, response.json()
