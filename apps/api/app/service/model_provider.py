from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import DEFAULT_MODEL_PROVIDER_ID, get_settings
from app.model.config import ModelProviderRow
from app.schema.model_provider import (
    ModelProviderListResponse,
    ModelProviderPayload,
    ModelProviderResponse,
    ProviderConnectionTestResponse,
    ProviderModelListResponse,
    ProviderModelResponse,
)


class ModelProviderService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_providers(self) -> ModelProviderListResponse:
        result = await self._db.execute(select(ModelProviderRow).order_by(ModelProviderRow.name))
        return ModelProviderListResponse(
            providers=[_provider_response(row) for row in result.scalars()]
        )

    async def create_provider(self, payload: ModelProviderPayload) -> ModelProviderResponse:
        await _require_models_from_payload(payload)
        now = datetime.now(UTC)
        row = ModelProviderRow(
            id=f"provider_{uuid4().hex[:16]}",
            name=payload.name.strip(),
            base_url=_clean_optional(payload.base_url),
            api_key=_clean_optional(payload.api_key),
            enabled=payload.enabled,
            created_at=now,
            updated_at=now,
        )
        self._db.add(row)
        await self._db.commit()
        await self._db.refresh(row)
        get_settings.cache_clear()
        return _provider_response(row)

    async def update_provider(
        self,
        provider_id: str,
        payload: ModelProviderPayload,
    ) -> ModelProviderResponse:
        await _require_models_from_payload(
            payload,
            existing_api_key=await self._provider_api_key(provider_id),
        )
        row = await self._require_provider(provider_id)
        row.name = payload.name.strip()
        row.base_url = _clean_optional(payload.base_url)
        next_api_key = _clean_optional(payload.api_key)
        if next_api_key is not None:
            row.api_key = next_api_key
        row.enabled = payload.enabled
        row.updated_at = datetime.now(UTC)
        await self._db.commit()
        await self._db.refresh(row)
        get_settings.cache_clear()
        return _provider_response(row)

    async def delete_provider(self, provider_id: str) -> None:
        get_settings.cache_clear()
        settings = get_settings()
        if settings.agent_provider_id == provider_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete the active model provider",
            )
        row = await self._require_provider(provider_id)
        if row.id == DEFAULT_MODEL_PROVIDER_ID:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete the default Anthropic provider",
            )
        await self._db.delete(row)
        await self._db.commit()
        get_settings.cache_clear()

    async def list_models(self, provider_id: str) -> ProviderModelListResponse:
        row = await self._require_provider(provider_id)
        if not row.enabled:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Provider is disabled",
            )
        return ProviderModelListResponse(
            provider_id=row.id,
            models=await _require_models_from_row(row),
        )

    async def test_provider(self, provider_id: str) -> ProviderConnectionTestResponse:
        row = await self._require_provider(provider_id)
        if not row.enabled:
            return ProviderConnectionTestResponse(ok=False, message="Provider is disabled")
        try:
            models = await _fetch_models_from_row(row)
        except ProviderModelFetchError as exc:
            return ProviderConnectionTestResponse(ok=False, message=str(exc))
        return ProviderConnectionTestResponse(
            ok=True,
            message=f"Provider tested, {len(models)} models available",
            models=models,
        )

    async def test_provider_payload(
        self,
        payload: ModelProviderPayload,
        *,
        provider_id: str | None = None,
    ) -> ProviderConnectionTestResponse:
        try:
            models = await _fetch_models_from_payload(
                payload,
                existing_api_key=await self._provider_api_key(provider_id) if provider_id else None,
            )
        except ProviderModelFetchError as exc:
            return ProviderConnectionTestResponse(ok=False, message=str(exc))
        return ProviderConnectionTestResponse(
            ok=True,
            message=f"Provider tested, {len(models)} models available",
            models=models,
        )

    async def _require_provider(self, provider_id: str) -> ModelProviderRow:
        row = await self._db.get(ModelProviderRow, provider_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model provider not found",
            )
        return row

    async def _provider_api_key(self, provider_id: str | None) -> str | None:
        if not provider_id:
            return None
        row = await self._db.get(ModelProviderRow, provider_id)
        return row.api_key if row is not None else None


def _provider_response(row: ModelProviderRow) -> ModelProviderResponse:
    return ModelProviderResponse(
        id=row.id,
        name=row.name,
        base_url=row.base_url,
        has_api_key=bool(row.api_key),
        enabled=row.enabled,
        created_at=row.created_at.isoformat(),
        updated_at=row.updated_at.isoformat(),
    )


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class ProviderModelFetchError(RuntimeError):
    pass


async def _fetch_models_from_row(row: ModelProviderRow) -> list[ProviderModelResponse]:
    return await _fetch_anthropic_models(
        base_url=row.base_url,
        api_key=row.api_key,
        enabled=row.enabled,
    )


async def _require_models_from_row(row: ModelProviderRow) -> list[ProviderModelResponse]:
    try:
        return await _fetch_models_from_row(row)
    except ProviderModelFetchError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc


async def _fetch_models_from_payload(
    payload: ModelProviderPayload,
    *,
    existing_api_key: str | None = None,
) -> list[ProviderModelResponse]:
    return await _fetch_anthropic_models(
        base_url=_clean_optional(payload.base_url),
        api_key=_clean_optional(payload.api_key) or existing_api_key,
        enabled=payload.enabled,
    )


async def _require_models_from_payload(
    payload: ModelProviderPayload,
    *,
    existing_api_key: str | None = None,
) -> list[ProviderModelResponse]:
    try:
        return await _fetch_models_from_payload(
            payload,
            existing_api_key=existing_api_key,
        )
    except ProviderModelFetchError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc


async def _fetch_anthropic_models(
    *,
    base_url: str | None,
    api_key: str | None,
    enabled: bool,
) -> list[ProviderModelResponse]:
    if not enabled:
        raise ProviderModelFetchError("Provider is disabled")
    if base_url and not base_url.startswith(("http://", "https://")):
        raise ProviderModelFetchError("Base URL must be http(s)")
    return await asyncio.to_thread(fetch_anthropic_models, base_url=base_url, api_key=api_key)


def fetch_anthropic_models(
    *,
    base_url: str | None,
    api_key: str | None,
) -> list[ProviderModelResponse]:
    endpoint = urljoin((base_url or "https://api.anthropic.com").rstrip("/") + "/", "v1/models")
    headers = {
        "Accept": "application/json",
        "Anthropic-Version": "2023-06-01",
    }
    if api_key:
        headers["X-Api-Key"] = api_key
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(endpoint, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise ProviderModelFetchError(f"Model list request failed: HTTP {exc.code}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ProviderModelFetchError(f"Model list request failed: {exc}") from exc

    models = _models_from_payload(payload)
    if not models:
        raise ProviderModelFetchError("Model list response did not contain models")
    return models


def _models_from_payload(payload: Any) -> list[ProviderModelResponse]:
    if not isinstance(payload, dict):
        return []
    raw_models = payload.get("data")
    if not isinstance(raw_models, list):
        return []
    models: list[ProviderModelResponse] = []
    for raw_model in raw_models:
        if not isinstance(raw_model, dict):
            continue
        model_id = raw_model.get("id")
        if not isinstance(model_id, str) or not model_id:
            continue
        display_name = raw_model.get("display_name")
        models.append(
            ProviderModelResponse(
                id=model_id,
                name=display_name if isinstance(display_name, str) and display_name else model_id,
            )
        )
    return models
