from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

StrategyParamValue = int | float | str | bool


def utc_now() -> datetime:
    return datetime.now(UTC)


class StrategyStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class StrategyVersionStatus(StrEnum):
    DRAFT = "draft"
    VALIDATING = "validating"
    VALIDATED = "validated"
    INVALID = "invalid"
    ARCHIVED = "archived"


class StrategyCopyMode(StrEnum):
    SUMMARY = "summary"
    NEW_STRATEGY = "new_strategy"


class ValidationCheckStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"


class StrategyParameterUi(BaseModel):
    control: Literal["number", "select", "checkbox", "text"] = "text"
    unit: str | None = None

    model_config = ConfigDict(extra="forbid")


class StrategyParameterSchema(BaseModel):
    type: Literal["integer", "number", "string", "boolean"]
    title: str
    description: str | None = None
    default: StrategyParamValue
    minimum: float | None = None
    maximum: float | None = None
    enum: list[StrategyParamValue] | None = None
    required: bool = True
    ui: StrategyParameterUi = Field(default_factory=StrategyParameterUi)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_default_value(self) -> StrategyParameterSchema:
        validate_param_value("default", self.default, self)
        return self


class StrategyPackage(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str | None = None
    strategy_type: str = Field(min_length=1, max_length=64)
    entrypoint: str = Field(min_length=3, max_length=256)
    code_artifact_id: str = Field(min_length=1, max_length=128)
    params_schema: dict[str, StrategyParameterSchema]
    default_params: dict[str, StrategyParamValue]
    logic_summary: str | None = None
    risk_notes: list[str] = Field(default_factory=list)
    version_name: str | None = Field(default=None, max_length=128)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_params_contract(self) -> StrategyPackage:
        if not self.params_schema:
            raise ValueError("params_schema must define at least one strategy parameter")

        schema_keys = set(self.params_schema)
        default_keys = set(self.default_params)
        if schema_keys != default_keys:
            raise ValueError("default_params keys must exactly match params_schema keys")

        for name, spec in self.params_schema.items():
            if not name.isidentifier():
                raise ValueError(f"parameter name must be a Python identifier: {name}")
            value = self.default_params[name]
            validate_param_value(name, value, spec)
            if value != spec.default:
                raise ValueError(f"default_params.{name} must match params_schema.{name}.default")

        if ":" not in self.entrypoint:
            raise ValueError("entrypoint must use '<file.py>:<ClassName>' format")

        module_path, class_name = self.entrypoint.split(":", 1)
        if not module_path.endswith(".py") or "/" in module_path or "\\" in module_path:
            raise ValueError("entrypoint module must be a Python file name")
        if not class_name.isidentifier():
            raise ValueError("entrypoint class must be a Python identifier")

        return self


class StrategyValidationCheck(BaseModel):
    name: str
    status: ValidationCheckStatus
    message: str | None = None


class StrategyRecord(BaseModel):
    id: str
    user_id: str
    project_id: str
    chat_session_id: str
    source_sdk_message_uuid: str | None = None
    name: str
    description: str | None = None
    strategy_type: str
    tags: list[str] = Field(default_factory=list)
    current_version_id: str | None = None
    status: StrategyStatus = StrategyStatus.ACTIVE
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StrategyVersionRecord(BaseModel):
    id: str
    strategy_id: str
    version: int
    version_name: str | None = None
    parent_version_id: str | None = None
    code_artifact_id: str
    entrypoint: str
    params_schema: dict[str, StrategyParameterSchema]
    default_params: dict[str, StrategyParamValue]
    logic_summary: str | None = None
    change_summary: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    code_checksum: str
    status: StrategyVersionStatus = StrategyVersionStatus.DRAFT
    validation_error: str | None = None
    validation_details: list[StrategyValidationCheck] = Field(default_factory=list)
    validated_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)


class StrategyCopyRecord(BaseModel):
    id: str
    source_strategy_version_id: str
    target_strategy_id: str | None = None
    target_chat_session_id: str | None = None
    mode: StrategyCopyMode
    created_by: str
    created_at: datetime = Field(default_factory=utc_now)


class StrategyValidationResult(BaseModel):
    strategy_version_id: str
    status: StrategyVersionStatus
    checks: list[StrategyValidationCheck]
    execution_result_id: str | None = None
    error: str | None = None
    validated_at: datetime | None = None


class StrategySummary(BaseModel):
    strategy_id: str
    strategy_version_id: str
    version: int
    name: str
    strategy_type: str
    status: StrategyStatus
    version_status: StrategyVersionStatus
    tags: list[str]
    logic_summary: str | None = None
    default_params: dict[str, StrategyParamValue]
    updated_at: datetime


class StrategyDetail(BaseModel):
    strategy: StrategyRecord
    versions: list[StrategyVersionRecord]


class StrategyCreateResult(BaseModel):
    strategy_id: str
    strategy_version_id: str
    version: int
    status: StrategyVersionStatus
    entrypoint: str


class StrategyCopySummary(BaseModel):
    mode: StrategyCopyMode
    source_strategy_version_id: str
    summary: str
    target_strategy_id: str | None = None
    copy_record_id: str

def validate_param_value(
    name: str,
    value: StrategyParamValue,
    spec: StrategyParameterSchema,
) -> None:
    if spec.type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        raise ValueError(f"{name} must be an integer")
    if spec.type == "number" and (not isinstance(value, int | float) or isinstance(value, bool)):
        raise ValueError(f"{name} must be a number")
    if spec.type == "string" and not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if spec.type == "boolean" and not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")

    if spec.enum is not None and value not in spec.enum:
        raise ValueError(f"{name} must be one of {spec.enum}")

    if isinstance(value, int | float) and not isinstance(value, bool):
        if spec.minimum is not None and value < spec.minimum:
            raise ValueError(f"{name} must be >= {spec.minimum}")
        if spec.maximum is not None and value > spec.maximum:
            raise ValueError(f"{name} must be <= {spec.maximum}")
