from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chat-Quant API"
    api_prefix: str = "/api"
    environment: str = Field(default="development", alias="CHATQ_ENV")
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"],
        validation_alias=AliasChoices("CHATQ_API_CORS_ORIGINS", "CORS_ORIGINS"),
    )
    agent_model: str = Field(default="claude-sonnet-4", alias="AGENT_MODEL")
    agent_max_turns: int = Field(default=8, alias="AGENT_MAX_TURNS")
    agent_turn_timeout_seconds: int = Field(default=300, alias="AGENT_TURN_TIMEOUT_SECONDS")
    agent_first_token_timeout_seconds: int = Field(
        default=15,
        alias="AGENT_FIRST_TOKEN_TIMEOUT_SECONDS",
    )
    agent_workdir_root: str = Field(
        default="/tmp/chatq/sdk-sessions",
        alias="AGENT_WORKDIR_ROOT",
    )
    agent_project_skill_dir: str = Field(
        default="apps/api/agent_workdir/.claude/skills",
        alias="AGENT_PROJECT_SKILL_DIR",
    )
    agent_include_partial_messages: bool = Field(
        default=True,
        alias="AGENT_INCLUDE_PARTIAL_MESSAGES",
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
