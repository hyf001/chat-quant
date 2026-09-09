import { Loader2 } from "lucide-react";
import {
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";
import {
  getStockPreview,
  type StockPreview,
  type StockPreviewCandle,
  type StockPreviewPeriod,
} from "@/shared/api";
import { LightweightKlineChart } from "@/shared/components/charts";

type StockHoverCardProps = {
  symbol: string;
  children: ReactNode;
  className?: string;
};

const cacheTtlMs = 60_000;
const periods: Array<{ value: StockPreviewPeriod; label: string }> = [
  { value: "daily", label: "日K" },
  { value: "weekly", label: "周K" },
  { value: "monthly", label: "月K" },
];

const previewCache = new Map<string, { data: StockPreview; expiresAt: number }>();
const previewRequests = new Map<string, Promise<StockPreview>>();

export function StockKlineDialog({ symbol, children, className }: StockHoverCardProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [period, setPeriod] = useState<StockPreviewPeriod>("daily");
  const [preview, setPreview] = useState<StockPreview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      return;
    }
    let isCurrent = true;
    const cacheKey = `${symbol.toUpperCase()}::${period}`;
    const cached = previewCache.get(cacheKey);
    if (cached && cached.expiresAt > Date.now()) {
      setPreview(cached.data);
      setError(null);
      return;
    }
    setIsLoading(true);
    setError(null);
    const request =
      previewRequests.get(cacheKey) ??
      getStockPreview(symbol, { period, limit: 180 }).finally(() => {
        previewRequests.delete(cacheKey);
      });
    previewRequests.set(cacheKey, request);
    request
      .then((data) => {
        previewCache.set(cacheKey, { data, expiresAt: Date.now() + cacheTtlMs });
        if (isCurrent) {
          setPreview(data);
        }
      })
      .catch((caught) => {
        if (isCurrent) {
          setPreview(null);
          setError(caught instanceof Error ? caught.message : "行情预览加载失败");
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoading(false);
        }
      });
    return () => {
      isCurrent = false;
    };
  }, [isOpen, period, symbol]);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <button
          className={cn(
            "inline-flex min-w-0 cursor-pointer items-center text-left focus:outline-none focus:ring-2 focus:ring-signal/20",
            className,
          )}
          type="button"
        >
          {children}
        </button>
      </DialogTrigger>
      <DialogContent
        className="max-h-[calc(100vh-2rem)] w-[calc(100vw-2rem)] max-w-[1180px] gap-0 overflow-hidden p-0"
      >
        <DialogTitle className="sr-only">
          {preview ? `${preview.name} ${preview.symbol} K线` : `${symbol} K线`}
        </DialogTitle>
        <DialogDescription className="sr-only">查看股票日K、周K和月K行情。</DialogDescription>
        <StockPreviewPanel
          error={error}
          isLoading={isLoading}
          period={period}
          preview={preview}
          symbol={symbol}
          onPeriodChange={setPeriod}
        />
      </DialogContent>
    </Dialog>
  );
}

export const StockHoverCard = StockKlineDialog;

type StockPreviewPanelProps = {
  error: string | null;
  isLoading: boolean;
  period: StockPreviewPeriod;
  preview: StockPreview | null;
  symbol: string;
  onPeriodChange: (period: StockPreviewPeriod) => void;
};

function StockPreviewPanel({
  error,
  isLoading,
  period,
  preview,
  symbol,
  onPeriodChange,
}: StockPreviewPanelProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const chartHeight = usePreviewChartHeight();
  const activeCandle = useMemo(() => {
    if (!preview || preview.candles.length === 0) {
      return null;
    }
    const fallbackIndex = preview.candles.length - 1;
    const index =
      activeIndex !== null && activeIndex >= 0 && activeIndex < preview.candles.length
        ? activeIndex
        : fallbackIndex;
    const candle = preview.candles[index];
    const previous = index > 0 ? preview.candles[index - 1] : null;
    const change = previous ? candle.close - previous.close : null;
    const pctChange = change !== null && previous?.close ? (change / previous.close) * 100 : null;
    return { candle, change, pctChange };
  }, [activeIndex, preview]);

  useEffect(() => {
    setActiveIndex(null);
  }, [period, preview?.symbol]);

  const trendClass =
    (activeCandle?.change ?? 0) > 0
      ? "text-risk"
      : (activeCandle?.change ?? 0) < 0
        ? "text-brand"
        : "text-mutedText";

  return (
    <div className="bg-panel text-ink">
      <div className="grid gap-3 border-b border-line px-5 py-4 pr-14 md:grid-cols-[190px_minmax(0,1fr)_auto]">
        <div className="min-w-0 self-start">
          <div className="truncate text-lg font-black">{preview?.name ?? "行情预览"}</div>
          <div className="font-mono text-sm text-mutedText">{preview?.symbol ?? symbol}</div>
        </div>
        <div className="min-w-0 self-start">
          <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs font-semibold">
            <span>{activeCandle?.candle.date ?? preview?.trade_date ?? "--"}</span>
            <span>开: {formatNumber(activeCandle?.candle.open, 2)}</span>
            <span>高: {formatNumber(activeCandle?.candle.high, 2)}</span>
            <span>低: {formatNumber(activeCandle?.candle.low, 2)}</span>
            <span>收: {formatNumber(activeCandle?.candle.close, 2)}</span>
            <span className={trendClass}>涨跌: {formatSigned(activeCandle?.change)}</span>
            <span className={trendClass}>涨跌幅: {formatSigned(activeCandle?.pctChange)}%</span>
          </div>
        </div>
        <Tabs
          value={period}
          onValueChange={(value) => onPeriodChange(value as StockPreviewPeriod)}
        >
          <TabsList className="h-8">
            {periods.map((item) => (
              <TabsTrigger key={item.value} className="h-7 px-3 text-xs" value={item.value}>
                {item.label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </div>

      {isLoading ? (
        <div
          className="grid place-items-center text-sm text-mutedText"
          style={{ height: chartHeight }}
        >
          <div className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            加载行情
          </div>
        </div>
      ) : null}

      {!isLoading && error ? (
        <div
          className="grid place-items-center px-6 text-center text-sm text-destructive"
          style={{ height: chartHeight }}
        >
          {error}
        </div>
      ) : null}

      {!isLoading && !error && preview ? (
        <>
          <StockMiniKlineChart
            candles={preview.candles}
            height={chartHeight}
            onActiveIndexChange={setActiveIndex}
          />
          <div className="border-t border-line px-4 py-2 text-[11px] text-mutedText">
            数据源：{preview.source_dataset}
          </div>
        </>
      ) : null}
    </div>
  );
}

function StockMiniKlineChart({
  candles,
  height,
  onActiveIndexChange,
}: {
  candles: StockPreviewCandle[];
  height: number;
  onActiveIndexChange: (index: number | null) => void;
}) {
  return (
    <LightweightKlineChart
      ariaLabel="股票K线预览"
      candles={candles}
      className="w-full"
      enablePriceLineActions
      height={height}
      onActiveCandleChange={(_, index) => onActiveIndexChange(index)}
    />
  );
}

function usePreviewChartHeight() {
  const [height, setHeight] = useState(560);

  useEffect(() => {
    const syncHeight = () => {
      setHeight(Math.min(620, Math.max(420, Math.floor(window.innerHeight - 220))));
    };
    syncHeight();
    window.addEventListener("resize", syncHeight);
    return () => window.removeEventListener("resize", syncHeight);
  }, []);

  return height;
}

function formatNumber(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "--";
  }
  return value.toFixed(digits);
}

function formatSigned(value: number | null | undefined): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "--";
  }
  return `${value > 0 ? "+" : ""}${value.toFixed(2)}`;
}
