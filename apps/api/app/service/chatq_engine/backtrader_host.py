"""Shared backtrader host for the backtest and training adapters.

The host owns the parts both adapters need and must not know about either one:

* the bar loop wiring (``ChatQBacktraderStrategyBase``) with the three seams
  (``next_actions`` / ``submit_action`` / ``on_bar_settled``),
* the chatq context/order/position normalization helpers,
* the analyzers (equity curve / closed trades / order execution / daily portfolio).

The host never publishes candles, never touches the database and never masks
data: backtest builds result records from the analyzers, training publishes
broker snapshots through its own transport.
"""

from __future__ import annotations

from datetime import datetime, time

import backtrader as bt
import pandas as pd

from app.service.strategy.protocol import (
    ChatQActionType,
    ChatQBar,
    ChatQBarContext,
    ChatQInitContext,
    ChatQOpenOrder,
    ChatQOrderEvent,
    ChatQPosition,
    ChatQStrategyModule,
    StrategyProtocolError,
    normalize_chatq_result,
)


class ChatQBacktraderStrategyBase(bt.Strategy):
    """bar 循环 + 三个接缝，回测与训练共用。"""

    params = (
        ("strategy_module", None),
        ("chatq_param_values", None),
        ("symbols", None),
        ("history", None),
        ("services", None),
    )

    def __init__(self) -> None:
        self.strategy_module: ChatQStrategyModule = self.p.strategy_module
        self.strategy_state: dict[str, object] = {}
        self.open_order_by_ref: dict[str, bt.Order] = {}
        self.pending_order_events: list[dict[str, object]] = []
        self.data_by_symbol = {data._name: data for data in self.datas}
        self.init_strategy_state()

    def init_strategy_state(self) -> None:
        """初始化 chatq 策略状态；训练侧没有策略模块，覆写为空实现。"""
        if self.strategy_module is None:
            return
        init_context: ChatQInitContext = {
            "mode": "backtest",
            "symbols": list(self.p.symbols),
            "params": dict(self.p.chatq_param_values),
            "history": self.p.history,
            "chatq": self.p.services,
        }
        raw_state = self.strategy_module.chatq_init(init_context)
        if not isinstance(raw_state, dict):
            raise StrategyProtocolError(
                "STRATEGY_STATE_INVALID",
                "chatq_init must return an object",
            )
        self.strategy_state = raw_state

    # -- 接缝 ---------------------------------------------------------------

    def next_actions(self, context: ChatQBarContext) -> list[dict[str, object]]:
        """接缝①：默认是策略信号（回测），训练侧覆写为"阻塞等人工动作"。"""
        raw_result = self.strategy_module.chatq_next(context, self.strategy_state)
        result = normalize_chatq_result(raw_result, old_state=self.strategy_state)
        self.strategy_state = result["state"]
        return list(result["actions"])

    def submit_action(self, action: dict[str, object]) -> None:
        """接缝②：统一走 backtrader broker 下单。"""
        action_name = action["action"]
        if action_name == ChatQActionType.CANCEL:
            order = self.open_order_by_ref.get(str(action["ref"]))
            if order is not None:
                self.cancel(order)
            return

        symbol = str(action["symbol"])
        data = self.data_by_symbol[symbol]
        size = action.get("size")
        price = action.get("price")
        order_type = str(action.get("order_type", "market"))

        if action_name == ChatQActionType.BUY:
            order = self.buy(
                data=data,
                size=size,
                price=price,
                exectype=to_backtrader_exectype(order_type),
            )
        elif action_name == ChatQActionType.SELL:
            order = self.sell(
                data=data,
                size=size,
                price=price,
                exectype=to_backtrader_exectype(order_type),
            )
        elif action_name == ChatQActionType.CLOSE:
            order = self.close(data=data, size=size)
        else:
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                f"unsupported action: {action_name}",
            )
        self.open_order_by_ref[str(order.ref)] = order

    def on_bar_settled(
        self,
        context: ChatQBarContext,
        actions: list[dict[str, object]],
    ) -> None:
        """接缝③：回测侧 no-op，训练侧在结算点把 broker 快照交给 transport。"""
        return None

    # -- bar 循环 -----------------------------------------------------------

    def next(self) -> None:
        context = self.build_context()
        actions = self.next_actions(context)
        for action in actions:
            self.submit_action(action)
        self.on_bar_settled(context, actions)

    def build_context(self) -> ChatQBarContext:
        current_dt = self.datas[0].datetime.datetime(0)
        context: ChatQBarContext = {
            "mode": "backtest",
            "datetime": current_dt.isoformat(),
            "symbols": list(self.p.symbols),
            "current_bars": extract_current_bars(self.datas),
            "bars": history_until(self.p.history, current_dt),
            "cash": float(self.broker.getcash()),
            "portfolio_value": float(self.broker.getvalue()),
            "positions": normalize_positions(self),
            "open_orders": normalize_open_orders(self.broker.get_orders_open()),
            "order_events": list(self.pending_order_events),
            "params": dict(self.p.chatq_param_values),
            "chatq": self.p.services,
        }
        self.pending_order_events = []
        return context

    def notify_order(self, order: bt.Order) -> None:
        self.pending_order_events.append(normalize_order_event(order))
        if is_terminal_order(order):
            self.open_order_by_ref.pop(str(order.ref), None)


def extract_current_bars(datas: list[bt.LineSeries]) -> dict[str, ChatQBar]:
    bars: dict[str, ChatQBar] = {}
    for data in datas:
        bars[data._name] = {
            "symbol": data._name,
            "datetime": data.datetime.datetime(0).isoformat(),
            "open": float(data.open[0]),
            "high": float(data.high[0]),
            "low": float(data.low[0]),
            "close": float(data.close[0]),
            "volume": float(data.volume[0]),
        }
    return bars


def history_until(
    history: dict[str, pd.DataFrame],
    current_dt: datetime,
) -> dict[str, pd.DataFrame]:
    current_ts = pd.Timestamp(current_dt)
    return {symbol: frame.loc[frame.index <= current_ts] for symbol, frame in history.items()}


def normalize_positions(strategy: bt.Strategy) -> dict[str, ChatQPosition]:
    positions: dict[str, ChatQPosition] = {}
    for data in strategy.datas:
        position = strategy.getposition(data)
        size = float(position.size)
        if size == 0:
            continue
        positions[data._name] = {
            "symbol": data._name,
            "size": size,
            "price": float(position.price),
        }
    return positions


def normalize_open_orders(orders: list[bt.Order]) -> list[ChatQOpenOrder]:
    return [normalize_order(order) for order in orders if not is_terminal_order(order)]


def normalize_order(order: bt.Order) -> ChatQOpenOrder:
    price = order_created_price(order)
    return {
        "ref": str(order.ref),
        "symbol": order.data._name,
        "side": "buy" if order.isbuy() else "sell",
        "status": order_status(order),
        "order_type": order_type(order),
        "size": abs(float(order.created.size)),
        "price": price,
    }


def normalize_order_event(order: bt.Order) -> ChatQOrderEvent:
    if order.status == order.Completed:
        price = float(order.executed.price)
        size = abs(float(order.executed.size))
    else:
        price = order_created_price(order)
        size = abs(float(order.created.size))
    return {
        "ref": str(order.ref),
        "symbol": order.data._name,
        "side": "buy" if order.isbuy() else "sell",
        "status": order_status(order),
        "price": price,
        "size": size,
    }


def order_status(order: bt.Order) -> str:
    if order.status == order.Completed:
        return "filled"
    if order.status == order.Canceled:
        return "cancelled"
    if order.status in {order.Margin, order.Rejected}:
        return "rejected"
    return order.getstatusname().lower()


def order_type(order: bt.Order) -> str:
    if order.exectype == bt.Order.Limit:
        return "limit"
    return "market"


def order_created_price(order: bt.Order) -> float | None:
    price = getattr(order.created, "price", None)
    return float(price) if price else None


def is_terminal_order(order: bt.Order) -> bool:
    return order.status in {
        order.Completed,
        order.Canceled,
        order.Margin,
        order.Rejected,
        order.Expired,
    }


def to_backtrader_exectype(order_type_value: str) -> int:
    if order_type_value == "limit":
        return bt.Order.Limit
    return bt.Order.Market


class EquityCurveAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.points: list[dict[str, object]] = []

    def next(self) -> None:
        point_date = self.strategy.datas[0].datetime.date(0)
        self.points.append(
            {
                "date": point_date,
                "value": self.strategy.broker.getvalue(),
                "cash": self.strategy.broker.getcash(),
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.points


class ClosedTradeAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.trades: list[dict[str, object]] = []

    def notify_trade(self, trade: bt.Trade) -> None:
        if not trade.isclosed:
            return
        close_date = bt.num2date(trade.dtclose).date()
        value = abs(float(trade.value))
        pnl = float(trade.pnlcomm)
        self.trades.append(
            {
                "symbol": trade.data._name,
                "date": close_date,
                "size": float(trade.size),
                "price": float(trade.price),
                "value": value,
                "pnl": pnl,
                "pnl_pct": (pnl / value * 100) if value else None,
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.trades


class OrderExecutionAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.orders: list[dict[str, object]] = []

    def notify_order(self, order: bt.Order) -> None:
        if order.status != order.Completed:
            return
        executed_at = (
            bt.num2date(order.executed.dt)
            if order.executed.dt
            else datetime.combine(order.data.datetime.date(0), time(hour=15))
        )
        self.orders.append(
            {
                "symbol": order.data._name,
                "side": "buy" if order.isbuy() else "sell",
                "datetime": executed_at,
                "price": float(order.executed.price),
                "size": float(order.executed.size),
                "value": float(order.executed.value),
                "commission": float(order.executed.comm),
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.orders


class DailyPortfolioAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.snapshots: list[dict[str, object]] = []
        self.previous_value = float(
            getattr(self.strategy.broker, "startingcash", self.strategy.broker.getvalue())
        )

    def next(self) -> None:
        current_date = self.strategy.datas[0].datetime.date(0)
        total_value = float(self.strategy.broker.getvalue())
        positions: list[dict[str, object]] = []
        for data in self.strategy.datas:
            position = self.strategy.getposition(data)
            size = float(position.size)
            if size == 0:
                continue
            close_price = float(data.close[0])
            positions.append(
                {
                    "symbol": data._name,
                    "size": size,
                    "close_price": close_price,
                    "market_value": size * close_price,
                    "unrealized_pnl": (close_price - float(position.price)) * size,
                }
            )
        self.snapshots.append(
            {
                "date": current_date,
                "cash": float(self.strategy.broker.getcash()),
                "total_value": total_value,
                "daily_pnl": total_value - self.previous_value,
                "positions": positions,
            }
        )
        self.previous_value = total_value

    def get_analysis(self) -> list[dict[str, object]]:
        return self.snapshots
