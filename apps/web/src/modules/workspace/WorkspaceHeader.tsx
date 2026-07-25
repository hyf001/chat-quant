import { Activity } from "lucide-react";

import { StatusPill } from "../../shared/components";
import type { BacktestRunStatus } from "../../shared/types/backtests";

type WorkspaceHeaderProps = {
  status: BacktestRunStatus;
};

export function WorkspaceHeader({ status }: WorkspaceHeaderProps) {
  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">沪深300 均线突破回测</h1>
        <p className="mt-1 truncate text-xs text-muted">数据口径：延迟行情 + 历史日线</p>
      </div>
      <StatusPill icon={<Activity size={14} />} label={`M6 ${status}`} />
    </header>
  );
}
