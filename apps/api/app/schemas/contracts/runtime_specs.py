from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.contracts.json_types import JsonObject

RuntimePurpose = Literal[
    "query_analysis",
    "stock_screening",
    "chart_generation",
    "strategy_smoke_test",
    "utility",
]


class RuntimeCodeFile(BaseModel):
    path: str
    content: str


class PythonExecutionSpec(BaseModel):
    chat_session_id: str
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    code_artifact_id: str
    entrypoint: str
    args: list[str] = Field(default_factory=list)
    stdin_json: JsonObject | None = None
    env: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int = 30
    expected_outputs: list[str] = Field(default_factory=list)
    result_schema: JsonObject | None = None
    purpose: RuntimePurpose = "query_analysis"
    code_files: list[RuntimeCodeFile] = Field(default_factory=list)

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, value: int) -> int:
        if value <= 0 or value > 600:
            raise ValueError("timeout_seconds must be between 1 and 600")
        return value


class BacktestRunSpec(BaseModel):
    backtest_run_id: str
    strategy_version_id: str
    code_artifact_id: str
    entrypoint: str
    symbols: list[str]
    market: Literal["CN", "US"]
    start_date: date
    end_date: date
    initial_cash: float
    commission: float
    slippage: float = 0
    data_adjust: str = "qfq"
    timeframe: str = "1d"
    params: JsonObject = Field(default_factory=dict)
    output_path: str = "result.json"
    code_files: list[RuntimeCodeFile] = Field(default_factory=list)

    @field_validator("symbols")
    @classmethod
    def validate_symbols(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("symbols must not be empty")
        if len(value) > 500:
            raise ValueError("symbols may not contain more than 500 items")
        return value

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("end_date may not be in the future")
        return value

    @field_validator("initial_cash")
    @classmethod
    def validate_initial_cash(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("initial_cash must be greater than 0")
        return value

    @field_validator("commission", "slippage")
    @classmethod
    def validate_non_negative_cost(cls, value: float) -> float:
        if value < 0:
            raise ValueError("commission and slippage must be non-negative")
        return value

    @field_validator("output_path")
    @classmethod
    def validate_output_path(cls, value: str) -> str:
        if value.startswith("/") or ".." in value.split("/"):
            raise ValueError("output_path must be a relative path within output_dir")
        return value

    def model_post_init(self, __context: object) -> None:
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
