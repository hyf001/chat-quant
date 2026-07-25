import type { SDKStreamEnvelope, ToolCallView } from "../../shared/types/agentRuntime";

type InsightPanelProps = {
  envelope: SDKStreamEnvelope | null;
  tools: ToolCallView[];
};

export function InsightPanel({ envelope, tools }: InsightPanelProps) {
  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      <div className="grid gap-3">
        <div className="rounded-lg border border-line bg-soft p-3 text-sm">
          <div className="text-xs font-semibold text-muted">SDK Session</div>
          <div className="mt-1 truncate font-mono text-xs">
            {envelope?.sdk_session_id ?? "等待会话创建"}
          </div>
        </div>
        <div className="rounded-lg border border-line bg-soft p-3 text-sm">
          <div className="text-xs font-semibold text-muted">最近事件</div>
          <div className="mt-1 font-mono text-xs">{String(envelope?.sdk_event.type ?? "idle")}</div>
          <div className="mt-1 text-xs text-muted">sequence {envelope?.sequence ?? 0}</div>
        </div>
        <div className="rounded-lg border border-line bg-soft p-3 text-sm">
          <div className="text-xs font-semibold text-muted">工具调用数</div>
          <div className="mt-1 text-2xl font-semibold">{tools.length}</div>
        </div>
      </div>
    </aside>
  );
}
