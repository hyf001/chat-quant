import type {
  AgentChatSessionDetail,
  AgentScenario,
  ChatMessageAccepted,
  SDKStreamEnvelope,
} from "../types/agentRuntime";
import type { BacktestDetail, BacktestRun, CreateBacktestRunPayload } from "../types/backtests";
import type {
  ChatSession,
  ChatSessionDetail,
  ChatSessionListResponse,
  CreateProjectPayload,
  CreateChatSessionPayload,
  Project,
  ProjectListResponse,
  SendMessageResponse,
  UpdateProjectPayload,
} from "./types";

const API_BASE_URL =
  window.chatqDesktop?.apiBaseUrl ?? import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
export { API_BASE_URL };

const API_USER_ID = import.meta.env.VITE_CHATQ_USER_ID ?? "local_user";
const API_PROJECT_ID = import.meta.env.VITE_CHATQ_PROJECT_ID ?? "local_project";
export { API_PROJECT_ID, API_USER_ID };

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  projectId?: string;
};

type SendAgentChatMessageInput = {
  message: string;
  chatSessionId?: string | null;
  projectId?: string;
  scenario?: AgentScenario;
};

async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": API_USER_ID,
      "X-Project-Id": options.projectId ?? API_PROJECT_ID,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function apiGet<T>(path: string): Promise<T> {
  return requestJson<T>(path);
}

export type RuntimeArtifact = {
  type: "json_result" | "chart" | "curve" | "table" | "image" | "html" | "log" | "file";
  path: string;
  name: string | null;
  mime_type: string | null;
  size_bytes: number | null;
  checksum: string | null;
  metadata: Record<string, unknown>;
};

export type RuntimeErrorInfo = {
  code: string;
  message: string;
  detail: string | null;
  traceback: string | null;
  phase: "prepare" | "execute" | "timeout" | "collect" | "schema_validation" | "persist";
};

export type ExecutionResult = {
  id: string | null;
  run_id: string;
  status: "succeeded" | "failed" | "timeout" | "canceled";
  exit_code: number | null;
  stdout: string;
  stderr: string;
  artifacts: RuntimeArtifact[];
  error: RuntimeErrorInfo | null;
  duration_ms: number;
  started_at: string;
  completed_at: string;
  python_version: string;
  command: string[];
  cwd: string;
  output_dir: string;
  schema_validation: Record<string, unknown>;
  metadata: Record<string, unknown>;
};

export type RuntimeHealth = {
  status: string;
  python_version: string;
  packages: Record<string, string>;
  project_home_writable: boolean;
};

export type BootstrapConfig = {
  config_file_path: string;
  database_path: string;
};

export type SystemSettings = {
  environment: "development" | "desktop" | "production";
  access_log_enabled: boolean;
  access_log_slow_threshold_ms: number;
  cors_origins: string[];
};

export type LoggingSettings = {
  level: "DEBUG" | "INFO" | "WARNING" | "ERROR";
  format: "text" | "json";
};

export type IdentitySettings = {
  default_user_id: string;
  default_project_id: string;
};

export type PathSettings = {
  claude_agent_cwd: string | null;
  project_home: string | null;
};

export type AgentSettings = {
  provider_id: string;
  model: string;
  max_turns: number;
  turn_timeout_seconds: number;
  first_token_timeout_seconds: number;
  skill_plugin_dir: string;
  skill_plugin_name: string;
  include_partial_messages: boolean;
  thinking: {
    type: "disabled" | "adaptive" | "enabled";
    budget_tokens: number;
  };
  allowed_tools_default: string[];
  env_allowlist: string[];
};

export type AppSettings = {
  system: SystemSettings;
  logging: LoggingSettings;
  identity: IdentitySettings;
  paths: PathSettings;
  agent: AgentSettings;
};

export type ConfigFieldDefinition = {
  namespace: string;
  key: string;
  label: string;
  value_type: string;
  description: string;
  options: string[];
  is_secret: boolean;
};

export type AppConfig = {
  bootstrap: BootstrapConfig;
  settings: AppSettings;
  fields: ConfigFieldDefinition[];
};

export type ModelProvider = {
  id: string;
  name: string;
  base_url: string | null;
  has_api_key: boolean;
  enabled: boolean;
  created_at: string;
  updated_at: string;
};

export type ModelProviderPayload = {
  name: string;
  base_url: string | null;
  api_key: string | null;
  enabled: boolean;
};

export type ModelProviderListResponse = {
  providers: ModelProvider[];
};

export type ProviderModel = {
  id: string;
  name: string;
};

export type ProviderModelListResponse = {
  provider_id: string;
  models: ProviderModel[];
};

export type ProviderConnectionTestResponse = {
  ok: boolean;
  message: string;
  models: ProviderModel[];
};

export async function getHealth(): Promise<{ status: string; service?: string }> {
  return requestJson<{ status: string; service?: string }>("/api/health");
}

export async function getAppConfig(): Promise<AppConfig> {
  return requestJson<AppConfig>("/api/config");
}

export async function updateAppConfig(settings: AppSettings): Promise<AppConfig> {
  return requestJson<AppConfig>("/api/config", {
    method: "PUT",
    body: { settings },
  });
}

export async function listModelProviders(): Promise<ModelProviderListResponse> {
  return requestJson<ModelProviderListResponse>("/api/model-providers");
}

export async function createModelProvider(
  payload: ModelProviderPayload,
): Promise<ModelProvider> {
  return requestJson<ModelProvider>("/api/model-providers", {
    method: "POST",
    body: payload,
  });
}

export async function updateModelProvider(
  providerId: string,
  payload: ModelProviderPayload,
): Promise<ModelProvider> {
  return requestJson<ModelProvider>(`/api/model-providers/${providerId}`, {
    method: "PUT",
    body: payload,
  });
}

export async function deleteModelProvider(providerId: string): Promise<void> {
  return requestJson<void>(`/api/model-providers/${providerId}`, {
    method: "DELETE",
  });
}

export async function listProviderModels(
  providerId: string,
): Promise<ProviderModelListResponse> {
  return requestJson<ProviderModelListResponse>(`/api/model-providers/${providerId}/models`);
}

export async function testModelProvider(
  providerId: string,
): Promise<ProviderConnectionTestResponse> {
  return requestJson<ProviderConnectionTestResponse>(
    `/api/model-providers/${providerId}/test`,
    { method: "POST" },
  );
}

export async function testModelProviderPayload(
  payload: ModelProviderPayload,
  providerId?: string | null,
): Promise<ProviderConnectionTestResponse> {
  const path = providerId
    ? `/api/model-providers/${providerId}/test-payload`
    : "/api/model-providers/test";
  return requestJson<ProviderConnectionTestResponse>(path, {
    method: "POST",
    body: payload,
  });
}

export async function listProjects(query?: string): Promise<ProjectListResponse> {
  const params = new URLSearchParams();
  if (query) {
    params.set("query", query);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return requestJson<ProjectListResponse>(`/api/projects${suffix}`);
}

export async function createProject(payload: CreateProjectPayload): Promise<Project> {
  return requestJson<Project>("/api/projects", {
    method: "POST",
    body: payload,
  });
}

export async function updateProject(
  projectId: string,
  payload: UpdateProjectPayload,
): Promise<Project> {
  return requestJson<Project>(`/api/projects/${projectId}`, {
    method: "PATCH",
    body: payload,
  });
}

export async function deleteProject(projectId: string): Promise<void> {
  return requestJson<void>(`/api/projects/${projectId}`, {
    method: "DELETE",
  });
}

export async function listChatSessions(
  query?: string,
  projectId?: string,
): Promise<ChatSessionListResponse> {
  const params = new URLSearchParams();
  if (query) {
    params.set("query", query);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return requestJson<ChatSessionListResponse>(`/api/chat-sessions${suffix}`, { projectId });
}

export async function createChatSession(
  payload: CreateChatSessionPayload = {},
  projectId?: string,
): Promise<ChatSession> {
  return requestJson<ChatSession>("/api/chat-sessions", {
    method: "POST",
    body: payload,
    projectId,
  });
}

export async function getChatSessionDetail(chatSessionId: string): Promise<ChatSessionDetail> {
  return requestJson<ChatSessionDetail>(`/api/chat-sessions/${chatSessionId}`);
}

export async function sendChatMessage(
  chatSessionId: string,
  content: string,
): Promise<SendMessageResponse> {
  return requestJson<SendMessageResponse>(`/api/chat-sessions/${chatSessionId}/messages`, {
    method: "POST",
    body: { content },
  });
}

export async function sendAgentChatMessage(
  input: SendAgentChatMessageInput,
): Promise<ChatMessageAccepted> {
  return requestJson<ChatMessageAccepted>("/api/chat/messages", {
    method: "POST",
    body: {
      message: input.message,
      chat_session_id: input.chatSessionId,
      scenario: input.scenario,
      user_id: API_USER_ID,
      project_id: input.projectId ?? API_PROJECT_ID,
    },
    projectId: input.projectId,
  });
}

export async function getAgentChatSessionDetail(
  chatSessionId: string,
): Promise<AgentChatSessionDetail> {
  return requestJson<AgentChatSessionDetail>(`/api/chat/sessions/${chatSessionId}`);
}

export async function readChatStream(
  streamUrl: string,
  onEnvelope: (envelope: SDKStreamEnvelope) => void,
): Promise<void> {
  const response = await fetch(toApiUrl(streamUrl), {
    headers: {
      "X-User-Id": API_USER_ID,
    },
  });
  if (!response.ok || response.body === null) {
    throw new Error(`Chat stream failed: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    buffer += decoder.decode(value, { stream: !done });
    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";
    for (const event of events) {
      const dataLine = event.split("\n").find((line) => line.startsWith("data: "));
      if (!dataLine || dataLine === "data: {}") {
        continue;
      }
      onEnvelope(JSON.parse(dataLine.slice(6)) as SDKStreamEnvelope);
    }
    if (done) {
      break;
    }
  }
}

export async function getRuntimeHealth(): Promise<RuntimeHealth> {
  return requestJson<RuntimeHealth>("/api/runtime/health");
}

export async function createBacktestRun(payload: CreateBacktestRunPayload): Promise<BacktestRun> {
  return requestJson<BacktestRun>("/api/backtests", {
    method: "POST",
    body: {
      ...payload,
      user_id: API_USER_ID,
      project_id: API_PROJECT_ID,
    },
  });
}

export async function runBacktest(backtestRunId: string): Promise<BacktestDetail> {
  return requestJson<BacktestDetail>(`/api/backtests/${backtestRunId}/run`, {
    method: "POST",
    body: { mode: "sync" },
  });
}

export async function getBacktest(backtestRunId: string): Promise<BacktestDetail> {
  return requestJson<BacktestDetail>(
    `/api/backtests/${backtestRunId}?include_trades=true&include_curves=true`,
  );
}

function toApiUrl(url: string): string {
  if (url.startsWith("http")) {
    return url;
  }
  return `${API_BASE_URL}${url}`;
}
