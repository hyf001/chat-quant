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
    <header className="glass-panel flex h-14 shrink-0 items-center justify-between gap-4 border-b border-line px-5 lg:px-6">
      <div className="flex min-w-0 items-center gap-3 text-xs">
        <span className="flex shrink-0 items-center gap-2 font-bold text-ink">
          <span
            className={`h-2.5 w-2.5 rounded-full shadow-[0_0_0_6px_rgba(22,132,95,0.12)] ${
              isActive ? "status-breathe bg-brand" : "bg-risk"
            }`}
          />
          <Cpu className="h-4 w-4 text-graphite" />
          Quant Execution Engine
        </span>
        <span className="text-line">/</span>
        <span className="max-w-56 truncate text-mutedText">{project?.name ?? "未选择项目"}</span>
        {project ? (
          <>
            <span className="text-line">/</span>
            <span className="max-w-80 truncate font-mono text-mutedText">{project.local_path}</span>
          </>
        ) : null}
        <span className="text-line">/</span>
        <span className="truncate font-mono text-mutedText">{taskLabel}</span>
      </div>
      <span
        className={`inline-flex h-7 items-center gap-1 rounded-full border px-2.5 font-mono text-[10px] font-bold ${
          isActive
            ? "border-brand/30 bg-gainSoft text-brand"
            : "border-risk/30 bg-riskSoft text-risk"
        }`}
      >
        <span
          className={`h-1.5 w-1.5 rounded-full ${isActive ? "animate-pulse bg-brand" : "bg-risk"}`}
        />
        {isActive ? "ACTIVE" : "OFFLINE"}
      </span>
    </header>
  );
}
