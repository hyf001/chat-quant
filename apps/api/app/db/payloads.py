from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schema.backtest import StrategyBacktestRecord, StrategyBacktestResultRecord


class StrategyBacktestPayload(BaseModel):
    schema_version: Literal[1] = 1
    backtest: StrategyBacktestRecord
    result: StrategyBacktestResultRecord | None = None

    model_config = ConfigDict(extra="forbid")
