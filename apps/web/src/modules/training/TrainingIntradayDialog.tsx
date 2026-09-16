import { useEffect, useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  TrainingApiError,
  getTrainingIntraday,
  type TrainingIntraday,
} from "@/shared/api/training";
import { EmptyState, LoadingState } from "@/shared/components";
import { IntradayChart, formatVolume } from "@/shared/components/charts";

import { formatMoney } from "./TrainingStatsBar";

type TrainingIntradayDialogProps = {
  open: boolean;
  sessionId: string;
  /** 双击的那一根日线的序号（与 K 线的 ``i`` 一致）；关闭时为 null。 */
  seq: number | null;
  onClose: () => void;
};

/**
 * 双击日线弹出的当日分时。
 *
 * 标题里的"第 N 根"与 K 线 X 轴同一套序号：分时数据里的真实日期不下发，页面上也没有
 * 能反推日历的字段。只能看**已揭示**的根，服务端会拒掉更靠后的请求。
 */
export function TrainingIntradayDialog({
  open,
  sessionId,
  seq,
  onClose,
}: TrainingIntradayDialogProps) {
  const [data, setData] = useState<TrainingIntraday | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!open || seq === null) {
      return undefined;
    }
    let cancelled = false;
    setData(null);
    setError(null);
    setIsLoading(true);
    getTrainingIntraday(sessionId, seq)
      .then((payload) => {
        if (!cancelled) {
          setData(payload);
        }
      })
      .catch((caught: unknown) => {
        if (!cancelled) {
          setError(
            caught instanceof TrainingApiError ? caught.message : "分时加载失败，请重试",
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [open, seq, sessionId]);

  const bar = data?.bar ?? null;
  const prevClose = data?.prev_close == null ? null : Number(data.prev_close);
  const basePrice = prevClose ?? bar?.o ?? null;
  const closeChange = bar && basePrice ? (bar.c / basePrice - 1) * 100 : null;

  return (
    <Dialog open={open} onOpenChange={(next) => (next ? undefined : onClose())}>
      <DialogContent className="max-h-[calc(100vh-2rem)] w-[calc(100vw-2rem)] max-w-3xl gap-0 overflow-y-auto p-0">
        <DialogHeader className="border-b border-line px-4 py-3 pr-12">
          <DialogTitle>
            第 {seq === null ? "—" : seq + 1} 根 · 当日分时
          </DialogTitle>
          <DialogDescription>
            双击的那一根日线的日内分钟走势；只有已揭示的根可以看，收盘价成交口径不变。
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-3 px-4 py-3">
          {isLoading ? <LoadingState title="正在加载分时" rows={2} /> : null}

          {error ? <EmptyState title="分时加载失败" description={error} /> : null}

          {!isLoading && !error && bar ? (
            <>
              <div className="grid grid-cols-3 gap-2 sm:grid-cols-5">
                <Stat label="开" value={bar.o.toFixed(2)} />
                <Stat label="高" value={bar.h.toFixed(2)} />
                <Stat label="低" value={bar.l.toFixed(2)} />
                <Stat
                  label="收"
                  value={bar.c.toFixed(2)}
                  tone={closeChange === null ? undefined : changeTone(closeChange)}
                />
                <Stat label="成交量" value={formatVolume(bar.v)} />
              </div>

              {data?.available && basePrice !== null ? (
                <IntradayChart
                  points={data.points}
                  basePrice={basePrice}
                  height={320}
                  ariaLabel={`第 ${(seq ?? 0) + 1} 根 当日分时`}
                />
              ) : (
                <EmptyState
                  title="这一天没有分时数据"
                  description="分钟行情只同步了最近若干个交易日，窗口里更早的日线拿不到分时；换最近几根试试。"
                />
              )}

              {data?.available ? (
                <p className="text-xs text-mutedText">
                  {prevClose === null
                    ? "基准用这一根的开盘价（切片里没有更早的一根）。"
                    : `基准（昨收）${formatMoney(prevClose)}，虚线位置即基准。`}
                  均价线按分钟成交量加权近似。
                </p>
              ) : null}
            </>
          ) : null}
        </div>
      </DialogContent>
    </Dialog>
  );
}

function Stat({
  label,
  value,
  tone = "text-ink",
}: {
  label: string;
  value: string;
  tone?: string;
}) {
  return (
    <div className="rounded-md border border-line bg-panel/60 px-3 py-2">
      <div className="text-[11px] text-mutedText">{label}</div>
      <div className={`text-sm font-medium ${tone}`}>{value}</div>
    </div>
  );
}

function changeTone(value: number): string {
  if (value > 0) {
    return "text-[#e11d48]";
  }
  if (value < 0) {
    return "text-[#16a34a]";
  }
  return "text-ink";
}
