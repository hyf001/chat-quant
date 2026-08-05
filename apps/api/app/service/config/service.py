from __future__ import annotations

import json
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (
    APP_CONFIG_DEFINITIONS,
    ConfigValue,
    Settings,
    coerce_config_value,
    get_settings,
)
from app.model.config import AppSettingRow, ModelProviderRow
from app.schema.config import (
    AgentSettingsPayload,
    AgentThinkingSettingsPayload,
    AppConfigResponse,
    AppSettingsPayload,
    BootstrapConfigResponse,
    ConfigFieldDefinitionResponse,
    IdentitySettingsPayload,
    LoggingSettingsPayload,
    PathSettingsPayload,
    SystemSettingsPayload,
    UpdateAppConfigRequest,
)


class AppConfigService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_config(self) -> AppConfigResponse:
        get_settings.cache_clear()
        settings = get_settings()
        return _response_from_settings(settings)

    async def update_config(self, request: UpdateAppConfigRequest) -> AppConfigResponse:
        values = _flatten_payload(request.settings)
        definitions = {definition.key: definition for definition in APP_CONFIG_DEFINITIONS}
        now = datetime.now(UTC)

        for key, raw_value in values.items():
            definition = definitions[key]
            value = coerce_config_value(definition, raw_value)
            if key == "agent_provider_id":
                await self._validate_agent_provider(str(value))
            row = await self._db.get(
                AppSettingRow,
                {
                    "scope": "global",
                    "namespace": definition.group,
                    "key": definition.key,
                },
            )
            if row is None:
                row = AppSettingRow(
                    scope="global",
                    namespace=definition.group,
                    key=definition.key,
                    value_json=json.dumps(value),
                    value_type=definition.value_type,
                    is_secret=definition.value_type == "password",
                    label=definition.label,
                    description=definition.description,
                    updated_at=now,
                )
                self._db.add(row)
            else:
                row.value_json = json.dumps(value)
                row.value_type = definition.value_type
                row.is_secret = definition.value_type == "password"
                row.label = definition.label
                row.description = definition.description
                row.updated_at = now

        await self._db.commit()
        get_settings.cache_clear()
        return await self.get_config()

    async def _validate_agent_provider(self, provider_id: str) -> None:
        row = await self._db.get(ModelProviderRow, provider_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Agent provider does not exist",
            )
        if not row.enabled:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Agent provider is disabled",
            )


async def list_setting_rows(db: AsyncSession) -> list[AppSettingRow]:
    rows = await db.execute(
        select(AppSettingRow).where(AppSettingRow.scope == "global").order_by(AppSettingRow.key)
    )
    return list(rows.scalars())


def _response_from_settings(settings: Settings) -> AppConfigResponse:
    return AppConfigResponse(
        bootstrap=BootstrapConfigResponse(
            config_file_path=str(settings.config_file_path),
            database_path=str(settings.database_path),
        ),
        settings=_payload_from_settings(settings),
        fields=[
            ConfigFieldDefinitionResponse(
                namespace=definition.group,
                key=definition.key,
                label=definition.label,
                value_type=definition.value_type,
                description=definition.description,
                options=list(definition.options),
                is_secret=definition.value_type == "password",
            )
            for definition in APP_CONFIG_DEFINITIONS
        ],
    )


def _payload_from_settings(settings: Settings) -> AppSettingsPayload:
    return AppSettingsPayload(
        system=SystemSettingsPayload(
            environment=settings.environment,  # type: ignore[arg-type]
            access_log_enabled=settings.access_log_enabled,
            access_log_slow_threshold_ms=settings.access_log_slow_threshold_ms,
            cors_origins=settings.cors_origins,
        ),
        logging=LoggingSettingsPayload(
            level=settings.log_level,  # type: ignore[arg-type]
            format=settings.log_format,
        ),
        identity=IdentitySettingsPayload(
            default_user_id=settings.default_user_id,
            default_project_id=settings.default_project_id,
        ),
        paths=PathSettingsPayload(
            claude_agent_cwd=settings.claude_agent_cwd,
            project_home=settings.project_home,
        ),
        agent=AgentSettingsPayload(
            provider_id=settings.agent_provider_id,
            model=settings.agent_model,
            max_turns=settings.agent_max_turns,
            turn_timeout_seconds=settings.agent_turn_timeout_seconds,
            first_token_timeout_seconds=settings.agent_first_token_timeout_seconds,
            skill_plugin_dir=settings.agent_skill_plugin_dir,
            skill_plugin_name=settings.agent_skill_plugin_name,
            include_partial_messages=settings.agent_include_partial_messages,
            thinking=AgentThinkingSettingsPayload(
                type=settings.agent_thinking_type,
                budget_tokens=settings.agent_thinking_budget_tokens,
            ),
            allowed_tools_default=settings.agent_allowed_tools_default,
            env_allowlist=settings.agent_env_allowlist,
        ),
    )


def _flatten_payload(payload: AppSettingsPayload) -> dict[str, ConfigValue]:
    return {
        "environment": payload.system.environment,
        "access_log_enabled": payload.system.access_log_enabled,
        "access_log_slow_threshold_ms": payload.system.access_log_slow_threshold_ms,
        "cors_origins": payload.system.cors_origins,
        "log_level": payload.logging.level,
        "log_format": payload.logging.format,
        "default_user_id": payload.identity.default_user_id,
        "default_project_id": payload.identity.default_project_id,
        "claude_agent_cwd": payload.paths.claude_agent_cwd,
        "project_home": payload.paths.project_home,
        "agent_provider_id": payload.agent.provider_id,
        "agent_model": payload.agent.model,
        "agent_max_turns": payload.agent.max_turns,
        "agent_turn_timeout_seconds": payload.agent.turn_timeout_seconds,
        "agent_first_token_timeout_seconds": payload.agent.first_token_timeout_seconds,
        "agent_skill_plugin_dir": payload.agent.skill_plugin_dir,
        "agent_skill_plugin_name": payload.agent.skill_plugin_name,
        "agent_include_partial_messages": payload.agent.include_partial_messages,
        "agent_thinking_type": payload.agent.thinking.type,
        "agent_thinking_budget_tokens": payload.agent.thinking.budget_tokens,
        "agent_allowed_tools_default": payload.agent.allowed_tools_default,
        "agent_env_allowlist": payload.agent.env_allowlist,
    }
