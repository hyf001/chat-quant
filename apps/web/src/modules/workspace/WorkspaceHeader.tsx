import { Activity, WifiOff } from "lucide-react";

import type { BacktestRunStatus, ChatSession, RuntimeHealth } from "../../shared/api";
import { StatusPill } from "../../shared/components";

type WorkspaceHeaderProps = {
  session: ChatSession | null;
  isConnected: boolean;
  health?: RuntimeHealth | null;
  backtestStatus?: BacktestRunStatus;
};

export function WorkspaceHeader({
  session,
  isConnected,
  health,
  backtestStatus,
}: WorkspaceHeaderProps) {
  const runtimeLabel = health?.status === "ok" ? "M4 已连接" : null;
  const backtestLabel = backtestStatus ? `M6 ${backtestStatus}` : null;
  const statusLabel = backtestLabel ?? runtimeLabel ?? (isConnected ? "M1 已连接" : "连接异常");

  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">{session?.title ?? "Chat-Quant 工作台"}</h1>
        <p className="mt-1 truncate text-xs text-muted">
          {session?.data_scope_label ?? session?.kind ?? "会话、消息、运行、回测和资产上下文"}
        </p>
      </div>
      <StatusPill
        icon={isConnected || runtimeLabel || backtestLabel ? <Activity size={14} /> : <WifiOff size={14} />}
        label={statusLabel}
      />
    </header>
  );
}
