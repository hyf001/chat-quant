"""Signal-protocol version of a ladder grid strategy.

This file is an example for the proposed ChatQ signal strategy protocol.
It is not executable by the current Backtrader engine until the protocol
adapter is implemented.
"""

from __future__ import annotations

import backtrader as bt


class LadderGridSignalStrategy(bt.Strategy):
    """Ladder grid strategy using chatq_signal_init/chatq_signal_next."""

    @classmethod
    def chatq_params(cls):
        return [
            {
                "name": "initial_buy_price",
                "type": "number",
                "default": 0,
                "label": "初始买入价格(0=首日开盘价市价买入)",
            },
            {
                "name": "drop_pct",
                "type": "number",
                "default": 0.10,
                "label": "买入触发:价格较持仓最低档下跌比例",
            },
            {
                "name": "profit_pct",
                "type": "number",
                "default": 0.20,
                "label": "卖出触发:持仓较买入价上涨比例",
            },
            {
                "name": "cash_per_pos",
                "type": "number",
                "default": 10000,
                "label": "每笔买入金额(元)",
            },
            {
                "name": "min_trade_amt",
                "type": "number",
                "default": 0,
                "label": "单笔最小成交金额(元),0为不限制",
            },
            {
                "name": "reanchor_on_exit",
                "type": "boolean",
                "default": True,
                "label": "全部清仓后重新锚定开启新一轮",
            },
        ]

    @classmethod
    def chatq_signal_init(cls, context=None):
        return {
            "initialized": False,
            "anchor_price": None,
            "next_buy_price": None,
            "pending_buy_price": None,
            "buy_order_ref": None,
            "holdings_by_price": {},
            "sell_orders": {},
        }

    @classmethod
    def chatq_signal_next(cls, context):
        """Return one action, an action list, or hold.

        Expected context keys:
        - bar: datetime/open/high/low/close/volume/openinterest
        - cash: current broker cash
        - position: net position snapshot
        - portfolio_value: current broker value
        - open_orders: open order snapshots
        - order_events: order events since last call
        - params: strategy runtime params
        - signal_state: mutable state returned by chatq_signal_init
        """
        state = context["signal_state"]
        params = _Params(context.get("params", {}))
        bar = context["bar"]
        actions = []

        cls._apply_order_events(state, context.get("order_events", []), params, actions)

        if not state["initialized"]:
            state["initialized"] = True
            state["anchor_price"] = float(bar["close"])
            if params.initial_buy_price > 0:
                price = round(params.initial_buy_price, 4)
                action = cls._build_limit_buy(context, params, price)
            else:
                action = cls._build_market_buy(context, params)
            if action is not None:
                actions.append(action)
            return actions or {"action": "hold"}

        sync_actions = cls._sync_buy_order(state, context, params)
        actions.extend(sync_actions)
        return actions or {"action": "hold"}

    def next(self):
        """The protocol adapter drives trading; this keeps old smoke checks happy."""

    @classmethod
    def _apply_order_events(cls, state, order_events, params, actions):
        for event in order_events:
            status = str(event.get("status", "")).lower()
            ref = event.get("ref")

            if status in {"submitted", "accepted"}:
                cls._remember_open_order(state, event, params)
                continue

            if status == "completed":
                if event.get("is_buy"):
                    cls._on_buy_completed(state, event, params, actions)
                else:
                    cls._on_sell_completed(state, event, params)
                continue

            if status in {"canceled", "cancelled", "margin", "rejected", "expired"}:
                if ref == state.get("buy_order_ref"):
                    state["buy_order_ref"] = None
                    state["pending_buy_price"] = None
                state["sell_orders"].pop(ref, None)

    @classmethod
    def _remember_open_order(cls, state, event, params):
        ref = event.get("ref")
        if ref is None:
            return

        created_price = _optional_float(event.get("created_price"))
        info = event.get("info") or {}
        if event.get("is_buy"):
            state["buy_order_ref"] = ref
            state["pending_buy_price"] = created_price
            return

        buy_price = _optional_float(info.get("buy_price"))
        if buy_price is None and created_price is not None:
            buy_price = cls._buy_price_from_sell_price(created_price, params)
        if buy_price is not None:
            state["sell_orders"][ref] = buy_price

    @classmethod
    def _on_buy_completed(cls, state, event, params, actions):
        price = round(float(event["executed_price"]), 4)
        size = float(event["executed_size"])
        holdings = state["holdings_by_price"]
        holdings[price] = holdings.get(price, 0.0) + size

        if event.get("ref") == state.get("buy_order_ref"):
            state["buy_order_ref"] = None
            state["pending_buy_price"] = None

        sell_price = round(price * (1 + params.profit_pct), 4)
        actions.append(
            {
                "action": "sell",
                "params": {
                    "size": size,
                    "exectype": bt.Order.Limit,
                    "price": sell_price,
                    "buy_price": price,
                },
            }
        )

    @classmethod
    def _on_sell_completed(cls, state, event, params):
        ref = event.get("ref")
        buy_price = state["sell_orders"].pop(ref, None)
        if buy_price is None:
            buy_price = cls._infer_buy_price_from_sell_event(event, params, state)
        if buy_price is None:
            return

        holdings = state["holdings_by_price"]
        sold_size = abs(float(event["executed_size"]))
        remaining = holdings.get(buy_price, 0.0) - sold_size
        if remaining > 1e-9:
            holdings[buy_price] = remaining
        else:
            holdings.pop(buy_price, None)

        if not holdings and params.reanchor_on_exit:
            close_price = _optional_float(event.get("bar_close"))
            if close_price is not None:
                state["anchor_price"] = close_price

    @classmethod
    def _sync_buy_order(cls, state, context, params):
        next_buy_price = cls._next_buy_price(state, params)
        state["next_buy_price"] = next_buy_price
        open_buy = cls._find_open_buy_order(context.get("open_orders", []), state)

        actions = []
        if open_buy is not None:
            old_price = _optional_float(open_buy.get("price"))
            if old_price is not None and abs(old_price - next_buy_price) > 1e-6:
                actions.append({"action": "cancel", "params": {"ref": open_buy["ref"]}})
                state["buy_order_ref"] = None
                state["pending_buy_price"] = None
            else:
                return actions

        action = cls._build_limit_buy(context, params, next_buy_price)
        if action is not None:
            actions.append(action)
        return actions

    @classmethod
    def _next_buy_price(cls, state, params):
        holdings = state["holdings_by_price"]
        if holdings:
            return round(min(holdings) * (1 - params.drop_pct), 4)
        return round(float(state["anchor_price"]) * (1 - params.drop_pct), 4)

    @classmethod
    def _build_market_buy(cls, context, params):
        bar = context["bar"]
        price = float(bar["open"])
        return cls._build_buy(context, params, price=price, exectype=None)

    @classmethod
    def _build_limit_buy(cls, context, params, price):
        return cls._build_buy(context, params, price=price, exectype=bt.Order.Limit)

    @classmethod
    def _build_buy(cls, context, params, *, price, exectype):
        cash = float(context.get("cash", 0.0))
        amount = min(params.cash_per_pos, cash)
        if amount <= 0:
            return None
        if params.min_trade_amt > 0 and amount < params.min_trade_amt:
            return None

        size = amount / price
        if size <= 0:
            return None

        action_params = {"size": size}
        if exectype is not None:
            action_params["exectype"] = exectype
            action_params["price"] = price
        return {"action": "buy", "params": action_params}

    @classmethod
    def _find_open_buy_order(cls, open_orders, state):
        buy_ref = state.get("buy_order_ref")
        for order in open_orders:
            if buy_ref is not None and order.get("ref") == buy_ref:
                return order
        for order in open_orders:
            if order.get("is_buy") and order.get("status") not in {"completed", "canceled"}:
                return order
        return None

    @classmethod
    def _infer_buy_price_from_sell_event(cls, event, params, state):
        info = event.get("info") or {}
        buy_price = _optional_float(info.get("buy_price"))
        if buy_price is not None:
            return buy_price

        created_price = _optional_float(event.get("created_price"))
        if created_price is None:
            return None
        inferred = cls._buy_price_from_sell_price(created_price, params)
        return _nearest_price(inferred, state["holdings_by_price"])

    @staticmethod
    def _buy_price_from_sell_price(sell_price, params):
        return round(float(sell_price) / (1 + params.profit_pct), 4)


class _Params:
    def __init__(self, values):
        self.initial_buy_price = float(values.get("initial_buy_price", 0))
        self.drop_pct = float(values.get("drop_pct", 0.10))
        self.profit_pct = float(values.get("profit_pct", 0.20))
        self.cash_per_pos = float(values.get("cash_per_pos", 10000))
        self.min_trade_amt = float(values.get("min_trade_amt", 0))
        self.reanchor_on_exit = bool(values.get("reanchor_on_exit", True))


def _optional_float(value):
    if value is None:
        return None
    return float(value)


def _nearest_price(price, holdings):
    if not holdings:
        return None
    nearest = min(holdings, key=lambda key: abs(float(key) - price))
    return nearest if abs(float(nearest) - price) < 1e-4 else None
