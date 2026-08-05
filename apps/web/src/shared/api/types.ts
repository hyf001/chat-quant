export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export type ChatSessionKind = "normal" | "strategy" | "screening";

export type AssetType = "strategy_version" | "backtest_run";

export type AssetRelationType = "created" | "used" | "displayed" | "result" | "reused";

export type SdkMessageRole = "user" | "assistant" | "tool" | "system";

export type SdkContentBlockType = "text" | "tool_use" | "tool_result";

export type SdkContentBlock = {
  type: SdkContentBlockType;
  text: string | null;
  tool_use_id: string | null;
  name: string | null;
};

export type SdkMessage = {
  uuid: string;
  role: SdkMessageRole;
  content: SdkContentBlock[];
  created_at: string;
  source_sequence?: number;
};

export type AssetLink = {
  id: string;
  chat_session_id: string;
  sdk_session_id: string | null;
  sdk_message_uuid: string | null;
  sdk_tool_use_id: string | null;
  asset_type: AssetType;
  asset_id: string;
  relation_type: AssetRelationType;
  display_snapshot: JsonValue | null;
  created_at: string;
  updated_at: string;
};

export type ChatSession = {
  id: string;
  project_id: string;
  sdk_session_id: string | null;
  sdk_project_key: string | null;
  title: string;
  snippet: string | null;
  summary: string | null;
  kind: ChatSessionKind;
  task_type: string | null;
  symbols: string[];
  markets: string[];
  tags: string[];
  current_strategy_version_id: string | null;
  current_backtest_run_id: string | null;
  data_scope_label: string | null;
  last_saved_at: string | null;
  archived_at: string | null;
  created_at: string;
  updated_at: string;
};

export type ChatSessionListResponse = {
  items: ChatSession[];
  total: number;
  limit: number;
  offset: number;
};

export type ChatSessionDetail = {
  session: ChatSession;
  messages: SdkMessage[];
  assets: AssetLink[];
  warning: string | null;
};

export type CreateChatSessionPayload = {
  project_id: string;
  title?: string;
  initial_prompt?: string;
  kind?: ChatSessionKind;
  task_type?: string;
  symbols?: string[];
  markets?: string[];
  tags?: string[];
  data_scope_label?: string;
};

export type SendMessageResponse = {
  chat_session_id: string;
  sdk_session_id: string;
  stream_url: string;
  messages: SdkMessage[];
};

export type Project = {
  id: string;
  local_path: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
};

export type ProjectListResponse = {
  items: Project[];
  total: number;
  limit: number;
  offset: number;
};

export type CreateProjectPayload = {
  local_path: string;
  name?: string | null;
  description?: string | null;
};

export type UpdateProjectPayload = {
  name?: string;
  description?: string | null;
};
