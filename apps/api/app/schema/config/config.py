from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class BootstrapConfigResponse(BaseModel):
    config_file_path: str
    database_path: str
    api_host: str
    api_port: int
    web_host: str
    web_port: int


class SystemSettingsPayload(BaseModel):
    environment: Literal["development", "desktop", "production"]
    access_log_enabled: bool
    access_log_slow_threshold_ms: int = Field(ge=0)
    job_runtime_creation_tick_minutes: int = Field(ge=1)
    job_runtime_dispatch_interval_seconds: int = Field(ge=1)
    job_runtime_dispatch_limit: int = Field(ge=1)
    job_runtime_max_concurrent_instances: int = Field(ge=1)


class SystemSettingsUpdatePayload(BaseModel):
    environment: Literal["development", "desktop", "production"] | None = None
    access_log_enabled: bool | None = None
    access_log_slow_threshold_ms: int | None = Field(default=None, ge=0)
    job_runtime_creation_tick_minutes: int | None = Field(default=None, ge=1)
    job_runtime_dispatch_interval_seconds: int | None = Field(default=None, ge=1)
    job_runtime_dispatch_limit: int | None = Field(default=None, ge=1)
    job_runtime_max_concurrent_instances: int | None = Field(default=None, ge=1)


class LoggingSettingsPayload(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class LoggingSettingsUpdatePayload(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] | None = None


class AgentThinkingSettingsPayload(BaseModel):
    type: Literal["disabled", "adaptive", "enabled"]
    budget_tokens: int = Field(ge=0)


class AgentThinkingSettingsUpdatePayload(BaseModel):
    type: Literal["disabled", "adaptive", "enabled"] | None = None
    budget_tokens: int | None = Field(default=None, ge=0)


class AgentSettingsPayload(BaseModel):
    provider_id: str = Field(min_length=1)
    model: str = Field(min_length=1)
    max_turns: int = Field(ge=0)
    turn_timeout_seconds: int = Field(ge=0)
    first_token_timeout_seconds: int = Field(ge=0)
    include_partial_messages: bool
    thinking: AgentThinkingSettingsPayload
    available_tools: list[str]


class AgentSettingsUpdatePayload(BaseModel):
    provider_id: str | None = Field(default=None, min_length=1)
    model: str | None = Field(default=None, min_length=1)
    max_turns: int | None = Field(default=None, ge=0)
    turn_timeout_seconds: int | None = Field(default=None, ge=0)
    first_token_timeout_seconds: int | None = Field(default=None, ge=0)
    include_partial_messages: bool | None = None
    thinking: AgentThinkingSettingsUpdatePayload | None = None
    available_tools: list[str] | None = None


class MindgoSettingsPayload(BaseModel):
    jupyter_url: str | None = None
    auth_scheme: str
    jupyter_token: str | None = None
    notebook_path: str
    kernel_id: str | None = None
    timeout_seconds: int = Field(ge=0)
    storage_root: str = Field(min_length=1)


class MindgoSettingsUpdatePayload(BaseModel):
    jupyter_url: str | None = None
    auth_scheme: str | None = None
    jupyter_token: str | None = None
    notebook_path: str | None = None
    kernel_id: str | None = None
    timeout_seconds: int | None = Field(default=None, ge=0)
    storage_root: str | None = Field(default=None, min_length=1)


class MarketDataDatasetSettingsPayload(BaseModel):
    dataset_id: str = ""
    symbol_field: str = ""
    datetime_field: str = ""
    open_field: str = ""
    high_field: str = ""
    low_field: str = ""
    close_field: str = ""
    volume_field: str = ""


class MarketDataBenchmarkDatasetSettingsPayload(BaseModel):
    dataset_id: str = ""
    symbol_field: str = ""
    datetime_field: str = ""
    close_field: str = ""


class MarketDataSettingsPayload(BaseModel):
    market_data_dataset: MarketDataDatasetSettingsPayload
    benchmark_dataset: MarketDataBenchmarkDatasetSettingsPayload


class MarketDataDatasetSettingsUpdatePayload(BaseModel):
    dataset_id: str | None = None
    symbol_field: str | None = None
    datetime_field: str | None = None
    open_field: str | None = None
    high_field: str | None = None
    low_field: str | None = None
    close_field: str | None = None
    volume_field: str | None = None


class MarketDataBenchmarkDatasetSettingsUpdatePayload(BaseModel):
    dataset_id: str | None = None
    symbol_field: str | None = None
    datetime_field: str | None = None
    close_field: str | None = None


class MarketDataSettingsUpdatePayload(BaseModel):
    market_data_dataset: MarketDataDatasetSettingsUpdatePayload | None = None
    benchmark_dataset: MarketDataBenchmarkDatasetSettingsUpdatePayload | None = None


class AppSettingsPayload(BaseModel):
    system: SystemSettingsPayload
    logging: LoggingSettingsPayload
    agent: AgentSettingsPayload
    mindgo: MindgoSettingsPayload
    market_data: MarketDataSettingsPayload


class AppSettingsUpdatePayload(BaseModel):
    system: SystemSettingsUpdatePayload | None = None
    logging: LoggingSettingsUpdatePayload | None = None
    agent: AgentSettingsUpdatePayload | None = None
    mindgo: MindgoSettingsUpdatePayload | None = None
    market_data: MarketDataSettingsUpdatePayload | None = None


class ConfigFieldDefinitionResponse(BaseModel):
    namespace: str
    key: str
    label: str
    value_type: str
    description: str
    options: list[str]
    is_secret: bool


class AppConfigResponse(BaseModel):
    bootstrap: BootstrapConfigResponse
    settings: AppSettingsPayload
    fields: list[ConfigFieldDefinitionResponse]


class UpdateAppConfigRequest(BaseModel):
    settings: AppSettingsUpdatePayload
