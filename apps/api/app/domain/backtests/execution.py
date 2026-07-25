from __future__ import annotations

from typing import Protocol

from app.domain.backtests.models import (
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
)
from app.domain.strategies.models import StrategyVersionRecord


class StrategyBacktestError(Exception):
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


class StrategyBacktestEngine(Protocol):
    name: str
    protocol_name: str

    def execute(
        self,
        *,
        backtest: StrategyBacktestRecord,
        version: StrategyVersionRecord,
    ) -> StrategyBacktestResultRecord:
        ...
