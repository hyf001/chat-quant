import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import { formatMoney, formatPercent } from "./TrainingStatsBar";
import { POSITION_RATIOS, type TrainingPositionRatio } from "./types";

type TrainingOrderPanelProps = {
  cash: string;
  positionSize: number;
  positionValue: string;
  positionPrice: string;
  positionPct: string;
  buyRatio: TrainingPositionRatio;
  sellRatio: TrainingPositionRatio;
  disabled: boolean;
  remaining: number;
  onBuyRatioChange: (ratio: TrainingPositionRatio) => void;
  onSellRatioChange: (ratio: TrainingPositionRatio) => void;
  onAction: (action: "buy" | "sell" | "hold") => void;
  onFinish: () => void;
};

export function TrainingOrderPanel({
  cash,
  positionSize,
  positionValue,
  positionPrice,
  positionPct,
  buyRatio,
  sellRatio,
  disabled,
  remaining,
  onBuyRatioChange,
  onSellRatioChange,
  onAction,
  onFinish,
}: TrainingOrderPanelProps) {
  const exhausted = remaining <= 0;
  // 下单按本根 close 成交，成交与结算在同一响应里：账户就是 broker 的实时值。
  // 有持仓才能卖、有剩余资金才能买。
  const hasPosition = positionSize > 0;
  const hasCash = Number(cash) > 0;
  const buyDisabled = disabled || exhausted || !hasCash;
  const sellDisabled = disabled || exhausted || !hasPosition;

  return (
    <div className="space-y-3 rounded-md border border-line bg-panel/60 p-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
        <span className="text-ink-muted">
          可用资金 <span className="font-medium text-ink">{formatMoney(cash)}</span>
        </span>
        <span className="text-ink-muted">
          持仓{" "}
          <span className={cn("font-medium", hasPosition ? "text-ink" : "text-ink-muted")}>
            {formatShares(positionSize)} 股
          </span>
          {hasPosition ? (
            <span className="ml-1 text-ink-muted">
              · 市值 {formatMoney(positionValue)} · 均价 {formatMoney(positionPrice)} · 占比{" "}
              {formatPercent(positionPct)}
            </span>
          ) : null}
        </span>
        <span className="ml-auto text-ink-muted">剩余 {remaining} 根</span>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            className="bg-risk text-white hover:bg-risk/90"
            disabled={buyDisabled}
            onClick={() => onAction("buy")}
          >
            买入（B）
          </Button>
          <RatioGroup
            label="买入档位"
            tone="buy"
            value={buyRatio}
            disabled={disabled}
            onChange={onBuyRatioChange}
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            className="bg-brandBlue text-white hover:bg-brandBlue/90"
            disabled={sellDisabled}
            onClick={() => onAction("sell")}
          >
            卖出（S）
          </Button>
          <RatioGroup
            label="卖出档位"
            tone="sell"
            value={sellRatio}
            disabled={disabled}
            onChange={onSellRatioChange}
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            disabled={disabled || exhausted}
            onClick={() => onAction("hold")}
          >
            观望 / 下一根（空格）
          </Button>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button size="sm" variant="ghost" disabled={disabled}>
                提前结束
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>提前结束这一局？</AlertDialogTitle>
                <AlertDialogDescription>
                  收局后不能再揭示 K 线，会直接进入复盘。
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>继续训练</AlertDialogCancel>
                <AlertDialogAction onClick={onFinish}>提前结束</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      {exhausted ? (
        <p className="text-xs text-mutedText">训练段已走完，本局会自动收局。</p>
      ) : null}
    </div>
  );
}

function RatioGroup({
  label,
  tone,
  value,
  disabled,
  onChange,
}: {
  label: string;
  tone: "buy" | "sell";
  value: TrainingPositionRatio;
  disabled: boolean;
  onChange: (ratio: TrainingPositionRatio) => void;
}) {
  // 选中的档位跟它对应的按钮同色：买入红、卖出蓝
  const activeClass = tone === "buy" ? "bg-risk text-white" : "bg-brandBlue text-white";

  return (
    <div className="flex items-center gap-1" role="group" aria-label={label}>
      <div className="flex overflow-hidden rounded-md border border-line">
        {POSITION_RATIOS.map((item) => (
          <button
            key={item.value}
            type="button"
            aria-pressed={value === item.value}
            disabled={disabled}
            className={cn(
              "px-2 py-1 text-xs transition-colors disabled:opacity-50",
              value === item.value ? activeClass : "bg-transparent text-ink hover:bg-panel",
            )}
            onClick={() => onChange(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </div>
  );
}

function formatShares(value: number): string {
  return value.toLocaleString("zh-CN", { maximumFractionDigits: 2 });
}
