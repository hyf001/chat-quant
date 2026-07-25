import { useCallback, useEffect, useMemo, useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import {
  createChatSession,
  getChatSessionDetail,
  listChatSessions,
  sendChatMessage,
  type ChatSession,
  type ChatSessionDetail,
} from "../shared/api";

export function WorkbenchPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [detail, setDetail] = useState<ChatSessionDetail | null>(null);
  const [historyQuery, setHistoryQuery] = useState("");
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const activeSession = useMemo(
    () => detail?.session ?? sessions.find((session) => session.id === activeSessionId) ?? null,
    [activeSessionId, detail?.session, sessions],
  );

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
      const data = await getChatSessionDetail(chatSessionId);
      setDetail(data);
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
    if (activeSessionId) {
      void loadDetail(activeSessionId);
    } else {
      setDetail(null);
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
      } else {
        await sendChatMessage(sessionId, content);
      }

      const updatedDetail = await getChatSessionDetail(sessionId);
      setDetail(updatedDetail);
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
      header={<WorkspaceHeader session={activeSession} isConnected={!error} />}
      conversation={
        <ConversationShell
          session={activeSession}
          messages={detail?.messages ?? []}
          assets={detail?.assets ?? []}
          isLoading={isDetailLoading}
          error={error}
        />
      }
      composer={<Composer disabled={isSending} onSendMessage={handleSendMessage} />}
      insight={<InsightPanel session={activeSession} assets={detail?.assets ?? []} />}
    />
  );
}
