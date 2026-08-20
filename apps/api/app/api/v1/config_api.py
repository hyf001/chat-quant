from fastapi import APIRouter

from app.api.v1.dependencies import DatabaseSession
from app.schema.config import AppConfigResponse, UpdateAppConfigRequest
from app.service.config import AppConfigService

router = APIRouter()

@router.get("", response_model=AppConfigResponse)
async def get_app_config(db: DatabaseSession) -> AppConfigResponse:
    return await AppConfigService(db).get_config()


@router.put("", response_model=AppConfigResponse)
async def update_app_config(
    payload: UpdateAppConfigRequest,
    db: DatabaseSession,
) -> AppConfigResponse:
    return await AppConfigService(db).update_config(payload)
