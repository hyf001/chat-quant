import {
  BaselineSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineSeries,
  LineStyle,
  createChart,
  type BaselineData,
  type HistogramData,
  type IPriceLine,
  type ISeriesApi,
  type LineData,
  type MouseEventParams,
  type Time,
  type UTCTimestamp,
} from "lightweight-charts";
import { useEffect, useMemo, useRef, useState } from "react";

/** 分时序列：t 是 HH:MM，p 是分钟价，v 是分钟成交量（训练与行情预览共用）。 */
export type IntradayChartPoint = {
  t: string;
  p: number;
  v: number;
};

type IntradayChartProps = {
  points: IntradayChartPoint[];
  /** 分时涨跌幅基准（昨收）：低于它画绿、高于它画红，虚线标出它的位置。 */
  basePrice: number;
  height?: number;
  ariaLabel?: string;
};

const upColor = "#e11d48";
const downColor = "#16a34a";
const averageColor = "#d97706";
const baseLineColor = "#94a3b8";

/**
 * 当日分时图：分钟价（相对昨收上色的基线线）+ 均价线 + 分钟成交量。
 *
 * X 轴用**序号**（不是时间戳），刻度与 crosshair 标签都由 formatter 映射成 ``HH:MM``：
 * 训练里分钟数据的真实日期不进前端，行情预览里也只需要"几点几分"这一层信息。
 */
export function IntradayChart({
  points,
  basePrice,
  height = 320,
  ariaLabel = "当日分时",
}: IntradayChartProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const priceRef = useRef<ISeriesApi<"Baseline", Time> | null>(null);
  const averageRef = useRef<ISeriesApi<"Line", Time> | null>(null);
  const volumeRef = useRef<ISeriesApi<"Histogram", Time> | null>(null);
  const baseLineRef = useRef<IPriceLine | null>(null);
  const pointsRef = useRef(points);
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  pointsRef.current = points;
  // 均价线用分钟价与成交量加权近似（分钟数据没有成交额字段）
  const series = useMemo(() => buildSeries(points), [points]);

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
        // 同上：图表左下角的 TradingView 角标不显示（归因见 README 技术栈）
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
        barSpacing: 3,
        minBarSpacing: 0.5,
        tickMarkFormatter: (time: Time) => formatMinute(time, pointsRef.current),
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { labelVisible: true, color: "#94a3b8", width: 1 },
        horzLine: { labelVisible: true, color: "#94a3b8", width: 1 },
      },
      localization: {
        locale: "zh-CN",
        timeFormatter: (time: Time) => formatMinute(time, pointsRef.current),
      },
    });
    priceRef.current = chart.addSeries(BaselineSeries, {
      topLineColor: upColor,
      topFillColor1: "rgba(225, 29, 72, 0.18)",
      topFillColor2: "rgba(225, 29, 72, 0.02)",
      bottomLineColor: downColor,
      bottomFillColor1: "rgba(22, 163, 74, 0.02)",
      bottomFillColor2: "rgba(22, 163, 74, 0.18)",
      priceLineVisible: false,
      lastValueVisible: true,
      priceFormat: { type: "price", precision: 2, minMove: 0.01 },
    });
    averageRef.current = chart.addSeries(LineSeries, {
      color: averageColor,
      lineWidth: 1,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    });
    volumeRef.current = chart.addSeries(
      HistogramSeries,
      { priceLineVisible: false, lastValueVisible: false, priceFormat: { type: "volume" } },
      1,
    );

    const handleCrosshairMove = (param: MouseEventParams<Time>) => {
      const time = param.time;
      setActiveIndex(typeof time === "number" && param.point ? time : null);
    };
    chart.subscribeCrosshairMove(handleCrosshairMove);

    return () => {
      chart.unsubscribeCrosshairMove(handleCrosshairMove);
      priceRef.current = null;
      averageRef.current = null;
      volumeRef.current = null;
      baseLineRef.current = null;
      chart.remove();
    };
  }, [height]);

  useEffect(() => {
    const price = priceRef.current;
    const average = averageRef.current;
    const volume = volumeRef.current;
    if (!price || !average || !volume) {
      return;
    }
    price.applyOptions({ baseValue: { type: "price", price: basePrice } });
    price.setData(series.price);
    average.setData(series.average);
    volume.setData(series.volume);

    if (baseLineRef.current) {
      baseLineRef.current.applyOptions({ price: basePrice });
    } else {
      baseLineRef.current = price.createPriceLine({
        price: basePrice,
        color: baseLineColor,
        lineWidth: 1,
        lineStyle: LineStyle.Dashed,
        axisLabelVisible: true,
        title: "昨收",
      });
    }
  }, [basePrice, series]);

  const shownIndex = activeIndex ?? points.length - 1;
  const shown = points[shownIndex] ?? null;
  const shownChange = shown === null ? null : changePct(shown.p, basePrice);

  return (
    <div className="relative">
      <div
        ref={containerRef}
        className="w-full rounded-md border border-line bg-[#fffefa]"
        role="img"
        aria-label={ariaLabel}
      />
      {shown && shownChange !== null ? (
        <div className="pointer-events-none absolute left-2 top-2 rounded border border-line bg-panel/90 px-2 py-1 text-[11px] leading-5 text-mutedText">
          <span className="mr-2 text-ink">{shown.t}</span>
          <span className="mr-2">
            价 <span className={toneClass(shownChange)}>{shown.p.toFixed(2)}</span>
          </span>
          <span className="mr-2">
            涨跌 <span className={toneClass(shownChange)}>{formatChange(shownChange)}</span>
          </span>
          <span>量 {formatVolume(shown.v)}</span>
        </div>
      ) : null}
    </div>
  );
}

function buildSeries(points: IntradayChartPoint[]): {
  price: BaselineData<Time>[];
  average: LineData<Time>[];
  volume: HistogramData<Time>[];
} {
  const price: BaselineData<Time>[] = [];
  const average: LineData<Time>[] = [];
  const volume: HistogramData<Time>[] = [];
  let amount = 0;
  let volumeSum = 0;
  let priceSum = 0;
  let previousPrice: number | null = null;

  points.forEach((point, index) => {
    const time = index as UTCTimestamp;
    price.push({ time, value: point.p });
    amount += point.p * point.v;
    volumeSum += point.v;
    priceSum += point.p;
    // 成交量全为 0 时退化成分钟价的简单均值，避免均价线整条断掉
    average.push({ time, value: volumeSum > 0 ? amount / volumeSum : priceSum / (index + 1) });
    volume.push({
      time,
      value: point.v,
      color:
        previousPrice === null || point.p >= previousPrice
          ? "rgba(225, 29, 72, 0.35)"
          : "rgba(22, 163, 74, 0.35)",
    });
    previousPrice = point.p;
  });

  return { price, average, volume };
}

function formatMinute(time: Time, points: IntradayChartPoint[]): string {
  if (typeof time !== "number") {
    return "";
  }
  return points[time]?.t ?? "";
}

function changePct(price: number, basePrice: number): number {
  if (!Number.isFinite(basePrice) || basePrice === 0) {
    return 0;
  }
  return (price / basePrice - 1) * 100;
}

function formatChange(value: number): string {
  const text = value.toFixed(2);
  return value > 0 ? `+${text}%` : `${text}%`;
}

function toneClass(value: number): string {
  if (value > 0) {
    return "text-[#e11d48]";
  }
  if (value < 0) {
    return "text-[#16a34a]";
  }
  return "text-ink";
}

export function formatVolume(value: number): string {
  if (!Number.isFinite(value)) {
    return "—";
  }
  if (Math.abs(value) >= 100_000_000) {
    return `${(value / 100_000_000).toFixed(2)}亿`;
  }
  if (Math.abs(value) >= 10_000) {
    return `${(value / 10_000).toFixed(2)}万`;
  }
  return value.toFixed(0);
}
