import type { AgentScenario, ChatMessageAccepted, SDKStreamEnvelope } from "../types/agentRuntime";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function getHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

type SendChatMessageInput = {
  message: string;
  chatSessionId?: string | null;
  scenario?: AgentScenario;
};

export async function sendChatMessage(input: SendChatMessageInput): Promise<ChatMessageAccepted> {
  const response = await fetch(`${API_BASE_URL}/api/chat/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: input.message,
      chat_session_id: input.chatSessionId,
      scenario: input.scenario,
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat message failed: ${response.status}`);
  }
  return response.json();
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
      onEnvelope(parseEnvelope(dataLine.slice(6)));
    }
    if (done) {
      break;
    }
  }
}

function toApiUrl(url: string): string {
  if (url.startsWith("http")) {
    return url;
  }
  return `${API_BASE_URL}${url}`;
}

function parseEnvelope(payload: string): SDKStreamEnvelope {
  const parsed = JSON.parse(payload) as SDKStreamEnvelope;
  return parsed;
}
