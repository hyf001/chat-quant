export type AgentScenario =
  | "chat_analysis"
  | "screening"
  | "strategy_build"
  | "backtest"
  | "follow_up";

export type SDKEvent = Record<string, unknown>;

export type SDKStreamEnvelope = {
  sequence: number;
  chat_session_id: string;
  sdk_session_id: string | null;
  turn_id: string | null;
  received_at: string;
  sdk_event: SDKEvent;
};

export type ChatHistoryMessage = {
  message_id: string;
  role: string;
  content: string;
  created_at: string;
};

export type ChatMessageAccepted = {
  chat_session_id: string;
  user_message_id: string;
  sdk_session_id: string | null;
  stream_url: string;
};

export type ChatMessageRole = "user" | "assistant";

export type ChatMessageView = {
  id: string;
  role: ChatMessageRole;
  content: string;
};

export type ToolCallView = {
  id: string;
  command: string;
  status: "running" | "completed" | "blocked" | "failed";
  output?: string;
};

export type AssetReference = {
  asset_type: string;
  asset_id: string;
  title: string | null;
  sdk_message_uuid: string | null;
  sdk_tool_use_id: string | null;
};

export type ChatSessionSummary = {
  chatSessionId: string | null;
  sdkSessionId: string | null;
  title: string;
  status: "idle" | "running" | "completed" | "failed";
};

export type AgentChatSessionDetail = {
  chat_session_id: string;
  sdk_session_id: string | null;
  title: string;
  summary: string | null;
  messages: ChatHistoryMessage[];
  sdk_messages: SDKStreamEnvelope[];
  envelopes: SDKStreamEnvelope[];
  assets: AssetReference[];
};
