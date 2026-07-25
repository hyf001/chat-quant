import type { BacktestDetail, BacktestRun, CreateBacktestRunPayload } from "../types/backtests";
import type {
  ChatSession,
  ChatSessionDetail,
  ChatSessionListResponse,
  CreateChatSessionPayload,
  SendMessageResponse,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
export { API_BASE_URL };

const DEFAULT_USER_ID = "demo_user";
const DEFAULT_PROJECT_ID = "default_project";

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  body?: unknown;
};

async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": DEFAULT_USER_ID,
      "X-Project-Id": DEFAULT_PROJECT_ID,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
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
  runtime_root_writable: boolean;
};

export type PythonExecutionRequest = {
  chat_session_id: string;
  code_artifact_id: string;
  entrypoint: string;
  stdin_json?: Record<string, unknown>;
  timeout_seconds?: number;
  expected_outputs?: string[];
  purpose?: "query_analysis" | "stock_screening" | "chart_generation" | "strategy_smoke_test" | "utility";
  code_files: Array<{ path: string; content: string }>;
};

export async function getHealth(): Promise<{ status: string; service?: string }> {
  return requestJson<{ status: string; service?: string }>("/api/health");
}

export async function listChatSessions(query?: string): Promise<ChatSessionListResponse> {
  const params = new URLSearchParams();
  if (query) {
    params.set("query", query);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return requestJson<ChatSessionListResponse>(`/api/conversations${suffix}`);
}

export async function createChatSession(
  payload: CreateChatSessionPayload = {},
): Promise<ChatSession> {
  return requestJson<ChatSession>("/api/conversations", {
    method: "POST",
    body: payload,
  });
}

export async function getChatSessionDetail(chatSessionId: string): Promise<ChatSessionDetail> {
  return requestJson<ChatSessionDetail>(`/api/conversations/${chatSessionId}`);
}

export async function sendChatMessage(
  chatSessionId: string,
  content: string,
): Promise<SendMessageResponse> {
  return requestJson<SendMessageResponse>(`/api/conversations/${chatSessionId}/messages`, {
    method: "POST",
    body: { content },
  });
}

export async function getRuntimeHealth(): Promise<RuntimeHealth> {
  return requestJson<RuntimeHealth>("/api/runtime/health");
}

export async function executePythonArtifact(
  payload: PythonExecutionRequest,
): Promise<ExecutionResult> {
  const data = await requestJson<{ execution_result: ExecutionResult }>("/api/runtime/execute", {
    method: "POST",
    body: payload,
  });
  return data.execution_result;
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
