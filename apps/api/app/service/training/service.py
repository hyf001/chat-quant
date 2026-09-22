"""训练会话生命周期编排（设计方案 §4.2 / §5）。

分工：

* **K 线由 service 揭示**：按 ``cursor`` 从开局那份切片里取"下一根"，走 masking 后返回；
* **账户与成交由引擎产出**：service 把动作交给引擎，在结算点拿 broker 快照；
* **落库与审计也在 service**：请求进来先校验 ``seq`` → 写一条 ``training_events`` →
  把动作交给引擎 → 组装响应。空闲回收后的 replay 同样由这里驱动。
"""

from __future__ import annotations

import asyncio
import math
from datetime import date, datetime
from decimal import Decimal
from random import Random
from typing import Any
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.training import TrainingEventRow, TrainingSessionRow
from app.schema.training import (
    DEFAULT_COMMISSION,
    DEFAULT_IDLE_TTL_SECONDS,
    DEFAULT_SLIPPAGE,
    DEFAULT_TRAINING_BARS_MAX,
    DEFAULT_TRAINING_BARS_MIN,
    DEFAULT_WARMUP_BARS,
    TrainingAccount,
    TrainingBar,
    TrainingClosedTrade,
    TrainingCurve,
    TrainingCurvePoint,
    TrainingEventType,
    TrainingFill,
    TrainingInstrument,
    TrainingIntradayPoint,
    TrainingIntradayResponse,
    TrainingMetrics,
    TrainingOrderRejection,
    TrainingReport,
    TrainingReportResponse,
    TrainingRevealedBar,
    TrainingRevealRequest,
    TrainingRevealResponse,
    TrainingSessionConfig,
    TrainingSessionCreate,
    TrainingSessionListResponse,
    TrainingSessionResponse,
    TrainingSessionStatus,
    TrainingSessionSummary,
    TrainingSessionView,
    TrainingWindow,
)
from app.service.chatq_engine import (
    drawdown_analysis,
    equity_returns,
    quantize,
    sharpe_ratio,
    win_rate_pct,
)
from app.service.market_data.minute_price import load_minute_prices
from app.service.strategy.protocol import validate_chatq_action
from app.service.training import masking
from app.service.training.engine_manager import (
    TrainingEngineHandle,
    training_engine_manager,
)
from app.service.training.slice_loader import (
    TrainingSlice,
    TrainingSliceError,
    load_slice_window,
    load_training_slice,
)
from app.service.training.transport import (
    TrainingTransportFailed,
    TrainingTransportTimeout,
)

SETTLEMENT_NOTE = (
    "撮合口径为 backtrader 通用多资产口径：点击后按这一根的收盘价成交，"
    "无 T+1 / 无涨跌停 / 无整手 / 无印花税与最低佣金；收局不强制平仓，"
    "持仓按最后一根 close 计入期末权益。"
)
ALLOWED_EVENT_TYPES = {item.value for item in TrainingEventType}


class TrainingError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class TrainingService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    # -- 开局 -------------------------------------------------------------

    async def create_session(self, payload: TrainingSessionCreate) -> TrainingSessionResponse:
        config = payload.config or TrainingSessionConfig()
        try:
            training_slice = await asyncio.to_thread(
                load_training_slice,
                warmup_bars=config.warmup_bars,
                training_bars_min=config.training_bars_min,
                training_bars_max=config.training_bars_max,
                exclude_st=config.exclude_st,
                rng=Random(),
            )
        except TrainingSliceError as error:
            raise _slice_error(error) from error

        now = datetime.now()
        session_id = _new_id("trn")
        row = TrainingSessionRow(
            id=session_id,
            project_id=payload.project_id,
            mode=payload.mode,
            period=payload.period,
            symbol=training_slice.symbol,
            name=training_slice.name,
            slice_start=training_slice.slice_start,
            slice_end=training_slice.slice_end,
            warmup_bars=training_slice.warmup_bars,
            status=TrainingSessionStatus.ACTIVE.value,
            initial_cash=Decimal(str(config.initial_cash)),
            config_json=_config_payload(config, training_bars=training_slice.training_bars),
            started_at=now,
            finished_at=None,
            created_at=now,
            updated_at=now,
        )
        self._db.add(row)
        await self._db.commit()

        handle = await self._acquire_engine(row, training_slice=training_slice, events=[])
        return TrainingSessionResponse(
            session=self._session_view(row, handle=handle, cursor=0),
            bars=[
                _bar_payload(training_slice, index) for index in range(training_slice.warmup_bars)
            ],
            markers=[],
        )

    # -- 查询 -------------------------------------------------------------

    async def get_session(self, session_id: str) -> TrainingSessionResponse:
        row = await self._require_session(session_id)
        events = await self._load_events(session_id)
        handle = await self._acquire_engine(row, events=events)
        cursor = len(events)
        handle.transport.touch()
        return TrainingSessionResponse(
            session=self._session_view(row, handle=handle, cursor=cursor),
            bars=self._revealed_bars(handle.training_slice, cursor),
            markers=masking.marker_payload(handle.transport.fills()),
        )

    async def list_sessions(
        self,
        project_id: str,
        *,
        status: str | None = None,
        keyword: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TrainingSessionListResponse:
        """项目下的训练列表：不重建引擎，进度直接按 ``training_events`` 的行数算。

        ``status`` 与 ``keyword``(会话 ID，前缀/片段匹配) 都是可选筛选，``total``
        跟着筛选走，这样前端的"第 N 页 / 共 M 条"始终自洽。
        """
        filters = [TrainingSessionRow.project_id == project_id]
        if status is not None:
            filters.append(TrainingSessionRow.status == status)
        needle = (keyword or "").strip()
        if needle:
            filters.append(TrainingSessionRow.id.contains(needle, autoescape=True))
        total = await self._db.scalar(
            select(func.count()).select_from(TrainingSessionRow).where(*filters)
        )
        rows = list(
            await self._db.scalars(
                select(TrainingSessionRow)
                .where(*filters)
                .order_by(TrainingSessionRow.created_at.desc(), TrainingSessionRow.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        cursors = await self._reveal_counts([row.id for row in rows])
        return TrainingSessionListResponse(
            total=int(total or 0),
            items=[_summary_payload(row, cursor=cursors.get(row.id, 0)) for row in rows],
        )

    # -- 推进一根 ---------------------------------------------------------

    async def reveal(
        self,
        session_id: str,
        payload: TrainingRevealRequest,
    ) -> TrainingRevealResponse:
        row = await self._require_session(session_id)
        if row.status == TrainingSessionStatus.FINISHED.value:
            raise TrainingError(
                "TRAINING_SESSION_FINISHED",
                "会话已结束，只能查看复盘报告",
                409,
            )

        events = await self._load_events(session_id)
        cursor = len(events)
        if payload.seq != cursor:
            raise TrainingError(
                "TRAINING_REVEAL_SEQ_CONFLICT",
                "客户端游标与服务端不一致，请先拉取当前状态",
                409,
                detail={"expected_seq": cursor, "received_seq": payload.seq},
            )

        handle = await self._acquire_engine(row, events=events)
        training_slice = handle.training_slice
        config = _config_from_row(row)
        if cursor >= training_slice.training_bars:
            raise TrainingError(
                "TRAINING_SESSION_FINISHED",
                "训练段已走完，只能收局",
                409,
                detail={"cursor_index": cursor, "training_bars": training_slice.training_bars},
            )

        snapshot = handle.latest_snapshot() or _initial_snapshot(training_slice, row)
        # 点击作用于当前已经展示的最后一根 K 线，并在其尾盘成交；撮合完成后，响应
        # 再揭示下一根。这样用户看到哪根就交易哪根，不会把成交标到未来 K 线上。
        fill_index = training_slice.warmup_bars - 1 + cursor
        fill_bar = training_slice.bar(fill_index)
        action = _build_action(
            payload=payload,
            symbol=row.symbol,
            fill_close=fill_bar.close,
            fill_high=fill_bar.high,
            snapshot=snapshot,
            config=config,
        )

        event_payload = (
            {**action, "_training_fill_index": fill_index}
            if action is not None
            else {
                "action": TrainingEventType.HOLD.value,
                "reason": payload.reason,
                "_training_fill_index": fill_index,
            }
        )
        event = TrainingEventRow(
            id=_new_id("tre"),
            session_id=session_id,
            seq=cursor,
            event_type=payload.action,
            payload_json=event_payload,
            created_at=datetime.now(),
        )
        self._db.add(event)
        await self._db.commit()

        try:
            settled = await asyncio.to_thread(
                handle.send_and_wait,
                cursor,
                action,
            )
        except (TrainingTransportTimeout, TrainingTransportFailed) as error:
            raise _engine_error(error) from error

        now = datetime.now()
        row.updated_at = now
        if cursor + 1 >= training_slice.training_bars:
            # 最后一根揭示完就自动收局："结束揭晓"这个按钮因此只承担"提前结束"。
            # 引擎那边正好把训练段跑完（下一根不存在），分析器结果已经就绪，
            # 随后 GET /report 直接可用。
            row.status = TrainingSessionStatus.FINISHED.value
            row.finished_at = now
        await self._db.commit()

        bar_index = training_slice.warmup_bars + cursor
        return TrainingRevealResponse(
            session=self._session_view(
                row,
                handle=handle,
                cursor=cursor + 1,
                snapshot=settled,
            ),
            bar=_bar_payload(training_slice, bar_index),
            markers=masking.marker_payload(handle.transport.fills()),
            fills=[_fill_payload(item) for item in settled.get("fills", [])],
            rejected=[
                TrainingOrderRejection(
                    i=int(item.get("i", fill_index)),
                    side="buy" if item.get("side") == "buy" else "sell",
                    size=round(float(item.get("size") or 0.0), 6),
                    reason=str(item.get("status") or "rejected"),
                )
                for item in settled.get("rejections", [])
            ],
        )

    # -- 收局 / 复盘 -------------------------------------------------------

    async def finish(self, session_id: str) -> TrainingReportResponse:
        """提前结束（或幂等地收掉已经自动结束的那一局）。"""
        row = await self._require_session(session_id)
        if row.status != TrainingSessionStatus.FINISHED.value:
            now = datetime.now()
            row.status = TrainingSessionStatus.FINISHED.value
            row.finished_at = now
            row.updated_at = now
            await self._db.commit()
        return await self._build_report(row)

    async def report(self, session_id: str) -> TrainingReportResponse:
        row = await self._require_session(session_id)
        if row.status != TrainingSessionStatus.FINISHED.value:
            raise TrainingError(
                "TRAINING_SESSION_ACTIVE",
                "会话还没结束，收局后才能查看复盘报告",
                409,
            )
        return await self._build_report(row)

    # -- 当日分时 ---------------------------------------------------------

    async def intraday(self, session_id: str, *, seq: int) -> TrainingIntradayResponse:
        """双击第 ``seq`` 根日线：把那一根的分钟走势取出来（只有已揭示的根可看）。

        分时不需要引擎：序号 → 交易日的映射由切片给出（引擎还活着就直接用它手里那份
        切片，否则按窗口重装），随后按交易日读分钟数据。出口不带日期，X 轴是 ``HH:MM``。
        """
        row = await self._require_session(session_id)
        cursor = len(await self._load_events(session_id))
        revealed_bars = row.warmup_bars + cursor
        if seq < 0 or seq >= revealed_bars:
            raise TrainingError(
                "TRAINING_INTRADAY_NOT_REVEALED",
                "这一根还没揭示，看不了分时",
                409,
                detail={"seq": seq, "revealed_bars": revealed_bars},
            )

        training_slice = await self._slice_for_row(row)
        if seq >= len(training_slice.bars):
            raise TrainingError(
                "TRAINING_INTRADAY_NOT_REVEALED",
                "这一根还没揭示，看不了分时",
                409,
                detail={"seq": seq, "revealed_bars": min(revealed_bars, len(training_slice.bars))},
            )

        bar = training_slice.bar(seq)
        previous = training_slice.bar(seq - 1) if seq > 0 else None
        points = await asyncio.to_thread(
            load_minute_prices,
            row.symbol,
            bar.trade_date,
        )
        return TrainingIntradayResponse(
            session_id=row.id,
            seq=seq,
            available=bool(points),
            bar=_bar_payload(training_slice, seq),
            prev_close=None if previous is None else quantize(previous.close),
            points=[
                TrainingIntradayPoint(t=item.minute, p=item.price, v=item.volume) for item in points
            ],
        )

    async def _build_report(self, row: TrainingSessionRow) -> TrainingReportResponse:
        events = await self._load_events(row.id)
        config = _config_from_row(row)
        handle = await self._acquire_engine(row, events=events)
        try:
            result = await asyncio.to_thread(handle.stop_and_collect)
        except (TrainingTransportTimeout, TrainingTransportFailed) as error:
            raise _engine_error(error) from error

        training_slice = handle.training_slice
        cursor = len(events)
        snapshots = [snapshot for snapshot in handle.snapshots() if snapshot]
        initial_cash = Decimal(str(row.initial_cash))

        equity_points = []
        for snapshot in snapshots:
            # 快照产生在当前可见 K 线的尾盘；同一响应随后揭示下一根，所以账户和复盘
            # 曲线都按新揭示 K 线的 close 做市值计价，与页面统计栏保持一致。
            valuation_index = min(int(snapshot["i"]) + 1, len(training_slice.bars) - 1)
            valuation_bar = training_slice.bar(valuation_index)
            equity_points.append(
                {
                    "i": valuation_index,
                    "date": valuation_bar.trade_date,
                    "value": quantize(
                        Decimal(str(snapshot["cash"]))
                        + Decimal(str(snapshot["position_size"]))
                        * Decimal(str(valuation_bar.close))
                    ),
                }
            )
        if not equity_points:
            initial_index = max(0, training_slice.warmup_bars - 1)
            equity_points = [
                {
                    "i": initial_index,
                    "date": training_slice.bar(initial_index).trade_date,
                    "value": initial_cash,
                }
            ]

        final_point = equity_points[-1]
        final_value = Decimal(str(final_point["value"]))
        last_index = min(
            training_slice.warmup_bars + cursor - 1,
            len(training_slice.bars) - 1,
        )
        last_bar = training_slice.bar(last_index)
        last_snapshot = snapshots[-1] if snapshots else _initial_snapshot(training_slice, row)
        position_size = float(last_snapshot["position_size"])
        position_price = last_snapshot.get("position_price")

        total_return = (
            (final_value / initial_cash - Decimal("1")) * Decimal("100")
            if initial_cash
            else Decimal("0")
        )
        open_return = (
            (Decimal(str(last_bar.close)) / Decimal(str(position_price)) - Decimal("1"))
            * Decimal("100")
            if position_size and position_price
            else Decimal("0")
        )
        position_value = Decimal(str(last_bar.close)) * Decimal(str(position_size))
        position_pct = (
            position_value / final_value * Decimal("100") if final_value else Decimal("0")
        )
        closed_trades = [item for item in result.get("closed_trades", []) if isinstance(item, dict)]
        realized_pnl = sum((Decimal(str(item["pnl"])) for item in closed_trades), Decimal("0"))
        unrealized_pnl = (
            (Decimal(str(last_bar.close)) - Decimal(str(position_price)))
            * Decimal(str(position_size))
            if position_size and position_price
            else Decimal("0")
        )
        max_drawdown, drawdown_start, drawdown_end, drawdown_points = drawdown_analysis(
            equity_points
        )
        win_rate = win_rate_pct(closed_trades)
        finished_at = row.finished_at or datetime.now()

        report = TrainingReport(
            metrics=TrainingMetrics(
                initial_cash=quantize(initial_cash, "0.01"),
                final_value=quantize(final_value, "0.01"),
                total_return_pct=quantize(total_return),
                realized_pnl=quantize(realized_pnl, "0.01"),
                unrealized_pnl=quantize(unrealized_pnl, "0.01"),
                open_return_pct=quantize(open_return),
                position_size=round(position_size, 6),
                position_pct=quantize(position_pct),
                max_drawdown_pct=quantize(max_drawdown),
                max_drawdown_start=drawdown_start,
                max_drawdown_end=drawdown_end,
                sharpe_ratio=_quantize_optional(sharpe_ratio(equity_returns(equity_points))),
                win_rate_pct=_quantize_optional(win_rate),
                total_trades=len(closed_trades),
                duration_seconds=max(0, int((finished_at - row.started_at).total_seconds())),
                settlement_note=_settlement_note(config),
            ),
            equity_curve=_curve("equity", equity_points),
            drawdown_curve=_curve("drawdown", drawdown_points),
            bars=self._report_bars(training_slice, cursor),
            markers=masking.marker_payload(handle.transport.fills()),
            fills=[_fill_payload(item) for item in handle.transport.fills()],
            closed_trades=[
                TrainingClosedTrade(
                    date=item["date"].isoformat()
                    if isinstance(item.get("date"), date)
                    else str(item.get("date")),
                    size=round(float(item.get("size") or 0.0), 6),
                    price=quantize(item.get("price") or 0),
                    value=quantize(item.get("value") or 0, "0.01"),
                    pnl=quantize(item.get("pnl") or 0, "0.01"),
                    pnl_pct=_quantize_optional(item.get("pnl_pct")),
                )
                for item in closed_trades
            ],
        )
        try:
            return TrainingReportResponse(
                session=self._session_view(
                    row, handle=handle, cursor=cursor, snapshot=last_snapshot
                ),
                instrument=TrainingInstrument(
                    symbol=row.symbol,
                    name=row.name,
                    instrument_alias=masking.instrument_alias(),
                ),
                window=TrainingWindow(
                    start_date=training_slice.slice_start,
                    end_date=last_bar.trade_date,
                    warmup_bars=training_slice.warmup_bars,
                    training_bars=training_slice.training_bars,
                ),
                report=report,
            )
        finally:
            # 收局后引擎线程已经退出：顺手把注册表条目摘掉，别把整局快照留到进程结束
            # （下次读复盘会按 training_events 重新 replay，事件是唯一真相）。
            training_engine_manager.discard(row.id)

    # -- 内部 -------------------------------------------------------------

    async def _require_session(self, session_id: str) -> TrainingSessionRow:
        row = await self._db.get(TrainingSessionRow, session_id)
        if row is None:
            raise TrainingError(
                "TRAINING_SESSION_NOT_FOUND",
                "训练会话不存在",
                404,
                detail={"session_id": session_id},
            )
        return row

    async def _load_events(self, session_id: str) -> list[TrainingEventRow]:
        rows = await self._db.scalars(
            select(TrainingEventRow)
            .where(TrainingEventRow.session_id == session_id)
            .order_by(TrainingEventRow.seq)
        )
        return list(rows)

    async def _reveal_counts(self, session_ids: list[str]) -> dict[str, int]:
        """一次点击 = 一条事件 = 一根推进，所以事件行数就是游标。"""
        if not session_ids:
            return {}
        rows = await self._db.execute(
            select(TrainingEventRow.session_id, func.count())
            .where(TrainingEventRow.session_id.in_(session_ids))
            .group_by(TrainingEventRow.session_id)
        )
        return {str(session_id): int(count) for session_id, count in rows.all()}

    async def _acquire_engine(
        self,
        row: TrainingSessionRow,
        *,
        events: list[TrainingEventRow],
        training_slice: TrainingSlice | None = None,
    ) -> TrainingEngineHandle:
        config = _config_from_row(row)
        actions = [_event_action(event) for event in events]
        # 新事件会明确记录实际成交 K 线。没有该字段的是旧版事件，仍按旧的“下一根”
        # 索引重放；重放完以后追加当前可见 K 线（可能与上一根重复），让旧会话也能
        # 从下一次点击起平滑切换到当前尾盘成交，而不会改写历史账户状态。
        bar_indices = [_event_fill_index(event, row.warmup_bars) for event in events]
        bar_indices.extend(
            row.warmup_bars - 1 + seq
            for seq in range(len(events), int(_resolved_training_bars(row) or 0))
        )
        try:
            return await asyncio.to_thread(
                training_engine_manager.acquire,
                session_id=row.id,
                slice_factory=lambda: (
                    training_slice
                    or load_slice_window(
                        symbol=row.symbol,
                        slice_start=row.slice_start,
                        slice_end=row.slice_end,
                        warmup_bars=row.warmup_bars,
                    )
                ),
                initial_cash=float(row.initial_cash),
                commission=float(config.commission),
                slippage=float(config.slippage),
                idle_ttl_seconds=float(config.idle_ttl_seconds),
                actions=actions,
                bar_indices=bar_indices,
            )
        except TrainingSliceError as error:
            raise _slice_error(error) from error
        except (TrainingTransportTimeout, TrainingTransportFailed) as error:
            raise _engine_error(error) from error

    async def _slice_for_row(self, row: TrainingSessionRow) -> TrainingSlice:
        """序号 → 交易日只认切片：引擎还在就直接借用它手里那份，否则按窗口重装。

        分时是只读的旁路，不 acquire 引擎——那会为了一次查看把整局 replay 起来。
        """
        handle = training_engine_manager.get(row.id)
        if handle is not None and handle.is_alive():
            return handle.training_slice
        try:
            return await asyncio.to_thread(
                load_slice_window,
                symbol=row.symbol,
                slice_start=row.slice_start,
                slice_end=row.slice_end,
                warmup_bars=row.warmup_bars,
            )
        except TrainingSliceError as error:
            raise _slice_error(error) from error

    def _session_view(
        self,
        row: TrainingSessionRow,
        *,
        handle: TrainingEngineHandle,
        cursor: int,
        snapshot: dict[str, Any] | None = None,
    ) -> TrainingSessionView:
        training_slice = handle.training_slice
        training_bars = training_slice.training_bars
        index = min(cursor, training_bars)
        latest = snapshot or handle.latest_snapshot()
        if latest is None:
            latest = _initial_snapshot(training_slice, row)
        close_index = min(
            training_slice.warmup_bars + index - 1,
            len(training_slice.bars) - 1,
        )
        return TrainingSessionView(
            id=row.id,
            status=row.status,
            instrument_alias=masking.instrument_alias(),
            started_at=row.started_at,
            elapsed_seconds=_elapsed_seconds(row),
            warmup_bars=training_slice.warmup_bars,
            training_bars=training_bars,
            cursor_index=index,
            remaining=max(0, training_bars - index),
            account=_account_payload(
                row=row,
                snapshot=latest,
                close=training_slice.bar(close_index).close,
            ),
        )

    def _revealed_bars(self, training_slice: TrainingSlice, cursor: int) -> list[TrainingBar]:
        return [
            _bar_payload(training_slice, index)
            for index in self._revealed_indices(training_slice, cursor)
        ]

    @staticmethod
    def _revealed_indices(training_slice: TrainingSlice, cursor: int) -> range:
        return range(training_slice.warmup_bars + min(cursor, training_slice.training_bars))

    def _report_bars(self, training_slice: TrainingSlice, cursor: int) -> list[TrainingRevealedBar]:
        return [
            masking.revealed_bar_payload(index, training_slice.bar(index))
            for index in self._revealed_indices(training_slice, cursor)
        ]


# -- 纯函数 ---------------------------------------------------------------


def _settlement_note(config: TrainingSessionConfig) -> str:
    """报告里带上本局生效的成本口径与出题过滤，避免"默认值是多少"说不清。"""
    st_note = "已剔除 ST 标的" if config.exclude_st else "未剔除 ST 标的"
    return (
        f"{SETTLEMENT_NOTE}"
        f"本局口径：手续费 {_rate_text(config.commission)}，滑点 {_rate_text(config.slippage)}，"
        f"{st_note}。"
    )


def _rate_text(value: Decimal) -> str:
    return f"{value}（{(value * 100).normalize():f}%）"


def _config_payload(
    config: TrainingSessionConfig,
    *,
    training_bars: int | None = None,
) -> dict[str, object]:
    """会话参数 + 开局时定下来的切片长度（列表页据此算进度，不重建引擎）。"""
    return {
        "warmup_bars": config.warmup_bars,
        "training_bars_min": config.training_bars_min,
        "training_bars_max": config.training_bars_max,
        "initial_cash": str(config.initial_cash),
        "commission": str(config.commission),
        "slippage": str(config.slippage),
        "exclude_st": config.exclude_st,
        "idle_ttl_seconds": config.idle_ttl_seconds,
        "training_bars": training_bars,
    }


def _resolved_training_bars(row: TrainingSessionRow) -> int | None:
    payload = row.config_json if isinstance(row.config_json, dict) else {}
    value = payload.get("training_bars")
    if value is None:
        return None
    try:
        bars = int(value)
    except (TypeError, ValueError):
        return None
    return bars if bars > 0 else None


def _summary_payload(row: TrainingSessionRow, *, cursor: int) -> TrainingSessionSummary:
    training_bars = _resolved_training_bars(row)
    index = cursor if training_bars is None else min(cursor, training_bars)
    return TrainingSessionSummary(
        id=row.id,
        status=row.status,
        instrument_alias=masking.instrument_alias(),
        initial_cash=quantize(row.initial_cash, "0.01"),
        started_at=row.started_at,
        finished_at=row.finished_at,
        elapsed_seconds=_elapsed_seconds(row),
        warmup_bars=row.warmup_bars,
        training_bars=training_bars,
        cursor_index=index,
        remaining=None if training_bars is None else max(0, training_bars - index),
    )


def _config_from_row(row: TrainingSessionRow) -> TrainingSessionConfig:
    payload = row.config_json if isinstance(row.config_json, dict) else {}
    return TrainingSessionConfig(
        warmup_bars=int(payload.get("warmup_bars", row.warmup_bars or DEFAULT_WARMUP_BARS)),
        training_bars_min=int(payload.get("training_bars_min", DEFAULT_TRAINING_BARS_MIN)),
        training_bars_max=int(payload.get("training_bars_max", DEFAULT_TRAINING_BARS_MAX)),
        initial_cash=Decimal(str(payload.get("initial_cash", row.initial_cash))),
        commission=Decimal(str(payload.get("commission", DEFAULT_COMMISSION))),
        slippage=Decimal(str(payload.get("slippage", DEFAULT_SLIPPAGE))),
        exclude_st=bool(payload.get("exclude_st", True)),
        idle_ttl_seconds=int(payload.get("idle_ttl_seconds", DEFAULT_IDLE_TTL_SECONDS)),
    )


def _initial_snapshot(training_slice: TrainingSlice, row: TrainingSessionRow) -> dict[str, Any]:
    del training_slice
    return {
        "i": -1,
        "cash": float(row.initial_cash),
        "value": float(row.initial_cash),
        "position_size": 0.0,
        "position_price": None,
        "fills": [],
        "rejections": [],
    }


def _event_action(event: TrainingEventRow) -> dict[str, Any] | None:
    payload = event.payload_json if isinstance(event.payload_json, dict) else {}
    if event.event_type in {TrainingEventType.HOLD.value, TrainingEventType.CANCEL.value}:
        return None
    if not payload:
        return None
    return {key: value for key, value in payload.items() if key != "_training_fill_index"}


def _event_fill_index(event: TrainingEventRow, warmup_bars: int) -> int:
    payload = event.payload_json if isinstance(event.payload_json, dict) else {}
    stored = payload.get("_training_fill_index")
    if stored is not None:
        try:
            return int(stored)
        except (TypeError, ValueError):
            pass
    # 兼容修复前已经落库的会话：旧动作撮合在 warmup + seq。
    return warmup_bars + int(event.seq)


def _build_action(
    *,
    payload: TrainingRevealRequest,
    symbol: str,
    fill_close: float,
    fill_high: float,
    snapshot: dict[str, Any],
    config: TrainingSessionConfig,
) -> dict[str, Any] | None:
    """仓位比例 → 股数（向下取整），只有市价单。

    ``snapshot`` 是引擎在上一根结算点给出的 broker 快照（现金 / 持仓都是 backtrader
    的原值）。市价单按当前可见 K 线的 close 成交（``set_coc(True)``）；买入时把
    Backtrader 的不利滑点和手续费完整算入每股成本，保证服务层验资与 broker 一致。
    """
    if payload.action in {TrainingEventType.HOLD.value, TrainingEventType.CANCEL.value}:
        return None
    if payload.action == TrainingEventType.BUY.value:
        ratio = float(payload.size if payload.size is not None else 1.0)
        cash = float(snapshot.get("cash") or 0.0)
        # Backtrader 的买入滑点为 close × (1 + slip)，并受当根 high 封顶；股票佣金
        # 再按实际成交金额计算。这里使用同一公式，不能把滑点和佣金简单相加近似。
        execution_price = min(
            float(fill_high),
            float(fill_close) * (1.0 + float(config.slippage)),
        )
        per_share_cost = execution_price * (1.0 + float(config.commission))
        shares = _floor_shares(cash * ratio / per_share_cost)
        if shares < 1:
            raise TrainingError(
                "TRAINING_BROKER_REJECTED",
                "可用资金不足，无法按该比例买入",
                422,
                detail={
                    "reason": "insufficient_cash",
                    "available_cash": cash,
                    "reference_price": execution_price,
                    "ratio": ratio,
                },
            )
        return validate_chatq_action(
            {
                "action": "buy",
                "symbol": symbol,
                "order_type": "market",
                "size": int(shares),
                "ref": _new_id("trf"),
                "reason": payload.reason or f"training_buy_{ratio:g}",
            }
        )

    position_size = float(snapshot.get("position_size") or 0.0)
    if position_size < 1:
        raise TrainingError(
            "TRAINING_BROKER_REJECTED",
            "当前没有可卖出的持仓",
            422,
            detail={"reason": "no_position", "position_size": position_size},
        )
    ratio = float(payload.size if payload.size is not None else 1.0)
    shares = _floor_shares(position_size * ratio)
    if shares < 1:
        shares = 1
    return validate_chatq_action(
        {
            "action": "close" if payload.action == TrainingEventType.CLOSE.value else "sell",
            "symbol": symbol,
            "order_type": "market",
            "size": int(min(shares, int(position_size))),
            "ref": _new_id("trf"),
            "reason": payload.reason or f"training_{payload.action}_{ratio:g}",
        }
    )


def _floor_shares(value: float) -> int:
    """按份数向下取整，先抹掉浮点噪声。

    1/3、1/5 这类档位换算过来是无限小数，直接 ``floor`` 会在 300 股的整数倍上
    少 1 股（300 × 1/3 = 99.999...）；先四舍五入到 6 位小数再取整即可。
    买入侧的多算量远小于预留的佣金 + 滑点缓冲，不会把"全仓"挤成拒单。
    """
    return math.floor(round(value, 6))


def _account_payload(
    *,
    row: TrainingSessionRow,
    snapshot: dict[str, Any],
    close: float,
) -> TrainingAccount:
    initial_cash = Decimal(str(row.initial_cash))
    cash = Decimal(str(snapshot.get("cash") or 0.0))
    position_size = float(snapshot.get("position_size") or 0.0)
    position_price = snapshot.get("position_price")
    position_value = Decimal(str(close)) * Decimal(str(position_size))
    equity = cash + position_value
    total_return = (
        (equity / initial_cash - Decimal("1")) * Decimal("100") if initial_cash else Decimal("0")
    )
    open_return = (
        (Decimal(str(close)) / Decimal(str(position_price)) - Decimal("1")) * Decimal("100")
        if position_size and position_price
        else Decimal("0")
    )
    position_pct = (
        Decimal(str(close)) * Decimal(str(position_size)) / equity * Decimal("100")
        if equity
        else Decimal("0")
    )
    return TrainingAccount(
        initial_cash=quantize(initial_cash, "0.01"),
        cash=quantize(cash, "0.01"),
        position_size=round(position_size, 6),
        position_price=quantize(position_price) if position_price else Decimal("0"),
        position_value=quantize(position_value, "0.01"),
        position_pct=quantize(position_pct),
        total_return=quantize(total_return),
        open_return=quantize(open_return),
    )


def _bar_payload(training_slice: TrainingSlice, index: int) -> TrainingBar:
    bar = training_slice.bar(index)
    return TrainingBar(**masking.bar_payload(index, bar))


def _fill_payload(item: dict[str, Any]) -> TrainingFill:
    return TrainingFill(
        i=int(item.get("i", 0)),
        side="buy" if item.get("side") == "buy" else "sell",
        price=quantize(item.get("price") or 0),
        size=round(float(item.get("size") or 0.0), 6),
        value=quantize(item.get("value") or 0, "0.01"),
        commission=quantize(item.get("commission") or 0, "0.01"),
    )


def _curve(curve_type: str, points: list[dict[str, Any]]) -> TrainingCurve:
    return TrainingCurve(
        curve_type=curve_type,
        point_count=len(points),
        points=[
            TrainingCurvePoint(
                i=int(point.get("i", index)),
                date=point["date"].isoformat()
                if isinstance(point.get("date"), date)
                else (str(point["date"]) if point.get("date") is not None else None),
                value=quantize(point.get("value") or 0, "0.01"),
                normalized_value=None,
            )
            for index, point in enumerate(points)
        ],
    )


def _quantize_optional(value: object | None) -> Decimal | None:
    if value is None:
        return None
    return quantize(value)


def _elapsed_seconds(row: TrainingSessionRow) -> int:
    end = row.finished_at or datetime.now()
    return max(0, int((end - row.started_at).total_seconds()))


def _slice_error(error: TrainingSliceError) -> TrainingError:
    return TrainingError(
        error.error_code,
        error.message,
        422,
        detail=dict(error.detail),
    )


def _engine_error(error: TrainingTransportTimeout | TrainingTransportFailed) -> TrainingError:
    if isinstance(error, TrainingTransportFailed):
        return TrainingError(
            "TRAINING_ENGINE_UNAVAILABLE",
            "训练引擎执行失败",
            500,
            detail={"reason": error.message, **error.detail},
        )
    return TrainingError(
        "TRAINING_ENGINE_UNAVAILABLE",
        "训练引擎无响应（空闲回收或线程已退出），请重试",
        503,
        detail={"reason": str(error)},
    )


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


__all__ = ["TrainingError", "TrainingService", "ALLOWED_EVENT_TYPES", "SETTLEMENT_NOTE"]
