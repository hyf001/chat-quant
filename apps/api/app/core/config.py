from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chat-Quant API"
    api_prefix: str = "/api"
    environment: str = Field(default="development", alias="CHATQ_ENV")
    claude_agent_cwd: str | None = Field(default=None, alias="CHATQ_CLAUDE_AGENT_CWD")
    artifact_root: Path = Field(default=Path("data/artifacts"), alias="CHATQ_ARTIFACT_ROOT")
    artifact_index_path: Path = Field(
        default=Path("data/artifacts.sqlite3"),
        alias="CHATQ_ARTIFACT_INDEX_PATH",
    )
    runtime_root: Path = Field(
        default=Path("storage/runtime"),
        validation_alias=AliasChoices("CHATQ_RUNTIME_ROOT", "RUNTIME_ROOT"),
    )
    runtime_stdout_limit_bytes: int = 200 * 1024
    runtime_max_output_files: int = 200
    runtime_max_artifact_bytes: int = 20 * 1024 * 1024
    runtime_timeout_grace_seconds: float = 5
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ],
        validation_alias=AliasChoices("CHATQ_API_CORS_ORIGINS", "CORS_ORIGINS"),
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
