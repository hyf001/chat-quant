"""训练适配器：阻塞取人工信号 + 提交 + 在结算点吐出 broker 快照。

三个接缝的差异全部在这里（设计方案 §4.2）：

* 接缝①：不问策略，阻塞等 transport 送来的一次点击（``hold`` 归一化成"只推进"）；
  回测走 ``next``/``next_actions``，训练挪到 ``next_open``（见下面的成交时点）；
* 接缝②：与人共用 ``submit_action``（服务端已把仓位比例换算成股数）；
* 接缝③：``on_bar_settled`` 把 broker 快照交给 transport（不发布 K 线、不落库）。

**成交时点**：训练开 ``cheat_on_open`` + ``broker.set_coc(True)``，一次点击在
``next_open`` 里提交，broker 在**同一根**按这根的 close 撮合，``notify_order`` 也在
同一根交付。所以"点击那一根"的结算点快照里就已经是成交后的现金与持仓，**不存在
挂单**，账户字段全部是 backtrader 的原值（见设计方案 §5.3）。

K 线与脱敏都留在 service：这里只认识账户与成交。
"""

from __future__ import annotations

from typing import Any

import backtrader as bt
import pandas as pd

from app.service.chatq_engine import (
    ChatQBacktraderStrategyBase,
    ClosedTradeAnalyzer,
    OrderExecutionAnalyzer,
)
from app.service.training.transport import (
    InMemoryTrainingSignalTransport,
    TrainingTransportStopped,
)


class TrainingStrategyAdapter(ChatQBacktraderStrategyBase):
    params = (
        ("transport", None),
        ("runtime", None),
        ("symbol", None),
        ("bar_offset", 0),
    )

    def __init__(self) -> None:
        self.bar_index = -1
        self.pending_fills: list[dict[str, Any]] = []
        self.pending_rejections: list[dict[str, Any]] = []
        super().__init__()
        runtime = self.p.runtime
        if isinstance(runtime, dict):
            runtime["strategy"] = self

    def init_strategy_state(self) -> None:
        """训练没有策略模块：人工点击就是信号源。"""
        return None

    # -- 接缝①+②：在本根开盘前取点击、提交订单 -----------------------------

    def prenext_open(self) -> None:
        self.next_open()

    def nextstart_open(self) -> None:
        self.next_open()

    def next_open(self) -> None:
        """接缝①②：阻塞等这一次点击，把它交给 broker。

        三个 ``*_open`` 钩子都指向这里：backtrader 在最小周期前后走的是不同的
        钩子（`prenext_open` / `nextstart_open` / `next_open`），合起来每根恰好
        一次。提交发生在 broker 撮合**之前**（coc 打开时按本根 close 成交），
        所以这一笔在本根的结算点快照里就能看到。
        """
        self.bar_index += 1
        action = self._transport().next_action(self.bar_index)
        if action is not None:
            self.submit_action(action)

    def submit_action(self, action: dict[str, object]) -> None:
        """接缝②：训练是纯多头，卖出按 broker 的实时持仓封顶（设计方案 §5.3）。

        服务端已经按当前持仓算过一遍股数，这里是最后一道闸：持仓直接取
        ``getposition``（backtrader 的值），任何一笔卖单都不会把多头卖成空头。
        超出部分不缩量成交，而是整单拒掉（记进 ``rejections``，前端据此提示）。
        """
        if isinstance(action, dict) and action.get("action") in {"sell", "close"}:
            action = self._clamp_sell(action)
            if action is None:
                return
        super().submit_action(action)

    def _clamp_sell(self, action: dict[str, object]) -> dict[str, object] | None:
        held = float(self.getposition(self.datas[0]).size)
        requested = action.get("size")
        wanted = held if requested is None else min(float(requested), held)
        if wanted < 1:
            self.pending_rejections.append(
                {
                    "side": "sell",
                    "size": abs(float(requested)) if requested is not None else 0.0,
                    "status": "oversell",
                }
            )
            return None
        return {**action, "size": int(wanted)}

    # -- 接缝③：结算点 ------------------------------------------------------

    def next(self) -> None:
        self.on_bar_settled(self.build_context(), [])

    def on_bar_settled(self, context: Any, actions: list[dict[str, object]]) -> None:
        self._transport().publish_bar(self.bar_index, self.build_snapshot())

    def notify_order(self, order: bt.Order) -> None:
        super().notify_order(order)
        if order.status == order.Completed:
            self.pending_fills.append(
                {
                    "side": "buy" if order.isbuy() else "sell",
                    "price": float(order.executed.price),
                    "size": abs(float(order.executed.size)),
                    "value": abs(float(order.executed.value)),
                    "commission": float(order.executed.comm),
                }
            )
        elif order.status in {order.Margin, order.Rejected}:
            self.pending_rejections.append(
                {
                    "side": "buy" if order.isbuy() else "sell",
                    "size": abs(float(order.created.size)),
                    "status": "rejected" if order.status == order.Rejected else "margin",
                }
            )

    def build_snapshot(self) -> dict[str, Any]:
        # 成交 / 拒单都发生在本根开盘，序号统一在这里落成切片坐标。
        index = self.p.bar_offset + self.bar_index
        position = self.getposition(self.datas[0])
        fills = [{**item, "i": index} for item in self.pending_fills]
        rejections = [{**item, "i": index} for item in self.pending_rejections]
        self.pending_fills = []
        self.pending_rejections = []
        # 全部是 backtrader 的原值：点击那一笔已经在同一根成交，这里没有挂单。
        return {
            "i": index,
            "cash": float(self.broker.getcash()),
            "value": float(self.broker.getvalue()),
            "position_size": float(position.size),
            "position_price": float(position.price) if position.size else None,
            "fills": fills,
            "rejections": rejections,
        }

    def _transport(self) -> InMemoryTrainingSignalTransport:
        transport = self.p.transport
        if transport is None:
            raise RuntimeError("training adapter requires a signal transport")
        return transport


def run_backtrader_training(
    *,
    frame: pd.DataFrame,
    symbol: str,
    initial_cash: float,
    commission: float,
    slippage: float = 0.0,
    transport: InMemoryTrainingSignalTransport,
    bar_offset: int,
) -> dict[str, Any]:
    """在调用线程里跑完训练段的 bar 循环（阻塞等人工信号）。

    ``cheat_on_open=True`` 让适配器在每根开盘前拿到点击并提交；配合
    ``set_coc(True)``，市价单按**本根的 close**（当天尾盘价）成交，且撮合与
    ``notify_order`` 都发生在同一根里——所以不存在"等下一根成交"的挂单。
    """
    cerebro = bt.Cerebro(stdstats=False, cheat_on_open=True)
    cerebro.broker.setcash(float(initial_cash))
    cerebro.broker.setcommission(commission=float(commission))
    if slippage > 0:
        # 按比例向不利方向滑（买入更贵、卖出更便宜），且越不过当根的 high / low；
        # slip_open 必须打开，否则"按本根 close 成交"的市价单完全不滑。
        cerebro.broker.set_slippage_perc(
            perc=float(slippage),
            slip_open=True,
            slip_match=True,
            slip_limit=True,
            slip_out=False,
        )
    # Cheat-On-Close：点击提交的市价单按本根 close 成交（当天尾盘价）。
    # 决策依据仍然是"已揭示的上一根"，当根 close 只在成交时使用，不构成未来函数。
    cerebro.broker.set_coc(True)
    cerebro.adddata(bt.feeds.PandasData(dataname=frame), name=symbol)
    runtime: dict[str, Any] = {}
    cerebro.addstrategy(
        TrainingStrategyAdapter,
        strategy_module=None,
        chatq_param_values={},
        symbols=[symbol],
        history={},
        services=None,
        execution_mode="current_close",  # 训练即 set_coc(True)，按本根 close 成交
        transport=transport,
        runtime=runtime,
        symbol=symbol,
        bar_offset=bar_offset,
    )
    cerebro.addanalyzer(ClosedTradeAnalyzer, _name="closed_trades")
    cerebro.addanalyzer(OrderExecutionAnalyzer, _name="orders")

    stopped = False
    strategy = None
    try:
        executed = cerebro.run()
        strategy = executed[0] if executed else runtime.get("strategy")
    except TrainingTransportStopped:
        # 收局（finish）或空闲回收：正常退出，分析器里已处理过的根仍然有效。
        stopped = True
        strategy = runtime.get("strategy")

    closed_trades = (
        list(strategy.analyzers.closed_trades.get_analysis()) if strategy is not None else []
    )
    orders = list(strategy.analyzers.orders.get_analysis()) if strategy is not None else []
    return {
        "stopped": stopped,
        "closed_trades": closed_trades,
        "orders": orders,
    }
