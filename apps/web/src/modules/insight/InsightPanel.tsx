import type { BacktestDetail } from "../../shared/types/backtests";

type InsightPanelProps = {
  detail: BacktestDetail;
};

export function InsightPanel({ detail }: InsightPanelProps) {
  const config = detail.run.config;
  const metrics = detail.result?.metrics;

  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-4">
        <div className="text-sm font-semibold">对象详情</div>
        <div className="mt-1 truncate text-xs text-muted">{detail.run.id}</div>
      </div>

      <div className="grid gap-3">
        <section className="rounded-lg border border-line bg-panel p-3">
          <div className="mb-3 text-xs font-semibold text-muted">参数快照</div>
          <DetailRow label="市场" value={config.market} />
          <DetailRow label="标的" value={config.symbols.join(", ")} />
          <DetailRow label="周期" value={`${config.start_date} 至 ${config.end_date}`} />
          <DetailRow label="初始资金" value={`${Number(config.initial_cash).toLocaleString("zh-CN")} ${config.currency}`} />
          <DetailRow label="手续费" value={config.commission} />
          <DetailRow label="滑点" value={config.slippage} />
        </section>

        <section className="rounded-lg border border-line bg-panel p-3">
          <div className="mb-3 text-xs font-semibold text-muted">风险口径</div>
          <DetailRow label="最大回撤区间" value={formatRange(metrics?.max_drawdown_start, metrics?.max_drawdown_end)} />
          <DetailRow label="年化波动" value={formatPercent(metrics?.volatility_annual_pct)} />
          <DetailRow label="Calmar" value={formatNumber(metrics?.calmar_ratio)} />
          <DetailRow label="交易次数" value={`${metrics?.total_trades ?? 0}`} />
        </section>

        <section className="rounded-lg border border-line bg-panel p-3">
          <div className="mb-3 text-xs font-semibold text-muted">资产引用</div>
          <DetailRow label="配置 Hash" value={detail.run.config_hash.replace("sha256:", "").slice(0, 12)} />
          <DetailRow label="策略版本" value={detail.run.strategy_version_id} />
          <DetailRow label="代码产物" value={detail.run.code_artifact_id} />
        </section>
      </div>
    </aside>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-3 border-t border-line py-2 first:border-t-0 first:pt-0 last:pb-0">
      <div className="shrink-0 text-xs text-muted">{label}</div>
      <div className="min-w-0 text-right text-xs font-medium text-ink">{value}</div>
    </div>
  );
}

function formatRange(start: string | null | undefined, end: string | null | undefined) {
  if (!start || !end) {
    return "--";
  }
  return `${start} 至 ${end}`;
}

function formatPercent(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return `${Number(value).toFixed(2)}%`;
}

function formatNumber(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return Number(value).toFixed(2);
}
