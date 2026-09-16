"""训练闭环集成：开局 → reveal → 下单 → 下一根成交 → finish → report（设计方案 §9）。"""

from __future__ import annotations

import json
import threading
from datetime import date, datetime, timedelta
from decimal import Decimal

import pandas as pd
import pytest
from app.model.training import TrainingSessionRow
from app.service.training.service import _floor_shares
from app.service.training.train_adapter import run_backtrader_training
from app.service.training.transport import InMemoryTrainingSignalTransport
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as SyncSession
from tests.test_training_masking import assert_masked

pytestmark = pytest.mark.usefixtures("project_test")

WARMUP_BARS = 180
TRAINING_BARS = 60
SYMBOL = "600000.SH"
SYMBOL_NAME = "测试标的"
COMMISSION = Decimal("0.0005")


@pytest.fixture(autouse=True)
def training_datasets(client: TestClient) -> None:
    _create_price_dataset(client)
    _create_adjust_factor_dataset(client)
    _create_snapshot_dataset(client)


def test_training_session_full_loop(client: TestClient) -> None:
    created = client.post(
        "/api/training/sessions",
        json={"project_id": "project_test", "config": _config()},
    )

    assert created.status_code == 201, created.json()
    start = created.json()
    assert_masked(start)
    session = start["session"]
    session_id = session["id"]
    assert session_id.startswith("trn_")
    assert session["status"] == "active"
    assert session["instrument_alias"] == "标的A"
    assert session["warmup_bars"] == WARMUP_BARS
    assert session["training_bars"] == TRAINING_BARS
    assert session["cursor_index"] == 0
    assert session["remaining"] == TRAINING_BARS
    assert session["account"]["cash"] == "100000.00"
    assert session["account"]["total_return"] == "0.0000"
    assert [bar["i"] for bar in start["bars"]] == list(range(WARMUP_BARS))

    # 开局看完 warmup 立刻买入（半仓）：市价单按**本根 close**成交，同一响应里就能
    # 看到成交与成交后的账户，没有"等下一根"的挂单。
    first = _reveal(client, session_id, seq=0, action="buy", size=0.5)
    assert first.status_code == 200, first.json()
    first_payload = first.json()
    assert_masked(first_payload)
    assert first_payload["bar"]["i"] == WARMUP_BARS
    assert first_payload["session"]["cursor_index"] == 1
    assert len(first_payload["fills"]) == 1
    fill = first_payload["fills"][0]
    # 成交价 == 这一根的 close（滑点关掉时）
    assert fill["i"] == WARMUP_BARS
    assert float(fill["price"]) == pytest.approx(first_payload["bar"]["c"], rel=1e-9)
    assert first_payload["markers"] == [{"i": WARMUP_BARS, "side": "buy", "text": "B"}]
    # 账户就是 broker 成交后的值：持仓与成交股数一致，现金扣掉了这笔
    assert float(first_payload["session"]["account"]["position_size"]) == fill["size"]
    assert Decimal(first_payload["session"]["account"]["cash"]) < Decimal("100000")

    second = _reveal(client, session_id, seq=1, action="hold")
    assert second.status_code == 200, second.json()
    second_payload = second.json()
    assert_masked(second_payload)
    assert second_payload["bar"]["i"] == WARMUP_BARS + 1
    assert second_payload["fills"] == []

    for seq in range(2, TRAINING_BARS):
        response = _reveal(client, session_id, seq=seq, action="hold")
        assert response.status_code == 200, response.json()

    last = response.json()
    assert_masked(last)
    assert last["session"]["cursor_index"] == TRAINING_BARS
    assert last["session"]["remaining"] == 0
    # 最后一根揭示完就自动收局：不用再点一次收局按钮
    assert last["session"]["status"] == "finished"

    # 自动收局后复盘报告直接可查（不用先 POST /finish）
    auto_report = client.get(f"/api/training/sessions/{session_id}/report")
    assert auto_report.status_code == 200, auto_report.json()
    assert auto_report.json()["session"]["status"] == "finished"
    assert len(auto_report.json()["report"]["bars"]) == WARMUP_BARS + TRAINING_BARS

    # 收局之后不再接受 reveal
    exhausted = _reveal(client, session_id, seq=TRAINING_BARS, action="hold")
    assert exhausted.status_code == 409
    assert exhausted.json()["detail"]["error_code"] == "TRAINING_SESSION_FINISHED"

    # finish 是幂等的：已自动收局的会话再收一次仍然给报告
    finished = client.post(f"/api/training/sessions/{session_id}/finish")
    assert finished.status_code == 200, finished.json()
    report_payload = finished.json()
    assert report_payload["instrument"] == {
        "symbol": SYMBOL,
        "name": SYMBOL_NAME,
        "instrument_alias": "标的A",
    }
    assert report_payload["window"]["warmup_bars"] == WARMUP_BARS
    assert report_payload["window"]["training_bars"] == TRAINING_BARS
    assert report_payload["session"]["status"] == "finished"

    metrics = report_payload["report"]["metrics"]
    # finish 不替用户平仓：持仓保持，期末权益 = 现金 + 持仓 × 最后一根 close。
    assert metrics["position_size"] == fill["size"]
    expected_value = (
        Decimal(last["session"]["account"]["cash"])
        + Decimal(str(metrics["position_size"])) * Decimal(str(last["bar"]["c"]))
    )
    assert Decimal(metrics["final_value"]) == pytest.approx(
        expected_value.quantize(Decimal("0.01")), abs=Decimal("0.05")
    )
    assert metrics["total_trades"] == 0
    assert metrics["win_rate_pct"] is None
    assert "backtrader" in metrics["settlement_note"]
    assert report_payload["report"]["equity_curve"]["point_count"] == TRAINING_BARS
    assert len(report_payload["report"]["bars"]) == WARMUP_BARS + TRAINING_BARS
    assert report_payload["report"]["fills"][0]["price"] == fill["price"]

    # 复盘接口：收局后可重复取
    report = client.get(f"/api/training/sessions/{session_id}/report")
    assert report.status_code == 200, report.json()
    assert report.json()["report"]["metrics"]["final_value"] == metrics["final_value"]

    # 收局后不能再推进
    after_finish = _reveal(client, session_id, seq=TRAINING_BARS, action="hold")
    assert after_finish.status_code == 409
    assert after_finish.json()["detail"]["error_code"] == "TRAINING_SESSION_FINISHED"

    # 每条事件 = 一次点击 = 一根推进
    assert _event_count(session_id) == TRAINING_BARS


def test_reveal_rejects_stale_seq(client: TestClient) -> None:
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200

    conflict = _reveal(client, session_id, seq=0, action="hold")

    assert conflict.status_code == 409
    detail = conflict.json()["detail"]
    assert detail["error_code"] == "TRAINING_REVEAL_SEQ_CONFLICT"
    assert detail["expected_seq"] == 1


def test_report_requires_finished_session(client: TestClient) -> None:
    session_id = _create_session(client)

    response = client.get(f"/api/training/sessions/{session_id}/report")

    assert response.status_code == 409
    assert response.json()["detail"]["error_code"] == "TRAINING_SESSION_ACTIVE"


def test_missing_session_returns_not_found(client: TestClient) -> None:
    response = client.get("/api/training/sessions/trn_missing")

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "TRAINING_SESSION_NOT_FOUND"


def test_finish_early_keeps_the_same_finished_state(client: TestClient) -> None:
    """走到最后一根之前点"提前结束"：与自动收局落到同一个状态与同一份报告。"""
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="buy", size=0.5).status_code == 200

    finished = client.post(f"/api/training/sessions/{session_id}/finish")

    assert finished.status_code == 200, finished.json()
    payload = finished.json()
    assert payload["session"]["status"] == "finished"
    # 提前结束不动已揭示的进度：只结算到当前游标
    assert payload["session"]["cursor_index"] == 1
    assert payload["session"]["remaining"] == TRAINING_BARS - 1
    assert payload["report"]["metrics"]["position_size"] > 0

    # 收局后既不能再推进，也不能再收一次以外地改状态
    assert _reveal(client, session_id, seq=1, action="hold").status_code == 409
    resumed = client.get("/api/training/sessions", params={"project_id": "project_test"})
    listed = {item["id"]: item for item in resumed.json()["items"]}
    assert listed[session_id]["status"] == "finished"
    assert listed[session_id]["finished_at"] is not None

    _stop_engine(session_id)


def test_finish_releases_the_engine_handle(client: TestClient) -> None:
    """收局就把注册表里的引擎摘掉：线程该退了，整局快照也不必再留着。"""
    from app.service.training.engine_manager import training_engine_manager

    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200
    assert session_id in training_engine_manager.active_sessions()

    finished = client.post(f"/api/training/sessions/{session_id}/finish")

    assert finished.status_code == 200, finished.json()
    assert session_id not in training_engine_manager.active_sessions()

    # 复盘仍然可读：句柄没了就按 training_events 重新 replay 一份出来
    report = client.get(f"/api/training/sessions/{session_id}/report")
    assert report.status_code == 200, report.json()
    assert session_id not in training_engine_manager.active_sessions()


def test_engine_recycler_drops_self_exited_engines(client: TestClient) -> None:
    """引擎自退（空闲超时那类）之后没人访问它：定时回收要能把条目清掉。"""
    from app.service.training.engine_manager import training_engine_manager
    from app.service.training.recycler import TrainingEngineRecycler

    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="hold").status_code == 200
    handle = training_engine_manager.get(session_id)
    assert handle is not None

    # 模拟"线程自己退了、但没人再来 acquire 顺手 prune"的残留
    handle.transport.request_stop()
    handle.join(timeout=10)
    assert not handle.is_alive()
    assert session_id in training_engine_manager.active_sessions()

    recycled = TrainingEngineRecycler().recycle_once()

    assert session_id in recycled
    assert session_id not in training_engine_manager.active_sessions()


def test_buy_is_rejected_when_cash_is_insufficient(client: TestClient) -> None:
    session_id = _create_session(client, initial_cash="5")

    response = _reveal(client, session_id, seq=0, action="buy", size=1.0)

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "TRAINING_BROKER_REJECTED"
    # 拒单不写事件：游标不动，前端可以按可用资金重下。
    assert _event_count(session_id) == 0
    current = client.get(f"/api/training/sessions/{session_id}").json()
    assert current["session"]["cursor_index"] == 0


def test_full_position_buy_settles_at_the_close_without_leftover_cash(
    client: TestClient,
) -> None:
    """全仓买入按本根 close 成交，股数按同一个价换算：现金用干净、不会因跳空被拒。"""
    session_id = _create_session(client)

    response = _reveal(client, session_id, seq=0, action="buy", size=1.0)

    assert response.status_code == 200, response.json()
    payload = response.json()
    assert payload["rejected"] == []
    assert len(payload["fills"]) == 1
    fill = payload["fills"][0]
    assert float(fill["price"]) == pytest.approx(payload["bar"]["c"], rel=1e-9)
    account = payload["session"]["account"]
    assert float(account["position_size"]) == fill["size"]
    # 剩下的钱不够按成交价再买一手（含手续费），但也不能是负数
    assert Decimal("0") <= Decimal(account["cash"]) < Decimal(fill["price"]) * Decimal("1.001")
    assert payload["session"]["cursor_index"] == 1

    _stop_engine(session_id)


def test_session_resumes_from_event_history(client: TestClient) -> None:
    session_id = _create_session(client)
    assert _reveal(client, session_id, seq=0, action="buy", size=0.5).status_code == 200
    second = _reveal(client, session_id, seq=1, action="hold")
    assert second.status_code == 200, second.json()
    before_account = second.json()["session"]["account"]

    # 模拟引擎回收：丢掉内存引擎，再按 training_events replay 重建。
    from app.service.training.engine_manager import training_engine_manager

    training_engine_manager.discard(session_id)

    resumed = client.get(f"/api/training/sessions/{session_id}")

    assert resumed.status_code == 200, resumed.json()
    payload = resumed.json()
    assert_masked(payload)
    assert payload["session"]["cursor_index"] == 2
    assert len(payload["bars"]) == WARMUP_BARS + 2
    assert payload["markers"] == [{"i": WARMUP_BARS, "side": "buy", "text": "B"}]
    # replay 出来的账户与当时逐字段一致（事件是唯一真相）
    assert payload["session"]["account"] == before_account

    # 续做：继续推进仍然对得上游标与成交
    third = _reveal(client, session_id, seq=2, action="hold")
    assert third.status_code == 200, third.json()
    assert third.json()["bar"]["i"] == WARMUP_BARS + 2


def test_list_sessions_reports_progress_without_leaks(client: TestClient) -> None:
    first_id = _create_session(client)
    assert _reveal(client, first_id, seq=0, action="hold").status_code == 200
    assert _reveal(client, first_id, seq=1, action="hold").status_code == 200
    finished_id = _create_session(client)
    assert client.post(f"/api/training/sessions/{finished_id}/finish").status_code == 200

    response = _list_sessions(client)

    assert response.status_code == 200, response.json()
    payload = response.json()
    assert_masked(payload)
    assert payload["total"] == 2
    listed = {item["id"]: item for item in payload["items"]}
    assert set(listed) == {first_id, finished_id}

    active = listed[first_id]
    assert active["status"] == "active"
    assert active["instrument_alias"] == "标的A"
    assert active["initial_cash"] == "100000.00"
    assert active["warmup_bars"] == WARMUP_BARS
    # 进度直接来自 training_events 的行数，不需要重建引擎
    assert active["cursor_index"] == 2
    assert active["training_bars"] == TRAINING_BARS
    assert active["remaining"] == TRAINING_BARS - 2
    assert active["finished_at"] is None
    assert active["elapsed_seconds"] >= 0

    finished = listed[finished_id]
    assert finished["status"] == "finished"
    assert finished["cursor_index"] == 0
    assert finished["remaining"] == TRAINING_BARS
    assert finished["finished_at"] is not None

    _stop_engine(first_id)


def test_list_sessions_scopes_project_orders_and_pages(client: TestClient) -> None:
    first_id = _create_session(client)
    second_id = _create_session(client)
    other = client.post(
        "/api/training/sessions",
        json={"project_id": "project_other", "config": _config()},
    )
    assert other.status_code == 201, other.json()

    other_id = other.json()["session"]["id"]

    scoped = _list_sessions(client)
    assert scoped.status_code == 200, scoped.json()
    assert [item["id"] for item in scoped.json()["items"]] == [second_id, first_id]
    assert scoped.json()["total"] == 2

    page = _list_sessions(client, limit=1, offset=1)
    assert page.status_code == 200, page.json()
    assert page.json()["total"] == 2
    assert [item["id"] for item in page.json()["items"]] == [first_id]

    empty = _list_sessions(client, offset=5)
    assert empty.status_code == 200, empty.json()
    assert empty.json() == {"items": [], "total": 2}

    other_project = _list_sessions(client, project_id="project_other")
    assert other_project.json()["total"] == 1

    for session_id in (first_id, second_id, other_id):
        _stop_engine(session_id)


def test_list_sessions_requires_project_id(client: TestClient) -> None:
    assert client.get("/api/training/sessions").status_code == 422
    assert client.get("/api/training/sessions", params={"project_id": ""}).status_code == 422


def test_list_sessions_filters_by_status_and_id(client: TestClient) -> None:
    active_id = _create_session(client)
    finished_id = _create_session(client)
    assert client.post(f"/api/training/sessions/{finished_id}/finish").status_code == 200

    active_only = _list_sessions(client, status="active")
    assert active_only.status_code == 200, active_only.json()
    assert active_only.json()["total"] == 1
    assert [item["id"] for item in active_only.json()["items"]] == [active_id]

    finished_only = _list_sessions(client, status="finished")
    assert finished_only.status_code == 200, finished_only.json()
    assert finished_only.json()["total"] == 1
    assert [item["id"] for item in finished_only.json()["items"]] == [finished_id]

    # 关键字命中会话 ID，total 也跟着筛选走
    matched = _list_sessions(client, keyword=active_id)
    assert matched.status_code == 200, matched.json()
    assert matched.json()["total"] == 1
    assert [item["id"] for item in matched.json()["items"]] == [active_id]

    # 筛选与分页叠加：命中的那一条不在这一页时只回空列表，total 仍是筛选后的总数
    paged = _list_sessions(client, limit=1, offset=1)
    assert paged.status_code == 200, paged.json()
    assert paged.json()["total"] == 2
    assert len(paged.json()["items"]) == 1

    blank = _list_sessions(client, keyword="   ")
    assert blank.status_code == 200, blank.json()
    assert blank.json()["total"] == 2

    miss = _list_sessions(client, keyword="trn_nope")
    assert miss.status_code == 200, miss.json()
    assert miss.json() == {"items": [], "total": 0}

    assert _list_sessions(client, status="paused").status_code == 422

    _stop_engine(active_id)


def test_list_sessions_tolerates_legacy_rows_without_resolved_bars(
    client: TestClient,
) -> None:
    """早期会话的 config_json 没有切片长度：列表退化成"已推进 N 根"，不报错。"""
    _insert_legacy_session("trn_legacy")

    response = _list_sessions(client)

    assert response.status_code == 200, response.json()
    item = next(row for row in response.json()["items"] if row["id"] == "trn_legacy")
    assert item["status"] == "finished"
    assert item["cursor_index"] == 0
    assert item["training_bars"] is None
    assert item["remaining"] is None
    assert item["warmup_bars"] == WARMUP_BARS


def test_account_exposes_backtrader_position_and_cash(client: TestClient) -> None:
    """买入的同一响应里就能看到 backtrader 的持仓：股数 / 均价 / 市值 + 剩余可用资金。"""
    session_id = _create_session(client)
    opened = _reveal(client, session_id, seq=0, action="buy", size=0.5)

    assert opened.status_code == 200, opened.json()
    payload = opened.json()
    fill = payload["fills"][0]
    account = payload["session"]["account"]
    bar = payload["bar"]

    assert account["position_size"] == fill["size"]
    assert Decimal(account["position_price"]) == pytest.approx(
        Decimal(fill["price"]), abs=Decimal("0.0001")
    )
    assert Decimal(account["position_value"]) == pytest.approx(
        Decimal(str(bar["c"])) * Decimal(str(fill["size"])), abs=Decimal("0.01")
    )
    # 半仓买入之后仍然有可用资金，且现金 + 市值 = 总权益
    assert Decimal(account["cash"]) > 0

    _stop_engine(session_id)


def test_sell_by_ratio_can_reduce_then_clear_the_position(client: TestClient) -> None:
    session_id = _create_session(client)
    opened = _reveal(client, session_id, seq=0, action="buy", size=0.5)
    assert opened.status_code == 200, opened.json()
    position = opened.json()["session"]["account"]["position_size"]
    assert position > 0

    # 卖 1/3：卖出的股数按持仓的 1/3 向下取整，本根 close 成交、同一响应可见
    partial = _reveal(client, session_id, seq=1, action="sell", size=1 / 3)
    assert partial.status_code == 200, partial.json()
    sold = partial.json()["fills"][0]["size"]
    assert sold == pytest.approx(position / 3, abs=1)
    remaining = partial.json()["session"]["account"]["position_size"]
    assert remaining == pytest.approx(position - sold, abs=1)

    # 全仓卖：持仓清零，现金回到账上
    closed = _reveal(client, session_id, seq=2, action="sell", size=1.0)
    assert closed.status_code == 200, closed.json()
    assert closed.json()["fills"][0]["size"] == pytest.approx(remaining, abs=1)
    account = closed.json()["session"]["account"]
    assert account["position_size"] == 0.0
    assert account["position_price"] == "0"
    assert account["position_value"] == "0.00"
    assert Decimal(account["cash"]) > Decimal("0")

    _stop_engine(session_id)


def test_sell_by_ratio_then_full_sell_never_shorts(client: TestClient) -> None:
    """先卖 1/2 再卖全仓：两笔各自在本根 close 成交，卖出总量正好等于持仓，不多卖一股。"""
    session_id = _create_session(client)
    opened = _reveal(client, session_id, seq=0, action="buy", size=0.5)
    assert opened.status_code == 200, opened.json()
    position = opened.json()["session"]["account"]["position_size"]
    assert position > 0

    half = _reveal(client, session_id, seq=1, action="sell", size=0.5)
    assert half.status_code == 200, half.json()
    half_size = half.json()["fills"][0]["size"]
    remaining = half.json()["session"]["account"]["position_size"]
    assert half_size == pytest.approx(position / 2, abs=1)
    assert remaining == pytest.approx(position - half_size, abs=1)

    # 全仓卖：按"这一根响应里的持仓"换算股数，正好清仓
    clear = _reveal(client, session_id, seq=2, action="sell", size=1.0)
    assert clear.status_code == 200, clear.json()
    assert _event_size(session_id, 2) == pytest.approx(remaining, abs=1)
    assert clear.json()["fills"][0]["size"] == pytest.approx(remaining, abs=1)
    assert clear.json()["session"]["account"]["position_size"] == 0.0

    # 空仓之后再点卖出：直接拒掉，不写事件、不推进游标
    rejected = _reveal(client, session_id, seq=3, action="sell", size=1.0)
    assert rejected.status_code == 422, rejected.json()
    assert rejected.json()["detail"]["error_code"] == "TRAINING_BROKER_REJECTED"
    assert _event_count(session_id) == 3

    _stop_engine(session_id)


def test_full_position_buy_twice_is_rejected_for_insufficient_cash(
    client: TestClient,
) -> None:
    """全仓买入当场成交后资金已经用尽：再点全仓买入会被拒，不会重复满仓。"""
    session_id = _create_session(client)

    first = _reveal(client, session_id, seq=0, action="buy", size=1.0)
    assert first.status_code == 200, first.json()
    position = first.json()["session"]["account"]["position_size"]
    assert position > 0

    second = _reveal(client, session_id, seq=1, action="buy", size=1.0)

    assert second.status_code == 422, second.json()
    assert second.json()["detail"]["error_code"] == "TRAINING_BROKER_REJECTED"
    assert _event_count(session_id) == 1

    _stop_engine(session_id)


def test_adapter_clamps_sell_to_the_live_position() -> None:
    """引擎侧兜底：卖出按 broker 的实时持仓封顶，历史事件 replay 也卖不出空头。"""
    frame = _frame(6)
    transport = InMemoryTrainingSignalTransport(idle_ttl_seconds=30)
    result: dict[str, object] = {}
    thread = threading.Thread(
        target=lambda: result.update(
            run_backtrader_training(
                frame=frame,
                symbol="TEST.SH",
                initial_cash=100000.0,
                commission=0.0005,
                transport=transport,
                bar_offset=180,
            )
        ),
        daemon=True,
    )
    thread.start()

    transport.send_action(
        {"action": "buy", "symbol": "TEST.SH", "order_type": "market", "size": 100}
    )
    first = transport.wait_bar(0, timeout=10)
    # 提交的那一根就成交了：没有挂单，持仓与成交价都是这一根的值
    assert first["position_size"] == 100
    assert first["fills"][0]["size"] == 100
    assert first["fills"][0]["price"] == pytest.approx(float(frame.iloc[0]["close"]))

    # 第 1 根上卖 40：同样本根成交，持仓剩 60
    transport.send_action(
        {"action": "sell", "symbol": "TEST.SH", "order_type": "market", "size": 40}
    )
    sold = transport.wait_bar(1, timeout=10)
    assert sold["position_size"] == 60

    # 第 2 根上再卖 100（历史事件里可能存着满仓卖）：持仓只剩 60，超出的部分被夹掉
    transport.send_action(
        {"action": "sell", "symbol": "TEST.SH", "order_type": "market", "size": 100}
    )
    settled = transport.wait_bar(2, timeout=10)
    assert settled["fills"][0]["size"] == 60
    assert settled["position_size"] == 0
    tracked = [transport.snapshot(index) or {} for index in transport.bar_indices()]
    assert all(float(snapshot.get("position_size") or 0.0) >= 0 for snapshot in tracked)

    # 持仓已经清零：再来的卖单整单拒掉，不会开空仓
    transport.send_action(
        {"action": "sell", "symbol": "TEST.SH", "order_type": "market", "size": 10}
    )
    after = transport.wait_bar(3, timeout=10)
    assert after["position_size"] == 0
    assert [item["status"] for item in after["rejections"]] == ["oversell"]

    transport.request_stop()
    thread.join(5)
    assert not thread.is_alive()


def test_floor_shares_removes_float_noise() -> None:
    """1/3、1/5 这类档位换算成无限小数：300 股的 1/3 必须是 100 股，不能是 99。"""
    assert _floor_shares(300 * (1 / 3)) == 100
    assert _floor_shares(500 * (1 / 5)) == 100
    assert _floor_shares(99.9) == 99


def test_slippage_moves_fill_price_against_the_close(client: TestClient) -> None:
    """滑点打开时：买入成交价 = 本根 close ×(1+滑点)，且越不过当根 high。"""
    session_id = _create_session(client, slippage="0.01")

    response = _reveal(client, session_id, seq=0, action="buy", size=0.5)

    assert response.status_code == 200, response.json()
    payload = response.json()
    bar = payload["bar"]
    fill = payload["fills"][0]
    assert float(fill["price"]) == pytest.approx(bar["c"] * 1.01, abs=0.0001)
    assert float(fill["price"]) > float(bar["c"])
    assert float(fill["price"]) <= float(bar["h"])

    _stop_engine(session_id)


def test_session_config_defaults_show_up_in_report_note(client: TestClient) -> None:
    """不传的可选项走产品默认：手续费 0.0005、滑点 0.001、剔除 ST。"""
    created = client.post(
        "/api/training/sessions",
        json={
            "project_id": "project_test",
            "config": {
                "warmup_bars": WARMUP_BARS,
                "training_bars_min": TRAINING_BARS,
                "training_bars_max": TRAINING_BARS,
                "initial_cash": "100000",
            },
        },
    )
    assert created.status_code == 201, created.json()
    session_id = created.json()["session"]["id"]

    report = client.post(f"/api/training/sessions/{session_id}/finish")

    assert report.status_code == 200, report.json()
    note = report.json()["report"]["metrics"]["settlement_note"]
    assert "手续费 0.0005（0.05%）" in note
    assert "滑点 0.001（0.1%）" in note
    assert "已剔除 ST 标的" in note


def test_adapters_drive_without_http_and_only_feed_training_segment() -> None:
    """分层边界：train_adapter 脱离 HTTP / 数据库也能驱动出正确的账户与成交序列。"""
    frame = _frame(5)
    transport = InMemoryTrainingSignalTransport(idle_ttl_seconds=30)
    result: dict[str, object] = {}
    thread = threading.Thread(
        target=lambda: result.update(
            run_backtrader_training(
                frame=frame,
                symbol="TEST.SH",
                initial_cash=100000.0,
                commission=0.0005,
                transport=transport,
                bar_offset=180,
            )
        ),
        daemon=True,
    )
    thread.start()

    transport.send_action(
        {"action": "buy", "symbol": "TEST.SH", "order_type": "market", "size": 100}
    )
    first = transport.wait_bar(0, timeout=10)
    # 提交的那一根就成交（coc）：快照里已经是从 backtrader 拿到的持仓与这笔成交
    assert first["i"] == 180
    assert first["position_size"] == 100
    assert first["fills"][0]["size"] == 100
    assert first["fills"][0]["price"] == pytest.approx(float(frame.iloc[0]["close"]))
    assert first["fills"][0]["i"] == 180

    for index in (1, 2):
        transport.send_action(None)
        settled = transport.wait_bar(index, timeout=10)
        assert settled["i"] == 180 + index
        assert settled["fills"] == []

    second = transport.snapshot(1)
    assert second is not None
    assert second["position_size"] == 100

    # 收局：引擎在等第 3 根时被叫停，处理过的根仍然有效
    transport.request_stop()
    thread.join(5)
    assert not thread.is_alive()
    assert result["stopped"] is True
    # data feed 只包含训练段：喂进来 5 根，结算点也从 0 开始数，没有 warmup 的份
    assert transport.bar_indices() == [0, 1, 2]
    assert len(result["orders"]) == 1
    assert result["orders"][0]["side"] == "buy"
    assert result["closed_trades"] == []


def test_session_defaults_when_config_is_omitted(client: TestClient) -> None:
    response = client.post(
        "/api/training/sessions",
        json={"project_id": "project_test"},
    )

    assert response.status_code == 201, response.json()
    session = response.json()["session"]
    assert session["warmup_bars"] == 180
    assert 60 <= session["training_bars"] <= 180
    assert session["account"]["initial_cash"] == "100000.00"


# -- helpers ---------------------------------------------------------------


def _config(*, initial_cash: str = "100000", slippage: str = "0") -> dict[str, object]:
    # 滑点默认关掉：这一层断言的是"第 t+1 根 open 成交"的下标对齐，滑点在下面单测。
    return {
        "warmup_bars": WARMUP_BARS,
        "training_bars_min": TRAINING_BARS,
        "training_bars_max": TRAINING_BARS,
        "initial_cash": initial_cash,
        "commission": str(COMMISSION),
        "slippage": slippage,
        "idle_ttl_seconds": 1800,
    }


def _create_session(
    client: TestClient,
    *,
    initial_cash: str = "100000",
    slippage: str = "0",
) -> str:
    response = client.post(
        "/api/training/sessions",
        json={
            "project_id": "project_test",
            "config": _config(initial_cash=initial_cash, slippage=slippage),
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()["session"]["id"]


def _stop_engine(session_id: str) -> None:
    """收掉这一局的引擎线程，别让测试结束时还挂着一个等信号的线程。"""
    from app.service.training.engine_manager import training_engine_manager

    training_engine_manager.discard(session_id)


def _list_sessions(client: TestClient, *, project_id: str = "project_test", **query: object):
    return client.get("/api/training/sessions", params={"project_id": project_id, **query})


def _reveal(
    client: TestClient,
    session_id: str,
    *,
    seq: int,
    action: str,
    size: float | None = None,
):
    payload: dict[str, object] = {"seq": seq, "action": action}
    if size is not None:
        payload["size"] = size
    return client.post(f"/api/training/sessions/{session_id}/reveal", json=payload)


def _event_size(session_id: str, seq: int) -> float:
    """直接读这一条事件里落库的股数：断言服务端换算出来的下单量。"""
    from app.core.config import get_settings

    engine = create_engine(f"sqlite:///{get_settings().database_path}")
    try:
        with engine.begin() as connection:
            row = connection.execute(
                text(
                    "SELECT payload_json FROM training_events "
                    "WHERE session_id = :id AND seq = :seq"
                ),
                {"id": session_id, "seq": seq},
            ).fetchone()
            assert row is not None
            return float(json.loads(row[0])["size"])
    finally:
        engine.dispose()


def _event_count(session_id: str) -> int:
    from app.core.config import get_settings
    from sqlalchemy import text

    engine = create_engine(f"sqlite:///{get_settings().database_path}")
    try:
        with engine.begin() as connection:
            row = connection.execute(
                text("SELECT COUNT(*) FROM training_events WHERE session_id = :id"),
                {"id": session_id},
            ).fetchone()
            return int(row[0])
    finally:
        engine.dispose()


def _insert_legacy_session(session_id: str) -> None:
    """模拟改动前落库的会话行：config_json 里只有参数，没有切出来的训练段长度。"""
    from app.core.config import get_settings

    engine = create_engine(f"sqlite:///{get_settings().database_path}")
    now = datetime.now()
    try:
        with SyncSession(engine) as session:
            session.add(
                TrainingSessionRow(
                    id=session_id,
                    project_id="project_test",
                    mode="daily",
                    period="1d",
                    symbol=SYMBOL,
                    name=SYMBOL_NAME,
                    slice_start=date(2024, 1, 1),
                    slice_end=date(2024, 6, 30),
                    warmup_bars=WARMUP_BARS,
                    status="finished",
                    initial_cash=Decimal("100000"),
                    config_json={
                        "warmup_bars": WARMUP_BARS,
                        "training_bars_min": TRAINING_BARS,
                        "training_bars_max": TRAINING_BARS,
                        "initial_cash": "100000",
                        "commission": str(COMMISSION),
                        "idle_ttl_seconds": 1800,
                    },
                    started_at=now,
                    finished_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            session.commit()
    finally:
        engine.dispose()


def _frame(count: int) -> pd.DataFrame:
    rows = []
    price = 10.0
    for index in range(count):
        price = price * 1.01
        rows.append(
            {
                "datetime": pd.Timestamp("2024-01-01") + pd.Timedelta(days=index),
                "open": price,
                "high": price * 1.01,
                "low": price * 0.99,
                "close": price * 1.005,
                "volume": 1000.0 + index,
                "openinterest": 0.0,
            }
        )
    return pd.DataFrame(rows).set_index("datetime")


def _dates(count: int) -> list[date]:
    start = date(2024, 1, 1)
    return [start + timedelta(days=index) for index in range(count)]


def _price_rows(count: int = 400) -> str:
    rows: list[str] = []
    previous_close = 10.0
    for index, current in enumerate(_dates(count)):
        open_price = previous_close
        close = 10.0 + (index + 1) * 0.05
        previous_close = close
        rows.append(
            f"('{SYMBOL}', '{current.isoformat()}', '{SYMBOL_NAME}', "
            f"{open_price:.6f}, {close * 1.01:.6f}, {close * 0.99:.6f}, {close:.6f}, "
            f"{100000 + index})"
        )
    return ", ".join(rows)


def _create_price_dataset(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_price",
            "name": "a_stock_daily_price_unadjusted",
            "description": "训练行情测试数据",
            "category_path": ["CN", "股票", "日频", "训练行情"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_unadjusted AS "
                "SELECT * FROM (VALUES "
                f"{_price_rows()}"
                ") AS t(symbol, trade_date, name, open, high, low, close, volume)"
            ),
        },
    )
    assert response.status_code == 201, response.json()


def _create_adjust_factor_dataset(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "id": "ds_training_factor",
            "name": "a_stock_daily_adjust_factor",
            "description": "训练复权因子测试数据",
            "category_path": ["CN", "股票", "日频", "复权因子"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_daily_adjust_factor AS "
                "SELECT * FROM (VALUES "
                f"('{SYMBOL}', '{_dates(1)[0].isoformat()}', '{SYMBOL_NAME}', 1.0)"
                ") AS t(symbol, trade_date, name, factor)"
            ),
        },
    )
    assert response.status_code == 201, response.json()


def _create_snapshot_dataset(client: TestClient) -> None:
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
                f"SELECT '{SYMBOL}' AS symbol, '{SYMBOL_NAME}' AS name"
            ),
        },
    )
    assert response.status_code == 201, response.json()
