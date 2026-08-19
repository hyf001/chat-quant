import {
  Activity,
  BarChart3,
  LineChart,
  ShieldAlert,
  TrendingUp,
  WalletCards,
} from "lucide-react";
import type { ReactNode } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import type { BacktestDetail, CurvePoint } from "../../shared/types/backtests";

type BacktestResultPanelProps = {
  detail: BacktestDetail | null;
  error: string | null;
};

type MetricCardProps = {
  label: string;
  value: string;
  tone?: "gain" | "risk" | "neutral";
  icon: ReactNode;
};

export function BacktestResultPanel({
  detail,
  error,
}: BacktestResultPanelProps) {
  const metrics = detail?.result?.metrics;
  const equityCurve = detail?.curves.find((curve) => curve.curve_type === "equity");
  const drawdownCurve = detail?.curves.find((curve) => curve.curve_type === "drawdown");

  return (
    <section className="grid gap-4" aria-label="回测结果">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="text-xs font-semibold uppercase text-mutedText">M6 Backtest</div>
          <h2 className="mt-1 truncate text-base font-semibold text-ink">{backtestTitle(detail)}</h2>
        </div>
      </div>

      {error ? (
        <div className="rounded-lg border border-destructive/40 bg-destructive/5 px-3 py-2 text-sm text-destructive">
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

      {detail ? (
        <div className="grid gap-4 2xl:grid-cols-[minmax(0,1fr)_280px]">
          <div className="grid gap-4 md:grid-cols-2">
            {equityCurve ? (
              <ChartBlock
                title="收益曲线"
                icon={<LineChart size={16} />}
                points={equityCurve.points}
                valueKey="normalized_value"
                tone="gain"
              />
            ) : null}
            {drawdownCurve ? (
              <ChartBlock
                title="回撤曲线"
                icon={<BarChart3 size={16} />}
                points={drawdownCurve.points}
                valueKey="value"
                tone="risk"
              />
            ) : null}
          </div>

          <Card>
            <CardHeader className="flex-row items-center justify-between gap-3 p-3">
              <CardTitle className="text-sm">交易明细</CardTitle>
              <div className="text-xs text-mutedText">{metrics?.total_trades ?? 0} 笔</div>
            </CardHeader>
            <CardContent className="p-3 pt-0">
              <div className="overflow-hidden rounded-lg border border-line">
                <Table className="table-fixed text-xs">
                  <TableHeader className="bg-soft text-mutedText">
                    <TableRow>
                      <TableHead>标的</TableHead>
                      <TableHead>方向</TableHead>
                      <TableHead>盈亏</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {detail.trades.slice(0, 4).map((trade) => (
                      <TableRow key={trade.id}>
                        <TableCell className="truncate">{trade.symbol}</TableCell>
                        <TableCell>{trade.side === "buy" ? "买入" : "卖出"}</TableCell>
                        <TableCell className={Number(trade.pnl) >= 0 ? "text-brand" : "text-risk"}>
                          {formatCurrency(trade.pnl)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              {detail.trades.length === 0 ? (
                <div className="mt-3 rounded-lg border border-dashed border-line bg-soft p-3 text-xs text-mutedText">
                  暂无交易明细
                </div>
              ) : null}
            </CardContent>
          </Card>
        </div>
      ) : null}
    </section>
  );
}

function backtestTitle(detail: BacktestDetail | null): string {
  if (!detail) {
    return "暂无回测结果";
  }
  const symbols = detail.run.config.symbols.join("、");
  const dateRange = `${detail.run.config.start_date} 至 ${detail.run.config.end_date}`;
  return `${symbols || detail.run.strategy_version_id} · ${dateRange}`;
}

function MetricCard({ label, value, tone = "neutral", icon }: MetricCardProps) {
  const toneClass =
    tone === "gain" ? "text-brand" : tone === "risk" ? "text-risk" : "text-brandBlue";

  return (
    <Card className="p-3">
      <div className={`mb-2 inline-flex items-center ${toneClass}`}>{icon}</div>
      <div className="text-xs text-mutedText">{label}</div>
      <div className="mt-1 truncate text-xl font-semibold text-ink">{value}</div>
    </Card>
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
    <Card className="p-3">
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
    </Card>
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
