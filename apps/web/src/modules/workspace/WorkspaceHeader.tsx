import { Cpu } from "lucide-react";

import type { BacktestRunStatus, ChatSession, Project, RuntimeHealth } from "../../shared/api";

type WorkspaceHeaderProps = {
  session: ChatSession | null;
  project: Project | null;
  isConnected: boolean;
  health?: RuntimeHealth | null;
  backtestStatus?: BacktestRunStatus;
};

export function WorkspaceHeader({
  session,
  project,
  isConnected,
  health,
  backtestStatus,
}: WorkspaceHeaderProps) {
  const taskLabel = session?.id ? `TASK-${session.id.slice(0, 4).toUpperCase()}` : "TASK-NEW";
  const isActive = Boolean(backtestStatus) || health?.status === "ok" || isConnected;

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-zinc-200 bg-white px-6">
      <div className="flex min-w-0 items-center gap-3 text-xs">
        <span className="flex shrink-0 items-center gap-1.5 font-bold text-zinc-900">
          <Cpu className="h-4 w-4 text-zinc-700" />
          Codex Execution Engine
        </span>
        <span className="text-zinc-300">|</span>
        <span className="max-w-48 truncate text-zinc-700">{project?.name ?? "未选择项目"}</span>
        <span className="text-zinc-300">|</span>
        <span className="truncate font-mono text-zinc-500">{taskLabel}</span>
      </div>
      <span
        className={`inline-flex items-center gap-1 rounded border px-2 py-0.5 font-mono text-[10px] ${
          isActive
            ? "border-emerald-200 bg-emerald-50 text-emerald-700"
            : "border-red-200 bg-red-50 text-red-700"
        }`}
      >
        <span
          className={`h-1.5 w-1.5 rounded-full ${isActive ? "animate-pulse bg-emerald-500" : "bg-red-500"}`}
        />
        {isActive ? "ACTIVE" : "OFFLINE"}
      </span>
    </header>
  );
}
