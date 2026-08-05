from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class BootstrapConfigResponse(BaseModel):
    config_file_path: str
    database_path: str


class SystemSettingsPayload(BaseModel):
    environment: Literal["development", "desktop", "production"]
    access_log_enabled: bool
    access_log_slow_threshold_ms: int = Field(ge=0)
    cors_origins: list[str]


class LoggingSettingsPayload(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    format: Literal["text", "json"]


class AgentThinkingSettingsPayload(BaseModel):
    type: Literal["disabled", "adaptive", "enabled"]
    budget_tokens: int = Field(ge=0)


class AgentSettingsPayload(BaseModel):
    provider_id: str = Field(min_length=1)
    model: str = Field(min_length=1)
    max_turns: int = Field(ge=0)
    turn_timeout_seconds: int = Field(ge=0)
    first_token_timeout_seconds: int = Field(ge=0)
    skill_plugin_dir: str = Field(min_length=1)
    skill_plugin_name: str = Field(min_length=1)
    include_partial_messages: bool
    thinking: AgentThinkingSettingsPayload
    allowed_tools_default: list[str]
    env_allowlist: list[str]


class AppSettingsPayload(BaseModel):
    system: SystemSettingsPayload
    logging: LoggingSettingsPayload
    agent: AgentSettingsPayload


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
    settings: AppSettingsPayload
