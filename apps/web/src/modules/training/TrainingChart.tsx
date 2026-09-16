import { useMemo } from "react";

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

  const last = bars[bars.length - 1];
  const lastPriceLine = useMemo(
    () => (last ? { color: "#2563eb", price: last.c, title: "最新" } : undefined),
    [last],
  );

  return (
    <LightweightKlineChart
      ariaLabel={ariaLabel}
      axis={indexTimeAxis}
      candles={candles}
      className="w-full rounded-md border border-line bg-[#fffefa]"
      crosshairLabels
      enablePriceLineActions
      height={height}
      keepViewportOnUpdate
      lastPriceLine={lastPriceLine}
      markers={chartMarkers}
      onViewIntraday={onViewIntraday ? (key) => onViewIntraday(Number(key)) : undefined}
      showMovingAverages={false}
      showVolume
    />
  );
}
