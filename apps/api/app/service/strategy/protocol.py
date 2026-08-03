from __future__ import annotations

import sys
from dataclasses import dataclass
from types import ModuleType
from typing import Literal
from uuid import uuid4

import backtrader as bt
from pydantic import ValidationError

from app.schema.strategy import StrategyCustomParameter, StrategyParamValue

ParamSource = Literal["chatq_params", "native_params", "none"]


@dataclass(frozen=True)
class StrategyProtocolSpec:
    strategy_cls: type[bt.Strategy]
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
        strategy_cls = load_strategy_class(source_code, module_name=module_name)
        custom_params, param_source = _extract_custom_params(strategy_cls)
        return StrategyProtocolSpec(
            strategy_cls=strategy_cls,
            custom_params=custom_params,
            param_source=param_source,
        )
    finally:
        sys.modules.pop(module_name, None)


def load_strategy_class(source_code: str, *, module_name: str) -> type[bt.Strategy]:
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

    strategy_classes = [
        value
        for value in module.__dict__.values()
        if isinstance(value, type) and issubclass(value, bt.Strategy) and value is not bt.Strategy
    ]
    if not strategy_classes:
        raise StrategyProtocolError(
            "STRATEGY_PROTOCOL_INVALID",
            "Source code must define a backtrader.Strategy subclass",
        )
    if len(strategy_classes) > 1:
        raise StrategyProtocolError(
            "STRATEGY_PROTOCOL_INVALID",
            "Source code must define exactly one backtrader.Strategy subclass",
        )
    return strategy_classes[0]


def with_backtrader_params(
    strategy_cls: type[bt.Strategy],
    custom_params: list[StrategyCustomParameter],
) -> type[bt.Strategy]:
    if not custom_params:
        return strategy_cls
    return type(
        strategy_cls.__name__,
        (strategy_cls,),
        {"params": tuple((param.name_en, param.default) for param in custom_params)},
    )


def _extract_custom_params(
    strategy_cls: type[bt.Strategy],
) -> tuple[list[StrategyCustomParameter], ParamSource]:
    chatq_params = getattr(strategy_cls, "chatq_params", None)
    if chatq_params is not None:
        if not callable(chatq_params):
            raise StrategyProtocolError(
                "STRATEGY_PROTOCOL_INVALID",
                "chatq_params must be callable",
            )
        try:
            raw_params = chatq_params()
        except Exception as exc:
            raise StrategyProtocolError("STRATEGY_PROTOCOL_INVALID", str(exc)) from exc
        return _parse_chatq_params(raw_params), "chatq_params"

    native_params = _native_backtrader_params(strategy_cls)
    if native_params:
        return native_params, "native_params"
    return [], "none"


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


def _native_backtrader_params(strategy_cls: type[bt.Strategy]) -> list[StrategyCustomParameter]:
    param_info = getattr(strategy_cls, "params", None)
    if not hasattr(param_info, "_getitems"):
        return []

    params: list[StrategyCustomParameter] = []
    for name, default in param_info._getitems():
        if not isinstance(name, str) or not name:
            continue
        if not _is_supported_param_value(default):
            continue
        params.append(
            StrategyCustomParameter(
                name_cn=name,
                name_en=name,
                type=_infer_param_type(default),
                default=default,
                required=True,
            )
        )
    return params


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
