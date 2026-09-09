import type {
  AgentChatSessionDetail,
  ChatMessageAccepted,
  SDKStreamEnvelope,
  StopChatSessionResponse,
} from "../types/agentRuntime";
import type { BacktestDetail, BacktestRun, CreateBacktestRunPayload } from "../types/backtests";
import type {
  ChatSession,
  ChatSessionDetail,
  ChatSessionListResponse,
  CreateProjectPayload,
  CreateChatSessionPayload,
  Project,
  ProjectDirectoryResponse,
  ProjectFileContentResponse,
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
  job_runtime_creation_tick_minutes: number;
  job_runtime_dispatch_interval_seconds: number;
  job_runtime_dispatch_limit: number;
  job_runtime_max_concurrent_instances: number;
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

export type MarketDataDatasetSettings = {
  dataset_id: string;
  symbol_field: string;
  datetime_field: string;
  open_field: string;
  high_field: string;
  low_field: string;
  close_field: string;
  volume_field: string;
};

export type BenchmarkDatasetSettings = {
  dataset_id: string;
  symbol_field: string;
  datetime_field: string;
  close_field: string;
};

export type MarketDataSettings = {
  market_data_dataset: MarketDataDatasetSettings;
  benchmark_dataset: BenchmarkDatasetSettings;
};

export type MarketDataSettingsUpdate = {
  market_data_dataset?: Partial<MarketDataDatasetSettings>;
  benchmark_dataset?: Partial<BenchmarkDatasetSettings>;
};

export type AppSettings = {
  system: SystemSettings;
  logging: LoggingSettings;
  agent: AgentSettings;
  mindgo: MindgoSettings;
  market_data: MarketDataSettings;
};

export type AppSettingsUpdate = {
  system?: Partial<SystemSettings>;
  logging?: Partial<LoggingSettings>;
  agent?: Partial<Omit<AgentSettings, "thinking">> & {
    thinking?: Partial<AgentSettings["thinking"]>;
  };
  mindgo?: Partial<MindgoSettings>;
  market_data?: MarketDataSettingsUpdate;
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

export type MindgoSourceStorageSpec = {
  path: string;
  format: "parquet";
  partitioned_by: string[];
  min_partition: string | null;
  max_partition: string | null;
  partition_count: number;
};

export type MindgoSourceSyncQueryWindow = {
  start_offset_days: number;
  end_offset_days: number;
};

export type MindgoSourceSyncSpec = {
  supports_query_window: boolean;
  default_query_window: MindgoSourceSyncQueryWindow;
  min_start_offset_days: number;
  max_end_offset_days: number;
};

export type MindgoSourceSchema = {
  name: string;
  name_zh: string;
  name_en: string;
  category_path: string[];
  category_path_en: string[];
  description: string;
  mindgo_function: string;
  storage: MindgoSourceStorageSpec;
  sync: MindgoSourceSyncSpec;
  query_params: MindgoParameterSpec[];
  result_schema: MindgoFieldSpec[];
};

export type MindgoSourceSummary = {
  id: string;
  name: string;
  name_zh: string;
  name_en: string;
  category_path: string[];
  category_path_en: string[];
  description: string;
  storage: MindgoSourceStorageSpec;
};

export type MindgoSourceListResponse = {
  sources: MindgoSourceSummary[];
};

export type MindgoSourceQueryPayload = {
  params: Record<string, MindgoJsonValue>;
  page: number;
  page_size: number;
};

export type MindgoSourceQueryResponse = {
  source_id: string;
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  columns: MindgoFieldSpec[];
  rows: Array<Record<string, MindgoJsonValue>>;
};

export type MindgoSourceSyncPayload = {
  trigger_start_date: string;
  trigger_end_date: string;
  trigger_time: string;
  write_mode: MindgoSourceSyncWriteMode;
  query_window: MindgoSourceSyncQueryWindow;
  params: Record<string, MindgoJsonValue>;
};

export type MindgoSourceSyncWriteMode = "overwrite" | "skip";

export type MindgoSourceSyncResult = {
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

export type MindgoSourceSyncTriggerResponse = {
  instance: JobRuntimeInstance;
  instances: JobRuntimeInstance[];
};

export type MindgoSourceSyncSchedulerPayload = {
  cron: string;
  write_mode: MindgoSourceSyncWriteMode;
  query_window: MindgoSourceSyncQueryWindow;
  params: Record<string, MindgoJsonValue>;
};

export type MindgoSourceSyncSchedulerState = {
  configured: boolean;
  scheduler_id: string | null;
  cron: string | null;
  write_mode: MindgoSourceSyncWriteMode;
  query_window: MindgoSourceSyncQueryWindow;
  params: Record<string, MindgoJsonValue>;
  last_run_at: string | null;
  next_run_at: string | null;
  created_at: string | null;
  updated_at: string | null;
};

export type MindgoSourceSyncStatusResponse = {
  source_id: string;
  job_type: string;
  job_id: string;
  scheduler: MindgoSourceSyncSchedulerState;
};

export type MindgoConnectionTestResponse = {
  ok: boolean;
  message: string;
};

export type Dataset = {
  id: string;
  name: string;
  name_zh: string;
  name_en: string;
  description: string;
  category_path: string[];
  category_path_en: string[];
  exposed_to_agent: boolean;
  created_at: string;
  updated_at: string;
};

export type DatasetDetail = Dataset & {
  create_sql: string;
};

export type DatasetPayload = {
  id?: string | null;
  name: string;
  description: string;
  category_path: string[];
  exposed_to_agent: boolean;
  create_sql: string;
};

export type DatasetUpdatePayload = Partial<
  Pick<Dataset, "description" | "category_path" | "exposed_to_agent">
>;

export type DatasetListResponse = {
  datasets: Dataset[];
};

export type DatasetNamingOption = {
  value: string;
  label: string;
  name_en: string;
};

export type DatasetNamingOptionsResponse = {
  markets: DatasetNamingOption[];
  asset_classes: DatasetNamingOption[];
  frequencies: DatasetNamingOption[];
};

export type DatasetQueryColumn = {
  name: string;
  value_type: string;
};

export type DatasetQueryPayload = {
  sql: string;
  page: number;
  page_size: number;
};

export type DatasetQueryResponse = {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  columns: DatasetQueryColumn[];
  rows: Array<Record<string, MindgoJsonValue>>;
};

export type NotebookServer = {
  project_id: string;
  status: "starting" | "running" | "stopped" | "error";
  url: string;
  base_url: string;
  proxy_base_url?: string | null;
  token: string;
  root_dir: string;
  pid: number;
  runtime_id: string;
  detail: string | null;
};

export type NotebookServerStatus = {
  project_id: string;
  status: "running" | "stopped";
  url: string | null;
  base_url: string | null;
  proxy_base_url?: string | null;
  root_dir: string | null;
  pid: number | null;
  runtime_id: string | null;
};

export type NotebookFile = {
  name: string;
  relative_path: string;
  size: number;
  modified_at: string;
};

export type NotebookFileListResponse = {
  project_id: string;
  root_dir: string;
  files: NotebookFile[];
};

export type NotebookSession = {
  path: string;
  session_id: string | null;
  kernel_id: string | null;
  kernel_name: string | null;
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

export async function listMindgoSources(): Promise<MindgoSourceListResponse> {
  return requestJson<MindgoSourceListResponse>("/api/mindgo/sources");
}

export async function testMindgoConnection(): Promise<MindgoConnectionTestResponse> {
  return requestJson<MindgoConnectionTestResponse>("/api/mindgo/test", {
    method: "POST",
    body: {},
  });
}

export async function getMindgoSourceSchema(
  sourceId: string,
): Promise<MindgoSourceSchema> {
  return requestJson<MindgoSourceSchema>(`/api/mindgo/sources/${sourceId}/schema`);
}

export async function queryMindgoSource(
  sourceId: string,
  payload: MindgoSourceQueryPayload,
): Promise<MindgoSourceQueryResponse> {
  return requestJson<MindgoSourceQueryResponse>(`/api/mindgo/sources/${sourceId}/query`, {
    method: "POST",
    body: payload,
  });
}

export async function syncMindgoSource(
  sourceId: string,
  payload: MindgoSourceSyncPayload,
): Promise<MindgoSourceSyncTriggerResponse> {
  return requestJson<MindgoSourceSyncTriggerResponse>(`/api/mindgo/sources/${sourceId}/sync`, {
    method: "POST",
    body: payload,
  });
}

export async function getMindgoSourceSyncStatus(
  sourceId: string,
): Promise<MindgoSourceSyncStatusResponse> {
  return requestJson<MindgoSourceSyncStatusResponse>(`/api/mindgo/sources/${sourceId}/sync`);
}

export async function upsertMindgoSourceSyncScheduler(
  sourceId: string,
  payload: MindgoSourceSyncSchedulerPayload,
): Promise<MindgoSourceSyncStatusResponse> {
  return requestJson<MindgoSourceSyncStatusResponse>(
    `/api/mindgo/sources/${sourceId}/sync/scheduler`,
    {
      method: "POST",
      body: payload,
    },
  );
}

export async function deleteMindgoSourceSyncScheduler(
  sourceId: string,
): Promise<MindgoSourceSyncStatusResponse> {
  return requestJson<MindgoSourceSyncStatusResponse>(
    `/api/mindgo/sources/${sourceId}/sync/scheduler`,
    {
      method: "DELETE",
    },
  );
}

export async function listDatasets(
  exposedToAgent?: boolean,
): Promise<DatasetListResponse> {
  const searchParams = new URLSearchParams();
  if (exposedToAgent !== undefined) {
    searchParams.set("exposed_to_agent", String(exposedToAgent));
  }
  const query = searchParams.toString();
  return requestJson<DatasetListResponse>(`/api/datasets${query ? `?${query}` : ""}`);
}

export async function getDatasetNamingOptions(): Promise<DatasetNamingOptionsResponse> {
  return requestJson<DatasetNamingOptionsResponse>("/api/datasets/naming-options");
}

export async function createDataset(
  payload: DatasetPayload,
): Promise<DatasetDetail> {
  return requestJson<DatasetDetail>("/api/datasets", {
    method: "POST",
    body: payload,
  });
}

export async function getDataset(datasetId: string): Promise<DatasetDetail> {
  return requestJson<DatasetDetail>(`/api/datasets/${datasetId}`);
}

export async function updateDataset(
  datasetId: string,
  payload: DatasetUpdatePayload,
): Promise<Dataset> {
  return requestJson<Dataset>(`/api/datasets/${datasetId}`, {
    method: "PUT",
    body: payload,
  });
}

export async function deleteDataset(datasetId: string): Promise<void> {
  return requestJson<void>(`/api/datasets/${datasetId}`, {
    method: "DELETE",
  });
}

export async function queryDatasets(
  payload: DatasetQueryPayload,
): Promise<DatasetQueryResponse> {
  return requestJson<DatasetQueryResponse>("/api/datasets/query", {
    method: "POST",
    body: payload,
  });
}

export async function listNotebookFiles(projectId: string): Promise<NotebookFileListResponse> {
  return requestJson<NotebookFileListResponse>(`/api/notebooks/${projectId}/files`);
}

export async function createNotebookFile(
  projectId: string,
  name?: string | null,
): Promise<NotebookFile> {
  return requestJson<NotebookFile>(`/api/notebooks/${projectId}/files`, {
    method: "POST",
    body: { name },
  });
}

export async function renameNotebookFile(
  projectId: string,
  path: string,
  name: string,
): Promise<NotebookFile> {
  return requestJson<NotebookFile>(`/api/notebooks/${projectId}/files`, {
    method: "PATCH",
    body: { path, name },
  });
}

export async function deleteNotebookFile(
  projectId: string,
  path: string,
): Promise<void> {
  return requestJson<void>(`/api/notebooks/${projectId}/files`, {
    method: "DELETE",
    body: { path },
  });
}

export async function ensureNotebookServer(projectId: string): Promise<NotebookServer> {
  return requestJson<NotebookServer>(`/api/notebooks/${projectId}/server`, {
    method: "POST",
  });
}

export async function getNotebookServerStatus(
  projectId: string,
): Promise<NotebookServerStatus> {
  return requestJson<NotebookServerStatus>(`/api/notebooks/${projectId}/server`);
}

export async function ensureNotebookSession(
  projectId: string,
  path: string,
): Promise<NotebookSession> {
  return requestJson<NotebookSession>(`/api/notebooks/${projectId}/sessions`, {
    method: "POST",
    body: { path },
  });
}

export async function stopNotebookServer(projectId: string): Promise<void> {
  return requestJson<void>(`/api/notebooks/${projectId}/server`, {
    method: "DELETE",
  });
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

export async function listProjectFiles(
  projectId: string,
  path = "",
): Promise<ProjectDirectoryResponse> {
  const params = new URLSearchParams();
  if (path) {
    params.set("path", path);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return requestJson<ProjectDirectoryResponse>(`/api/projects/${projectId}/files${suffix}`);
}

export async function getProjectFileContent(
  projectId: string,
  path: string,
): Promise<ProjectFileContentResponse> {
  const params = new URLSearchParams({ path });
  return requestJson<ProjectFileContentResponse>(
    `/api/projects/${projectId}/files/content?${params.toString()}`,
  );
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

export async function stopAgentChatSession(
  chatSessionId: string,
): Promise<StopChatSessionResponse> {
  return requestJson<StopChatSessionResponse>(`/api/chat/sessions/${chatSessionId}/stop`, {
    method: "POST",
    body: { reason: "user_requested_stop" },
  });
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
