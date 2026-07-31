import {
  type BacktestDetail,
  type ExecutionResult,
  type RuntimeHealth,
} from "../../shared/api";
import type { AssetLink, ChatSession, JsonValue } from "../../shared/api/types";

type InsightPanelProps = {
  session: ChatSession | null;
  assets: AssetLink[];
  health: RuntimeHealth | null;
  result: ExecutionResult | null;
  backtestDetail: BacktestDetail | null;
};

const formatter = new Intl.DateTimeFormat("zh-CN", {
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});

function snapshotTitle(snapshot: JsonValue | null): string | null {
  if (snapshot && typeof snapshot === "object" && !Array.isArray(snapshot)) {
    const title = snapshot.title;
    return typeof title === "string" ? title : null;
  }
  return null;
}

export function InsightPanel({
  session,
  assets,
  health,
  result,
  backtestDetail,
}: InsightPanelProps) {
  return (
    <aside
      className="hidden min-h-0 overflow-auto border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      {result ? (
        <RuntimeDetail health={health} result={result} />
      ) : backtestDetail ? (
        <BacktestDetailCard detail={backtestDetail} />
      ) : (
        <SessionDetail assets={assets} session={session} />
      )}
    </aside>
  );
}

function RuntimeDetail({ health, result }: { health: RuntimeHealth | null; result: ExecutionResult }) {
  return (
    <div className="grid gap-3">
      <DetailCard label="运行 ID" value={result.run_id} />
      <DetailCard label="Python" value={health?.python_version ?? result.python_version} />
      <DetailCard label="exit code" value={result.exit_code === null ? "-" : String(result.exit_code)} />
      <DetailCard label="输出目录" value={result.output_dir} />
    </div>
  );
}

function BacktestDetailCard({ detail }: { detail: BacktestDetail }) {
  const metrics = detail.result?.metrics;
  return (
    <div className="grid gap-3">
      <DetailCard label="回测 ID" value={detail.run.id} />
      <DetailCard label="状态" value={detail.run.status} />
      <DetailCard label="年化收益" value={metrics?.annual_return_pct ? `${metrics.annual_return_pct}%` : "-"} />
      <DetailCard label="最大回撤" value={metrics?.max_drawdown_pct ? `${metrics.max_drawdown_pct}%` : "-"} />
    </div>
  );
}

function SessionDetail({ session, assets }: { session: ChatSession | null; assets: AssetLink[] }) {
  return (
    <div className="grid gap-3">
      <section className="rounded-lg border border-line bg-soft p-4">
        <div className="text-xs font-semibold text-muted">当前会话</div>
        <div className="mt-2 truncate text-sm font-semibold">{session?.title ?? "未选择会话"}</div>
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
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1">
      <dt className="text-muted">{label}</dt>
      <dd className="break-all font-medium text-ink">{value}</dd>
    </div>
  );
}

function DetailCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-line bg-soft p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 truncate text-xs font-semibold">{value}</div>
    </div>
  );
}
