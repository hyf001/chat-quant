from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import JsonValue

type JSONValue = JsonValue


class ChatSessionKind(StrEnum):
    NORMAL = "normal"
    STRATEGY = "strategy"
    SCREENING = "screening"


class AssetType(StrEnum):
    STRATEGY = "strategy"
    STRATEGY_VERSION = "strategy_version"
    BACKTEST_RUN = "backtest_run"


class AssetRelationType(StrEnum):
    CREATED = "created"
    USED = "used"
    DISPLAYED = "displayed"
    RESULT = "result"
    REUSED = "reused"


class SDKMessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"


class SDKContentBlockType(StrEnum):
    TEXT = "text"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class AssetLink:
    id: str
    chat_session_id: str
    asset_type: AssetType
    asset_id: str
    relation_type: AssetRelationType
    sdk_session_id: str | None = None
    sdk_message_uuid: str | None = None
    sdk_tool_use_id: str | None = None
    display_snapshot: JSONValue | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class ChatSession:
    id: str
    project_id: str
    title: str
    kind: ChatSessionKind = ChatSessionKind.NORMAL
    sdk_session_id: str | None = None
    sdk_project_key: str | None = None
    snippet: str | None = None
    summary: str | None = None
    task_type: str | None = None
    symbols: list[str] = field(default_factory=list)
    markets: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    current_strategy_version_id: str | None = None
    current_backtest_run_id: str | None = None
    data_scope_label: str | None = None
    last_saved_at: datetime | None = None
    archived_at: datetime | None = None
    deleted_at: datetime | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
