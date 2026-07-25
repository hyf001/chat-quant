import type { AssetLink, ChatSession, JsonValue } from "../../shared/api/types";

type InsightPanelProps = {
  session: ChatSession | null;
  assets: AssetLink[];
};

function snapshotTitle(snapshot: JsonValue | null): string | null {
  if (snapshot && typeof snapshot === "object" && !Array.isArray(snapshot)) {
    const title = snapshot.title;
    return typeof title === "string" ? title : null;
  }
  return null;
}

export function InsightPanel({ session, assets }: InsightPanelProps) {
  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      <div className="grid gap-3">
        <section className="rounded-lg border border-line bg-soft p-4">
          <div className="text-xs font-semibold text-muted">当前会话</div>
          <div className="mt-2 truncate text-sm font-semibold">
            {session?.title ?? "未选择会话"}
          </div>
          <div className="mt-2 grid gap-1 text-xs text-muted">
            <div>SDK Session: {session?.sdk_session_id ?? "未建立"}</div>
            <div>策略版本: {session?.current_strategy_version_id ?? "无"}</div>
            <div>回测结果: {session?.current_backtest_run_id ?? "无"}</div>
          </div>
        </section>

        <section className="rounded-lg border border-line bg-soft p-4">
          <div className="text-xs font-semibold text-muted">关联资产</div>
          <div className="mt-3 grid gap-2">
            {assets.length === 0 ? (
              <div className="text-sm text-muted">暂无资产</div>
            ) : (
              assets.map((asset) => (
                <div className="rounded-lg border border-line bg-panel p-3" key={asset.id}>
                  <div className="truncate text-sm font-medium">
                    {snapshotTitle(asset.display_snapshot) ?? asset.asset_id}
                  </div>
                  <div className="mt-1 text-xs text-muted">
                    {asset.asset_type} · {asset.relation_type}
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </aside>
  );
}
