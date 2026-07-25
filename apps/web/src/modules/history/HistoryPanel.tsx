import { Plus, Search } from "lucide-react";

import { IconButton } from "../../shared/components";
import type { ChatSession } from "../../shared/api";

type HistoryPanelProps = {
  sessions: ChatSession[];
  activeSessionId: string | null;
  query: string;
  isLoading: boolean;
  onCreateSession: () => void;
  onQueryChange: (query: string) => void;
  onSelectSession: (chatSessionId: string) => void;
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
        {isLoading ? (
          <div className="rounded-lg border border-line bg-soft p-4 text-sm text-muted">加载中</div>
        ) : null}
        {!isLoading && sessions.length === 0 ? (
          <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
            暂无会话
          </div>
        ) : null}
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
              <div className="mt-2 flex flex-wrap gap-1">
                {session.symbols.slice(0, 3).map((symbol) => (
                  <span
                    className="rounded border border-line bg-panel px-1.5 py-0.5 text-[11px] text-muted"
                    key={symbol}
                  >
                    {symbol}
                  </span>
                ))}
                {session.tags.slice(0, 2).map((tag) => (
                  <span
                    className="rounded border border-line bg-panel px-1.5 py-0.5 text-[11px] text-muted"
                    key={tag}
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </button>
          );
        })}
      </div>

      <div className="mt-4 lg:hidden">
        <IconButton label="关闭历史" icon={<Plus size={16} />} />
      </div>
    </aside>
  );
}
