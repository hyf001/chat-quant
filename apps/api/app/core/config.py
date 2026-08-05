import json
import os
import sqlite3
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

JsonPrimitive = str | int | bool | None
ConfigValue = JsonPrimitive | list[str]
DEFAULT_MODEL_PROVIDER_ID = "provider_anthropic_default"
DEFAULT_MODEL_PROVIDER_NAME = "Anthropic"
ANTHROPIC_DEFAULT_MODELS = (
    "claude-opus-4-1",
    "claude-opus-4",
    "claude-sonnet-4",
    "claude-3-7-sonnet-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-latest",
)


@dataclass(frozen=True)
class ConfigDefinition:
    key: str
    label: str
    group: str
    value_type: Literal["string", "password", "integer", "boolean", "list", "select"]
    default: ConfigValue
    description: str
    options: tuple[str, ...] = ()
    nullable: bool = False


APP_CONFIG_DEFINITIONS: tuple[ConfigDefinition, ...] = (
    ConfigDefinition(
        "environment",
        "运行环境",
        "system",
        "select",
        "development",
        "应用运行环境。",
        ("development", "desktop", "production"),
    ),
    ConfigDefinition(
        "log_level",
        "日志级别",
        "logging",
        "select",
        "INFO",
        "API 日志输出级别。",
        ("DEBUG", "INFO", "WARNING", "ERROR"),
    ),
    ConfigDefinition(
        "log_format",
        "日志格式",
        "logging",
        "select",
        "text",
        "日志格式。",
        ("text", "json"),
    ),
    ConfigDefinition(
        "access_log_enabled",
        "访问日志",
        "system",
        "boolean",
        True,
        "记录 HTTP 请求日志。",
    ),
    ConfigDefinition(
        "access_log_slow_threshold_ms",
        "慢请求阈值",
        "system",
        "integer",
        1000,
        "超过该毫秒数的请求会被标记为慢请求。",
    ),
    ConfigDefinition(
        "default_user_id",
        "默认用户",
        "identity",
        "string",
        "local_user",
        "未提供请求头时使用的用户 ID。",
    ),
    ConfigDefinition(
        "default_project_id",
        "默认项目",
        "identity",
        "string",
        "local_project",
        "未提供请求头时使用的项目 ID。",
    ),
    ConfigDefinition(
        "claude_agent_cwd",
        "Agent 工作目录",
        "paths",
        "string",
        None,
        "读取 Claude SDK 历史会话时使用的工作目录；留空使用项目目录。",
        nullable=True,
    ),
    ConfigDefinition(
        "cors_origins",
        "CORS 来源",
        "system",
        "list",
        [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "null",
        ],
        "允许访问 API 的 Web 来源。",
    ),
    ConfigDefinition(
        "agent_provider_id",
        "Agent Provider",
        "agent",
        "string",
        DEFAULT_MODEL_PROVIDER_ID,
        "当前 Agent 使用的 Anthropic 协议模型供应商。",
    ),
    ConfigDefinition(
        "agent_model",
        "Agent 模型",
        "agent",
        "string",
        "claude-sonnet-4",
        "Claude Agent SDK 使用的模型。",
    ),
    ConfigDefinition(
        "agent_max_turns",
        "最大轮数",
        "agent",
        "integer",
        8,
        "单次 Agent 执行允许的最大回合数。",
    ),
    ConfigDefinition(
        "agent_turn_timeout_seconds",
        "执行超时",
        "agent",
        "integer",
        300,
        "单次 Agent 执行总超时秒数。",
    ),
    ConfigDefinition(
        "agent_first_token_timeout_seconds",
        "首包超时",
        "agent",
        "integer",
        15,
        "等待 Agent 首个有效输出的秒数。",
    ),
    ConfigDefinition(
        "project_home",
        "项目目录",
        "paths",
        "string",
        None,
        "项目文件、运行产物和会话工作目录位置；默认跟随数据库目录。",
        nullable=True,
    ),
    ConfigDefinition(
        "agent_skill_plugin_dir",
        "技能插件目录",
        "agent",
        "string",
        "plugin",
        "传给 Agent SDK 的插件目录。",
    ),
    ConfigDefinition(
        "agent_skill_plugin_name",
        "技能插件名",
        "agent",
        "string",
        "chat-quant",
        "传给 Agent SDK 的插件名称。",
    ),
    ConfigDefinition(
        "agent_include_partial_messages",
        "保留增量消息",
        "agent",
        "boolean",
        True,
        "是否保留 Agent SDK 的 partial message。",
    ),
    ConfigDefinition(
        "agent_thinking_type",
        "思考模式",
        "agent",
        "select",
        "disabled",
        "Agent thinking 配置。",
        ("disabled", "adaptive", "enabled"),
    ),
    ConfigDefinition(
        "agent_thinking_budget_tokens",
        "思考预算",
        "agent",
        "integer",
        2048,
        "thinking=enabled 时使用的 token 预算。",
    ),
    ConfigDefinition(
        "agent_allowed_tools_default",
        "默认工具",
        "agent",
        "list",
        ["Bash"],
        "未显式指定时允许 Agent 使用的工具。",
    ),
    ConfigDefinition(
        "agent_env_allowlist",
        "环境变量白名单",
        "agent",
        "list",
        ["CHATQ_API_BASE", "CHATQ_AGENT_TOKEN"],
        "允许透传给 Agent 的环境变量名。",
    ),
)


class DatabaseConfig(BaseSettings):
    database_path: Path = Field(default=Path("data/chat-quant.db"), alias="CHATQ_DATABASE_PATH")

    model_config = SettingsConfigDict(extra="ignore")


class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    app_name: str = "Chat-Quant API"
    api_prefix: str = "/api"
    config_file_path: Path = Path(".env")
    database_path: Path = Field(
        default=Path("data/chat-quant.db"),
        validation_alias=AliasChoices("database_path", "CHATQ_DATABASE_PATH"),
    )
    environment: str = "development"
    log_level: str = "INFO"
    log_format: Literal["text", "json"] = "text"
    access_log_enabled: bool = True
    access_log_slow_threshold_ms: int = 1000
    default_user_id: str = "local_user"
    default_project_id: str = "local_project"
    claude_agent_cwd: str | None = None
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "null",
    ]
    agent_provider_id: str = DEFAULT_MODEL_PROVIDER_ID
    agent_model: str = "claude-sonnet-4"
    agent_base_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("agent_base_url", "ANTHROPIC_BASE_URL"),
    )
    agent_api_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "agent_api_token",
            "ANTHROPIC_AUTH_TOKEN",
            "ANTHROPIC_API_KEY",
        ),
    )
    agent_max_turns: int = 8
    agent_turn_timeout_seconds: int = 300
    agent_first_token_timeout_seconds: int = 15
    project_home: str = Field(
        default="data/projects",
        validation_alias=AliasChoices("project_home", "PROJECT_HOME"),
    )
    agent_skill_plugin_dir: str = Field(
        default="plugin",
        validation_alias=AliasChoices("agent_skill_plugin_dir", "AGENT_SKILL_PLUGIN_DIR"),
    )
    agent_skill_plugin_name: str = "chat-quant"
    agent_include_partial_messages: bool = True
    agent_thinking_type: Literal["disabled", "adaptive", "enabled"] = "disabled"
    agent_thinking_budget_tokens: int = 2048
    agent_allowed_tools_default: list[str] = ["Bash"]
    agent_env_allowlist: list[str] = ["CHATQ_API_BASE", "CHATQ_AGENT_TOKEN"]

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


def config_file_path() -> Path:
    return Path(os.environ.get("CHATQ_CONFIG_FILE", ".env"))


def default_app_config_values(database_path: Path) -> dict[str, ConfigValue]:
    values = {definition.key: definition.default for definition in APP_CONFIG_DEFINITIONS}
    values["project_home"] = str(database_path.parent / "projects")
    return values


def coerce_config_value(definition: ConfigDefinition, value: object) -> ConfigValue:
    if value == "" and definition.nullable:
        return None
    if value is None:
        if definition.nullable:
            return None
        raise ValueError(f"{definition.key} cannot be empty")
    if definition.value_type in {"string", "password"}:
        return str(value)
    if definition.value_type == "select":
        selected = str(value)
        if selected not in definition.options:
            raise ValueError(f"{definition.key} must be one of: {', '.join(definition.options)}")
        return selected
    if definition.value_type == "integer":
        integer_value = int(value)
        if integer_value < 0:
            raise ValueError(f"{definition.key} must be greater than or equal to 0")
        return integer_value
    if definition.value_type == "boolean":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"true", "1", "yes", "on"}:
                return True
            if lowered in {"false", "0", "no", "off"}:
                return False
        raise ValueError(f"{definition.key} must be a boolean")
    if definition.value_type == "list":
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
    raise ValueError(f"unsupported value for {definition.key}")


def config_definition_by_key() -> dict[str, ConfigDefinition]:
    return {definition.key: definition for definition in APP_CONFIG_DEFINITIONS}


@lru_cache
def get_settings() -> Settings:
    file_path = config_file_path()
    database_config = DatabaseConfig(_env_file=file_path, _env_file_encoding="utf-8")
    database_path = database_config.database_path
    values = default_app_config_values(database_path)
    values.update(_load_sqlite_config_values(database_path))
    values.update(_load_agent_provider_values(database_path, values.get("agent_provider_id")))
    return Settings(
        config_file_path=file_path,
        database_path=database_path,
        **values,
    )


def _load_sqlite_config_values(database_path: Path) -> dict[str, ConfigValue]:
    if not database_path.exists():
        return {}

    definitions = config_definition_by_key()
    try:
        connection = sqlite3.connect(database_path)
        try:
            rows = connection.execute("SELECT key, value_json FROM app_settings").fetchall()
        finally:
            connection.close()
    except sqlite3.Error:
        return {}

    values: dict[str, ConfigValue] = {}
    for key, value_json in rows:
        definition = definitions.get(str(key))
        if definition is None:
            continue
        try:
            decoded = json.loads(str(value_json))
            values[definition.key] = coerce_config_value(definition, decoded)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
    return values


def _load_agent_provider_values(
    database_path: Path,
    provider_id: object,
) -> dict[str, ConfigValue]:
    if not database_path.exists() or not provider_id:
        return {}

    try:
        connection = sqlite3.connect(database_path)
        try:
            row = connection.execute(
                "SELECT base_url, api_key FROM model_providers "
                "WHERE id = ? AND enabled = 1",
                (str(provider_id),),
            ).fetchone()
        finally:
            connection.close()
    except sqlite3.Error:
        return {}
    if row is None:
        return {}
    base_url, api_key = row
    return {
        "agent_base_url": str(base_url) if base_url else None,
        "agent_api_token": str(api_key) if api_key else None,
    }
