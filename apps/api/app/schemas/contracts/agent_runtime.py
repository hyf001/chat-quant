from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class AgentScenario(StrEnum):
    CHAT_ANALYSIS = "chat_analysis"
    SCREENING = "screening"
    STRATEGY_BUILD = "strategy_build"
    BACKTEST = "backtest"
    FOLLOW_UP = "follow_up"


class RuntimeErrorCode(StrEnum):
    SDK_UNAVAILABLE = "SDK_UNAVAILABLE"
    SDK_SESSION_EXPIRED = "SDK_SESSION_EXPIRED"
    FIRST_TOKEN_TIMEOUT = "FIRST_TOKEN_TIMEOUT"
    RUN_TIMEOUT = "RUN_TIMEOUT"
    COMMAND_NOT_ALLOWED = "COMMAND_NOT_ALLOWED"
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


class AgentTurnCommand(BaseModel):
    user_id: str
    project_id: str
    chat_session_id: str
    user_message_id: str
    scenario: AgentScenario = AgentScenario.CHAT_ANALYSIS
    context: ChatSessionContext = Field(default_factory=ChatSessionContext)
    system_prompt_key: str = "base:v1"
    sdk_skill_names: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    bash_command_policy_id: str = "default"
    working_dir: str
    sdk_session_id: str | None = None
    request_id: str
    deadline_seconds: int | None = None
    user_prompt: str


class GeneratedArtifact(BaseModel):
    artifact_type: str
    artifact_id: str
    title: str | None = None
    uri: str | None = None


class SDKMessageRef(BaseModel):
    sdk_message_uuid: str
    chat_session_id: str
    sdk_session_id: str
    message_type: str
    role: str | None = None


class SDKToolUseRef(BaseModel):
    sdk_tool_use_id: str
    sdk_message_uuid: str | None = None
    chat_session_id: str
    sdk_session_id: str
    tool_name: str = "Bash"
    bash_command: str
    chatq_command: str | None = None
    input_preview: str
    tool_result_json: dict[str, object] | None = None
    is_error: bool = False
    output_ref: str | None = None


class AgentTurnResult(BaseModel):
    chat_session_id: str
    user_message_id: str
    sdk_session_id: str | None = None
    sdk_result_message_id: str | None = None
    sdk_result_subtype: str | None = None
    assistant_message: str = ""
    generated_artifacts: list[GeneratedArtifact] = Field(default_factory=list)
    sdk_message_refs: list[SDKMessageRef] = Field(default_factory=list)
    sdk_tool_uses: list[SDKToolUseRef] = Field(default_factory=list)
    error_code: RuntimeErrorCode | None = None
    error_message: str | None = None
    retryable: bool = False


class SDKStreamEnvelope(BaseModel):
    sequence: int
    chat_session_id: str
    sdk_session_id: str | None = None
    received_at: datetime
    sdk_event: dict[str, object]


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    chat_session_id: str | None = None
    scenario: AgentScenario | None = None
    user_id: str = "demo_user"
    project_id: str = "default"


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
    sdk_messages: list[dict[str, object]] = Field(default_factory=list)
    envelopes: list[SDKStreamEnvelope] = Field(default_factory=list)
    assets: list[AssetReference] = Field(default_factory=list)


class CancelSessionRequest(BaseModel):
    reason: str = Field(default="user_requested", max_length=256)


class CancelSessionResponse(BaseModel):
    chat_session_id: str
    cancelled: bool
