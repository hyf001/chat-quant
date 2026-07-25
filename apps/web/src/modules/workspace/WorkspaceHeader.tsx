import { Activity } from "lucide-react";

import { StatusPill } from "../../shared/components";
import type { ChatSessionSummary } from "../../shared/types/agentRuntime";

type WorkspaceHeaderProps = {
  status: ChatSessionSummary["status"];
  sdkSessionId: string | null;
};

export function WorkspaceHeader({ status, sdkSessionId }: WorkspaceHeaderProps) {
  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">Chat-Quant 工作台</h1>
        <p className="mt-1 truncate text-xs text-muted">
          {sdkSessionId ? `SDK ${sdkSessionId}` : "M2 Claude Agent Runtime"}
        </p>
      </div>
      <StatusPill icon={<Activity size={14} />} label={statusText[status]} />
    </header>
  );
}

const statusText: Record<ChatSessionSummary["status"], string> = {
  idle: "等待输入",
  running: "运行中",
  completed: "已完成",
  failed: "请求失败",
};
