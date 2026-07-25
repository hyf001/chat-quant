import { Activity } from "lucide-react";

import { StatusPill } from "../../shared/components";
import type { RuntimeHealth } from "../../shared/api";

type WorkspaceHeaderProps = {
  health: RuntimeHealth | null;
};

export function WorkspaceHeader({ health }: WorkspaceHeaderProps) {
  const statusLabel = health?.status === "ok" ? "M4 已连接" : "M4 检查中";

  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">Chat-Quant 工作台</h1>
        <p className="mt-1 truncate text-xs text-muted">策略分析、Python 执行和运行产物</p>
      </div>
      <StatusPill icon={<Activity size={14} />} label={statusLabel} />
    </header>
  );
}
