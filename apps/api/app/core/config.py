from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chat-Quant API"
    api_prefix: str = "/api"
    environment: str = Field(default="development", alias="CHATQ_ENV")
    log_level: str = Field(default="INFO", alias="CHATQ_LOG_LEVEL")
    log_format: Literal["text", "json"] = Field(default="text", alias="CHATQ_LOG_FORMAT")
    access_log_enabled: bool = Field(default=True, alias="CHATQ_ACCESS_LOG_ENABLED")
    access_log_slow_threshold_ms: int = Field(
        default=1000,
        alias="CHATQ_ACCESS_LOG_SLOW_THRESHOLD_MS",
    )
    default_user_id: str = Field(
        default="local_user",
        validation_alias=AliasChoices("CHATQ_DEFAULT_USER_ID", "DEFAULT_USER_ID"),
    )
    default_project_id: str = Field(
        default="local_project",
        validation_alias=AliasChoices("CHATQ_DEFAULT_PROJECT_ID", "DEFAULT_PROJECT_ID"),
    )
    claude_agent_cwd: str | None = Field(default=None, alias="CHATQ_CLAUDE_AGENT_CWD")
    artifact_root: Path = Field(default=Path("data/artifacts"), alias="CHATQ_ARTIFACT_ROOT")
    database_path: Path = Field(default=Path("data/chat-quant.db"), alias="CHATQ_DATABASE_PATH")
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ],
        validation_alias=AliasChoices("CHATQ_API_CORS_ORIGINS", "CORS_ORIGINS"),
    )
    agent_model: str = Field(
        default="claude-sonnet-4",
        validation_alias=AliasChoices("ANTHROPIC_MODEL", "AGENT_MODEL"),
    )
    agent_base_url: str | None = Field(default=None, alias="ANTHROPIC_BASE_URL")
    agent_api_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"),
    )
    agent_max_turns: int = Field(default=8, alias="AGENT_MAX_TURNS")
    agent_turn_timeout_seconds: int = Field(default=300, alias="AGENT_TURN_TIMEOUT_SECONDS")
    agent_first_token_timeout_seconds: int = Field(
        default=15,
        alias="AGENT_FIRST_TOKEN_TIMEOUT_SECONDS",
    )
    project_home: str = Field(default="data/projects", alias="PROJECT_HOME")
    agent_skill_plugin_dir: str = Field(
        default="plugin",
        alias="AGENT_SKILL_PLUGIN_DIR",
    )
    agent_skill_plugin_name: str = Field(
        default="chat-quant",
        alias="AGENT_SKILL_PLUGIN_NAME",
    )
    agent_include_partial_messages: bool = Field(
        default=True,
        alias="AGENT_INCLUDE_PARTIAL_MESSAGES",
    )
    agent_thinking_type: Literal["disabled", "adaptive", "enabled"] = Field(
        default="disabled",
        alias="AGENT_THINKING_TYPE",
    )
    agent_thinking_budget_tokens: int = Field(
        default=2048,
        alias="AGENT_THINKING_BUDGET_TOKENS",
    )
    agent_allowed_tools_default: list[str] = Field(
        default=["Bash"],
        alias="AGENT_ALLOWED_TOOLS_DEFAULT",
    )
    agent_env_allowlist: list[str] = Field(
        default=["CHATQ_API_BASE", "CHATQ_AGENT_TOKEN"],
        alias="AGENT_ENV_ALLOWLIST",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("agent_allowed_tools_default", "agent_env_allowlist", mode="before")
    @classmethod
    def split_csv_values(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
