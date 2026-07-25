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

export async function getHealth(): Promise<{ status: string }> {
  return requestJson<{ status: string }>("/api/health");
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
