import {
  CandlestickSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineStyle,
  createChart,
  createSeriesMarkers,
  type CandlestickData,
  type HistogramData,
  type IPriceLine,
  type ISeriesApi,
  type ISeriesMarkersPluginApi,
  type MouseEventParams,
  type SeriesMarker,
  type Time,
  type UTCTimestamp,
} from "lightweight-charts";
import { useEffect, useRef } from "react";

import type { TrainingBar, TrainingMarker } from "./types";

type TrainingChartProps = {
  bars: TrainingBar[];
  markers: TrainingMarker[];
  height?: number;
  ariaLabel?: string;
  /** 双击某一根日线：回调参数是这一根的序号（与 ``TrainingBar.i`` 一致）。 */
  onBarDoubleClick?: (index: number) => void;
};

const upColor = "#e11d48";
const downColor = "#16a34a";
const CHART_TIME_PREFIX = "第 ";

/**
 * 训练专用图表：K 线 + 成交量 + B/S + 最新价格线。
 *
 * 与行情图唯一的差别是 X 轴：服务端不下发日期，``time`` 直接用序号 ``i``，
 * 刻度与 crosshair 标签都由 formatter 显示成序号（不生成伪日期）。
 */
export function TrainingChart({
  bars,
  markers,
  height = 460,
  ariaLabel = "训练 K 线",
  onBarDoubleClick,
}: TrainingChartProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const candleRef = useRef<ISeriesApi<"Candlestick", Time> | null>(null);
  const volumeRef = useRef<ISeriesApi<"Histogram", Time> | null>(null);
  const markerRef = useRef<ISeriesMarkersPluginApi<Time> | null>(null);
  const priceLineRef = useRef<IPriceLine | null>(null);
  const drawnRef = useRef(0);
  // 双击回调放 ref：图表只在 height 变化时重建，订阅不用跟着回调换而重装。
  const doubleClickRef = useRef(onBarDoubleClick);
  doubleClickRef.current = onBarDoubleClick;

  useEffect(() => {
    if (!containerRef.current) {
      return undefined;
    }
    const chart = createChart(containerRef.current, {
      autoSize: true,
      height,
      layout: {
        background: { type: ColorType.Solid, color: "#fffefa" },
        textColor: "#71717a",
        fontSize: 11,
        // 关掉 lightweight-charts 默认的 TradingView 归因角标（归因见 README 技术栈）
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: "rgba(228, 228, 231, 0.55)" },
        horzLines: { color: "rgba(228, 228, 231, 0.9)" },
      },
      rightPriceScale: { borderColor: "#d4d4d8" },
      timeScale: {
        borderColor: "#d4d4d8",
        timeVisible: false,
        secondsVisible: false,
        rightOffset: 2,
        barSpacing: 6,
        minBarSpacing: 1.5,
        tickMarkFormatter: (time: Time) => formatIndex(time),
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { labelVisible: true, color: "#94a3b8", width: 1 },
        horzLine: { labelVisible: true, color: "#94a3b8", width: 1 },
      },
      localization: {
        locale: "zh-CN",
        timeFormatter: (time: Time) => formatIndex(time),
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
    candleRef.current = candleSeries;
    markerRef.current = createSeriesMarkers(candleSeries, []);

    const volumeSeries = chart.addSeries(
      HistogramSeries,
      { priceLineVisible: false, lastValueVisible: false, priceFormat: { type: "volume" } },
      1,
    );
    volumeRef.current = volumeSeries;

    // 双击一根日线：``time`` 就是序号（X 轴即序号轴），空白区与两条坐标轴上的双击忽略
    // （价格轴上的双击仍是 lightweight-charts 的"重置比例"）。
    const handleDoubleClick = (param: MouseEventParams<Time>) => {
      const time = param.time;
      if (typeof time !== "number" || !param.point) {
        return;
      }
      const container = containerRef.current;
      if (container) {
        const { x, y } = param.point;
        const priceAxisWidth = chart.priceScale("right").width();
        const timeAxisHeight = chart.timeScale().height();
        if (
          x < 0 ||
          y < 0 ||
          x > container.clientWidth - priceAxisWidth ||
          y > container.clientHeight - timeAxisHeight
        ) {
          return;
        }
      }
      doubleClickRef.current?.(time);
    };
    chart.subscribeDblClick(handleDoubleClick);

    return () => {
      chart.unsubscribeDblClick(handleDoubleClick);
      candleRef.current = null;
      volumeRef.current = null;
      markerRef.current = null;
      priceLineRef.current = null;
      drawnRef.current = 0;
      chart.remove();
    };
  }, [height]);

  useEffect(() => {
    const candleSeries = candleRef.current;
    const volumeSeries = volumeRef.current;
    if (!candleSeries || !volumeSeries) {
      return;
    }

    if (bars.length < drawnRef.current) {
      candleSeries.setData(bars.map(toCandle));
      volumeSeries.setData(bars.map(toVolume));
      drawnRef.current = bars.length;
    } else {
      // 增量追加：每 reveal 只 update 新的一根（不要每根 setData 全量）
      for (let index = drawnRef.current; index < bars.length; index += 1) {
        candleSeries.update(toCandle(bars[index]));
        volumeSeries.update(toVolume(bars[index]));
      }
      drawnRef.current = bars.length;
    }

    const last = bars[bars.length - 1];
    if (last) {
      if (priceLineRef.current) {
        priceLineRef.current.applyOptions({ price: last.c });
      } else {
        priceLineRef.current = candleSeries.createPriceLine({
          price: last.c,
          color: "#2563eb",
          lineWidth: 1,
          lineStyle: LineStyle.Dashed,
          axisLabelVisible: true,
          title: "最新",
        });
      }
    }
  }, [bars]);

  useEffect(() => {
    markerRef.current?.setMarkers(
      markers.map((marker) => ({
        time: marker.i as UTCTimestamp,
        position: marker.side === "buy" ? "belowBar" : "aboveBar",
        color: marker.side === "buy" ? upColor : downColor,
        shape: marker.side === "buy" ? "arrowUp" : "arrowDown",
        text: marker.text,
      })) as SeriesMarker<Time>[],
    );
  }, [markers]);

  return (
    <div
      ref={containerRef}
      className="w-full rounded-md border border-line bg-[#fffefa]"
      role="img"
      aria-label={ariaLabel}
    />
  );
}

function toCandle(bar: TrainingBar): CandlestickData<Time> {
  return {
    time: bar.i as UTCTimestamp,
    open: bar.o,
    high: bar.h,
    low: bar.l,
    close: bar.c,
  };
}

function toVolume(bar: TrainingBar): HistogramData<Time> {
  return {
    time: bar.i as UTCTimestamp,
    value: bar.v,
    color: bar.c >= bar.o ? "rgba(225, 29, 72, 0.35)" : "rgba(22, 163, 74, 0.35)",
  };
}

function formatIndex(time: Time): string {
  if (typeof time === "number") {
    return `${CHART_TIME_PREFIX}${time + 1} 根`;
  }
  if (typeof time === "string") {
    return `${CHART_TIME_PREFIX}${time} 根`;
  }
  return `${CHART_TIME_PREFIX}${time.day} 根`;
}
