from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Literal, NotRequired, Protocol, Required, TypedDict
from uuid import uuid4

import pandas as pd
from pydantic import ValidationError

from app.schema.strategy import StrategyCustomParameter, StrategyParamValue

ParamSource = Literal["chatq_params", "none"]
ChatQMode = Literal["backtest", "signal", "paper", "live"]
ChatQActionName = Literal["buy", "sell", "close", "cancel", "hold"]
ChatQOrderSide = Literal["buy", "sell"]
ChatQOrderType = Literal["market", "limit"]
ChatQState = dict[str, Any]


class ChatQReadOnlyServices(Protocol):
    def sql(self, sql: str) -> pd.DataFrame:
        ...


class ChatQBar(TypedDict):
    symbol: str
    datetime: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class ChatQPosition(TypedDict):
    symbol: str
    size: float
    price: float


class ChatQOpenOrder(TypedDict):
    ref: str
    symbol: str
    side: ChatQOrderSide
    status: str
    order_type: ChatQOrderType
    size: float
    price: float | None


class ChatQOrderEvent(TypedDict):
    ref: str
    symbol: str
    side: ChatQOrderSide
    status: str
    price: float | None
    size: float


class ChatQInitContext(TypedDict):
    mode: ChatQMode
    symbols: list[str]
    timeframe: str
    params: dict[str, Any]
    history: dict[str, pd.DataFrame]
    chatq: ChatQReadOnlyServices


class ChatQBarContext(TypedDict):
    mode: ChatQMode
    datetime: str
    symbols: list[str]
    current_bars: dict[str, ChatQBar]
    bars: dict[str, pd.DataFrame]
    cash: float
    portfolio_value: float
    positions: dict[str, ChatQPosition]
    open_orders: list[ChatQOpenOrder]
    order_events: list[ChatQOrderEvent]
    params: dict[str, Any]
    chatq: ChatQReadOnlyServices


class ChatQAction(TypedDict, total=False):
    action: Required[ChatQActionName]
    symbol: str
    order_type: ChatQOrderType
    size: float
    price: float | None
    ref: str
    reason: str
    client_signal_id: str


class ChatQNextResult(TypedDict):
    actions: list[ChatQAction]
    state: ChatQState
    logs: NotRequired[list[Any]]


ChatQInitFunc = Callable[[ChatQInitContext], ChatQState]
ChatQNextFunc = Callable[[ChatQBarContext, ChatQState], ChatQNextResult]


@dataclass(frozen=True)
class ChatQStrategyModule:
    module: ModuleType
    chatq_init: ChatQInitFunc
    chatq_next: ChatQNextFunc
    chatq_params: Callable[[], object] | None = None


@dataclass(frozen=True)
class StrategyProtocolSpec:
    strategy_module: ChatQStrategyModule
    custom_params: list[StrategyCustomParameter]
    param_source: ParamSource


class StrategyProtocolError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message


def parse_strategy_source(
    source_code: str,
    *,
    module_name: str | None = None,
) -> StrategyProtocolSpec:
    module_name = module_name or f"chatq_strategy_protocol_{uuid4().hex}"
    try:
        strategy_module = load_strategy_module(source_code, module_name=module_name)
        custom_params, param_source = _extract_custom_params(strategy_module)
        return StrategyProtocolSpec(
            strategy_module=strategy_module,
            custom_params=custom_params,
            param_source=param_source,
        )
    finally:
        sys.modules.pop(module_name, None)


def load_strategy_module(source_code: str, *, module_name: str) -> ChatQStrategyModule:
    module = ModuleType(module_name)
    module.__file__ = f"<{module_name}>"
    sys.modules[module_name] = module
    try:
        compiled = compile(source_code, module.__file__, "exec")
        exec(compiled, module.__dict__)
    except StrategyProtocolError:
        raise
    except Exception as exc:
        raise StrategyProtocolError("STRATEGY_IMPORT_FAILED", str(exc)) from exc

    chatq_init = _required_callable(module, "chatq_init")
    chatq_next = _required_callable(module, "chatq_next")
    chatq_params = getattr(module, "chatq_params", None)
    if chatq_params is not None and not callable(chatq_params):
        raise StrategyProtocolError(
            "STRATEGY_PROTOCOL_INVALID",
            "chatq_params must be callable",
        )
    return ChatQStrategyModule(
        module=module,
        chatq_init=chatq_init,
        chatq_next=chatq_next,
        chatq_params=chatq_params,
    )


def normalize_chatq_result(
    raw_result: object,
    *,
    old_state: ChatQState,
) -> ChatQNextResult:
    if not isinstance(raw_result, dict):
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "chatq_next must return an object",
        )

    if "actions" in raw_result:
        raw_actions = raw_result["actions"]
    elif "action" in raw_result:
        raw_actions = [raw_result]
    else:
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "chatq_next result must define actions or action",
        )

    if not isinstance(raw_actions, list):
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "actions must be a list",
        )

    actions = [_normalize_action(action) for action in raw_actions]
    state = raw_result.get("state", old_state)
    logs = raw_result.get("logs", [])
    if not isinstance(state, dict):
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "state must be an object",
        )
    if not isinstance(logs, list):
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "logs must be a list",
        )

    return {
        "actions": actions or [{"action": "hold"}],
        "state": state,
        "logs": logs,
    }


def validate_chatq_action(action: dict[str, Any]) -> dict[str, Any]:
    action_name = action["action"]
    if action_name == "hold":
        return action

    symbol = action.get("symbol")
    if action_name != "cancel" and (not isinstance(symbol, str) or not symbol):
        raise StrategyProtocolError(
            "STRATEGY_ACTION_INVALID",
            f"{action_name} action must define symbol",
        )

    if action_name in {"buy", "sell"}:
        size = action.get("size")
        if not isinstance(size, int | float) or isinstance(size, bool) or size <= 0:
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                f"{action_name} action must define size > 0",
            )
        order_type = action.get("order_type", "market")
        if order_type not in {"market", "limit"}:
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                "order_type must be market or limit",
            )
        if order_type == "limit" and action.get("price") is None:
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                "limit order must define price",
            )

    if action_name == "close":
        size = action.get("size")
        if size is not None and (
            not isinstance(size, int | float) or isinstance(size, bool) or size <= 0
        ):
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                "close action size must be empty or > 0",
            )

    if action_name == "cancel":
        ref = action.get("ref")
        if not isinstance(ref, str | int) or ref == "":
            raise StrategyProtocolError(
                "STRATEGY_ACTION_INVALID",
                "cancel action must define ref",
            )

    return action


def _required_callable(module: ModuleType, name: str) -> Callable[..., Any]:
    value = getattr(module, name, None)
    if not callable(value):
        raise StrategyProtocolError(
            "STRATEGY_PROTOCOL_INVALID",
            f"Source code must define callable {name}(...)",
        )
    return value


def _extract_custom_params(
    strategy_module: ChatQStrategyModule,
) -> tuple[list[StrategyCustomParameter], ParamSource]:
    if strategy_module.chatq_params is None:
        return [], "none"
    try:
        raw_params = strategy_module.chatq_params()
    except Exception as exc:
        raise StrategyProtocolError("STRATEGY_PROTOCOL_INVALID", str(exc)) from exc
    return _parse_chatq_params(raw_params), "chatq_params"


def _parse_chatq_params(raw_params: object) -> list[StrategyCustomParameter]:
    if not isinstance(raw_params, list | tuple):
        raise StrategyProtocolError("STRATEGY_PROTOCOL_INVALID", "chatq_params must return a list")

    params: list[StrategyCustomParameter] = []
    seen: set[str] = set()
    for raw_param in raw_params:
        if not isinstance(raw_param, dict):
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                "Each chatq_params item must be an object",
            )
        name = raw_param.get("name_en", raw_param.get("name"))
        if not isinstance(name, str) or not name:
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                "Each chatq_params item must define name or name_en",
            )
        label = raw_param.get("name_cn", raw_param.get("label", name))
        if not isinstance(label, str) or not label:
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                f"{name} label/name_cn must be a non-empty string",
            )
        if "default" not in raw_param:
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                f"{name} must define a default value",
            )
        param_type = raw_param.get("type") or _infer_param_type(raw_param["default"])
        payload = {
            "name_cn": label,
            "name_en": name,
            "type": param_type,
            "default": raw_param["default"],
            "required": raw_param.get("required", True),
        }
        try:
            param = StrategyCustomParameter.model_validate(payload)
        except ValidationError as exc:
            raise StrategyProtocolError("STRATEGY_PROTOCOL_INVALID", str(exc)) from exc
        if param.name_en in seen:
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                f"duplicate custom parameter name_en: {param.name_en}",
            )
        seen.add(param.name_en)
        params.append(param)
    return params


def _normalize_action(raw_action: object) -> ChatQAction:
    if not isinstance(raw_action, dict):
        raise StrategyProtocolError(
            "STRATEGY_RESULT_INVALID",
            "Each action must be an object",
        )
    action_name = raw_action.get("action")
    if action_name not in {"buy", "sell", "close", "cancel", "hold"}:
        raise StrategyProtocolError(
            "STRATEGY_ACTION_INVALID",
            "action must be buy, sell, close, cancel, or hold",
        )
    action = dict(raw_action)
    if action_name in {"buy", "sell"}:
        action.setdefault("order_type", "market")
    return validate_chatq_action(action)


def _infer_param_type(value: object) -> Literal["integer", "number", "string", "boolean"]:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    raise StrategyProtocolError(
        "STRATEGY_PROTOCOL_INVALID",
        "Parameter default values must be integer, number, string, or boolean",
    )


def _is_supported_param_value(value: object) -> bool:
    return isinstance(value, StrategyParamValue)
