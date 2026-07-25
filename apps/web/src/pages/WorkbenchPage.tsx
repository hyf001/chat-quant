import { useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import { readChatStream, sendChatMessage } from "../shared/api";
import type {
  ChatMessageView,
  ChatSessionSummary,
  SDKEvent,
  SDKStreamEnvelope,
  ToolCallView,
} from "../shared/types/agentRuntime";

export function WorkbenchPage() {
  const [chatSessionId, setChatSessionId] = useState<string | null>(null);
  const [sdkSessionId, setSdkSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessageView[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "可以直接输入股票分析、选股条件、策略想法或回测问题，我会按 M2 Runtime 契约透传执行过程。",
    },
  ]);
  const [tools, setTools] = useState<ToolCallView[]>([]);
  const [lastEnvelope, setLastEnvelope] = useState<SDKStreamEnvelope | null>(null);
  const [status, setStatus] = useState<ChatSessionSummary["status"]>("idle");
  const [error, setError] = useState<string | null>(null);

  const sessionSummary: ChatSessionSummary = {
    chatSessionId,
    sdkSessionId,
    title: messages.find((message) => message.role === "user")?.content.slice(0, 24) || "新的分析会话",
    status,
  };

  async function handleSend(message: string) {
    const assistantMessageId = `assistant-${Date.now()}`;
    setError(null);
    setStatus("running");
    setMessages((current) => [
      ...current,
      { id: `user-${Date.now()}`, role: "user", content: message },
      { id: assistantMessageId, role: "assistant", content: "正在读取上下文..." },
    ]);

    try {
      const accepted = await sendChatMessage({ message, chatSessionId });
      setChatSessionId(accepted.chat_session_id);
      setSdkSessionId(accepted.sdk_session_id);
      await readChatStream(accepted.stream_url, (envelope) => {
        setLastEnvelope(envelope);
        if (envelope.sdk_session_id) {
          setSdkSessionId(envelope.sdk_session_id);
        }
        applyEnvelope(envelope, assistantMessageId);
      });
      setStatus("completed");
    } catch (caught) {
      const messageText = caught instanceof Error ? caught.message : "Chat request failed";
      setError(messageText);
      setStatus("failed");
      setMessages((current) =>
        current.map((item) =>
          item.id === assistantMessageId ? { ...item, content: `请求失败：${messageText}` } : item,
        ),
      );
    }
  }

  function applyEnvelope(envelope: SDKStreamEnvelope, assistantMessageId: string) {
    const event = envelope.sdk_event;
    if (event.type === "assistant_message") {
      const text = extractAssistantText(event);
      if (text) {
        setMessages((current) =>
          current.map((item) =>
            item.id === assistantMessageId ? { ...item, content: text } : item,
          ),
        );
      }
    }

    if (event.type === "tool_use") {
      const id = String(event.id ?? `tool-${envelope.sequence}`);
      setTools((current) => [
        ...current,
        {
          id,
          command: String(event.command ?? "Bash"),
          status: "running",
        },
      ]);
    }

    if (event.type === "tool_result") {
      const toolUseId = String(event.tool_use_id ?? "");
      setTools((current) =>
        current.map((tool) =>
          tool.id === toolUseId
            ? {
                ...tool,
                status: event.is_error === true ? "failed" : "completed",
                output: String(event.content ?? ""),
              }
            : tool,
        ),
      );
    }

    if (event.type === "result_message") {
      setMessages((current) =>
        current.map((item) =>
          item.id === assistantMessageId ? { ...item, content: String(event.result ?? "") } : item,
        ),
      );
    }
  }

  return (
    <WorkspaceLayout
      history={<HistoryPanel session={sessionSummary} />}
      header={<WorkspaceHeader status={status} sdkSessionId={sdkSessionId} />}
      conversation={<ConversationShell messages={messages} tools={tools} error={error} />}
      composer={<Composer disabled={status === "running"} onSend={handleSend} />}
      insight={<InsightPanel envelope={lastEnvelope} tools={tools} />}
    />
  );
}

function extractAssistantText(event: SDKEvent): string {
  const content = event.content;
  if (!Array.isArray(content)) {
    return "";
  }
  return content
    .map((block) => {
      if (typeof block !== "object" || block === null || !("type" in block)) {
        return "";
      }
      const typedBlock = block as Record<string, unknown>;
      return typedBlock.type === "text" ? String(typedBlock.text ?? "") : "";
    })
    .filter(Boolean)
    .join("\n");
}
