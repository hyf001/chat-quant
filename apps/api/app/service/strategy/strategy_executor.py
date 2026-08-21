from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from app.schema.strategy import JsonValue, StrategyDeploymentMode, StrategyVersionRecord
from app.service.strategy.protocol import (
    ChatQBar,
    ChatQOpenOrder,
    ChatQOrderEvent,
    ChatQPosition,
    ChatQReadOnlyServices,
    StrategyProtocolError,
    load_strategy_module,
    normalize_chatq_result,
)
from app.service.strategy.runtime import ChatQStrategyRuntime


class StrategyExecutionError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


class StrategyExecutionConfig(BaseModel):
    mode: StrategyDeploymentMode
    symbols: list[str] = Field(default_factory=list)
    lookback_bars: int = Field(default=250, ge=1)
    params: dict[str, JsonValue] = Field(default_factory=dict)
    broker_id: str | None = None
    requires_manual_confirm: bool = True
    risk_config: dict[str, JsonValue] = Field(default_factory=dict)
    validate_actions: bool = True


@dataclass(frozen=True)
class StrategyExecutionContext:
    execution_time: str
    history: dict[str, pd.DataFrame]
    current_bars: dict[str, ChatQBar]
    bars: dict[str, pd.DataFrame]
    cash: float = 0.0
    portfolio_value: float = 0.0
    positions: dict[str, ChatQPosition] | None = None
    open_orders: list[ChatQOpenOrder] | None = None
    order_events: list[ChatQOrderEvent] | None = None
    chatq: ChatQReadOnlyServices | None = None


class StrategyExecutionResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    actions: list[dict[str, object]] = Field(default_factory=list)
    state: dict[str, Any] = Field(default_factory=dict)


class StrategyExecutor:
    def __init__(
        self,
        *,
        strategy_version: StrategyVersionRecord,
        config: StrategyExecutionConfig,
        module_name: str | None = None,
    ) -> None:
        self._strategy_version = strategy_version
        self._config = config
        self._module_name = module_name or f"chatq_strategy_executor_{uuid4().hex}"
        try:
            self._module = load_strategy_module(
                strategy_version.source_code,
                module_name=self._module_name,
            )
        except StrategyProtocolError as exc:
            raise StrategyExecutionError(exc.error_code, exc.message) from exc

    def close(self) -> None:
        sys.modules.pop(self._module_name, None)

    def init(self, context: StrategyExecutionContext) -> dict[str, Any]:
        try:
            raw_state = self._module.chatq_init(
                {
                    "mode": self._config.mode.value,
                    "symbols": list(self._config.symbols),
                    "params": dict(self._config.params),
                    "history": context.history,
                    "chatq": context.chatq or ChatQStrategyRuntime(),
                }
            )
        except StrategyProtocolError as exc:
            raise StrategyExecutionError(exc.error_code, exc.message) from exc
        if not isinstance(raw_state, dict):
            raise StrategyExecutionError(
                "STRATEGY_STATE_INVALID",
                "chatq_init must return an object",
            )
        return raw_state

    def next(
        self,
        *,
        state: dict[str, Any],
        context: StrategyExecutionContext,
    ) -> StrategyExecutionResult:
        services = context.chatq or ChatQStrategyRuntime()
        try:
            raw_result = self._module.chatq_next(
                {
                    "mode": self._config.mode.value,
                    "datetime": context.execution_time,
                    "symbols": list(self._config.symbols),
                    "current_bars": context.current_bars,
                    "bars": context.bars,
                    "cash": context.cash,
                    "portfolio_value": context.portfolio_value,
                    "positions": dict(context.positions or {}),
                    "open_orders": list(context.open_orders or []),
                    "order_events": list(context.order_events or []),
                    "params": dict(self._config.params),
                    "chatq": services,
                },
                state,
            )
            result = normalize_chatq_result(
                raw_result,
                old_state=state,
                validate_actions=self._config.validate_actions,
            )
        except StrategyProtocolError as exc:
            raise StrategyExecutionError(exc.error_code, exc.message) from exc
        return StrategyExecutionResult(
            actions=list(result["actions"]),
            state=dict(result["state"]),
        )

    def run_next(
        self,
        *,
        state: dict[str, Any],
        context: StrategyExecutionContext,
    ) -> StrategyExecutionResult:
        initialized_state = dict(state)
        if not initialized_state:
            initialized_state = self.init(context)
        return self.next(state=initialized_state, context=context)
