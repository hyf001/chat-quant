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
  CreateChatSessionPayload,
  SendMessageResponse,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
export { API_BASE_URL };

const API_USER_ID = import.meta.env.VITE_CHATQ_USER_ID ?? "local_user";
const API_PROJECT_ID = import.meta.env.VITE_CHATQ_PROJECT_ID ?? "local_project";
export { API_PROJECT_ID, API_USER_ID };

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  body?: unknown;
};

type SendAgentChatMessageInput = {
  message: string;
  chatSessionId?: string | null;
  scenario?: AgentScenario;
};

async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": API_USER_ID,
      "X-Project-Id": API_PROJECT_ID,
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
  return requestJson<ChatSessionListResponse>(`/api/chat-sessions${suffix}`);
}

export async function createChatSession(
  payload: CreateChatSessionPayload = {},
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
      scenario: input.scenario,
      user_id: API_USER_ID,
      project_id: API_PROJECT_ID,
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
