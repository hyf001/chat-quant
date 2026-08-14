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
from app.core.logging import configure_logging
from app.model.config import AppSettingRow, ModelProviderRow
from app.schema.config import (
    AgentSettingsPayload,
    AgentThinkingSettingsPayload,
    AppConfigResponse,
    AppSettingsPayload,
    AppSettingsUpdatePayload,
    BootstrapConfigResponse,
    ConfigFieldDefinitionResponse,
    LoggingSettingsPayload,
    MindgoSettingsPayload,
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
        configure_logging(get_settings())
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
            api_host=settings.api_host,
            api_port=settings.api_port,
            web_host=settings.web_host,
            web_port=settings.web_port,
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
        ),
        logging=LoggingSettingsPayload(
            level=settings.log_level,  # type: ignore[arg-type]
        ),
        agent=AgentSettingsPayload(
            provider_id=settings.agent_provider_id,
            model=settings.agent_model,
            max_turns=settings.agent_max_turns,
            turn_timeout_seconds=settings.agent_turn_timeout_seconds,
            first_token_timeout_seconds=settings.agent_first_token_timeout_seconds,
            include_partial_messages=settings.agent_include_partial_messages,
            thinking=AgentThinkingSettingsPayload(
                type=settings.agent_thinking_type,
                budget_tokens=settings.agent_thinking_budget_tokens,
            ),
            available_tools=settings.agent_available_tools,
        ),
        mindgo=MindgoSettingsPayload(
            jupyter_url=settings.mindgo_jupyter_url,
            auth_scheme=settings.mindgo_auth_scheme,
            jupyter_token=settings.mindgo_jupyter_token,
            notebook_path=settings.mindgo_notebook_path,
            kernel_id=settings.mindgo_kernel_id,
            timeout_seconds=settings.mindgo_timeout_seconds,
            storage_root=settings.mindgo_storage_root,
        ),
    )


def _flatten_payload(payload: AppSettingsUpdatePayload) -> dict[str, ConfigValue]:
    values: dict[str, ConfigValue] = {}
    if payload.system is not None:
        if payload.system.environment is not None:
            values["environment"] = payload.system.environment
        if payload.system.access_log_enabled is not None:
            values["access_log_enabled"] = payload.system.access_log_enabled
        if payload.system.access_log_slow_threshold_ms is not None:
            values["access_log_slow_threshold_ms"] = payload.system.access_log_slow_threshold_ms
    if payload.logging is not None:
        if payload.logging.level is not None:
            values["log_level"] = payload.logging.level
    if payload.agent is not None:
        if payload.agent.provider_id is not None:
            values["agent_provider_id"] = payload.agent.provider_id
        if payload.agent.model is not None:
            values["agent_model"] = payload.agent.model
        if payload.agent.max_turns is not None:
            values["agent_max_turns"] = payload.agent.max_turns
        if payload.agent.turn_timeout_seconds is not None:
            values["agent_turn_timeout_seconds"] = payload.agent.turn_timeout_seconds
        if payload.agent.first_token_timeout_seconds is not None:
            values["agent_first_token_timeout_seconds"] = payload.agent.first_token_timeout_seconds
        if payload.agent.include_partial_messages is not None:
            values["agent_include_partial_messages"] = payload.agent.include_partial_messages
        if payload.agent.thinking is not None:
            if payload.agent.thinking.type is not None:
                values["agent_thinking_type"] = payload.agent.thinking.type
            if payload.agent.thinking.budget_tokens is not None:
                values["agent_thinking_budget_tokens"] = payload.agent.thinking.budget_tokens
        if payload.agent.available_tools is not None:
            values["agent_available_tools"] = payload.agent.available_tools
    if payload.mindgo is not None:
        if payload.mindgo.jupyter_url is not None:
            values["mindgo_jupyter_url"] = payload.mindgo.jupyter_url
        if payload.mindgo.auth_scheme is not None:
            values["mindgo_auth_scheme"] = payload.mindgo.auth_scheme
        if payload.mindgo.jupyter_token is not None:
            values["mindgo_jupyter_token"] = payload.mindgo.jupyter_token
        if payload.mindgo.notebook_path is not None:
            values["mindgo_notebook_path"] = payload.mindgo.notebook_path
        if payload.mindgo.kernel_id is not None:
            values["mindgo_kernel_id"] = payload.mindgo.kernel_id
        if payload.mindgo.timeout_seconds is not None:
            values["mindgo_timeout_seconds"] = payload.mindgo.timeout_seconds
        if payload.mindgo.storage_root is not None:
            values["mindgo_storage_root"] = payload.mindgo.storage_root
    return values
