import { useCallback, useEffect, useMemo, useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import {
  createChatSession,
  getAgentChatSessionDetail,
  getChatSessionDetail,
  getRuntimeHealth,
  listChatSessions,
  readChatStream,
  sendAgentChatMessage,
  type AgentChatSessionDetail,
  type ChatSession,
  type ChatSessionDetail,
  type RuntimeHealth,
  type SDKStreamEnvelope,
  type SdkMessage,
} from "../shared/api";

export function WorkbenchPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [detail, setDetail] = useState<ChatSessionDetail | null>(null);
  const [agentMessages, setAgentMessages] = useState<SdkMessage[]>([]);
  const [conversationEnvelopes, setConversationEnvelopes] = useState<SDKStreamEnvelope[]>([]);
  const [historyQuery, setHistoryQuery] = useState("");
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [runtimeHealth, setRuntimeHealth] = useState<RuntimeHealth | null>(null);

  const activeSession = useMemo(
    () => detail?.session ?? sessions.find((session) => session.id === activeSessionId) ?? null,
    [activeSessionId, detail?.session, sessions],
  );
  const conversationMessages = agentMessages.length > 0 ? agentMessages : detail?.messages ?? [];
  const conversationRuntimeEnvelopes = agentMessages.length > 0 ? conversationEnvelopes : [];

  const refreshSessions = useCallback(
    async (query = historyQuery) => {
      setIsHistoryLoading(true);
      setError(null);
      try {
        const data = await listChatSessions(query.trim() || undefined);
        setSessions(data.items);
        if (!activeSessionId && data.items.length > 0) {
          setActiveSessionId(data.items[0].id);
        }
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "会话列表加载失败");
      } finally {
        setIsHistoryLoading(false);
      }
    },
    [activeSessionId, historyQuery],
  );

  const loadDetail = useCallback(async (chatSessionId: string) => {
    setIsDetailLoading(true);
    setError(null);
    try {
      const sessionDetail = await getChatSessionDetail(chatSessionId);
      setDetail(sessionDetail);
      const agentDetail = await getAgentDetailOrNull(chatSessionId);
      setAgentMessages(agentDetail ? agentDetailToMessages(agentDetail) : []);
      setConversationEnvelopes(agentDetail?.envelopes ?? []);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "会话详情加载失败");
    } finally {
      setIsDetailLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshSessions("");
  }, [refreshSessions]);

  useEffect(() => {
    getRuntimeHealth()
      .then(setRuntimeHealth)
      .catch(() => setRuntimeHealth(null));
  }, []);

  useEffect(() => {
    if (activeSessionId) {
      void loadDetail(activeSessionId);
    } else {
      setDetail(null);
      setAgentMessages([]);
      setConversationEnvelopes([]);
    }
  }, [activeSessionId, loadDetail]);

  const handleSearchChange = (query: string) => {
    setHistoryQuery(query);
    void refreshSessions(query);
  };

  const handleCreateSession = async () => {
    setError(null);
    try {
      const session = await createChatSession({ title: "新的量化会话" });
      setSessions((current) => [session, ...current]);
      setActiveSessionId(session.id);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "新建会话失败");
    }
  };

  const handleSendMessage = async (content: string) => {
    setIsSending(true);
    setError(null);
    try {
      let sessionId = activeSessionId;
      if (!sessionId) {
        const created = await createChatSession({ initial_prompt: content });
        setSessions((current) => [created, ...current]);
        setActiveSessionId(created.id);
        sessionId = created.id;
      }

      const optimisticUserMessage = makeTextMessage({
        id: `local_user_${Date.now()}`,
        role: "user",
        text: content,
        createdAt: new Date().toISOString(),
      });
      setAgentMessages((current) => [...current, optimisticUserMessage]);

      const accepted = await sendAgentChatMessage({ chatSessionId: sessionId, message: content });
      let assistantDraft = "";
      const assistantMessageId = `local_assistant_${accepted.user_message_id}`;
      await readChatStream(accepted.stream_url, (envelope) => {
        setConversationEnvelopes((current) => upsertEnvelope(current, envelope));
        const text = assistantTextFromEnvelope(envelope);
        if (!text) {
          return;
        }
        assistantDraft = appendStreamText(assistantDraft, text, isDeltaEnvelope(envelope));
        setAgentMessages((current) =>
          upsertTextMessage(current, {
            id: assistantMessageId,
            role: "assistant",
            text: assistantDraft,
            createdAt: envelope.received_at,
          }),
        );
      });

      const agentDetail = await getAgentDetailOrNull(sessionId);
      if (agentDetail) {
        setAgentMessages(agentDetailToMessages(agentDetail));
        setConversationEnvelopes(agentDetail.envelopes);
      }
      setDetail(await getChatSessionDetail(sessionId));
      await refreshSessions(historyQuery);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "消息发送失败");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <WorkspaceLayout
      history={
        <HistoryPanel
          sessions={sessions}
          activeSessionId={activeSessionId}
          query={historyQuery}
          isLoading={isHistoryLoading}
          onCreateSession={handleCreateSession}
          onQueryChange={handleSearchChange}
          onSelectSession={setActiveSessionId}
        />
      }
      header={
        <WorkspaceHeader
          session={activeSession}
          isConnected={!error}
          health={runtimeHealth}
        />
      }
      conversation={
        <ConversationShell
          session={activeSession}
          messages={conversationMessages}
          envelopes={conversationRuntimeEnvelopes}
          assets={detail?.assets ?? []}
          isLoading={isDetailLoading}
          isStreaming={isSending}
          error={error}
        />
      }
      composer={<Composer disabled={isSending} onSendMessage={handleSendMessage} />}
      insight={
        <InsightPanel
          session={activeSession}
          assets={detail?.assets ?? []}
          artifact={null}
          health={runtimeHealth}
          result={null}
          backtestDetail={null}
        />
      }
    />
  );
}

async function getAgentDetailOrNull(chatSessionId: string): Promise<AgentChatSessionDetail | null> {
  try {
    return await getAgentChatSessionDetail(chatSessionId);
  } catch {
    return null;
  }
}

function agentDetailToMessages(agentDetail: AgentChatSessionDetail): SdkMessage[] {
  return agentDetail.messages.map((message) =>
    makeTextMessage({
      id: message.message_id,
      role: toSdkRole(message.role),
      text: message.content,
      createdAt: message.created_at,
    }),
  );
}

function makeTextMessage({
  id,
  role,
  text,
  createdAt,
}: {
  id: string;
  role: SdkMessage["role"];
  text: string;
  createdAt: string;
}): SdkMessage {
  return {
    uuid: id,
    role,
    content: [{ type: "text", text, tool_use_id: null, name: null }],
    created_at: createdAt,
  };
}

function upsertTextMessage(
  messages: SdkMessage[],
  next: { id: string; role: SdkMessage["role"]; text: string; createdAt: string },
): SdkMessage[] {
  const replacement = makeTextMessage({
    id: next.id,
    role: next.role,
    text: next.text,
    createdAt: next.createdAt,
  });
  const existingIndex = messages.findIndex((message) => message.uuid === next.id);
  if (existingIndex === -1) {
    return [...messages, replacement];
  }
  return messages.map((message, index) => (index === existingIndex ? replacement : message));
}

function assistantTextFromEnvelope(envelope: SDKStreamEnvelope): string | null {
  const event = unwrapEvent(envelope.sdk_event);
  const type = typeof event.type === "string" ? event.type : "";
  if (type === "assistant_message") {
    return textFromContentBlocks(event.content);
  }
  if (type === "content_block_delta") {
    const delta = asRecord(event.delta);
    return asString(delta?.text) ?? asString(event.text) ?? null;
  }
  if (type === "text_delta") {
    return asString(event.text) ?? asString(asRecord(event.delta)?.text);
  }
  if (type === "result_message" && typeof event.result === "string") {
    return event.result.trim() || null;
  }
  if (type === "runtime_error" && typeof event.message === "string") {
    return `运行失败：${event.message}`;
  }
  return null;
}

function isDeltaEnvelope(envelope: SDKStreamEnvelope): boolean {
  const type = asString(unwrapEvent(envelope.sdk_event).type);
  return type === "content_block_delta" || type === "text_delta";
}

function appendStreamText(current: string, next: string, isDelta: boolean): string {
  if (!current) {
    return next;
  }
  if (!next) {
    return current;
  }
  if (!isDelta) {
    return `${current}\n\n${next}`;
  }
  if (current.endsWith("\n") || next.startsWith("\n") || next.startsWith(" ")) {
    return `${current}${next}`;
  }
  if (shouldInsertSpace(current, next)) {
    return `${current} ${next}`;
  }
  return `${current}${next}`;
}

function shouldInsertSpace(current: string, next: string): boolean {
  const last = current[current.length - 1];
  const first = next[0];
  return /[A-Za-z0-9]/.test(last) && /[A-Za-z0-9]/.test(first);
}

function textFromContentBlocks(content: unknown): string | null {
  if (!Array.isArray(content)) {
    return null;
  }
  const text = content
    .map((block) =>
      block &&
      typeof block === "object" &&
      "type" in block &&
      block.type === "text" &&
      "text" in block &&
      typeof block.text === "string"
        ? block.text
        : null,
    )
    .filter((value): value is string => Boolean(value))
    .join("\n");
  return text || null;
}

function upsertEnvelope(
  envelopes: SDKStreamEnvelope[],
  nextEnvelope: SDKStreamEnvelope,
): SDKStreamEnvelope[] {
  const existingIndex = envelopes.findIndex((envelope) => envelope.sequence === nextEnvelope.sequence);
  if (existingIndex === -1) {
    return [...envelopes, nextEnvelope].sort((left, right) => left.sequence - right.sequence);
  }
  return envelopes.map((envelope, index) => (index === existingIndex ? nextEnvelope : envelope));
}

function unwrapEvent(event: Record<string, unknown>): Record<string, unknown> {
  const innerEvent = asRecord(event.event);
  if (event.type === "stream_event" && innerEvent) {
    return { ...innerEvent, uuid: event.uuid, session_id: event.session_id };
  }
  if (event.type === "stream_event") {
    return normalizeFlattenedStreamEvent(event);
  }
  return event;
}

function normalizeFlattenedStreamEvent(event: Record<string, unknown>): Record<string, unknown> {
  const delta = asRecord(event.delta);
  const deltaType = asString(delta?.type);
  if (deltaType === "text_delta") {
    return { ...event, type: "text_delta", text: delta?.text };
  }
  if (deltaType === "thinking_delta") {
    return { ...event, type: "content_block_delta" };
  }
  if (delta && ("text" in delta || "thinking" in delta)) {
    return { ...event, type: "content_block_delta" };
  }

  const contentBlock = asRecord(event.content_block);
  const contentBlockType = asString(contentBlock?.type);
  if (contentBlockType) {
    return { ...event, ...contentBlock, type: contentBlockType };
  }

  if (typeof event.result === "string") {
    return { ...event, type: "result_message" };
  }
  return event;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" && value.trim().length > 0 ? value : null;
}

function toSdkRole(role: string): SdkMessage["role"] {
  if (role === "assistant" || role === "tool" || role === "system" || role === "user") {
    return role;
  }
  return "assistant";
}
