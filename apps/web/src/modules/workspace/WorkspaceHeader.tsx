import { Activity, WifiOff } from "lucide-react";

import { StatusPill } from "../../shared/components";
import type { ChatSession } from "../../shared/api";

type WorkspaceHeaderProps = {
  session: ChatSession | null;
  isConnected: boolean;
};

export function WorkspaceHeader({ session, isConnected }: WorkspaceHeaderProps) {
  return (
    <header className="flex min-h-16 items-center justify-between gap-4 border-b border-line bg-panel/80 px-5">
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold">{session?.title ?? "Chat-Quant 工作台"}</h1>
        <p className="mt-1 truncate text-xs text-muted">
          {session?.data_scope_label ?? session?.kind ?? "会话、消息和资产上下文"}
        </p>
      </div>
      <StatusPill
        icon={isConnected ? <Activity size={14} /> : <WifiOff size={14} />}
        label={isConnected ? "M1 已连接" : "连接异常"}
      />
    </header>
  );
}
