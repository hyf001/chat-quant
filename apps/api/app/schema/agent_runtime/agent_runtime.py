from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class RuntimeErrorCode(StrEnum):
    SDK_UNAVAILABLE = "SDK_UNAVAILABLE"
    SDK_SESSION_EXPIRED = "SDK_SESSION_EXPIRED"
    FIRST_TOKEN_TIMEOUT = "FIRST_TOKEN_TIMEOUT"
    RUN_TIMEOUT = "RUN_TIMEOUT"
    TOOL_PERMISSION_DENIED = "TOOL_PERMISSION_DENIED"
    COMMAND_FAILED = "COMMAND_FAILED"
    COMMAND_OUTPUT_INVALID = "COMMAND_OUTPUT_INVALID"
    SDK_SESSION_STORE_FAILED = "SDK_SESSION_STORE_FAILED"
    STREAM_CLIENT_DISCONNECTED = "STREAM_CLIENT_DISCONNECTED"


class ChatHistoryMessage(BaseModel):
    message_id: str
    role: str
    content: str
    created_at: datetime


class AssetReference(BaseModel):
    asset_type: str
    asset_id: str
    title: str | None = None
    sdk_message_uuid: str | None = None
    sdk_tool_use_id: str | None = None


class ChatSessionContext(BaseModel):
    recent_messages: list[ChatHistoryMessage] = Field(default_factory=list)
    summary: str | None = None
    related_assets: list[AssetReference] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class AgentExecutionCommand(BaseModel):
    project_id: str
    chat_session_id: str
    user_message_id: str
    context: ChatSessionContext = Field(default_factory=ChatSessionContext)
    system_prompt_key: str = "base:v1"
    allowed_tools: list[str] = Field(default_factory=list)
    project_dir: str
    sdk_session_id: str | None = None
    should_finalize_initial_title: bool = False
    request_id: str
    deadline_seconds: int | None = None
    user_prompt: str


class SDKStreamEnvelope(BaseModel):
    sequence: int
    chat_session_id: str
    sdk_session_id: str | None = None
    turn_id: str | None = None
    received_at: datetime
    sdk_event: dict[str, object]


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    chat_session_id: str | None = None
    project_id: str = Field(min_length=1)


class ChatMessageAccepted(BaseModel):
    chat_session_id: str
    user_message_id: str
    sdk_session_id: str | None
    stream_url: str


class ChatSessionDetail(BaseModel):
    chat_session_id: str
    sdk_session_id: str | None = None
    title: str
    summary: str | None = None
    messages: list[ChatHistoryMessage] = Field(default_factory=list)
    sdk_messages: list[SDKStreamEnvelope] = Field(default_factory=list)
    envelopes: list[SDKStreamEnvelope] = Field(default_factory=list)
    assets: list[AssetReference] = Field(default_factory=list)


class CancelSessionRequest(BaseModel):
    reason: str = Field(default="user_requested", max_length=256)


class CancelSessionResponse(BaseModel):
    chat_session_id: str
    cancelled: bool
