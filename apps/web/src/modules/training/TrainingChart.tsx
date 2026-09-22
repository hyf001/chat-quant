import { useMemo, useState } from "react";

import {
  indexTimeAxis,
  LightweightKlineChart,
  type LightweightKlineCandle,
  type LightweightKlineMarker,
} from "@/shared/components/charts";

import type { TrainingBar, TrainingMarker } from "./types";

type TrainingChartProps = {
  bars: TrainingBar[];
  markers: TrainingMarker[];
  height?: number;
  ariaLabel?: string;
  /** 点了菜单里的"查看分时"：回调参数是这一根的序号（与 ``TrainingBar.i`` 一致）。 */
  onViewIntraday?: (index: number) => void;
};

/**
 * 训练专用图表：K 线 + 成交量的薄封装。
 *
 * 与行情图共用 ``LightweightKlineChart``（同一套点菜单 / 画标注 / 拖动交互），
 * 唯一的差别是 X 轴：服务端不下发日期，用序号轴 ``indexTimeAxis``，
 * 刻度和编辑框都写成"第 N 根"（不生成任何伪日期）。
 */
export function TrainingChart({
  bars,
  markers,
  height = 460,
  ariaLabel = "训练 K 线",
  onViewIntraday,
}: TrainingChartProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const candles = useMemo<LightweightKlineCandle[]>(
    () =>
      bars.map((bar) => ({
        close: bar.c,
        date: String(bar.i),
        high: bar.h,
        low: bar.l,
        open: bar.o,
        volume: bar.v,
      })),
    [bars],
  );
  const chartMarkers = useMemo<LightweightKlineMarker[]>(
    () =>
      markers.map((marker) => ({
        date: String(marker.i),
        side: marker.side,
        text: marker.text,
      })),
    [markers],
  );

  const activeBar = activeIndex === null ? null : bars[activeIndex];
  const previousBar = activeIndex === null || activeIndex < 1 ? null : bars[activeIndex - 1];
  const changePct =
    activeBar && previousBar && previousBar.c !== 0
      ? ((activeBar.c - previousBar.c) / previousBar.c) * 100
      : null;

  return (
    <div className="relative">
      <LightweightKlineChart
        ariaLabel={ariaLabel}
        axis={indexTimeAxis}
        candles={candles}
        className="w-full rounded-md border border-line bg-[#fffefa]"
        crosshairLabels
        enablePriceLineActions
        height={height}
        keepViewportOnUpdate
        markers={chartMarkers}
        onActiveCandleChange={(_candle, index) => setActiveIndex(index)}
        onViewIntraday={onViewIntraday ? (key) => onViewIntraday(Number(key)) : undefined}
        showMovingAverages={false}
        showVolume
      />
      {activeBar ? (
        <div className="pointer-events-none absolute left-3 top-2 z-10 flex flex-wrap items-center gap-x-3 gap-y-1 rounded border border-line bg-white/90 px-2 py-1 font-mono text-[11px] shadow-sm backdrop-blur-sm">
          <span className="font-sans font-medium text-ink">第 {activeBar.i + 1} 根</span>
          <span>开 {formatChartPrice(activeBar.o)}</span>
          <span>高 {formatChartPrice(activeBar.h)}</span>
          <span>低 {formatChartPrice(activeBar.l)}</span>
          <span>收 {formatChartPrice(activeBar.c)}</span>
          <span
            className={
              changePct === null || changePct === 0
                ? "text-mutedText"
                : changePct > 0
                  ? "text-rose-600"
                  : "text-green-600"
            }
          >
            涨幅{" "}
            {changePct === null
              ? "--"
              : `${changePct >= 0 ? "+" : ""}${changePct.toFixed(2)}%`}
          </span>
        </div>
      ) : null}
    </div>
  );
}

function formatChartPrice(value: number): string {
  return value.toFixed(2);
}
