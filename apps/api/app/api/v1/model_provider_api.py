from fastapi import APIRouter, Response, status

from app.api.v1.dependencies import DatabaseSession
from app.schema.model_provider import (
    ModelProviderListResponse,
    ModelProviderPayload,
    ModelProviderResponse,
    ProviderConnectionTestResponse,
    ProviderModelListResponse,
)
from app.service.model_provider import ModelProviderService

router = APIRouter()


@router.get("", response_model=ModelProviderListResponse)
async def list_model_providers(db: DatabaseSession) -> ModelProviderListResponse:
    return await ModelProviderService(db).list_providers()


@router.post("", response_model=ModelProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_model_provider(
    payload: ModelProviderPayload,
    db: DatabaseSession,
) -> ModelProviderResponse:
    return await ModelProviderService(db).create_provider(payload)


@router.post("/test", response_model=ProviderConnectionTestResponse)
async def test_model_provider_payload(
    payload: ModelProviderPayload,
    db: DatabaseSession,
) -> ProviderConnectionTestResponse:
    return await ModelProviderService(db).test_provider_payload(payload)


@router.put("/{provider_id}", response_model=ModelProviderResponse)
async def update_model_provider(
    provider_id: str,
    payload: ModelProviderPayload,
    db: DatabaseSession,
) -> ModelProviderResponse:
    return await ModelProviderService(db).update_provider(provider_id, payload)


@router.post("/{provider_id}/test-payload", response_model=ProviderConnectionTestResponse)
async def test_existing_model_provider_payload(
    provider_id: str,
    payload: ModelProviderPayload,
    db: DatabaseSession,
) -> ProviderConnectionTestResponse:
    return await ModelProviderService(db).test_provider_payload(
        payload,
        provider_id=provider_id,
    )


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model_provider(provider_id: str, db: DatabaseSession) -> Response:
    await ModelProviderService(db).delete_provider(provider_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{provider_id}/test", response_model=ProviderConnectionTestResponse)
async def test_model_provider(
    provider_id: str,
    db: DatabaseSession,
) -> ProviderConnectionTestResponse:
    return await ModelProviderService(db).test_provider(provider_id)


@router.get("/{provider_id}/models", response_model=ProviderModelListResponse)
async def list_model_provider_models(
    provider_id: str,
    db: DatabaseSession,
) -> ProviderModelListResponse:
    return await ModelProviderService(db).list_models(provider_id)
