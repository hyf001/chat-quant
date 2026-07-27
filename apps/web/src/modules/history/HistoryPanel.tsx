import { Code2, Plus, Settings, Terminal } from "lucide-react";

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

export function HistoryPanel({
  sessions,
  activeSessionId,
  query: _query,
  isLoading,
  onCreateSession,
  onQueryChange: _onQueryChange,
  onSelectSession,
}: HistoryPanelProps) {
  return (
    <aside
      className="flex h-full w-64 shrink-0 flex-col border-r border-zinc-800 bg-zinc-900 text-zinc-300"
      aria-label="历史会话"
    >
      <div className="border-b border-zinc-800 p-3">
        <button
          className="flex w-full items-center justify-center gap-2 rounded-md bg-white px-3 py-2 text-xs font-semibold text-zinc-900 transition-colors hover:bg-zinc-100 focus:outline-none focus:ring-2 focus:ring-white/40"
          type="button"
          onClick={onCreateSession}
        >
          <Plus className="h-4 w-4" />
          <span>新建 Agent 任务</span>
        </button>
      </div>

      <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-2">
        <div>
          <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-zinc-500">
            历史执行记录
          </div>
          <div className="mt-1 space-y-1">
            {isLoading ? <Notice text="加载中" /> : null}
            {!isLoading && sessions.length === 0 ? <Notice text="暂无会话" /> : null}
            {sessions.map((session) => {
              const isActive = session.id === activeSessionId;
              return (
                <button
                  className={`flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs transition-colors focus:outline-none focus:ring-2 focus:ring-white/20 ${
                    isActive
                      ? "border border-zinc-700 bg-zinc-800 font-medium text-white"
                      : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200"
                  }`}
                  key={session.id}
                  type="button"
                  onClick={() => onSelectSession(session.id)}
                >
                  {isActive ? (
                    <Terminal className="h-3.5 w-3.5 shrink-0 text-zinc-400" />
                  ) : (
                    <Code2 className="h-3.5 w-3.5 shrink-0" />
                  )}
                  <span className="truncate">{session.title}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-zinc-800 p-3 text-xs text-zinc-400">
        <span className="truncate font-mono text-[11px]">workspace: chat-quant</span>
        <button
          className="grid h-6 w-6 shrink-0 place-items-center rounded text-zinc-400 transition-colors hover:text-white focus:outline-none focus:ring-2 focus:ring-white/20"
          type="button"
          aria-label="设置"
        >
          <Settings className="h-4 w-4" />
        </button>
      </div>
    </aside>
  );
}

function Notice({ text }: { text: string }) {
  return (
    <div className="rounded-md border border-dashed border-zinc-700 px-2.5 py-2 text-xs text-zinc-500">
      {text}
    </div>
  );
}
