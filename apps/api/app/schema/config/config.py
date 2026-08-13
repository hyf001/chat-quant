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


class SystemSettingsUpdatePayload(BaseModel):
    environment: Literal["development", "desktop", "production"] | None = None
    access_log_enabled: bool | None = None
    access_log_slow_threshold_ms: int | None = Field(default=None, ge=0)


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


class MindgoSettingsUpdatePayload(BaseModel):
    jupyter_url: str | None = None
    auth_scheme: str | None = None
    jupyter_token: str | None = None
    notebook_path: str | None = None
    kernel_id: str | None = None
    timeout_seconds: int | None = Field(default=None, ge=0)


class AppSettingsPayload(BaseModel):
    system: SystemSettingsPayload
    logging: LoggingSettingsPayload
    agent: AgentSettingsPayload
    mindgo: MindgoSettingsPayload


class AppSettingsUpdatePayload(BaseModel):
    system: SystemSettingsUpdatePayload | None = None
    logging: LoggingSettingsUpdatePayload | None = None
    agent: AgentSettingsUpdatePayload | None = None
    mindgo: MindgoSettingsUpdatePayload | None = None


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
