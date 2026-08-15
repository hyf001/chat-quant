import type {
  AgentChatSessionDetail,
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
  window.chatqDesktop?.apiBaseUrl ?? __CHATQ_API_BASE_URL__;
export { API_BASE_URL };

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
};

type SendAgentChatMessageInput = {
  message: string;
  chatSessionId?: string | null;
  projectId?: string;
};

async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(errorMessageFromResponse(message, response.status));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

function errorMessageFromResponse(body: string, status: number): string {
  if (!body) {
    return `Request failed: ${status}`;
  }

  try {
    const payload = JSON.parse(body) as unknown;
    if (
      typeof payload === "object" &&
      payload !== null &&
      "detail" in payload
    ) {
      const detail = (payload as { detail: unknown }).detail;
      if (typeof detail === "string") {
        return detail;
      }
      return JSON.stringify(detail);
    }
  } catch {
    return body;
  }

  return body;
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
};

export type BootstrapConfig = {
  config_file_path: string;
  database_path: string;
  api_host: string;
  api_port: number;
  web_host: string;
  web_port: number;
};

export type SystemSettings = {
  environment: "development" | "desktop" | "production";
  access_log_enabled: boolean;
  access_log_slow_threshold_ms: number;
};

export type LoggingSettings = {
  level: "DEBUG" | "INFO" | "WARNING" | "ERROR";
};

export type AgentSettings = {
  provider_id: string;
  model: string;
  max_turns: number;
  turn_timeout_seconds: number;
  first_token_timeout_seconds: number;
  include_partial_messages: boolean;
  thinking: {
    type: "disabled" | "adaptive" | "enabled";
    budget_tokens: number;
  };
  available_tools: string[];
};

export type MindgoSettings = {
  jupyter_url: string | null;
  auth_scheme: string;
  jupyter_token: string | null;
  notebook_path: string;
  kernel_id: string | null;
  timeout_seconds: number;
  storage_root: string;
};

export type AppSettings = {
  system: SystemSettings;
  logging: LoggingSettings;
  agent: AgentSettings;
  mindgo: MindgoSettings;
};

export type AppSettingsUpdate = {
  system?: Partial<SystemSettings>;
  logging?: Partial<LoggingSettings>;
  agent?: Partial<Omit<AgentSettings, "thinking">> & {
    thinking?: Partial<AgentSettings["thinking"]>;
  };
  mindgo?: Partial<MindgoSettings>;
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

export type LogCategory = "access" | "business";

export type LogEntry = {
  timestamp: string;
  level: string;
  logger: string;
  message: string;
  request_id: string;
  category: LogCategory | "system";
  method: string | null;
  path: string | null;
  status_code: number | null;
  duration_ms: number | null;
  client_host: string | null;
  error: string | null;
  exception: string | null;
  stack: string | null;
};

export type LogListResponse = {
  items: LogEntry[];
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

export type ModelProviderApiKeyResponse = {
  api_key: string | null;
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

export type MindgoJsonValue =
  | string
  | number
  | boolean
  | null
  | MindgoJsonValue[]
  | { [key: string]: MindgoJsonValue };

export type MindgoParameterOption = {
  label: string;
  value: string | number | boolean | null;
};

export type MindgoParameterSpec = {
  name: string;
  label: string;
  value_type: "string" | "string[]" | "integer" | "number" | "boolean" | "enum" | "date";
  required: boolean;
  default: MindgoJsonValue;
  options: MindgoParameterOption[];
  description: string;
  validation: Record<string, MindgoJsonValue>;
};

export type MindgoFieldSpec = {
  name: string;
  label: string;
  value_type: "string" | "integer" | "number" | "boolean" | "date";
  required: boolean;
  description: string;
};

export type MindgoDatasetStorageSpec = {
  path: string;
  format: "parquet";
  partitioned_by: string[];
  min_partition: string | null;
  max_partition: string | null;
  partition_count: number;
};

export type MindgoDatasetSchema = {
  name: string;
  category_path: string[];
  description: string;
  mindgo_function: string;
  storage: MindgoDatasetStorageSpec;
  query_params: MindgoParameterSpec[];
  result_schema: MindgoFieldSpec[];
};

export type MindgoDatasetSummary = {
  id: string;
  name: string;
  category_path: string[];
  description: string;
  storage: MindgoDatasetStorageSpec;
};

export type MindgoDatasetListResponse = {
  datasets: MindgoDatasetSummary[];
};

export type MindgoDatasetQueryPayload = {
  params: Record<string, MindgoJsonValue>;
  page: number;
  page_size: number;
};

export type MindgoDatasetDuckDBQueryPayload = {
  sql: string;
  page: number;
  page_size: number;
};

export type MindgoDatasetQueryResponse = {
  dataset_id: string;
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  columns: MindgoFieldSpec[];
  rows: Array<Record<string, MindgoJsonValue>>;
};

export type MindgoDatasetSyncPayload = {
  trigger_start_date: string;
  trigger_end_date: string;
  trigger_time: string;
  write_mode: MindgoDatasetSyncWriteMode;
  params: Record<string, MindgoJsonValue>;
};

export type MindgoDatasetSyncWriteMode = "overwrite" | "skip";

export type MindgoDatasetSyncResult = {
  status: "success" | "failed";
  elapsed_ms: number;
  synced_count: number;
};

export type JobTriggerType = "schedule" | "manual" | "rerun" | "system";

export type JobInstanceStatus =
  | "waiting"
  | "dispatching"
  | "running"
  | "completed"
  | "failed"
  | "cancelled";

export type JobRuntimeInstance = {
  id: string;
  job_type: string;
  job_id: string;
  trigger_type: JobTriggerType;
  trigger_key: string;
  payload: Record<string, MindgoJsonValue>;
  priority: number;
  scheduled_for: string;
  started_at: string | null;
  completed_at: string | null;
  status: JobInstanceStatus;
  result_status: string | null;
  summary: string;
  error_message: string;
  created_at: string;
  updated_at: string;
};

export type JobRuntimeInstanceListResponse = {
  items: JobRuntimeInstance[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  status_counts: JobRuntimeInstanceStatusCount[];
};

export type JobRuntimeInstanceStatusCount = {
  status: JobInstanceStatus;
  count: number;
};

export type JobRuntimeInstanceListParams = {
  job_type?: string;
  job_id?: string;
  status?: JobInstanceStatus;
  page?: number;
  page_size?: number;
};

export type MindgoDatasetSyncTriggerResponse = {
  instance: JobRuntimeInstance;
  instances: JobRuntimeInstance[];
};

export type MindgoDatasetSyncSchedulerPayload = {
  cron: string;
  write_mode: MindgoDatasetSyncWriteMode;
  params: Record<string, MindgoJsonValue>;
};

export type MindgoDatasetSyncSchedulerState = {
  configured: boolean;
  scheduler_id: string | null;
  cron: string | null;
  write_mode: MindgoDatasetSyncWriteMode;
  params: Record<string, MindgoJsonValue>;
  last_run_at: string | null;
  next_run_at: string | null;
  created_at: string | null;
  updated_at: string | null;
};

export type MindgoDatasetSyncStatusResponse = {
  dataset_id: string;
  job_type: string;
  job_id: string;
  scheduler: MindgoDatasetSyncSchedulerState;
};

export type MindgoConnectionTestResponse = {
  ok: boolean;
  message: string;
};

export async function getHealth(): Promise<{ status: string; service?: string }> {
  return requestJson<{ status: string; service?: string }>("/api/health");
}

export async function getAppConfig(): Promise<AppConfig> {
  return requestJson<AppConfig>("/api/config");
}

export async function listSystemLogs(
  limit = 100,
  category?: LogCategory,
): Promise<LogListResponse> {
  const searchParams = new URLSearchParams({ limit: String(limit) });
  if (category) {
    searchParams.set("category", category);
  }
  return requestJson<LogListResponse>(`/api/logs?${searchParams.toString()}`);
}

export async function updateAppConfig(settings: AppSettingsUpdate): Promise<AppConfig> {
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

export async function getModelProviderApiKey(
  providerId: string,
): Promise<ModelProviderApiKeyResponse> {
  return requestJson<ModelProviderApiKeyResponse>(`/api/model-providers/${providerId}/api-key`);
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

export async function listMindgoDatasets(): Promise<MindgoDatasetListResponse> {
  return requestJson<MindgoDatasetListResponse>("/api/mindgo/datasets");
}

export async function testMindgoConnection(): Promise<MindgoConnectionTestResponse> {
  return requestJson<MindgoConnectionTestResponse>("/api/mindgo/test", {
    method: "POST",
    body: {},
  });
}

export async function getMindgoDatasetSchema(
  datasetId: string,
): Promise<MindgoDatasetSchema> {
  return requestJson<MindgoDatasetSchema>(`/api/mindgo/datasets/${datasetId}/schema`);
}

export async function queryMindgoDataset(
  datasetId: string,
  payload: MindgoDatasetQueryPayload,
): Promise<MindgoDatasetQueryResponse> {
  return requestJson<MindgoDatasetQueryResponse>(`/api/mindgo/datasets/${datasetId}/query`, {
    method: "POST",
    body: payload,
  });
}

export async function queryMindgoDatasetFromDuckDB(
  datasetId: string,
  payload: MindgoDatasetDuckDBQueryPayload,
): Promise<MindgoDatasetQueryResponse> {
  return requestJson<MindgoDatasetQueryResponse>(
    `/api/mindgo/datasets/${datasetId}/query_from_duckdb`,
    {
      method: "POST",
      body: payload,
    },
  );
}

export async function syncMindgoDataset(
  datasetId: string,
  payload: MindgoDatasetSyncPayload,
): Promise<MindgoDatasetSyncTriggerResponse> {
  return requestJson<MindgoDatasetSyncTriggerResponse>(`/api/mindgo/datasets/${datasetId}/sync`, {
    method: "POST",
    body: payload,
  });
}

export async function getMindgoDatasetSyncStatus(
  datasetId: string,
): Promise<MindgoDatasetSyncStatusResponse> {
  return requestJson<MindgoDatasetSyncStatusResponse>(`/api/mindgo/datasets/${datasetId}/sync`);
}

export async function upsertMindgoDatasetSyncScheduler(
  datasetId: string,
  payload: MindgoDatasetSyncSchedulerPayload,
): Promise<MindgoDatasetSyncStatusResponse> {
  return requestJson<MindgoDatasetSyncStatusResponse>(
    `/api/mindgo/datasets/${datasetId}/sync/scheduler`,
    {
      method: "POST",
      body: payload,
    },
  );
}

export async function deleteMindgoDatasetSyncScheduler(
  datasetId: string,
): Promise<MindgoDatasetSyncStatusResponse> {
  return requestJson<MindgoDatasetSyncStatusResponse>(
    `/api/mindgo/datasets/${datasetId}/sync/scheduler`,
    {
      method: "DELETE",
    },
  );
}

export async function listJobRuntimeInstances(
  params: JobRuntimeInstanceListParams = {},
): Promise<JobRuntimeInstanceListResponse> {
  const searchParams = new URLSearchParams();
  if (params.job_type) {
    searchParams.set("job_type", params.job_type);
  }
  if (params.job_id) {
    searchParams.set("job_id", params.job_id);
  }
  if (params.status) {
    searchParams.set("status", params.status);
  }
  if (params.page) {
    searchParams.set("page", String(params.page));
  }
  if (params.page_size) {
    searchParams.set("page_size", String(params.page_size));
  }
  const suffix = searchParams.toString() ? `?${searchParams.toString()}` : "";
  return requestJson<JobRuntimeInstanceListResponse>(`/api/job-runtime/instances${suffix}`);
}

export async function rerunJobRuntimeInstance(instanceId: string): Promise<JobRuntimeInstance> {
  return requestJson<JobRuntimeInstance>(`/api/job-runtime/instances/${instanceId}/rerun`, {
    method: "POST",
  });
}

export async function deleteJobRuntimeInstance(instanceId: string): Promise<void> {
  return requestJson<void>(`/api/job-runtime/instances/${instanceId}`, {
    method: "DELETE",
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
  return requestJson<Project>("/api/projects/create", {
    method: "POST",
    body: payload,
  });
}

export async function openProject(payload: CreateProjectPayload): Promise<Project> {
  return requestJson<Project>("/api/projects/open", {
    method: "POST",
    body: payload,
  });
}

export async function resolveProject(payload: CreateProjectPayload): Promise<Project> {
  return requestJson<Project>("/api/projects/resolve", {
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
  projectId?: string | null,
): Promise<ChatSessionListResponse> {
  const params = new URLSearchParams();
  if (!projectId) {
    return { items: [], total: 0, limit: 20, offset: 0 };
  }
  params.set("project_id", projectId);
  if (query) {
    params.set("query", query);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return requestJson<ChatSessionListResponse>(`/api/chat-sessions${suffix}`);
}

export async function createChatSession(
  payload: CreateChatSessionPayload,
): Promise<ChatSession> {
  return requestJson<ChatSession>("/api/chat-sessions", {
    method: "POST",
    body: payload,
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
      project_id: input.projectId,
    },
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
  const response = await fetch(toApiUrl(streamUrl));
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
    body: payload,
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
