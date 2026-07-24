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
