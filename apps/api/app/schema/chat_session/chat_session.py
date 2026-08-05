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

from app.service.chat_session.types import (
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
    project_id: str = Field(min_length=1)
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
    if session_response := _session_message_to_response(message):
        return session_response
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


def _session_message_to_response(message: object) -> SDKMessageResponse | None:
    record = _object_record(message)
    message_type = _string_value(record.get("type"))
    if message_type not in {
        "user",
        "assistant",
        "system",
        "result",
        "user_message",
        "assistant_message",
        "system_message",
        "result_message",
    }:
        return None

    payload = record.get("message")
    payload_record = payload if isinstance(payload, dict) else {}
    role = _session_message_role(message_type, payload_record)
    if role is None:
        return None

    content = _session_message_content(message_type, payload)
    content_blocks = _json_content_blocks(content)
    if not content_blocks:
        return None
    return SDKMessageResponse(
        uuid=_string_value(record.get("uuid")) or _new_message_id(),
        role=role,
        content=content_blocks,
        created_at=_now(),
    )


def _session_message_role(
    message_type: str,
    payload: dict[object, object],
) -> SDKMessageRole | None:
    payload_role = _string_value(payload.get("role"))
    if payload_role == "user" or message_type == "user" or message_type == "user_message":
        return SDKMessageRole.USER
    if (
        payload_role == "assistant"
        or message_type == "assistant"
        or message_type == "assistant_message"
        or message_type == "result"
        or message_type == "result_message"
    ):
        return SDKMessageRole.ASSISTANT
    if payload_role == "system" or message_type == "system" or message_type == "system_message":
        return SDKMessageRole.SYSTEM
    if payload_role == "tool":
        return SDKMessageRole.TOOL
    return None


def _session_message_content(message_type: str, payload: object) -> object:
    if not isinstance(payload, dict):
        return payload
    if "content" in payload:
        return payload["content"]
    if message_type in {"result", "result_message"} and "result" in payload:
        return payload["result"]
    return payload


def _json_content_blocks(content: object) -> list[SDKContentBlockResponse]:
    if isinstance(content, str):
        return [SDKContentBlockResponse(type=SDKContentBlockType.TEXT, text=content)]
    if not isinstance(content, list):
        return [
            SDKContentBlockResponse(
                type=SDKContentBlockType.TEXT,
                text=_tool_result_text(content),
            )
        ]

    blocks: list[SDKContentBlockResponse] = []
    for block in content:
        if not isinstance(block, dict):
            blocks.append(
                SDKContentBlockResponse(type=SDKContentBlockType.TEXT, text=str(block))
            )
            continue
        block_type = _string_value(block.get("type"))
        if block_type == "text":
            blocks.append(
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TEXT,
                    text=_string_value(block.get("text")),
                )
            )
        elif block_type == "tool_use":
            blocks.append(
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TOOL_USE,
                    tool_use_id=_string_value(block.get("id")),
                    name=_string_value(block.get("name")),
                )
            )
        elif block_type == "tool_result":
            blocks.append(
                SDKContentBlockResponse(
                    type=SDKContentBlockType.TOOL_RESULT,
                    text=_tool_result_text(block.get("content")),
                    tool_use_id=_string_value(block.get("tool_use_id")),
                )
            )
    return blocks


def _object_record(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    if not hasattr(value, "__dict__"):
        return {}
    return {
        key: item
        for key, item in vars(value).items()
        if not key.startswith("_")
    }


def _string_value(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


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
