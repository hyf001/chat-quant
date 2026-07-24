import { Activity } from "lucide-react";

import { StatusPill } from "../../shared/components";

export function WorkspaceHeader() {
  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">Chat-Quant 工作台</h1>
        <p className="mt-1 truncate text-xs text-muted">历史会话、对话线程和对象详情的前端框架</p>
      </div>
      <StatusPill icon={<Activity size={14} />} label="API 待接入" />
    </header>
  );
}
