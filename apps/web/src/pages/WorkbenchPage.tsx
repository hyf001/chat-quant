import { useCallback, useEffect, useMemo, useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import {
  ArtifactList,
  BacktestResultPanel,
  RuntimeResultPanel,
  demoBacktestDetail,
  demoBacktestPayload,
} from "../modules/result";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import {
  createBacktestRun,
  createChatSession,
  executePythonArtifact,
  getChatSessionDetail,
  getRuntimeHealth,
  listArtifacts,
  listChatSessions,
  runBacktest,
  sendChatMessage,
  type BacktestDetail,
  type ChatSession,
  type ChatSessionDetail,
  type CodeArtifact,
  type ExecutionResult,
  type RuntimeHealth,
} from "../shared/api";

const sampleCode = `
import csv
import json
import os
from pathlib import Path

payload = json.loads(Path(os.environ["CHATQ_STDIN_JSON"]).read_text(encoding="utf-8"))
output_dir = Path(os.environ["CHATQ_OUTPUT_DIR"])
tables_dir = output_dir / "tables"
tables_dir.mkdir(parents=True, exist_ok=True)

rows = [
    {"symbol": symbol, "score": 88 - index * 3, "signal": "watch"}
    for index, symbol in enumerate(payload["symbols"])
]

with (tables_dir / "screening.csv").open("w", newline="", encoding="utf-8") as file_obj:
    writer = csv.DictWriter(file_obj, fieldnames=["symbol", "score", "signal"])
    writer.writeheader()
    writer.writerows(rows)

result = {
    "status": "succeeded",
    "summary": "sample screening completed",
    "rows": rows,
    "warnings": [],
}
(output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
print(f"screened {len(rows)} symbols")
`.trim();

export function WorkbenchPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [detail, setDetail] = useState<ChatSessionDetail | null>(null);
  const [historyQuery, setHistoryQuery] = useState("");
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [artifacts, setArtifacts] = useState<CodeArtifact[]>([]);
  const [selectedArtifactId, setSelectedArtifactId] = useState<string | null>(null);
  const [isLoadingArtifacts, setIsLoadingArtifacts] = useState(true);
  const [artifactError, setArtifactError] = useState<string | null>(null);
  const [runtimeHealth, setRuntimeHealth] = useState<RuntimeHealth | null>(null);
  const [runtimeResult, setRuntimeResult] = useState<ExecutionResult | null>(null);
  const [isRuntimeRunning, setIsRuntimeRunning] = useState(false);
  const [runtimeError, setRuntimeError] = useState<string | null>(null);
  const [backtestDetail, setBacktestDetail] = useState<BacktestDetail>(demoBacktestDetail);
  const [isRunningBacktest, setIsRunningBacktest] = useState(false);
  const [backtestError, setBacktestError] = useState<string | null>(null);

  const activeSession = useMemo(
    () => detail?.session ?? sessions.find((session) => session.id === activeSessionId) ?? null,
    [activeSessionId, detail?.session, sessions],
  );

  const selectedArtifact = useMemo(
    () => artifacts.find((artifact) => artifact.artifact_id === selectedArtifactId) ?? null,
    [artifacts, selectedArtifactId],
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
      setDetail(await getChatSessionDetail(chatSessionId));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "会话详情加载失败");
    } finally {
      setIsDetailLoading(false);
    }
  }, []);

  const loadArtifacts = useCallback((chatSessionId?: string | null) => {
    setIsLoadingArtifacts(true);
    setArtifactError(null);
    listArtifacts(chatSessionId ?? undefined)
      .then((items) => {
        setArtifacts(items);
        setSelectedArtifactId((current) =>
          current && items.some((item) => item.artifact_id === current)
            ? current
            : items[0]?.artifact_id ?? null,
        );
      })
      .catch((caught: unknown) => {
        setArtifactError(caught instanceof Error ? caught.message : "Artifact request failed");
      })
      .finally(() => setIsLoadingArtifacts(false));
  }, []);

  useEffect(() => {
    void refreshSessions("");
  }, [refreshSessions]);

  useEffect(() => {
    getRuntimeHealth()
      .then(setRuntimeHealth)
      .catch((caught: unknown) => {
        setRuntimeError(caught instanceof Error ? caught.message : "Runtime health failed");
      });
  }, []);

  useEffect(() => {
    if (activeSessionId) {
      void loadDetail(activeSessionId);
      loadArtifacts(activeSessionId);
    } else {
      setDetail(null);
      loadArtifacts(null);
    }
  }, [activeSessionId, loadArtifacts, loadDetail]);

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
      setDetail(await getChatSessionDetail(sessionId));
      await refreshSessions(historyQuery);
      loadArtifacts(sessionId);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "消息发送失败");
    } finally {
      setIsSending(false);
    }
  };

  const handleRunSample = async () => {
    setIsRuntimeRunning(true);
    setRuntimeError(null);
    try {
      setRuntimeResult(
        await executePythonArtifact({
          chat_session_id: activeSessionId ?? "conv_demo_m4",
          code_artifact_id: selectedArtifactId ?? "code_demo_inline",
          entrypoint: "analysis.py",
          stdin_json: {
            symbols: ["沪深300", "中证500", "创业板指"],
            start_date: "2026-04-24",
            end_date: "2026-07-24",
          },
          timeout_seconds: 30,
          expected_outputs: ["result.json", "tables/screening.csv"],
          purpose: "stock_screening",
          code_files: [{ path: "analysis.py", content: sampleCode }],
        }),
      );
    } catch (caught: unknown) {
      setRuntimeError(caught instanceof Error ? caught.message : "Runtime execute failed");
    } finally {
      setIsRuntimeRunning(false);
    }
  };

  const handleRunDemoBacktest = async () => {
    setIsRunningBacktest(true);
    setBacktestError(null);
    try {
      const run = await createBacktestRun(demoBacktestPayload);
      setBacktestDetail(await runBacktest(run.id));
    } catch (caught) {
      setBacktestError(caught instanceof Error ? caught.message : "回测请求失败");
    } finally {
      setIsRunningBacktest(false);
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
          backtestStatus={backtestDetail.run.status}
        />
      }
      conversation={
        <ConversationShell
          session={activeSession}
          messages={detail?.messages ?? []}
          assets={detail?.assets ?? []}
          isLoading={isDetailLoading}
          error={error}
          artifactList={
            <ArtifactList
              artifacts={artifacts}
              selectedArtifactId={selectedArtifactId}
              isLoading={isLoadingArtifacts}
              error={artifactError}
              onRefresh={() => loadArtifacts(activeSessionId)}
              onSelectArtifact={setSelectedArtifactId}
            />
          }
        />
      }
      result={
        <div className="grid gap-4">
          <RuntimeResultPanel
            health={runtimeHealth}
            result={runtimeResult}
            isRunning={isRuntimeRunning}
            error={runtimeError}
            onRunSample={handleRunSample}
          />
          <BacktestResultPanel
            detail={backtestDetail}
            isRunning={isRunningBacktest}
            error={backtestError}
            onRunDemo={handleRunDemoBacktest}
          />
        </div>
      }
      composer={<Composer disabled={isSending} onSendMessage={handleSendMessage} />}
      insight={
        <InsightPanel
          session={activeSession}
          assets={detail?.assets ?? []}
          artifact={selectedArtifact}
          health={runtimeHealth}
          result={runtimeResult}
          backtestDetail={backtestDetail}
        />
      }
    />
  );
}
