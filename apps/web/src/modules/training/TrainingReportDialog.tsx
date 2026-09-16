import { useMemo } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { formatMoney, signed } from "./TrainingStatsBar";
import type { TrainingReportResponse } from "./types";

type TrainingReportDialogProps = {
  open: boolean;
  report: TrainingReportResponse | null;
  onClose: () => void;
  onRestart: () => void;
};

export function TrainingReportDialog({
  open,
  report,
  onClose,
  onRestart,
}: TrainingReportDialogProps) {
  const equityPath = useMemo(
    () => sparkPath(report?.report.equity_curve.points.map((point) => Number(point.value)) ?? []),
    [report],
  );
  const drawdownPath = useMemo(
    () => sparkPath(report?.report.drawdown_curve.points.map((point) => Number(point.value)) ?? []),
    [report],
  );

  if (!report) {
    return null;
  }

  const metrics = report.report.metrics;
  const instrumentLabel = report.instrument.name
    ? `${report.instrument.name}（${report.instrument.symbol}）`
    : report.instrument.symbol;

  return (
    <Dialog open={open} onOpenChange={(next) => (next ? undefined : onClose())}>
      <DialogContent className="max-h-[85vh] max-w-3xl overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            揭晓：{instrumentLabel}
            <Badge className="ml-2" variant="secondary">
              {report.window.start_date} ~ {report.window.end_date}
            </Badge>
          </DialogTitle>
          <DialogDescription>
            持仓按最后一根 close 计市值，收局不强制平仓；{metrics.settlement_note}
          </DialogDescription>
        </DialogHeader>

        <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          <Metric label="本局收益" value={`${signed(metrics.total_return_pct)}%`} />
          <Metric label="期末权益" value={formatMoney(metrics.final_value)} />
          <Metric label="开仓收益" value={`${signed(metrics.open_return_pct)}%`} />
          <Metric label="最大回撤" value={`${metrics.max_drawdown_pct}%`} />
          <Metric label="已实现盈亏" value={formatMoney(metrics.realized_pnl)} />
          <Metric label="浮动盈亏" value={formatMoney(metrics.unrealized_pnl)} />
          <Metric
            label="胜率"
            value={metrics.win_rate_pct === null ? "—" : `${metrics.win_rate_pct}%`}
          />
          <Metric label="平仓次数" value={String(metrics.total_trades)} />
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <CurveCard title="收益曲线" path={equityPath} tone="#2563eb" />
          <CurveCard title="回撤曲线" path={drawdownPath} tone="#16a34a" />
        </div>

        <section className="space-y-2">
          <h3 className="text-sm font-medium text-ink">逐笔成交</h3>
          {report.report.fills.length === 0 ? (
            <p className="text-xs text-ink-muted">本局没有成交。</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>序号</TableHead>
                  <TableHead>方向</TableHead>
                  <TableHead>价格</TableHead>
                  <TableHead>数量</TableHead>
                  <TableHead>金额</TableHead>
                  <TableHead>佣金</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {report.report.fills.map((fill) => (
                  <TableRow key={`${fill.i}-${fill.side}-${fill.price}`}>
                    <TableCell>第 {fill.i + 1} 根</TableCell>
                    <TableCell>{fill.side === "buy" ? "买入" : "卖出"}</TableCell>
                    <TableCell>{fill.price}</TableCell>
                    <TableCell>{fill.size}</TableCell>
                    <TableCell>{fill.value}</TableCell>
                    <TableCell>{fill.commission}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </section>

        <section className="space-y-2">
          <h3 className="text-sm font-medium text-ink">已平仓交易</h3>
          {report.report.closed_trades.length === 0 ? (
            <p className="text-xs text-ink-muted">本局没有平仓交易（一路持有或一直观望）。</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>日期</TableHead>
                  <TableHead>价格</TableHead>
                  <TableHead>数量</TableHead>
                  <TableHead>盈亏</TableHead>
                  <TableHead>收益率</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {report.report.closed_trades.map((trade, index) => (
                  <TableRow key={`${trade.date}-${index}`}>
                    <TableCell>{trade.date}</TableCell>
                    <TableCell>{trade.price}</TableCell>
                    <TableCell>{trade.size}</TableCell>
                    <TableCell>{trade.pnl}</TableCell>
                    <TableCell>{trade.pnl_pct === null ? "—" : `${trade.pnl_pct}%`}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </section>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            关闭
          </Button>
          <Button onClick={onRestart}>再来一局</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-panel/60 px-3 py-2">
      <div className="text-[11px] text-ink-muted">{label}</div>
      <div className="text-sm font-medium text-ink">{value}</div>
    </div>
  );
}

function CurveCard({ title, path, tone }: { title: string; path: string; tone: string }) {
  return (
    <div className="rounded-md border border-line bg-panel/60 p-3">
      <div className="mb-2 text-xs text-ink-muted">{title}</div>
      {path ? (
        <svg viewBox="0 0 100 32" preserveAspectRatio="none" className="h-20 w-full">
          <path d={path} fill="none" stroke={tone} strokeWidth={1.2} />
        </svg>
      ) : (
        <div className="text-xs text-ink-muted">没有曲线数据</div>
      )}
    </div>
  );
}

function sparkPath(values: number[]): string {
  if (values.length < 2) {
    return "";
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  return values
    .map((value, index) => {
      const x = (index / (values.length - 1)) * 100;
      const y = 30 - ((value - min) / span) * 28;
      return `${index === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");
}
