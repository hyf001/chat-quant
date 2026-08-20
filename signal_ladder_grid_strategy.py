"""ChatQ signal-protocol example: simplified ladder grid strategy."""

from __future__ import annotations

from app.service.strategy.protocol import ChatQBarContext, ChatQInitContext, ChatQNextResult, ChatQState


def chatq_params() -> list[dict]:
    return [
        {
            "name": "drop_pct",
            "type": "number",
            "default": 0.10,
            "label": "买入触发:价格较锚点下跌比例",
        },
        {
            "name": "profit_pct",
            "type": "number",
            "default": 0.20,
            "label": "卖出触发:价格较买入价上涨比例",
        },
        {
            "name": "order_size",
            "type": "integer",
            "default": 100,
            "label": "每次下单股数",
        },
    ]


def chatq_init(context: ChatQInitContext) -> ChatQState:
    symbol = context["symbols"][0]
    history = context["history"][symbol]
    anchor_price = float(history["close"].iloc[-1]) if len(history) else None
    return {
        "anchor_price": anchor_price,
        "last_buy_price": None,
    }


def chatq_next(context: ChatQBarContext, state: ChatQState) -> ChatQNextResult:
    symbol = context["symbols"][0]
    params = context["params"]
    close = float(context["current_bars"][symbol]["close"])
    position = context["positions"].get(symbol, {"size": 0})

    anchor_price = state.get("anchor_price") or close
    last_buy_price = state.get("last_buy_price")
    drop_pct = float(params["drop_pct"])
    profit_pct = float(params["profit_pct"])
    order_size = int(params["order_size"])

    if position["size"] == 0 and close <= float(anchor_price) * (1 - drop_pct):
        state["last_buy_price"] = close
        return {
            "actions": [
                {
                    "action": "buy",
                    "symbol": symbol,
                    "order_type": "market",
                    "size": order_size,
                    "reason": "grid_drop_buy",
                }
            ],
            "state": state,
        }

    if position["size"] > 0 and last_buy_price is not None:
        take_profit_price = float(last_buy_price) * (1 + profit_pct)
        if close >= take_profit_price:
            state["anchor_price"] = close
            state["last_buy_price"] = None
            return {
                "actions": [
                    {
                        "action": "close",
                        "symbol": symbol,
                        "reason": "grid_take_profit",
                    }
                ],
                "state": state,
            }

    return {"actions": [{"action": "hold", "reason": "grid_wait"}], "state": state}
