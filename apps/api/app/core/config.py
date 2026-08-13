import json
import sqlite3
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

JsonPrimitive = str | int | bool | None
ConfigValue = JsonPrimitive | list[str]
DEFAULT_CONFIG_FILE_PATH = Path("config.json")
DEFAULT_DATABASE_PATH = Path("data/chat-quant.db")
DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 12345
DEFAULT_WEB_HOST = "127.0.0.1"
DEFAULT_WEB_PORT = 12346
DEFAULT_MINDGO_NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"
DEFAULT_MODEL_PROVIDER_ID = "provider_anthropic_default"
DEFAULT_MODEL_PROVIDER_NAME = "Anthropic"
DEFAULT_AGENT_TOOLS = [
    "Task",
    "Bash",
    "Glob",
    "Grep",
    "LS",
    "Read",
    "Edit",
    "MultiEdit",
    "Write",
    "NotebookRead",
    "NotebookEdit",
    "WebFetch",
    "TodoWrite",
    "WebSearch",
]
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
        "agent_available_tools",
        "可用工具",
        "agent",
        "list",
        DEFAULT_AGENT_TOOLS,
        "传给 Agent SDK 的可用工具列表；删除某项即禁用该工具。",
        tuple(DEFAULT_AGENT_TOOLS),
    ),
    ConfigDefinition(
        "mindgo_jupyter_url",
        "MindGo Notebook 地址",
        "mindgo",
        "string",
        "",
        "MindGo / SuperMind Jupyter Notebook 服务地址。",
        nullable=True,
    ),
    ConfigDefinition(
        "mindgo_auth_scheme",
        "MindGo 认证方式",
        "mindgo",
        "string",
        "Bearer",
        "MindGo Jupyter 认证方式。",
    ),
    ConfigDefinition(
        "mindgo_jupyter_token",
        "MindGo 访问 Token",
        "mindgo",
        "password",
        "",
        "MindGo / SuperMind Jupyter 访问 Token。",
        nullable=True,
    ),
    ConfigDefinition(
        "mindgo_notebook_path",
        "MindGo Notebook 路径",
        "mindgo",
        "string",
        DEFAULT_MINDGO_NOTEBOOK_PATH,
        "用于创建或复用 kernel 的远端 Notebook 路径。",
    ),
    ConfigDefinition(
        "mindgo_kernel_id",
        "MindGo Kernel ID",
        "mindgo",
        "string",
        "",
        "可选；填写后复用指定 Jupyter kernel。",
        nullable=True,
    ),
    ConfigDefinition(
        "mindgo_timeout_seconds",
        "MindGo 超时秒数",
        "mindgo",
        "integer",
        120,
        "MindGo 远端执行超时秒数。",
    ),
)


class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    app_name: str = "Chat-Quant API"
    api_prefix: str = "/api"
    config_file_path: Path = DEFAULT_CONFIG_FILE_PATH
    database_path: Path = DEFAULT_DATABASE_PATH
    api_host: str = DEFAULT_API_HOST
    api_port: int = DEFAULT_API_PORT
    web_host: str = DEFAULT_WEB_HOST
    web_port: int = DEFAULT_WEB_PORT
    environment: str = "development"
    log_level: str = "INFO"
    access_log_enabled: bool = True
    access_log_slow_threshold_ms: int = 1000
    agent_provider_id: str = DEFAULT_MODEL_PROVIDER_ID
    agent_model: str = "claude-sonnet-4"
    agent_base_url: str | None = None
    agent_api_token: str | None = None
    agent_max_turns: int = 8
    agent_turn_timeout_seconds: int = 300
    agent_first_token_timeout_seconds: int = 15
    agent_include_partial_messages: bool = True
    agent_thinking_type: Literal["disabled", "adaptive", "enabled"] = "disabled"
    agent_thinking_budget_tokens: int = 2048
    agent_available_tools: list[str] = DEFAULT_AGENT_TOOLS
    mindgo_jupyter_url: str | None = None
    mindgo_auth_scheme: str = "Bearer"
    mindgo_jupyter_token: str | None = None
    mindgo_notebook_path: str = DEFAULT_MINDGO_NOTEBOOK_PATH
    mindgo_kernel_id: str | None = None
    mindgo_timeout_seconds: int = 120

    @field_validator("agent_available_tools", mode="before")
    @classmethod
    def split_csv_values(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("agent_available_tools")
    @classmethod
    def remove_system_managed_tools(cls, value: list[str]) -> list[str]:
        return [tool for tool in value if tool != "Skill"]


def config_file_path() -> Path:
    return DEFAULT_CONFIG_FILE_PATH


def default_app_config_values() -> dict[str, ConfigValue]:
    return {definition.key: definition.default for definition in APP_CONFIG_DEFINITIONS}


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
    file_config = _load_file_config_values(file_path)
    database_path = _coerce_path(file_config.get("database_path"), DEFAULT_DATABASE_PATH)
    api_host = _coerce_string(file_config.get("api_host"), DEFAULT_API_HOST)
    api_port = _coerce_port(file_config.get("api_port"), DEFAULT_API_PORT)
    web_host = _coerce_string(file_config.get("web_host"), DEFAULT_WEB_HOST)
    web_port = _coerce_port(file_config.get("web_port"), DEFAULT_WEB_PORT)
    values = default_app_config_values()
    values.update(_load_sqlite_config_values(database_path))
    values.update(_load_agent_provider_values(database_path, values.get("agent_provider_id")))
    return Settings(
        config_file_path=file_path,
        database_path=database_path,
        api_host=api_host,
        api_port=api_port,
        web_host=web_host,
        web_port=web_port,
        **values,
    )


def _load_file_config_values(file_path: Path) -> dict[str, object]:
    if not file_path.exists():
        return {}
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _coerce_path(value: object, default: Path) -> Path:
    if isinstance(value, str) and value.strip():
        return Path(value).expanduser()
    return default


def _coerce_string(value: object, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _coerce_port(value: object, default: int) -> int:
    try:
        port = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default
    return port if 0 < port <= 65535 else default


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
        config_key = _normalized_config_key(str(key))
        definition = definitions.get(config_key)
        if definition is None:
            continue
        try:
            decoded = json.loads(str(value_json))
            if config_key == "agent_available_tools" and _is_legacy_agent_tools_default(decoded):
                continue
            values[definition.key] = coerce_config_value(definition, decoded)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
    return values


def _normalized_config_key(key: str) -> str:
    if key == "agent_allowed_tools_default":
        return "agent_available_tools"
    return key


def _is_legacy_agent_tools_default(value: object) -> bool:
    return value == ["Bash"]


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
