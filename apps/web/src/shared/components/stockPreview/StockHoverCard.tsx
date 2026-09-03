import { Loader2 } from "lucide-react";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
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

const openDelayMs = 300;
const closeDelayMs = 120;
const cacheTtlMs = 60_000;
const periods: Array<{ value: StockPreviewPeriod; label: string }> = [
  { value: "daily", label: "日K" },
  { value: "weekly", label: "周K" },
  { value: "monthly", label: "月K" },
];

const previewCache = new Map<string, { data: StockPreview; expiresAt: number }>();
const previewRequests = new Map<string, Promise<StockPreview>>();

export function StockHoverCard({ symbol, children, className }: StockHoverCardProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [period, setPeriod] = useState<StockPreviewPeriod>("daily");
  const [preview, setPreview] = useState<StockPreview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const openTimer = useRef<number | null>(null);
  const closeTimer = useRef<number | null>(null);

  const clearTimers = useCallback(() => {
    if (openTimer.current !== null) {
      window.clearTimeout(openTimer.current);
      openTimer.current = null;
    }
    if (closeTimer.current !== null) {
      window.clearTimeout(closeTimer.current);
      closeTimer.current = null;
    }
  }, []);

  const scheduleOpen = () => {
    if (closeTimer.current !== null) {
      window.clearTimeout(closeTimer.current);
      closeTimer.current = null;
    }
    openTimer.current = window.setTimeout(() => setIsOpen(true), openDelayMs);
  };

  const scheduleClose = () => {
    if (openTimer.current !== null) {
      window.clearTimeout(openTimer.current);
      openTimer.current = null;
    }
    closeTimer.current = window.setTimeout(() => setIsOpen(false), closeDelayMs);
  };

  useEffect(() => clearTimers, [clearTimers]);

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
      getStockPreview(symbol, { period, limit: 120 }).finally(() => {
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
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <span
          className={cn("inline-flex cursor-default", className)}
          onPointerEnter={scheduleOpen}
          onPointerLeave={scheduleClose}
          onFocus={() => setIsOpen(true)}
          onBlur={scheduleClose}
        >
          {children}
        </span>
      </PopoverTrigger>
      <PopoverContent
        align="start"
        className="w-[min(720px,calc(100vw-32px))] overflow-hidden p-0"
        side="right"
        sideOffset={10}
        onPointerEnter={() => {
          if (closeTimer.current !== null) {
            window.clearTimeout(closeTimer.current);
            closeTimer.current = null;
          }
        }}
        onPointerLeave={scheduleClose}
      >
        <StockPreviewPanel
          error={error}
          isLoading={isLoading}
          period={period}
          preview={preview}
          onPeriodChange={setPeriod}
        />
      </PopoverContent>
    </Popover>
  );
}

type StockPreviewPanelProps = {
  error: string | null;
  isLoading: boolean;
  period: StockPreviewPeriod;
  preview: StockPreview | null;
  onPeriodChange: (period: StockPreviewPeriod) => void;
};

function StockPreviewPanel({
  error,
  isLoading,
  period,
  preview,
  onPeriodChange,
}: StockPreviewPanelProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
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
      <div className="grid gap-3 border-b border-line px-4 py-3 md:grid-cols-[150px_minmax(0,1fr)_auto]">
        <div className="min-w-0 self-start">
          <div className="truncate text-lg font-black">{preview?.name ?? "行情预览"}</div>
          <div className="font-mono text-sm text-mutedText">{preview?.symbol ?? ""}</div>
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
        <div className="grid h-[360px] place-items-center text-sm text-mutedText">
          <div className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            加载行情
          </div>
        </div>
      ) : null}

      {!isLoading && error ? (
        <div className="grid h-[360px] place-items-center px-6 text-center text-sm text-destructive">
          {error}
        </div>
      ) : null}

      {!isLoading && !error && preview ? (
        <>
          <StockMiniKlineChart candles={preview.candles} onActiveIndexChange={setActiveIndex} />
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
  onActiveIndexChange,
}: {
  candles: StockPreviewCandle[];
  onActiveIndexChange: (index: number | null) => void;
}) {
  return (
    <LightweightKlineChart
      ariaLabel="股票K线预览"
      candles={candles}
      className="w-full"
      enablePriceLineActions
      height={370}
      onActiveCandleChange={(_, index) => onActiveIndexChange(index)}
    />
  );
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
