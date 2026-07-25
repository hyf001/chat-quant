from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

from claude_agent_sdk.types import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)
from pydantic import BaseModel, ConfigDict, Field

from app.domain.chat_sessions.models import (
    AssetRelationType,
    AssetType,
    ChatSessionKind,
    JSONValue,
    SDKContentBlockType,
    SDKMessageRole,
)


class SDKContentBlockResponse(BaseModel):
    type: SDKContentBlockType
    text: str | None = None
    tool_use_id: str | None = None
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SDKMessageResponse(BaseModel):
    uuid: str
    role: SDKMessageRole
    content: list[SDKContentBlockResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetLinkResponse(BaseModel):
    id: str
    chat_session_id: str
    sdk_session_id: str | None = None
    sdk_message_uuid: str | None = None
    sdk_tool_use_id: str | None = None
    asset_type: AssetType
    asset_id: str
    relation_type: AssetRelationType
    display_snapshot: JSONValue | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    project_id: str
    sdk_session_id: str | None = None
    sdk_project_key: str | None = None
    title: str
    snippet: str | None = None
    summary: str | None = None
    kind: ChatSessionKind
    task_type: str | None = None
    symbols: list[str]
    markets: list[str]
    tags: list[str]
    current_strategy_version_id: str | None = None
    current_backtest_run_id: str | None = None
    data_scope_label: str | None = None
    last_saved_at: datetime | None = None
    archived_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatSessionListResponse(BaseModel):
    items: list[ChatSessionResponse]
    total: int
    limit: int
    offset: int


class ChatSessionCreateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    initial_prompt: str | None = Field(default=None, max_length=8000)
    kind: ChatSessionKind = ChatSessionKind.NORMAL
    task_type: str | None = Field(default=None, max_length=32)
    symbols: list[str] = Field(default_factory=list)
    markets: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    sdk_project_key: str | None = Field(default=None, max_length=256)
    data_scope_label: str | None = Field(default=None, max_length=120)


class ChatSessionUpdateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    snippet: str | None = Field(default=None, max_length=500)
    summary: str | None = None
    sdk_session_id: str | None = Field(default=None, max_length=128)
    sdk_project_key: str | None = Field(default=None, max_length=256)
    kind: ChatSessionKind | None = None
    task_type: str | None = Field(default=None, max_length=32)
    symbols: list[str] | None = None
    markets: list[str] | None = None
    tags: list[str] | None = None
    current_strategy_version_id: str | None = Field(default=None, max_length=40)
    current_backtest_run_id: str | None = Field(default=None, max_length=40)
    data_scope_label: str | None = Field(default=None, max_length=120)
    archived: bool | None = None


class ChatSessionDetailResponse(BaseModel):
    session: ChatSessionResponse
    messages: list[SDKMessageResponse]
    assets: list[AssetLinkResponse]
    warning: str | None = None


class ChatSessionContextResponse(BaseModel):
    chat_session_id: str
    sdk_session_id: str | None = None
    summary: str | None = None
    current_strategy_version_id: str | None = None
    current_backtest_run_id: str | None = None
    assets: list[AssetLinkResponse]


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=8000)


class SendMessageResponse(BaseModel):
    chat_session_id: str
    sdk_session_id: str
    stream_url: str
    messages: list[SDKMessageResponse]


class LinkAssetRequest(BaseModel):
    sdk_session_id: str | None = Field(default=None, max_length=128)
    sdk_message_uuid: str | None = Field(default=None, max_length=128)
    sdk_tool_use_id: str | None = Field(default=None, max_length=128)
    asset_type: AssetType
    asset_id: str = Field(min_length=1, max_length=64)
    relation_type: AssetRelationType
    display_snapshot: JSONValue | None = None


def sdk_message_to_response(message: object) -> SDKMessageResponse | None:
    if isinstance(message, UserMessage):
        return SDKMessageResponse(
            uuid=message.uuid or _new_message_id(),
            role=SDKMessageRole.USER,
            content=_content_blocks(message.content),
            created_at=_now(),
        )
    if isinstance(message, AssistantMessage):
        return SDKMessageResponse(
            uuid=message.uuid or message.message_id or _new_message_id(),
            role=SDKMessageRole.ASSISTANT,
            content=_content_blocks(message.content),
            created_at=_now(),
        )
    if isinstance(message, ResultMessage):
        return SDKMessageResponse(
            uuid=message.uuid or _new_message_id(),
            role=SDKMessageRole.ASSISTANT,
            content=[
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TEXT,
                    text=message.result or message.stop_reason or message.subtype,
                )
            ],
            created_at=_now(),
        )
    if isinstance(message, SystemMessage):
        return SDKMessageResponse(
            uuid=_new_message_id(),
            role=SDKMessageRole.SYSTEM,
            content=[
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TEXT,
                    text=json.dumps(message.data, ensure_ascii=False, default=str),
                )
            ],
            created_at=_now(),
        )
    return None


def sdk_messages_to_response(messages: list[object]) -> list[SDKMessageResponse]:
    return [
        response
        for message in messages
        if (response := sdk_message_to_response(message)) is not None
    ]


def _content_blocks(content: object) -> list[SDKContentBlockResponse]:
    if isinstance(content, str):
        return [SDKContentBlockResponse(type=SDKContentBlockType.TEXT, text=content)]
    if not isinstance(content, list):
        return [SDKContentBlockResponse(type=SDKContentBlockType.TEXT, text=str(content))]

    blocks: list[SDKContentBlockResponse] = []
    for block in content:
        if isinstance(block, TextBlock):
            blocks.append(SDKContentBlockResponse(type=SDKContentBlockType.TEXT, text=block.text))
        elif isinstance(block, ToolUseBlock):
            blocks.append(
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TOOL_USE,
                    tool_use_id=block.id,
                    name=block.name,
                )
            )
        elif isinstance(block, ToolResultBlock):
            blocks.append(
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TOOL_RESULT,
                    text=_tool_result_text(block.content),
                    tool_use_id=block.tool_use_id,
                )
            )
    return blocks


def _tool_result_text(content: object) -> str | None:
    if content is None:
        return None
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False, default=str)


def _new_message_id() -> str:
    return f"msg_{uuid4().hex[:16]}"


def _now() -> datetime:
    return datetime.now(UTC)
