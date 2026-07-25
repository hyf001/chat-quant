import { Plus, RefreshCw, Search } from "lucide-react";
import { useEffect, useState } from "react";

import { listStrategies, type ChatSession, type StrategySummary } from "../../shared/api";

type HistoryPanelProps = {
  sessions: ChatSession[];
  activeSessionId: string | null;
  query: string;
  isLoading: boolean;
  onCreateSession: () => void;
  onQueryChange: (query: string) => void;
  onSelectSession: (chatSessionId: string) => void;
};

const statusLabel: Record<StrategySummary["version_status"], string> = {
  draft: "草稿",
  validating: "校验中",
  validated: "已校验",
  invalid: "未通过",
  archived: "已归档",
};

function formatTime(value: string): string {
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function HistoryPanel({
  sessions,
  activeSessionId,
  query,
  isLoading,
  onCreateSession,
  onQueryChange,
  onSelectSession,
}: HistoryPanelProps) {
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [isLoadingStrategies, setIsLoadingStrategies] = useState(true);
  const [strategyError, setStrategyError] = useState<string | null>(null);

  useEffect(() => {
    void refreshStrategies();
  }, []);

  async function refreshStrategies() {
    try {
      setIsLoadingStrategies(true);
      setStrategyError(null);
      setStrategies(await listStrategies());
    } catch (error) {
      setStrategyError(error instanceof Error ? error.message : "历史策略加载失败");
    } finally {
      setIsLoadingStrategies(false);
    }
  }

  return (
    <aside className="hidden border-r border-line bg-panel/85 px-4 py-5 lg:block" aria-label="历史会话">
      <div className="mb-5 flex items-center gap-3">
        <div className="grid size-9 place-items-center rounded-lg bg-brand text-sm font-bold text-white">
          CQ
        </div>
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold">Chat-Quant</div>
          <div className="truncate text-xs text-muted">股票分析智能体</div>
        </div>
      </div>

      <button
        className="mb-4 flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white transition hover:bg-strong focus:outline-none focus:ring-2 focus:ring-brand/40"
        type="button"
        onClick={onCreateSession}
      >
        <Plus size={16} />
        新建会话
      </button>

      <label className="mb-4 flex h-9 items-center gap-2 rounded-lg border border-line bg-soft px-3 text-sm text-muted">
        <Search size={15} />
        <input
          className="min-w-0 flex-1 bg-transparent text-ink outline-none placeholder:text-muted"
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="搜索标题、摘要、标签"
        />
      </label>

      <div className="mb-3 text-xs font-semibold text-muted">最近会话</div>
      <div className="grid gap-2">
        {isLoading ? <Notice text="加载中" /> : null}
        {!isLoading && sessions.length === 0 ? <Notice text="暂无会话" /> : null}
        {sessions.map((session) => {
          const isActive = session.id === activeSessionId;
          return (
            <button
              className={`w-full rounded-lg border p-3 text-left transition focus:outline-none focus:ring-2 focus:ring-brand/30 ${
                isActive
                  ? "border-brand bg-brand/10"
                  : "border-line bg-soft hover:border-strong hover:bg-panel"
              }`}
              key={session.id}
              type="button"
              onClick={() => onSelectSession(session.id)}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1 truncate text-sm font-semibold">{session.title}</div>
                <div className="shrink-0 text-[11px] text-muted">{formatTime(session.updated_at)}</div>
              </div>
              <div className="mt-1 line-clamp-2 text-xs leading-5 text-muted">
                {session.snippet || session.data_scope_label || "未输入消息"}
              </div>
            </button>
          );
        })}
      </div>

      <div className="mb-3 mt-5 flex items-center justify-between gap-2">
        <div className="text-xs font-semibold text-muted">策略资产</div>
        <button
          className="grid size-8 place-items-center rounded-lg border border-line bg-soft text-ink transition hover:border-strong hover:bg-panel disabled:cursor-not-allowed disabled:opacity-50"
          type="button"
          aria-label="刷新策略资产"
          onClick={refreshStrategies}
          disabled={isLoadingStrategies}
        >
          <RefreshCw size={14} />
        </button>
      </div>

      <div className="grid gap-2">
        {isLoadingStrategies ? <Notice text="正在读取策略资产" /> : null}
        {!isLoadingStrategies && strategyError ? <Notice text={strategyError} tone="risk" /> : null}
        {!isLoadingStrategies && !strategyError && strategies.length === 0 ? (
          <Notice text="暂无策略资产" />
        ) : null}
        {!isLoadingStrategies && !strategyError
          ? strategies.slice(0, 4).map((strategy) => (
              <div className="rounded-lg border border-line bg-soft p-3" key={strategy.strategy_id}>
                <div className="flex items-center justify-between gap-2">
                  <div className="min-w-0 truncate text-sm font-semibold">{strategy.name}</div>
                  <span className="shrink-0 rounded-full border border-line bg-panel px-2 py-0.5 text-xs text-muted">
                    V{strategy.version}
                  </span>
                </div>
                <div className="mt-2 line-clamp-2 text-xs leading-5 text-muted">
                  {strategy.logic_summary ?? "策略逻辑摘要待补充"}
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  <Tag text={statusLabel[strategy.version_status]} />
                  <Tag text={strategy.strategy_type} />
                </div>
              </div>
            ))
          : null}
      </div>
    </aside>
  );
}

function Tag({ text }: { text: string }) {
  return (
    <span className="max-w-full truncate rounded-full border border-line bg-panel px-2 py-0.5 text-xs text-muted">
      {text}
    </span>
  );
}

function Notice({ text, tone = "muted" }: { text: string; tone?: "muted" | "risk" }) {
  const toneClass = tone === "risk" ? "border-risk/40 text-risk" : "border-dashed text-muted";
  return <div className={`rounded-lg border bg-soft p-4 text-sm ${toneClass}`}>{text}</div>;
}
