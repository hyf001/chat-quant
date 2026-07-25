import {
  Activity,
  BarChart3,
  LineChart,
  Loader2,
  Repeat2,
  ShieldAlert,
  TrendingUp,
  WalletCards,
} from "lucide-react";
import type { ReactNode } from "react";

import type { BacktestDetail, CurvePoint } from "../../shared/types/backtests";

type BacktestResultPanelProps = {
  detail: BacktestDetail;
  isRunning: boolean;
  error: string | null;
  onRunDemo: () => void;
};

type MetricCardProps = {
  label: string;
  value: string;
  tone?: "gain" | "risk" | "neutral";
  icon: ReactNode;
};

export function BacktestResultPanel({
  detail,
  isRunning,
  error,
  onRunDemo,
}: BacktestResultPanelProps) {
  const metrics = detail.result?.metrics;
  const equityCurve = detail.curves.find((curve) => curve.curve_type === "equity");
  const drawdownCurve = detail.curves.find((curve) => curve.curve_type === "drawdown");

  return (
    <section className="grid gap-4" aria-label="回测结果">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="text-xs font-semibold uppercase text-muted">M6 Backtest</div>
          <h2 className="mt-1 truncate text-base font-semibold text-ink">
            沪深300 均线突破回测
          </h2>
        </div>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-lg border border-line bg-panel px-3 text-sm font-semibold text-ink transition hover:border-strong disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          onClick={onRunDemo}
          disabled={isRunning}
        >
          {isRunning ? <Loader2 className="animate-spin" size={16} /> : <Repeat2 size={16} />}
          再次回测
        </button>
      </div>

      {error ? (
        <div className="rounded-lg border border-risk/40 bg-risk/5 px-3 py-2 text-sm text-risk">
          {error}
        </div>
      ) : null}

      <div className="grid gap-3 md:grid-cols-4">
        <MetricCard
          icon={<TrendingUp size={17} />}
          label="年化收益"
          value={formatPercent(metrics?.annual_return_pct)}
          tone="gain"
        />
        <MetricCard
          icon={<ShieldAlert size={17} />}
          label="最大回撤"
          value={formatPercent(metrics?.max_drawdown_pct)}
          tone="risk"
        />
        <MetricCard
          icon={<Activity size={17} />}
          label="夏普比率"
          value={formatNumber(metrics?.sharpe_ratio)}
        />
        <MetricCard
          icon={<WalletCards size={17} />}
          label="交易胜率"
          value={formatPercent(metrics?.win_rate_pct)}
        />
      </div>

      <div className="grid gap-4 2xl:grid-cols-[minmax(0,1fr)_280px]">
        <div className="grid gap-4 md:grid-cols-2">
          <ChartBlock
            title="收益曲线"
            icon={<LineChart size={16} />}
            points={equityCurve?.points ?? []}
            valueKey="normalized_value"
            tone="gain"
          />
          <ChartBlock
            title="回撤曲线"
            icon={<BarChart3 size={16} />}
            points={drawdownCurve?.points ?? []}
            valueKey="value"
            tone="risk"
          />
        </div>

        <div className="rounded-lg border border-line bg-panel p-3">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div className="text-sm font-semibold">交易明细</div>
            <div className="text-xs text-muted">{metrics?.total_trades ?? 0} 笔</div>
          </div>
          <div className="overflow-hidden rounded-lg border border-line">
            <table className="w-full table-fixed border-collapse text-left text-xs">
              <thead className="bg-soft text-muted">
                <tr>
                  <th className="px-2 py-2 font-medium">标的</th>
                  <th className="px-2 py-2 font-medium">方向</th>
                  <th className="px-2 py-2 font-medium">盈亏</th>
                </tr>
              </thead>
              <tbody>
                {detail.trades.slice(0, 4).map((trade) => (
                  <tr className="border-t border-line" key={trade.id}>
                    <td className="truncate px-2 py-2">{trade.symbol}</td>
                    <td className="px-2 py-2">{trade.side === "buy" ? "买入" : "卖出"}</td>
                    <td className={Number(trade.pnl) >= 0 ? "px-2 py-2 text-brand" : "px-2 py-2 text-risk"}>
                      {formatCurrency(trade.pnl)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}

function MetricCard({ label, value, tone = "neutral", icon }: MetricCardProps) {
  const toneClass =
    tone === "gain" ? "text-brand" : tone === "risk" ? "text-risk" : "text-brandBlue";

  return (
    <div className="rounded-lg border border-line bg-panel p-3">
      <div className={`mb-2 inline-flex items-center ${toneClass}`}>{icon}</div>
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 truncate text-xl font-semibold text-ink">{value}</div>
    </div>
  );
}

function ChartBlock({
  title,
  icon,
  points,
  valueKey,
  tone,
}: {
  title: string;
  icon: ReactNode;
  points: CurvePoint[];
  valueKey: "value" | "normalized_value";
  tone: "gain" | "risk";
}) {
  return (
    <div className="rounded-lg border border-line bg-panel p-3">
      <div className="mb-3 flex items-center gap-2 text-sm font-semibold">
        <span className={tone === "gain" ? "text-brand" : "text-risk"}>{icon}</span>
        {title}
      </div>
      <svg className="h-36 w-full overflow-visible" viewBox="0 0 320 120" role="img" aria-label={title}>
        <path d="M0 96H320" className="stroke-line" strokeWidth="1" />
        <path d="M0 56H320" className="stroke-line" strokeWidth="1" />
        <path d="M0 16H320" className="stroke-line" strokeWidth="1" />
        <polyline
          fill="none"
          points={toPolyline(points, valueKey)}
          className={tone === "gain" ? "stroke-brand" : "stroke-risk"}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="3"
        />
      </svg>
    </div>
  );
}

function toPolyline(points: CurvePoint[], valueKey: "value" | "normalized_value") {
  const values = points
    .map((point) => Number(point[valueKey] ?? point.value))
    .filter((value) => Number.isFinite(value));

  if (values.length === 0) {
    return "";
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(1, max - min);
  const lastIndex = Math.max(1, values.length - 1);

  return values
    .map((value, index) => {
      const x = (index / lastIndex) * 320;
      const y = 104 - ((value - min) / span) * 88;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

function formatNumber(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return Number(value).toFixed(2);
}

function formatPercent(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return `${Number(value).toFixed(2)}%`;
}

function formatCurrency(value: string | null) {
  if (value == null) {
    return "--";
  }
  return Number(value).toLocaleString("zh-CN", { maximumFractionDigits: 0 });
}
