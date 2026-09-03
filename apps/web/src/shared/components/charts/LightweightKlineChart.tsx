import {
  CandlestickSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineSeries,
  LineStyle,
  createChart,
  createSeriesMarkers,
  type CandlestickData,
  type HistogramData,
  type IPriceLine,
  type ISeriesApi,
  type LineData,
  type MouseEventParams,
  type SeriesMarker,
  type Time,
} from "lightweight-charts";
import { Plus, X } from "lucide-react";
import type { PointerEvent as ReactPointerEvent } from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

export type LightweightKlineCandle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number | null;
  ma5?: number | null;
  ma10?: number | null;
  ma20?: number | null;
  ma60?: number | null;
};

export type LightweightKlineMarker = {
  date: string;
  side: "buy" | "sell";
  text?: string;
};

export type LightweightKlinePriceLineKind = "price";

export type LightweightKlinePriceLine = {
  id: string;
  price: number;
  title?: string;
  kind?: LightweightKlinePriceLineKind;
  color?: string;
};

type LightweightKlineChartProps = {
  candles: LightweightKlineCandle[];
  markers?: LightweightKlineMarker[];
  priceLines?: LightweightKlinePriceLine[];
  defaultPriceLines?: LightweightKlinePriceLine[];
  height: number;
  ariaLabel: string;
  className?: string;
  enablePriceLineActions?: boolean;
  showVolume?: boolean;
  showMovingAverages?: boolean;
  onActiveCandleChange?: (candle: LightweightKlineCandle | null, index: number | null) => void;
  onPriceLinesChange?: (priceLines: LightweightKlinePriceLine[]) => void;
};

const upColor = "#e11d48";
const downColor = "#16a34a";
const lineColors = {
  ma5: "#7c3aed",
  ma10: "#2563eb",
  ma20: "#d97706",
  ma60: "#64748b",
};
const emptyMarkers: LightweightKlineMarker[] = [];
const emptyPriceLines: LightweightKlinePriceLine[] = [];
const customLineNameValue = "__custom__";
const defaultLineName = "价格线";
const presetLineNames = ["价格线", "支撑线", "压力线", "止损线", "止盈线", "买入线", "卖出线", "观察线"];

export function LightweightKlineChart({
  candles,
  markers = emptyMarkers,
  priceLines,
  defaultPriceLines = emptyPriceLines,
  height,
  ariaLabel,
  className,
  enablePriceLineActions = false,
  showVolume = true,
  showMovingAverages = true,
  onActiveCandleChange,
  onPriceLinesChange,
}: LightweightKlineChartProps) {
  const chartRef = useRef<HTMLDivElement | null>(null);
  const activePriceRef = useRef<number | null>(null);
  const activeCandleChangeRef = useRef(onActiveCandleChange);
  const activePriceLinesRef = useRef<LightweightKlinePriceLine[]>([]);
  const candleSeriesRef = useRef<ISeriesApi<"Candlestick", Time> | null>(null);
  const priceLineRefs = useRef<IPriceLine[]>([]);
  const refreshLinePositionsRef = useRef<() => void>(() => undefined);
  const coordinateToPriceRef = useRef<(coordinate: number) => number | null>(() => null);
  const suppressNextClickRef = useRef(false);
  const linePointerStartRef = useRef<{
    id: string;
    clientX: number;
    clientY: number;
    moved: boolean;
  } | null>(null);
  const [internalPriceLines, setInternalPriceLines] =
    useState<LightweightKlinePriceLine[]>(defaultPriceLines);
  const [actionMenu, setActionMenu] = useState<{
    x: number;
    y: number;
    price: number;
    lineId?: string;
  } | null>(null);
  const [lineNameSelection, setLineNameSelection] = useState(defaultLineName);
  const [customLineName, setCustomLineName] = useState("");
  const [draggingLineId, setDraggingLineId] = useState<string | null>(null);
  const [linePositions, setLinePositions] = useState<Array<{ id: string; y: number }>>([]);
  const chartData = useMemo(() => toLightweightData(candles), [candles]);
  const chartMarkers = useMemo(() => toLightweightMarkers(markers), [markers]);
  const activePriceLines = priceLines ?? internalPriceLines;
  const latestClose = candles.at(-1)?.close;

  useEffect(() => {
    activeCandleChangeRef.current = onActiveCandleChange;
  }, [onActiveCandleChange]);

  useEffect(() => {
    activePriceLinesRef.current = activePriceLines;
  }, [activePriceLines]);

  useEffect(() => {
    if (!actionMenu) {
      return;
    }
    const lineTitle =
      activePriceLines.find((line) => line.id === actionMenu.lineId)?.title ?? defaultLineName;
    if (presetLineNames.includes(lineTitle)) {
      setLineNameSelection(lineTitle);
      setCustomLineName("");
    } else {
      setLineNameSelection(customLineNameValue);
      setCustomLineName(lineTitle);
    }
  }, [actionMenu, activePriceLines]);

  const updatePriceLines = useCallback(
    (nextPriceLines: LightweightKlinePriceLine[]) => {
      if (priceLines === undefined) {
        setInternalPriceLines(nextPriceLines);
      }
      onPriceLinesChange?.(nextPriceLines);
    },
    [onPriceLinesChange, priceLines],
  );

  const handleSavePriceLine = useCallback(() => {
    const price = actionMenu?.price ?? activePriceRef.current ?? latestClose;
    if (price === undefined || !Number.isFinite(price)) {
      return;
    }
    const roundedPrice = roundPrice(price);
    const title = resolveLineName(lineNameSelection, customLineName);
    if (actionMenu?.lineId) {
      updatePriceLines(
        activePriceLines.map((line) =>
          line.id === actionMenu.lineId
            ? {
                ...line,
                kind: "price",
                color: priceLineColor(title),
                title,
              }
            : line,
        ),
      );
    } else {
      updatePriceLines([
        ...activePriceLines,
        {
          id: `price_line_${Date.now()}_${activePriceLines.length}`,
          kind: "price",
          color: priceLineColor(title),
          price: roundedPrice,
          title,
        },
      ]);
    }
    setActionMenu(null);
  }, [
    actionMenu,
    activePriceLines,
    customLineName,
    latestClose,
    lineNameSelection,
    updatePriceLines,
  ]);

  const handleRemovePriceLine = useCallback(
    (id: string) => {
      updatePriceLines(activePriceLines.filter((line) => line.id !== id));
      setActionMenu(null);
    },
    [activePriceLines, updatePriceLines],
  );

  const refreshLinePositions = useCallback(() => {
    const candleSeries = candleSeriesRef.current;
    if (!candleSeries) {
      setLinePositions([]);
      return;
    }
    setLinePositions(
      activePriceLines
        .map((line) => {
          const y = candleSeries.priceToCoordinate(line.price);
          return y === null ? null : { id: line.id, y: Number(y) };
        })
        .filter((line): line is { id: string; y: number } => line !== null),
    );
  }, [activePriceLines]);

  useEffect(() => {
    refreshLinePositionsRef.current = refreshLinePositions;
    refreshLinePositions();
  }, [refreshLinePositions]);

  useEffect(() => {
    if (!chartRef.current) {
      return undefined;
    }

    const container = chartRef.current;
    const volumeUnit = volumeAxisUnit(chartData.volume.map((item) => item.value));
    const chart = createChart(container, {
      autoSize: true,
      height,
      layout: {
        background: { type: ColorType.Solid, color: "#fffefa" },
        textColor: "#71717a",
        fontFamily:
          'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        fontSize: 11,
      },
      grid: {
        vertLines: { color: "rgba(228, 228, 231, 0.55)" },
        horzLines: { color: "rgba(228, 228, 231, 0.9)" },
      },
      rightPriceScale: {
        borderColor: "#d4d4d8",
        scaleMargins: showVolume ? { top: 0.08, bottom: 0.08 } : undefined,
      },
      timeScale: {
        borderColor: "#d4d4d8",
        timeVisible: false,
        secondsVisible: false,
        rightOffset: 2,
        barSpacing: 6,
        minBarSpacing: 2,
        fixLeftEdge: false,
        fixRightEdge: false,
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { labelVisible: false, color: "#94a3b8", width: 1 },
        horzLine: { labelVisible: false, color: "#94a3b8", width: 1 },
      },
      handleScroll: {
        mouseWheel: true,
        pressedMouseMove: true,
        horzTouchDrag: true,
        vertTouchDrag: false,
      },
      handleScale: {
        axisPressedMouseMove: true,
        mouseWheel: true,
        pinch: true,
      },
      localization: {
        locale: "zh-CN",
        timeFormatter: (time: Time) => timeToKey(time),
      },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor,
      downColor,
      borderUpColor: upColor,
      borderDownColor: downColor,
      wickUpColor: upColor,
      wickDownColor: downColor,
      priceFormat: { type: "price", precision: 2, minMove: 0.01 },
    });
    candleSeriesRef.current = candleSeries;
    coordinateToPriceRef.current = (coordinate: number) => {
      const price = candleSeries.coordinateToPrice(coordinate);
      return typeof price === "number" && Number.isFinite(price) ? price : null;
    };
    candleSeries.setData(chartData.candles);

    if (chartMarkers.length > 0) {
      createSeriesMarkers(candleSeries, chartMarkers);
    }

    if (showMovingAverages) {
      addLineSeries(chart, chartData.ma5, lineColors.ma5);
      addLineSeries(chart, chartData.ma10, lineColors.ma10);
      addLineSeries(chart, chartData.ma20, lineColors.ma20);
      addLineSeries(chart, chartData.ma60, lineColors.ma60);
    }

    if (showVolume) {
      const volumeSeries = chart.addSeries(
        HistogramSeries,
        {
          priceFormat: {
            type: "custom",
            formatter: (value: number) => formatVolumeAxis(value, volumeUnit),
            tickmarksFormatter: (values: number[]) =>
              values.map((value: number) => formatVolumeAxis(value, volumeUnit)),
            minMove: 1,
          },
          priceLineVisible: false,
          lastValueVisible: false,
        },
        1,
      );
      volumeSeries.setData(chartData.volume);
      const panes = chart.panes();
      panes[0]?.setStretchFactor(4);
      panes[1]?.setStretchFactor(1.1);
    }

    const candleIndexByDate = new Map(candles.map((candle, index) => [candle.date, index]));
    const handleCrosshairMove = (param: MouseEventParams<Time>) => {
      if (!param.point || param.time === undefined) {
        activePriceRef.current = null;
        activeCandleChangeRef.current?.(null, null);
        return;
      }
      const price = candleSeries.coordinateToPrice(param.point.y);
      activePriceRef.current = typeof price === "number" && Number.isFinite(price) ? price : null;
      const index = candleIndexByDate.get(timeToKey(param.time));
      activeCandleChangeRef.current?.(index === undefined ? null : candles[index], index ?? null);
      refreshLinePositionsRef.current();
    };
    const handleChartClick = (param: MouseEventParams<Time>) => {
      if (!enablePriceLineActions) {
        return;
      }
      if (suppressNextClickRef.current) {
        suppressNextClickRef.current = false;
        return;
      }
      if (!param.point) {
        setActionMenu(null);
        return;
      }
      const price = coordinateToPriceRef.current(param.point.y);
      if (price === null) {
        setActionMenu(null);
        return;
      }
      const clickedLine = nearestPriceLine(price, activePriceLinesRef.current);
      setActionMenu({
        x: param.point.x,
        y: param.point.y,
        price: clickedLine?.price ?? roundPrice(price),
        lineId: clickedLine?.id,
      });
    };
    chart.subscribeCrosshairMove(handleCrosshairMove);
    chart.subscribeClick(handleChartClick);
    chart.timeScale().fitContent();
    window.setTimeout(() => refreshLinePositionsRef.current(), 0);

    return () => {
      chart.unsubscribeCrosshairMove(handleCrosshairMove);
      chart.unsubscribeClick(handleChartClick);
      candleSeriesRef.current = null;
      coordinateToPriceRef.current = () => null;
      priceLineRefs.current = [];
      chart.remove();
    };
  }, [
    candles,
    chartData,
    chartMarkers,
    enablePriceLineActions,
    height,
    showMovingAverages,
    showVolume,
  ]);

  useEffect(() => {
    const candleSeries = candleSeriesRef.current;
    if (!candleSeries) {
      return;
    }
    for (const priceLine of priceLineRefs.current) {
      candleSeries.removePriceLine(priceLine);
    }
    priceLineRefs.current = activePriceLines.map((priceLine) =>
      candleSeries.createPriceLine({
        price: priceLine.price,
        color: priceLine.color ?? priceLineColor(priceLine.title),
        lineWidth: 2,
        lineStyle: LineStyle.Solid,
        axisLabelVisible: true,
        title: priceLine.title ?? defaultLineName,
      }),
    );
    refreshLinePositionsRef.current();
  }, [activePriceLines]);

  useEffect(() => {
    if (!draggingLineId) {
      return undefined;
    }

    const handlePointerMove = (event: PointerEvent) => {
      if (!chartRef.current) {
        return;
      }
      const pointerStart = linePointerStartRef.current;
      if (pointerStart) {
        const distance = Math.hypot(
          event.clientX - pointerStart.clientX,
          event.clientY - pointerStart.clientY,
        );
        if (distance > 3) {
          pointerStart.moved = true;
        }
      }
      const rect = chartRef.current.getBoundingClientRect();
      const price = coordinateToPriceRef.current(event.clientY - rect.top);
      if (price === null) {
        return;
      }
      const roundedPrice = roundPrice(price);
      updatePriceLines(
        activePriceLinesRef.current.map((line) =>
          line.id === draggingLineId
            ? {
                ...line,
                kind: "price",
                price: roundedPrice,
              }
            : line,
        ),
      );
    };
    const handlePointerUp = (event: PointerEvent) => {
      const pointerStart = linePointerStartRef.current;
      if (pointerStart && !pointerStart.moved && chartRef.current) {
        const line = activePriceLinesRef.current.find((item) => item.id === pointerStart.id);
        const rect = chartRef.current.getBoundingClientRect();
        if (line) {
          setActionMenu({
            x: event.clientX - rect.left,
            y: event.clientY - rect.top,
            price: line.price,
            lineId: line.id,
          });
        }
      }
      linePointerStartRef.current = null;
      setDraggingLineId(null);
      window.setTimeout(() => {
        suppressNextClickRef.current = false;
      }, 0);
    };

    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerup", handlePointerUp, { once: true });
    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerup", handlePointerUp);
    };
  }, [draggingLineId, updatePriceLines]);

  const handleLinePointerDown = (event: ReactPointerEvent<HTMLButtonElement>, id: string) => {
    event.preventDefault();
    event.stopPropagation();
    suppressNextClickRef.current = true;
    linePointerStartRef.current = {
      id,
      clientX: event.clientX,
      clientY: event.clientY,
      moved: false,
    };
    setActionMenu(null);
    setDraggingLineId(id);
  };

  return (
    <div className={cn("relative min-w-0", className)}>
      <div
        ref={chartRef}
        aria-label={ariaLabel}
        role="img"
        style={{ height }}
      />
      {enablePriceLineActions
        ? linePositions.map((position) => {
            const line = activePriceLines.find((item) => item.id === position.id);
            if (!line) {
              return null;
            }
            return (
              <Tooltip key={line.id}>
                <TooltipTrigger asChild>
                  <button
                    aria-label={`移动${line.title ?? defaultLineName} ${formatPrice(line.price)}`}
                    className={cn(
                      "absolute right-14 z-10 h-5 w-14 -translate-y-1/2 cursor-ns-resize rounded border border-white/80 bg-white/70 text-[10px] font-semibold text-mutedText shadow-sm backdrop-blur-sm hover:border-line hover:bg-white",
                      draggingLineId === line.id ? "border-line bg-white text-ink" : null,
                    )}
                    onPointerDown={(event) => handleLinePointerDown(event, line.id)}
                    style={{ top: Math.max(10, position.y) }}
                    type="button"
                  >
                    {formatPrice(line.price)}
                  </button>
                </TooltipTrigger>
                <TooltipContent>
                  {line.title ?? defaultLineName} {formatPrice(line.price)}
                </TooltipContent>
              </Tooltip>
            );
          })
        : null}
      {enablePriceLineActions && actionMenu ? (
        <div
          className="absolute z-20 w-48 rounded-md border border-line bg-white p-2 text-xs shadow-lg"
          style={{
            left: Math.min(Math.max(8, actionMenu.x + 8), 520),
            top: Math.max(8, actionMenu.y - 12),
          }}
        >
          <div className="mb-2 flex items-center justify-between gap-2">
            <span className="font-semibold text-ink">
              {actionMenu.lineId ? "价格线" : "添加价格线"}
            </span>
            <span className="font-mono text-[11px] text-mutedText">
              {formatPrice(actionMenu.price)}
            </span>
          </div>
          <div className="space-y-2">
            <select
              className="h-8 w-full rounded-md border border-input bg-background px-2 text-xs shadow-sm outline-none focus:ring-2 focus:ring-ring/30"
              onChange={(event) => setLineNameSelection(event.target.value)}
              value={lineNameSelection}
            >
              {presetLineNames.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
              <option value={customLineNameValue}>自定义</option>
            </select>
            {lineNameSelection === customLineNameValue ? (
              <Input
                className="h-8 text-xs"
                onChange={(event) => setCustomLineName(event.target.value)}
                placeholder="输入名称"
                value={customLineName}
              />
            ) : null}
          </div>
          {actionMenu.lineId ? (
            <div className="mt-2 grid grid-cols-3 gap-2">
              <Button
                className="h-8 text-xs"
                onClick={handleSavePriceLine}
                size="sm"
                type="button"
                variant="default"
              >
                保存
              </Button>
              <Button
                className="h-8 text-xs"
                onClick={() => setActionMenu(null)}
                size="sm"
                type="button"
                variant="outline"
              >
                取消
              </Button>
              <Button
                className="h-8 gap-1 text-xs"
                onClick={() => handleRemovePriceLine(actionMenu.lineId as string)}
                size="sm"
                type="button"
                variant="outline"
              >
                <X className="h-3.5 w-3.5" />
                删除
              </Button>
            </div>
          ) : (
            <div className="mt-2 grid grid-cols-2 gap-2">
              <Button
                className="h-8 justify-start gap-2 text-xs"
                onClick={handleSavePriceLine}
                size="sm"
                type="button"
                variant="default"
              >
                <Plus className="h-4 w-4" />
                确定添加
              </Button>
              <Button
                className="h-8 text-xs"
                onClick={() => setActionMenu(null)}
                size="sm"
                type="button"
                variant="outline"
              >
                取消
              </Button>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}

function toLightweightData(candles: LightweightKlineCandle[]) {
  const candleData: CandlestickData<Time>[] = candles.map((candle) => ({
    time: candle.date,
    open: candle.open,
    high: candle.high,
    low: candle.low,
    close: candle.close,
  }));
  const volumeData: HistogramData<Time>[] = candles.map((candle) => ({
    time: candle.date,
    value: candle.volume ?? 0,
    color: candle.close >= candle.open ? "rgba(225, 29, 72, 0.85)" : "rgba(22, 163, 74, 0.85)",
  }));
  return {
    candles: candleData,
    volume: volumeData,
    ma5: movingAverageData(candles, "ma5"),
    ma10: movingAverageData(candles, "ma10"),
    ma20: movingAverageData(candles, "ma20"),
    ma60: movingAverageData(candles, "ma60"),
  };
}

function movingAverageData(
  candles: LightweightKlineCandle[],
  key: "ma5" | "ma10" | "ma20" | "ma60",
): LineData<Time>[] {
  return candles
    .filter((candle) => typeof candle[key] === "number" && Number.isFinite(candle[key]))
    .map((candle) => ({
      time: candle.date,
      value: candle[key] as number,
    }));
}

function addLineSeries(
  chart: ReturnType<typeof createChart>,
  data: LineData<Time>[],
  color: string,
) {
  if (data.length === 0) {
    return;
  }
  const series = chart.addSeries(LineSeries, {
    color,
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
  });
  series.setData(data);
}

function toLightweightMarkers(markers: LightweightKlineMarker[]): SeriesMarker<Time>[] {
  return markers.map((marker) => ({
    time: marker.date,
    position: marker.side === "buy" ? "belowBar" : "aboveBar",
    shape: marker.side === "buy" ? "arrowUp" : "arrowDown",
    color: marker.side === "buy" ? downColor : upColor,
    text: marker.text ?? (marker.side === "buy" ? "B" : "S"),
    size: 1.2,
  }));
}

function nearestPriceLine(
  price: number,
  priceLines: LightweightKlinePriceLine[],
): LightweightKlinePriceLine | null {
  const threshold = Math.max(Math.abs(price) * 0.003, 0.02);
  let nearest: LightweightKlinePriceLine | null = null;
  let nearestDistance = Number.POSITIVE_INFINITY;
  for (const line of priceLines) {
    const distance = Math.abs(line.price - price);
    if (distance < nearestDistance) {
      nearest = line;
      nearestDistance = distance;
    }
  }
  return nearest && nearestDistance <= threshold ? nearest : null;
}

function resolveLineName(selection: string, customName: string): string {
  if (selection === customLineNameValue) {
    return customName.trim() || defaultLineName;
  }
  return selection || defaultLineName;
}

function priceLineColor(title: string | undefined): string {
  if (title && !presetLineNames.includes(title)) {
    return "#7c3aed";
  }
  if (title === "支撑线" || title === "买入线") {
    return "#16a34a";
  }
  if (title === "压力线" || title === "止损线" || title === "卖出线") {
    return "#e11d48";
  }
  if (title === "止盈线") {
    return "#d97706";
  }
  if (title === "观察线") {
    return "#7c3aed";
  }
  return "#2563eb";
}

function roundPrice(value: number): number {
  return Math.round(value * 100) / 100;
}

function formatPrice(value: number): string {
  return value.toFixed(2);
}

type VolumeAxisUnit = {
  divisor: number;
  suffix: string;
};

function volumeAxisUnit(values: number[]): VolumeAxisUnit {
  const maxValue = Math.max(0, ...values);
  if (maxValue >= 100_000_000) {
    return { divisor: 100_000_000, suffix: "亿" };
  }
  if (maxValue >= 10_000) {
    return { divisor: 10_000, suffix: "万" };
  }
  return { divisor: 1, suffix: "" };
}

function formatVolumeAxis(value: number, unit: VolumeAxisUnit): string {
  if (!Number.isFinite(value)) {
    return "";
  }
  const scaled = value / unit.divisor;
  if (!unit.suffix) {
    return String(Math.round(scaled));
  }
  const formatted = scaled >= 10 ? scaled.toFixed(0) : scaled.toFixed(1);
  return `${formatted.replace(/\.0$/, "")}${unit.suffix}`;
}

function timeToKey(time: Time): string {
  if (typeof time === "string") {
    return time;
  }
  if (typeof time === "number") {
    return new Date(time * 1000).toISOString().slice(0, 10);
  }
  return `${time.year}-${String(time.month).padStart(2, "0")}-${String(time.day).padStart(2, "0")}`;
}
