from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ModelProviderPayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    base_url: str | None = None
    api_key: str | None = None
    enabled: bool = True

    @field_validator("base_url", "api_key", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value


class ModelProviderResponse(BaseModel):
    id: str
    name: str
    base_url: str | None
    has_api_key: bool
    enabled: bool
    created_at: str
    updated_at: str


class ModelProviderListResponse(BaseModel):
    providers: list[ModelProviderResponse]


class ModelProviderApiKeyResponse(BaseModel):
    api_key: str | None


class ProviderModelResponse(BaseModel):
    id: str
    name: str


class ProviderModelListResponse(BaseModel):
    provider_id: str
    models: list[ProviderModelResponse]


class ProviderConnectionTestResponse(BaseModel):
    ok: bool
    message: str
    models: list[ProviderModelResponse] = []
