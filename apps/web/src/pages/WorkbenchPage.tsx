import { useCallback, useEffect, useMemo, useRef, useState } from "react";

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
  const [conversationEnvelopes, setConversationEnvelopes] = useState<SDKStreamEnvelope[]>([]);
  const [historyQuery, setHistoryQuery] = useState("");
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [runtimeHealth, setRuntimeHealth] = useState<RuntimeHealth | null>(null);
  const streamingSessionIdRef = useRef<string | null>(null);
  const loadDetailRequestIdRef = useRef(0);

  const activeSession = useMemo(
    () => detail?.session ?? sessions.find((session) => session.id === activeSessionId) ?? null,
    [activeSessionId, detail?.session, sessions],
  );
  const conversationMessages = useMemo(
    () => messagesFromEnvelopes(conversationEnvelopes),
    [conversationEnvelopes],
  );
  const conversationRuntimeEnvelopes = conversationEnvelopes;

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
    const requestId = loadDetailRequestIdRef.current + 1;
    loadDetailRequestIdRef.current = requestId;
    setIsDetailLoading(true);
    setError(null);
    try {
      const sessionDetail = await getChatSessionDetail(chatSessionId);
      if (requestId !== loadDetailRequestIdRef.current) {
        return;
      }
      setDetail(sessionDetail);
      const agentDetail = await getAgentDetailOrNull(chatSessionId);
      if (requestId !== loadDetailRequestIdRef.current) {
        return;
      }
      setConversationEnvelopes((current) =>
        streamingSessionIdRef.current === chatSessionId
          ? current
          : agentDetail
            ? agentDetailEnvelopes(agentDetail)
            : [],
      );
    } catch (caught) {
      if (requestId === loadDetailRequestIdRef.current) {
        setError(caught instanceof Error ? caught.message : "会话详情加载失败");
      }
    } finally {
      if (requestId === loadDetailRequestIdRef.current) {
        setIsDetailLoading(false);
      }
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
      loadDetailRequestIdRef.current += 1;
      setDetail(null);
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
        streamingSessionIdRef.current = created.id;
        setActiveSessionId(created.id);
        sessionId = created.id;
      } else {
        streamingSessionIdRef.current = sessionId;
      }

      const accepted = await sendAgentChatMessage({ chatSessionId: sessionId, message: content });
      setConversationEnvelopes((current) =>
        appendOptimisticUserMessage({
          envelopes: current,
          chatSessionId: sessionId,
          sdkSessionId: accepted.sdk_session_id,
          userMessageId: accepted.user_message_id,
          content,
        }),
      );
      await readChatStream(accepted.stream_url, (envelope) => {
        setConversationEnvelopes((current) => appendStreamEnvelope(current, envelope));
      });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "消息发送失败");
    } finally {
      streamingSessionIdRef.current = null;
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

function agentDetailEnvelopes(agentDetail: AgentChatSessionDetail): SDKStreamEnvelope[] {
  return agentDetail.envelopes.length > 0 ? agentDetail.envelopes : agentDetail.sdk_messages;
}

function messagesFromEnvelopes(envelopes: SDKStreamEnvelope[]): SdkMessage[] {
  const messages: SdkMessage[] = [];
  const seenUserMessageIds = new Set<string>();
  let activeAssistant: {
    id: string;
    text: string;
    createdAt: string;
    sourceSequence: number;
  } | null = null;

  const flushAssistant = () => {
    if (!activeAssistant?.text.trim()) {
      activeAssistant = null;
      return;
    }
    messages.push(
      makeTextMessage({
        id: activeAssistant.id,
        role: "assistant",
        text: activeAssistant.text,
        createdAt: activeAssistant.createdAt,
        sourceSequence: activeAssistant.sourceSequence,
      }),
    );
    activeAssistant = null;
  };

  [...envelopes]
    .sort((left, right) => left.sequence - right.sequence)
    .forEach((envelope) => {
      const event = unwrapEvent(envelope.sdk_event);
      const type = asString(event.type);

      if (type === "user_message") {
        flushAssistant();
        const text = textFromUserEvent(event);
        const id = userEventId(event) ?? `sdk_user_${envelope.sequence}`;
        if (text && isDisplayableUserMessage(event) && !seenUserMessageIds.has(id)) {
          seenUserMessageIds.add(id);
          messages.push(
            makeTextMessage({
              id,
              role: "user",
              text,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            }),
          );
        }
        return;
      }

      if (type === "assistant_message") {
        const text = assistantTextFromEvent(event);
        if (text) {
          activeAssistant = {
            id: asString(event.id) ?? asString(event.uuid) ?? `sdk_assistant_${envelope.sequence}`,
            text,
            createdAt: activeAssistant?.createdAt ?? envelope.received_at,
            sourceSequence: activeAssistant?.sourceSequence ?? envelope.sequence,
          };
          flushAssistant();
        }
        return;
      }

      const deltaText = assistantDeltaTextFromEvent(event);
      if (deltaText) {
        activeAssistant = {
          id: activeAssistant?.id ?? `sdk_assistant_stream_${envelope.sequence}`,
          text: appendStreamText(activeAssistant?.text ?? "", deltaText, true),
          createdAt: activeAssistant?.createdAt ?? envelope.received_at,
          sourceSequence: activeAssistant?.sourceSequence ?? envelope.sequence,
        };
        return;
      }

      if (type === "result_message") {
        if (!activeAssistant && messages.every((message) => message.role !== "assistant")) {
          const resultText = asString(event.result);
          if (resultText) {
            activeAssistant = {
              id: asString(event.uuid) ?? `sdk_result_${envelope.sequence}`,
              text: resultText,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            };
          }
        }
        flushAssistant();
        return;
      }

      if (type === "runtime_error") {
        flushAssistant();
        const message = asString(event.message);
        if (message) {
          messages.push(
            makeTextMessage({
              id: asString(event.uuid) ?? `sdk_error_${envelope.sequence}`,
              role: "assistant",
              text: `运行失败：${message}`,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            }),
          );
        }
      }
    });

  flushAssistant();
  return messages;
}

function makeTextMessage({
  id,
  role,
  text,
  createdAt,
  sourceSequence,
}: {
  id: string;
  role: SdkMessage["role"];
  text: string;
  createdAt: string;
  sourceSequence?: number;
}): SdkMessage {
  return {
    uuid: id,
    role,
    content: [{ type: "text", text, tool_use_id: null, name: null }],
    created_at: createdAt,
    source_sequence: sourceSequence,
  };
}

function assistantTextFromEvent(event: Record<string, unknown>): string | null {
  const text = textFromContentBlocks(event.content);
  if (text) {
    return text;
  }
  const message = asRecord(event.message);
  return message ? textFromContentBlocks(message.content) : null;
}

function assistantDeltaTextFromEvent(event: Record<string, unknown>): string | null {
  const type = asString(event.type);
  if (type === "content_block_delta") {
    const delta = asRecord(event.delta);
    return asString(delta?.text) ?? asString(event.text) ?? null;
  }
  if (type === "text_delta") {
    return asString(event.text) ?? asString(asRecord(event.delta)?.text);
  }
  return null;
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

function textFromUserEvent(event: Record<string, unknown>): string | null {
  const content = event.content;
  if (typeof content === "string") {
    return content;
  }
  const text = textFromContentBlocks(content);
  if (text) {
    return text;
  }
  const message = asRecord(event.message);
  const messageContent = message?.content;
  return typeof messageContent === "string" ? messageContent : textFromContentBlocks(messageContent);
}

function isDisplayableUserMessage(event: Record<string, unknown>): boolean {
  if (typeof event.content === "string") {
    return true;
  }
  const message = asRecord(event.message);
  return typeof message?.content === "string";
}

function appendStreamEnvelope(
  envelopes: SDKStreamEnvelope[],
  nextEnvelope: SDKStreamEnvelope,
): SDKStreamEnvelope[] {
  const lastSequence = envelopes.at(-1)?.sequence ?? 0;
  const sequence =
    nextEnvelope.sequence > lastSequence ? nextEnvelope.sequence : lastSequence + 1;
  return [...envelopes, { ...nextEnvelope, sequence }];
}

function appendOptimisticUserMessage({
  envelopes,
  chatSessionId,
  sdkSessionId,
  userMessageId,
  content,
}: {
  envelopes: SDKStreamEnvelope[];
  chatSessionId: string;
  sdkSessionId: string | null;
  userMessageId: string;
  content: string;
}): SDKStreamEnvelope[] {
  if (envelopes.some((envelope) => userEventId(unwrapEvent(envelope.sdk_event)) === userMessageId)) {
    return envelopes;
  }
  const lastSequence = envelopes.at(-1)?.sequence ?? 0;
  return [
    ...envelopes,
    {
      sequence: lastSequence + 1,
      chat_session_id: chatSessionId,
      sdk_session_id: sdkSessionId,
      turn_id: null,
      received_at: new Date().toISOString(),
      sdk_event: {
        type: "user_message",
        id: userMessageId,
        content,
      },
    },
  ];
}

function userEventId(event: Record<string, unknown>): string | null {
  const message = asRecord(event.message);
  return asString(event.id) ?? asString(event.uuid) ?? asString(message?.id) ?? asString(message?.uuid);
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
