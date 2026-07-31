from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

StrategyParamValue = int | float | str | bool
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def utc_now() -> datetime:
    return datetime.now(UTC)


class StrategyStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class StrategyPythonFile(BaseModel):
    path: str = Field(min_length=1, max_length=256)
    content: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_code_path(self) -> StrategyPythonFile:
        validate_relative_python_path(self.path)
        return self


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
    entrypoint: str = Field(min_length=3, max_length=256)
    python_file: StrategyPythonFile
    params_schema: dict[str, StrategyParameterSchema]
    default_params: dict[str, StrategyParamValue]
    risk_notes: list[str] = Field(default_factory=list)

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
        validate_relative_python_path(module_path)
        if not class_name.isidentifier():
            raise ValueError("entrypoint class must be a Python identifier")
        if module_path != self.python_file.path:
            raise ValueError("entrypoint module must match python_file.path")

        return self


class StrategyRecord(BaseModel):
    id: str
    user_id: str
    project_id: str
    name: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    current_version_id: str | None = None
    status: StrategyStatus = StrategyStatus.ACTIVE
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StrategyVersionRecord(BaseModel):
    id: str
    strategy_id: str
    version: int
    entrypoint: str
    python_file: StrategyPythonFile
    params_schema: dict[str, StrategyParameterSchema]
    default_params: dict[str, StrategyParamValue]
    code_checksum: str
    created_at: datetime = Field(default_factory=utc_now)


class StrategySummary(BaseModel):
    strategy_id: str
    strategy_version_id: str
    version: int
    name: str
    status: StrategyStatus
    tags: list[str]
    default_params: dict[str, StrategyParamValue]
    updated_at: datetime


class StrategyDetail(BaseModel):
    strategy: StrategyRecord


class StrategyCreateResult(BaseModel):
    strategy_id: str
    entrypoint: str


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


def validate_relative_python_path(path_text: str) -> None:
    if not path_text.endswith(".py"):
        raise ValueError("entrypoint module must be a Python file")
    if path_text.startswith("/") or "\\" in path_text:
        raise ValueError("entrypoint module must be a relative POSIX path")
    parts = path_text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("entrypoint module must stay inside the strategy package")
