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
  type IChartApi,
  type IPriceLine,
  type ISeriesApi,
  type ISeriesMarkersPluginApi,
  type LineData,
  type LineWidth,
  type MouseEventParams,
  type SeriesMarker,
  type Time,
  type UTCTimestamp,
} from "lightweight-charts";
import { LineChart, Minus, Square, Type, X } from "lucide-react";
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
  /** 线宽 1~4（px），缺省 2。 */
  width?: number;
};

export type LightweightKlinePriceBox = {
  id: string;
  top: number;
  bottom: number;
  /** 左边界钉在哪一根 K 线上；与 `to` 一起缺省时按整幅图宽画。 */
  from?: string;
  /** 右边界钉在哪一根 K 线上。 */
  to?: string;
  title?: string;
  color?: string;
  /** 边框粗细 1~4（px），缺省 1。 */
  width?: number;
};

export type LightweightKlineVerticalLine = {
  id: string;
  /** 钉在哪一根 K 线上（与 candle.date 同格式）。 */
  date: string;
  title?: string;
  color?: string;
  /** 线宽 1~4（px），缺省 1。 */
  width?: number;
};

/**
 * X 轴的"时间键"抽象。
 *
 * 行情图直接用交易日字符串当键（默认实现 ``dateTimeAxis``）；训练图不下发真实日期，
 * 用 bar 序号当键（``indexTimeAxis``），刻度 / crosshair / 编辑框里的文案都是"第 N 根"。
 * **传进来的对象要保证引用稳定**（模块级常量），否则图表会跟着重建。
 */
export type ChartTimeAxis = {
  /** 键 → lightweight-charts 的 time。 */
  toTime: (key: string) => Time;
  /** time → 键；不是有效的一根时返回 null。 */
  fromTime: (time: Time) => string | null;
  /** 轴刻度 / crosshair 上显示的文案。 */
  formatTime: (time: Time) => string;
  /** 界面里显示某一根的文案（如编辑框里的日期 / "第 N 根"）。 */
  formatKey: (key: string) => string;
  /** 把输入框里的文案解析回键；解析不出来返回 null。 */
  parseKey: (text: string) => string | null;
  /** 编辑框里"钉在哪一根"的占位提示（日期轴给日期样例，序号轴给"第 N 根"）。 */
  keyPlaceholder?: string;
};

export type LightweightKlineLastPrice = {
  price: number;
  title?: string;
  color?: string;
};

export type LightweightKlineTextNote = {
  id: string;
  date: string;
  price: number;
  text: string;
  color?: string;
  /** 粗细：加粗（缺省 true）或常规。 */
  bold?: boolean;
};

type LightweightKlineChartProps = {
  candles: LightweightKlineCandle[];
  markers?: LightweightKlineMarker[];
  priceLines?: LightweightKlinePriceLine[];
  defaultPriceLines?: LightweightKlinePriceLine[];
  priceBoxes?: LightweightKlinePriceBox[];
  defaultPriceBoxes?: LightweightKlinePriceBox[];
  verticalLines?: LightweightKlineVerticalLine[];
  defaultVerticalLines?: LightweightKlineVerticalLine[];
  textNotes?: LightweightKlineTextNote[];
  defaultTextNotes?: LightweightKlineTextNote[];
  height: number;
  ariaLabel: string;
  className?: string;
  enablePriceLineActions?: boolean;
  showVolume?: boolean;
  showMovingAverages?: boolean;
  /** X 轴用哪套时间键；缺省是按真实交易日（见 ``ChartTimeAxis``）。 */
  axis?: ChartTimeAxis;
  /** 最新价虚线（训练图用）；不传就不画。 */
  lastPriceLine?: LightweightKlineLastPrice;
  /** crosshair 上的时间标签；日期轴缺省关（轴上有刻度），序号轴一般要开。 */
  crosshairLabels?: boolean;
  /**
   * 数据只追加（训练图一根一根揭示）时别每次重建都 fitContent 回全览，
   * 保持"贴右边缘"的默认视野；换标的 / 换周期仍然会重新适配。
   */
  keepViewportOnUpdate?: boolean;
  /** 菜单里的"查看分时"：宿主决定那一根的分时怎么展示；不传就不显示这一项。 */
  onViewIntraday?: (key: string) => void;
  onActiveCandleChange?: (candle: LightweightKlineCandle | null, index: number | null) => void;
  onPriceLinesChange?: (priceLines: LightweightKlinePriceLine[]) => void;
  onPriceBoxesChange?: (priceBoxes: LightweightKlinePriceBox[]) => void;
  onVerticalLinesChange?: (verticalLines: LightweightKlineVerticalLine[]) => void;
  onTextNotesChange?: (textNotes: LightweightKlineTextNote[]) => void;
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
const emptyPriceBoxes: LightweightKlinePriceBox[] = [];
const emptyVerticalLines: LightweightKlineVerticalLine[] = [];
const emptyTextNotes: LightweightKlineTextNote[] = [];
const defaultLineName = "水平线";
const defaultBoxName = "矩形";
const defaultVerticalLineName = "垂直线";
const defaultTextNoteText = "文字";
const defaultLineColor = "#2563eb";
const defaultBoxColor = "#2563eb";
const defaultVerticalLineColor = "#2563eb";
const defaultTextNoteColor = "#7c3aed";
const defaultLineWidth = 2;
const defaultBoxWidth = 1;
const defaultVerticalLineWidth = 1;
/** 标注可选的颜色（下拉色板）。 */
const annotationColors = ["#2563eb", "#e11d48", "#16a34a", "#d97706", "#7c3aed", "#64748b"];
/** 标注可选的粗细（px）；文字用它表示字重，1~2 常规、3~4 加粗。 */
const annotationWidths = [1, 2, 3, 4];
/** 长按超过这个时长才算"要拖动"；短按是选中 + 编辑。 */
const longPressMs = 240;

/** 默认时间轴：键就是真实交易日字符串。 */
export const dateTimeAxis: ChartTimeAxis = {
  fromTime: (time) => timeToKey(time),
  formatKey: (key) => key,
  formatTime: (time) => timeToKey(time),
  keyPlaceholder: "日期，如 2026-09-14",
  parseKey: (text) => text.trim(),
  toTime: (key) => key as Time,
};

/**
 * 序号轴：图上不出现任何真实日期，键就是 bar 的序号（"0"、"1"…），
 * 刻度 / crosshair / 编辑框文案都显示成"第 N 根"（训练图用）。
 */
export const indexTimeAxis: ChartTimeAxis = {
  fromTime: (time) => (typeof time === "number" ? String(time) : null),
  formatKey: (key) => `第 ${Number(key) + 1} 根`,
  formatTime: (time) => (typeof time === "number" ? `第 ${time + 1} 根` : ""),
  keyPlaceholder: "第 N 根",
  // 输入按"第几根"理解（1 起）：输入 "4" 或 "第 4 根" 都落到第 4 根
  parseKey: (text) => {
    const digits = text.replace(/\D/g, "");
    return digits ? String(Number(digits) - 1) : null;
  },
  toTime: (key) => Number(key) as UTCTimestamp,
};
/** 新建矩形时左右各留几根 K 线（之后拖边可以改）。 */
const defaultBoxHalfBars = 10;
/** 预设名只用于"调用方没给颜色"时的兜底配色；新建的线都带显式颜色。 */
const presetLineNames = [
  "水平线",
  "价格线",
  "支撑线",
  "压力线",
  "止损线",
  "止盈线",
  "买入线",
  "卖出线",
  "观察线",
];

type ChartActionMenu = {
  x: number;
  y: number;
  /** 点击位置的价格；垂直线这类没有价格的标注可以不带。 */
  price?: number;
  /** 点击位置落在哪一根 K 线上：垂直线 / 文字 / 查看分时都要用到。 */
  date?: string;
  lineId?: string;
  boxId?: string;
  vlineId?: string;
  textId?: string;
  mode: "choose" | "priceLine" | "box" | "vline" | "text";
};

type BoxDragMode = "move" | "top" | "bottom" | "left" | "right";

type AnnotationKind = "line" | "box" | "vline" | "text";

/** 被按住的标注：线 / 框 / 文字（框带上沿、下沿、整体移动三种模式）。 */
type AnnotationTarget = {
  kind: AnnotationKind;
  id: string;
  mode?: BoxDragMode;
};

/** 长按成立后开始的拖动会话。 */
type DragSession = {
  target: AnnotationTarget;
  /** 按下时的画布内坐标（与坐标换算同一套空间）。 */
  startX: number;
  startY: number;
  startTopPrice: number;
  startBottomPrice: number;
  startTopY: number;
  startBottomY: number;
  /** 左右边界当前所在的画布内 x（没有边界时是整幅图的左右端点）。 */
  startLeftX: number;
  startRightX: number;
  /** 左右边界当前钉着的 K 线日期。 */
  startFromDate: string;
  startToDate: string;
};

export function LightweightKlineChart({
  candles,
  markers = emptyMarkers,
  priceLines,
  defaultPriceLines = emptyPriceLines,
  priceBoxes,
  defaultPriceBoxes = emptyPriceBoxes,
  verticalLines,
  defaultVerticalLines = emptyVerticalLines,
  textNotes,
  defaultTextNotes = emptyTextNotes,
  height,
  ariaLabel,
  className,
  enablePriceLineActions = false,
  showVolume = true,
  showMovingAverages = true,
  axis = dateTimeAxis,
  lastPriceLine,
  crosshairLabels = false,
  keepViewportOnUpdate = false,
  onViewIntraday,
  onActiveCandleChange,
  onPriceLinesChange,
  onPriceBoxesChange,
  onVerticalLinesChange,
  onTextNotesChange,
}: LightweightKlineChartProps) {
  const chartRef = useRef<HTMLDivElement | null>(null);
  const chartInstanceRef = useRef<IChartApi | null>(null);
  const activePriceRef = useRef<number | null>(null);
  const activeCandleChangeRef = useRef(onActiveCandleChange);
  const viewIntradayRef = useRef(onViewIntraday);
  const activePriceLinesRef = useRef<LightweightKlinePriceLine[]>([]);
  const activePriceBoxesRef = useRef<LightweightKlinePriceBox[]>([]);
  const activeVerticalLinesRef = useRef<LightweightKlineVerticalLine[]>([]);
  const activeTextNotesRef = useRef<LightweightKlineTextNote[]>([]);
  const vlinePositionsRef = useRef<Array<{ id: string; x: number }>>([]);
  const textPositionsRef = useRef<Array<{ id: string; x: number; y: number }>>([]);
  const candleSeriesRef = useRef<ISeriesApi<"Candlestick", Time> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<"Histogram", Time> | null>(null);
  const movingAverageSeriesRef = useRef<
    Partial<Record<"ma5" | "ma10" | "ma20" | "ma60", ISeriesApi<"Line", Time>>>
  >({});
  const seriesMarkersRef = useRef<ISeriesMarkersPluginApi<Time> | null>(null);
  const priceLineRefs = useRef<IPriceLine[]>([]);
  const lastPriceLineRef = useRef<IPriceLine | null>(null);
  const lastPriceLinePropRef = useRef(lastPriceLine);
  const refreshAnnotationPositionsRef = useRef<() => void>(() => undefined);
  const coordinateToPriceRef = useRef<(coordinate: number) => number | null>(() => null);
  const dateAtXRef = useRef<(x: number) => string | null>(() => null);
  const pressRef = useRef<{
    target: AnnotationTarget;
    startX: number;
    startY: number;
    longPressed: boolean;
    timer: number;
  } | null>(null);
  const [internalPriceLines, setInternalPriceLines] =
    useState<LightweightKlinePriceLine[]>(defaultPriceLines);
  const [internalPriceBoxes, setInternalPriceBoxes] =
    useState<LightweightKlinePriceBox[]>(defaultPriceBoxes);
  const [internalVerticalLines, setInternalVerticalLines] =
    useState<LightweightKlineVerticalLine[]>(defaultVerticalLines);
  const [internalTextNotes, setInternalTextNotes] =
    useState<LightweightKlineTextNote[]>(defaultTextNotes);
  const [actionMenu, setActionMenu] = useState<ChartActionMenu | null>(null);
  const [lineTitle, setLineTitle] = useState(defaultLineName);
  const [boxTitle, setBoxTitle] = useState(defaultBoxName);
  const [boxTop, setBoxTop] = useState("");
  const [boxBottom, setBoxBottom] = useState("");
  const [vlineTitle, setVlineTitle] = useState(defaultVerticalLineName);
  const [vlineDate, setVlineDate] = useState("");
  const [textNoteText, setTextNoteText] = useState(defaultTextNoteText);
  const [textNoteDate, setTextNoteDate] = useState("");
  const [dragging, setDragging] = useState<DragSession | null>(null);
  const [lineColor, setLineColor] = useState(defaultLineColor);
  const [lineWidth, setLineWidth] = useState(defaultLineWidth);
  const [boxColor, setBoxColor] = useState(defaultBoxColor);
  const [boxWidth, setBoxWidth] = useState(defaultBoxWidth);
  const [vlineColor, setVlineColor] = useState(defaultVerticalLineColor);
  const [vlineWidth, setVlineWidth] = useState(defaultVerticalLineWidth);
  const [textColor, setTextColor] = useState(defaultTextNoteColor);
  const [textBold, setTextBold] = useState(true);
  const [linePositions, setLinePositions] = useState<Array<{ id: string; y: number }>>([]);
  const [boxPositions, setBoxPositions] = useState<
    Array<{ id: string; top: number; bottom: number; left: number | null; right: number | null }>
  >([]);
  const [vlinePositions, setVlinePositions] = useState<Array<{ id: string; x: number }>>([]);
  const [textPositions, setTextPositions] = useState<
    Array<{ id: string; x: number; y: number }>
  >([]);
  const chartData = useMemo(() => toLightweightData(candles, axis), [axis, candles]);
  const chartMarkers = useMemo(() => toLightweightMarkers(markers, axis), [axis, markers]);
  const candlesRef = useRef(candles);
  const chartDataRef = useRef(chartData);
  const chartMarkersRef = useRef(chartMarkers);
  const activePriceLines = priceLines ?? internalPriceLines;
  const activePriceBoxes = priceBoxes ?? internalPriceBoxes;
  const activeVerticalLines = verticalLines ?? internalVerticalLines;
  const activeTextNotes = textNotes ?? internalTextNotes;
  /** 图上出现过的时间键（日期轴的交易日 / 序号轴的 "0"、"1"…）。 */
  const candleKeys = useMemo(() => new Set(candles.map((candle) => candle.date)), [candles]);
  /** 时间键 → 这根 K 线的序号：矩形左右边界、拖动吸附都用它定先后。 */
  const candleOrder = useMemo(
    () => new Map(candles.map((candle, index) => [candle.date, index])),
    [candles],
  );

  // 图表实例不随行情追加重建；事件处理器通过 ref 读取最新数据，避免捕获首屏快照。
  candlesRef.current = candles;
  chartDataRef.current = chartData;
  chartMarkersRef.current = chartMarkers;

  useEffect(() => {
    activeCandleChangeRef.current = onActiveCandleChange;
  }, [onActiveCandleChange]);

  useEffect(() => {
    lastPriceLinePropRef.current = lastPriceLine;
  }, [lastPriceLine]);

  useEffect(() => {
    viewIntradayRef.current = onViewIntraday;
  }, [onViewIntraday]);

  useEffect(() => {
    activePriceLinesRef.current = activePriceLines;
  }, [activePriceLines]);

  useEffect(() => {
    activePriceBoxesRef.current = activePriceBoxes;
  }, [activePriceBoxes]);

  useEffect(() => {
    activeVerticalLinesRef.current = activeVerticalLines;
  }, [activeVerticalLines]);

  useEffect(() => {
    activeTextNotesRef.current = activeTextNotes;
  }, [activeTextNotes]);

  useEffect(() => {
    if (!actionMenu) {
      return;
    }
    if (actionMenu.mode === "vline") {
      const line = activeVerticalLines.find((item) => item.id === actionMenu.vlineId);
      const key = line?.date ?? actionMenu.date;
      setVlineTitle(line?.title ?? defaultVerticalLineName);
      setVlineDate(key === undefined ? "" : axis.formatKey(key));
      setVlineColor(line?.color ?? defaultVerticalLineColor);
      setVlineWidth(line?.width ?? defaultVerticalLineWidth);
      return;
    }
    if (actionMenu.mode === "text") {
      const note = activeTextNotes.find((item) => item.id === actionMenu.textId);
      const key = note?.date ?? actionMenu.date;
      setTextNoteText(note?.text ?? "");
      setTextNoteDate(key === undefined ? "" : axis.formatKey(key));
      setTextColor(note?.color ?? defaultTextNoteColor);
      setTextBold(note?.bold ?? true);
      return;
    }
    if (actionMenu.mode === "box") {
      const box = activePriceBoxes.find((item) => item.id === actionMenu.boxId);
      const menuPrice = actionMenu.price ?? 0;
      const defaultHalfHeight = Math.max(Math.abs(menuPrice) * 0.03, 0.03);
      setBoxTitle(box?.title ?? defaultBoxName);
      setBoxTop(formatEditablePrice(box?.top ?? menuPrice + defaultHalfHeight));
      setBoxBottom(formatEditablePrice(box?.bottom ?? menuPrice - defaultHalfHeight));
      setBoxColor(box?.color ?? defaultBoxColor);
      setBoxWidth(box?.width ?? defaultBoxWidth);
      return;
    }
    if (actionMenu.mode !== "priceLine") {
      return;
    }
    const activeLine = activePriceLines.find((line) => line.id === actionMenu.lineId);
    setLineColor(activeLine?.color ?? priceLineColor(activeLine?.title ?? defaultLineName));
    setLineWidth(activeLine?.width ?? defaultLineWidth);
    setLineTitle(activeLine?.title ?? defaultLineName);
  }, [
    actionMenu,
    activePriceBoxes,
    activePriceLines,
    activeTextNotes,
    activeVerticalLines,
    axis,
  ]);

  const updatePriceLines = useCallback(
    (nextPriceLines: LightweightKlinePriceLine[]) => {
      if (priceLines === undefined) {
        setInternalPriceLines(nextPriceLines);
      }
      onPriceLinesChange?.(nextPriceLines);
    },
    [onPriceLinesChange, priceLines],
  );

  const updatePriceBoxes = useCallback(
    (nextPriceBoxes: LightweightKlinePriceBox[]) => {
      if (priceBoxes === undefined) {
        setInternalPriceBoxes(nextPriceBoxes);
      }
      onPriceBoxesChange?.(nextPriceBoxes);
    },
    [onPriceBoxesChange, priceBoxes],
  );

  const updateVerticalLines = useCallback(
    (nextVerticalLines: LightweightKlineVerticalLine[]) => {
      if (verticalLines === undefined) {
        setInternalVerticalLines(nextVerticalLines);
      }
      onVerticalLinesChange?.(nextVerticalLines);
    },
    [onVerticalLinesChange, verticalLines],
  );

  const updateTextNotes = useCallback(
    (nextTextNotes: LightweightKlineTextNote[]) => {
      if (textNotes === undefined) {
        setInternalTextNotes(nextTextNotes);
      }
      onTextNotesChange?.(nextTextNotes);
    },
    [onTextNotesChange, textNotes],
  );

  const handleSavePriceLine = useCallback(() => {
    if (!actionMenu?.lineId) {
      return;
    }
    const title = lineTitle.trim() || defaultLineName;
    updatePriceLines(
      activePriceLines.map((line) =>
        line.id === actionMenu.lineId
          ? {
              ...line,
              kind: "price",
              color: lineColor,
              title,
              width: lineWidth,
            }
          : line,
      ),
    );
    setActionMenu(null);
  }, [actionMenu, activePriceLines, lineColor, lineTitle, lineWidth, updatePriceLines]);

  const handleSavePriceBox = useCallback(() => {
    if (!actionMenu) {
      return;
    }
    const firstPrice = Number.parseFloat(boxTop);
    const secondPrice = Number.parseFloat(boxBottom);
    if (!Number.isFinite(firstPrice) || !Number.isFinite(secondPrice)) {
      return;
    }
    if (!actionMenu.boxId) {
      return;
    }
    const { top, bottom } = normalizeBoxPrices(firstPrice, secondPrice);
    const title = boxTitle.trim() || defaultBoxName;
    updatePriceBoxes(
      activePriceBoxes.map((item) =>
        item.id === actionMenu.boxId
          ? {
              ...item,
              bottom,
              color: boxColor,
              title,
              top,
              width: boxWidth,
            }
          : item,
      ),
    );
    setActionMenu(null);
  }, [
    actionMenu,
    activePriceBoxes,
    boxBottom,
    boxColor,
    boxTitle,
    boxTop,
    boxWidth,
    updatePriceBoxes,
  ]);

  const handleRemovePriceLine = useCallback(
    (id: string) => {
      updatePriceLines(activePriceLines.filter((line) => line.id !== id));
      setActionMenu(null);
    },
    [activePriceLines, updatePriceLines],
  );

  const handleRemovePriceBox = useCallback(
    (id: string) => {
      updatePriceBoxes(activePriceBoxes.filter((box) => box.id !== id));
      setActionMenu(null);
    },
    [activePriceBoxes, updatePriceBoxes],
  );

  const handleSaveVerticalLine = useCallback(() => {
    const date = axis.parseKey(vlineDate);
    if (!date || !candleKeys.has(date)) {
      return;
    }
    if (!actionMenu?.vlineId) {
      return;
    }
    const title = vlineTitle.trim() || defaultVerticalLineName;
    updateVerticalLines(
      activeVerticalLines.map((line) =>
        line.id === actionMenu.vlineId
          ? { ...line, color: vlineColor, date, title, width: vlineWidth }
          : line,
      ),
    );
    setActionMenu(null);
  }, [
    actionMenu,
    activeVerticalLines,
    axis,
    candleKeys,
    updateVerticalLines,
    vlineColor,
    vlineDate,
    vlineTitle,
    vlineWidth,
  ]);

  const handleRemoveVerticalLine = useCallback(
    (id: string) => {
      updateVerticalLines(activeVerticalLines.filter((line) => line.id !== id));
      setActionMenu(null);
    },
    [activeVerticalLines, updateVerticalLines],
  );

  const handleSaveTextNote = useCallback(() => {
    const date = axis.parseKey(textNoteDate);
    if (!date || !candleKeys.has(date) || !actionMenu?.textId) {
      return;
    }
    const text = textNoteText.trim() || defaultTextNoteText;
    updateTextNotes(
      activeTextNotes.map((note) =>
        note.id === actionMenu.textId
          ? { ...note, bold: textBold, color: textColor, date, text }
          : note,
      ),
    );
    setActionMenu(null);
  }, [
    actionMenu,
    activeTextNotes,
    axis,
    candleKeys,
    textBold,
    textColor,
    textNoteDate,
    textNoteText,
    updateTextNotes,
  ]);

  const handleRemoveTextNote = useCallback(
    (id: string) => {
      updateTextNotes(activeTextNotes.filter((note) => note.id !== id));
      setActionMenu(null);
    },
    [activeTextNotes, updateTextNotes],
  );

  const refreshAnnotationPositions = useCallback(() => {
    const candleSeries = candleSeriesRef.current;
    const chart = chartInstanceRef.current;
    if (!candleSeries || !chart) {
      setLinePositions([]);
      setBoxPositions([]);
      vlinePositionsRef.current = [];
      setVlinePositions([]);
      textPositionsRef.current = [];
      setTextPositions([]);
      return;
    }
    const timeScale = chart.timeScale();
    setLinePositions(
      activePriceLines
        .map((line) => {
          const y = candleSeries.priceToCoordinate(line.price);
          return y === null ? null : { id: line.id, y: Number(y) };
        })
        .filter((line): line is { id: string; y: number } => line !== null),
    );
    setBoxPositions(
      activePriceBoxes
        .map((box) => {
          const topY = candleSeries.priceToCoordinate(Math.max(box.top, box.bottom));
          const bottomY = candleSeries.priceToCoordinate(Math.min(box.top, box.bottom));
          if (topY === null || bottomY === null) {
            return null;
          }
          const fromX =
            box.from === undefined ? null : timeScale.timeToCoordinate(axis.toTime(box.from));
          const toX =
            box.to === undefined ? null : timeScale.timeToCoordinate(axis.toTime(box.to));
          return {
            id: box.id,
            top: Math.min(Number(topY), Number(bottomY)),
            bottom: Math.max(Number(topY), Number(bottomY)),
            left: fromX === null ? null : Number(fromX),
            right: toX === null ? null : Number(toX),
          };
        })
        .filter(
          (
            box,
          ): box is {
            id: string;
            top: number;
            bottom: number;
            left: number | null;
            right: number | null;
          } => box !== null,
        ),
    );
    const nextVlinePositions = activeVerticalLines
      .map((line) => {
        const x = timeScale.timeToCoordinate(axis.toTime(line.date));
        return x === null ? null : { id: line.id, x: Number(x) };
      })
      .filter((line): line is { id: string; x: number } => line !== null);
    vlinePositionsRef.current = nextVlinePositions;
    setVlinePositions(nextVlinePositions);
    const nextTextPositions = activeTextNotes
      .map((note) => {
        const x = timeScale.timeToCoordinate(axis.toTime(note.date));
        const y = candleSeries.priceToCoordinate(note.price);
        if (x === null || y === null) {
          return null;
        }
        return { id: note.id, x: Number(x), y: Number(y) };
      })
      .filter((note): note is { id: string; x: number; y: number } => note !== null);
    textPositionsRef.current = nextTextPositions;
    setTextPositions(nextTextPositions);
  }, [activePriceBoxes, activePriceLines, activeTextNotes, activeVerticalLines, axis]);

  useEffect(() => {
    refreshAnnotationPositionsRef.current = refreshAnnotationPositions;
    refreshAnnotationPositions();
  }, [refreshAnnotationPositions]);

  useEffect(() => {
    if (!chartRef.current) {
      return undefined;
    }

    const container = chartRef.current;
    const initialChartData = chartDataRef.current;
    const volumeUnit = volumeAxisUnit(initialChartData.volume.map((item) => item.value));
    const chart = createChart(container, {
      autoSize: true,
      height,
      layout: {
        // 关掉 lightweight-charts 默认的 TradingView 归因角标（归因见 README）
        attributionLogo: false,
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
        tickMarkFormatter: (time: Time) => axis.formatTime(time),
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { labelVisible: crosshairLabels, color: "#94a3b8", width: 1 },
        horzLine: { labelVisible: crosshairLabels, color: "#94a3b8", width: 1 },
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
        timeFormatter: (time: Time) => axis.formatTime(time),
      },
    });
    chartInstanceRef.current = chart;

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
    candleSeries.setData(initialChartData.candles);

    const initialLastPrice = lastPriceLinePropRef.current;
    if (initialLastPrice) {
      lastPriceLineRef.current = createLastPriceLine(candleSeries, initialLastPrice);
    }

    seriesMarkersRef.current = createSeriesMarkers(candleSeries, chartMarkersRef.current);

    if (showMovingAverages) {
      movingAverageSeriesRef.current = {
        ma5: addLineSeries(chart, initialChartData.ma5, lineColors.ma5),
        ma10: addLineSeries(chart, initialChartData.ma10, lineColors.ma10),
        ma20: addLineSeries(chart, initialChartData.ma20, lineColors.ma20),
        ma60: addLineSeries(chart, initialChartData.ma60, lineColors.ma60),
      };
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
      volumeSeriesRef.current = volumeSeries;
      volumeSeries.setData(initialChartData.volume);
      const panes = chart.panes();
      panes[0]?.setStretchFactor(4);
      panes[1]?.setStretchFactor(1.1);
    }

    // 拖动垂直线 / 文字时用得上：横向坐标 → 最近一根 K 线的日期
    dateAtXRef.current = (x: number) => {
      const logical = chart.timeScale().coordinateToLogical(x);
      if (logical === null) {
        return null;
      }
      const currentCandles = candlesRef.current;
      const index = Math.max(
        0,
        Math.min(currentCandles.length - 1, Math.round(Number(logical))),
      );
      return currentCandles[index]?.date ?? null;
    };
    const handleCrosshairMove = (param: MouseEventParams<Time>) => {
      if (!param.point || param.time === undefined) {
        activePriceRef.current = null;
        activeCandleChangeRef.current?.(null, null);
        return;
      }
      const price = candleSeries.coordinateToPrice(param.point.y);
      activePriceRef.current = typeof price === "number" && Number.isFinite(price) ? price : null;
      const key = axis.fromTime(param.time);
      const currentCandles = candlesRef.current;
      const candleIndexByDate = new Map(
        currentCandles.map((candle, index) => [candle.date, index]),
      );
      const index = key === null ? undefined : candleIndexByDate.get(key);
      activeCandleChangeRef.current?.(
        index === undefined ? null : currentCandles[index],
        index ?? null,
      );
      refreshAnnotationPositionsRef.current();
    };
    const handleChartClick = (param: MouseEventParams<Time>) => {
      if (!enablePriceLineActions) {
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
      const clickedVline = nearestVerticalLine(param.point.x, vlinePositionsRef.current);
      const clickedTextNote = clickedVline
        ? null
        : nearestTextNote(param.point, textPositionsRef.current);
      const clickedLine = clickedVline || clickedTextNote
        ? null
        : nearestPriceLine(price, activePriceLinesRef.current);
      const candleIndexByDate = new Map(
        candlesRef.current.map((candle, index) => [candle.date, index]),
      );
      const clickedKey = param.time === undefined ? null : axis.fromTime(param.time);
      const date =
        clickedKey !== null && candleIndexByDate.has(clickedKey) ? clickedKey : undefined;
      const clickedBox =
        clickedVline || clickedTextNote || clickedLine
          ? null
          : nearestPriceBox(price, date, activePriceBoxesRef.current, candleIndexByDate);
      const clickedText = clickedTextNote
        ? activeTextNotesRef.current.find((note) => note.id === clickedTextNote.id)
        : undefined;
      const clickedVertical = clickedVline
        ? activeVerticalLinesRef.current.find((line) => line.id === clickedVline.id)
        : undefined;
      setActionMenu({
        boxId: clickedBox?.id,
        date,
        x: param.point.x,
        y: param.point.y,
        mode: clickedVertical
          ? "vline"
          : clickedTextNote
            ? "text"
            : clickedLine
              ? "priceLine"
              : clickedBox
                ? "box"
                : "choose",
        price: clickedText?.price ?? clickedLine?.price ?? clickedBox?.top ?? roundPrice(price),
        lineId: clickedLine?.id,
        textId: clickedTextNote?.id,
        vlineId: clickedVertical?.id,
      });
    };
    chart.subscribeCrosshairMove(handleCrosshairMove);
    chart.subscribeClick(handleChartClick);
    // 缩放 / 平移会让"按坐标画"的标注（垂直线、文字）错位：跟随可视区间重算
    const handleVisibleRangeChange = () => refreshAnnotationPositionsRef.current();
    chart.timeScale().subscribeVisibleLogicalRangeChange(handleVisibleRangeChange);
    // 行情图每次数据变化都拉回全览（改动前的行为）；
    // 训练图（keepViewportOnUpdate）只追加一根，保持"贴右边缘"的默认视野，
    // 否则每 reveal 一根都会被 fitContent 拉回全览，缩放着看盘就废了。
    if (!keepViewportOnUpdate) {
      chart.timeScale().fitContent();
    }
    window.setTimeout(() => refreshAnnotationPositionsRef.current(), 0);

    return () => {
      chart.unsubscribeCrosshairMove(handleCrosshairMove);
      chart.unsubscribeClick(handleChartClick);
      chart.timeScale().unsubscribeVisibleLogicalRangeChange(handleVisibleRangeChange);
      candleSeriesRef.current = null;
      volumeSeriesRef.current = null;
      movingAverageSeriesRef.current = {};
      seriesMarkersRef.current = null;
      chartInstanceRef.current = null;
      coordinateToPriceRef.current = () => null;
      dateAtXRef.current = () => null;
      priceLineRefs.current = [];
      lastPriceLineRef.current = null;
      chart.remove();
    };
  }, [
    axis,
    crosshairLabels,
    enablePriceLineActions,
    height,
    keepViewportOnUpdate,
    showMovingAverages,
    showVolume,
  ]);

  // 行情推进只更新现有 series，绝不销毁图表。这样缩放位置、十字线和用户标注都会
  // 留在原实例上；训练每次追加一根 K 线时，水平线也不会因 series 换绑而消失。
  useEffect(() => {
    const candleSeries = candleSeriesRef.current;
    if (!candleSeries) {
      return;
    }
    candleSeries.setData(chartData.candles);
    volumeSeriesRef.current?.setData(chartData.volume);
    movingAverageSeriesRef.current.ma5?.setData(chartData.ma5);
    movingAverageSeriesRef.current.ma10?.setData(chartData.ma10);
    movingAverageSeriesRef.current.ma20?.setData(chartData.ma20);
    movingAverageSeriesRef.current.ma60?.setData(chartData.ma60);
    seriesMarkersRef.current?.setMarkers(chartMarkers);
    refreshAnnotationPositionsRef.current();
  }, [chartData, chartMarkers]);

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
        lineWidth: (priceLine.width ?? defaultLineWidth) as LineWidth,
        lineStyle: LineStyle.Solid,
        axisLabelVisible: true,
        // 线上文字由我们自己的标签渲染（显示标题），库自带的标题就留空
        title: "",
      }),
    );
    refreshAnnotationPositionsRef.current();
  }, [activePriceLines]);

  // 最新价虚线（训练图用）：只有宿主显式传 ``lastPriceLine`` 才画。
  useEffect(() => {
    const candleSeries = candleSeriesRef.current;
    if (!candleSeries) {
      return;
    }
    if (lastPriceLineRef.current) {
      candleSeries.removePriceLine(lastPriceLineRef.current);
      lastPriceLineRef.current = null;
    }
    if (!lastPriceLine) {
      return;
    }
    lastPriceLineRef.current = createLastPriceLine(candleSeries, lastPriceLine);
  }, [lastPriceLine]);

  /**
   * 收尾：清掉长按定时器并结束拖动。
   *
   * 松手必须走这里，不能只靠 window 上的 pointerup —— 组件里的 pointerup 处理器会
   * ``stopPropagation()``，而 React 把监听挂在 root 容器上，原生事件到 root 就被截住，
   * 冒不到 window，拖动会一直粘着鼠标。
   */
  const endAnnotationPress = useCallback(() => {
    if (pressRef.current) {
      window.clearTimeout(pressRef.current.timer);
      pressRef.current = null;
    }
    setDragging(null);
  }, []);

  /** 长按成立时把那一层的几何记下来，后面按指针位移换算。 */
  const buildDragSession = (
    target: AnnotationTarget,
    startX: number,
    startY: number,
  ): DragSession => {
    const box =
      target.kind === "box"
        ? activePriceBoxesRef.current.find((item) => item.id === target.id)
        : undefined;
    const position = box ? boxPositions.find((item) => item.id === target.id) : undefined;
    const timeScale = chartInstanceRef.current?.timeScale();
    // 没有左右边界的老矩形按整幅图宽算：第一次拖左右边就把边界实体化
    const fromDate = box?.from ?? candles[0]?.date ?? "";
    const toDate = box?.to ?? candles.at(-1)?.date ?? "";
    return {
      startBottomPrice: box ? Math.min(box.top, box.bottom) : 0,
      startBottomY: position?.bottom ?? 0,
      startFromDate: fromDate,
      startLeftX:
        position?.left ?? Number(timeScale?.timeToCoordinate(axis.toTime(fromDate)) ?? 0),
      startRightX:
        position?.right ?? Number(timeScale?.timeToCoordinate(axis.toTime(toDate)) ?? 0),
      startToDate: toDate,
      startTopPrice: box ? Math.max(box.top, box.bottom) : 0,
      startTopY: position?.top ?? 0,
      startX,
      startY,
      target,
    };
  };

  useEffect(() => {
    if (!dragging) {
      return undefined;
    }
    const { target } = dragging;
    const handlePointerMove = (event: PointerEvent) => {
      if (!chartRef.current) {
        return;
      }
      const rect = chartRef.current.getBoundingClientRect();
      const point = { x: event.clientX - rect.left, y: event.clientY - rect.top };

      if (target.kind === "line") {
        const price = coordinateToPriceRef.current(point.y);
        if (price === null) {
          return;
        }
        updatePriceLines(
          activePriceLinesRef.current.map((line) =>
            line.id === target.id
              ? { ...line, kind: "price", price: roundPrice(price) }
              : line,
          ),
        );
        return;
      }

      if (target.kind === "box") {
        const mode = target.mode ?? "move";
        let nextTop: number | null = dragging.startTopPrice;
        let nextBottom: number | null = dragging.startBottomPrice;
        let nextFrom = dragging.startFromDate;
        let nextTo = dragging.startToDate;

        if (mode === "left") {
          nextFrom = dateAtXRef.current(point.x) ?? nextFrom;
        } else if (mode === "right") {
          nextTo = dateAtXRef.current(point.x) ?? nextTo;
        } else if (mode === "move") {
          // 整体平移：上下按价格、左右按 K 线
          const deltaY = point.y - dragging.startY;
          const deltaX = point.x - dragging.startX;
          nextTop = coordinateToPriceRef.current(dragging.startTopY + deltaY);
          nextBottom = coordinateToPriceRef.current(dragging.startBottomY + deltaY);
          nextFrom = dateAtXRef.current(dragging.startLeftX + deltaX) ?? nextFrom;
          nextTo = dateAtXRef.current(dragging.startRightX + deltaX) ?? nextTo;
        } else {
          const pointerPrice = coordinateToPriceRef.current(point.y);
          if (mode === "top") {
            nextTop = pointerPrice;
          } else {
            nextBottom = pointerPrice;
          }
        }

        if (nextTop === null || nextBottom === null) {
          return;
        }
        const prices = normalizeBoxPrices(nextTop, nextBottom);
        const dates = normalizeBoxDates(nextFrom, nextTo, candleOrder);
        updatePriceBoxes(
          activePriceBoxesRef.current.map((box) =>
            box.id === target.id
              ? { ...box, bottom: prices.bottom, from: dates.from, to: dates.to, top: prices.top }
              : box,
          ),
        );
        return;
      }

      if (target.kind === "vline") {
        // 垂直线只左右挪：改它钉在哪一根上，纵向没有可动的位置
        const date = dateAtXRef.current(point.x);
        if (!date) {
          return;
        }
        updateVerticalLines(
          activeVerticalLinesRef.current.map((line) =>
            line.id === target.id ? { ...line, date } : line,
          ),
        );
        return;
      }

      const date = dateAtXRef.current(point.x);
      const price = coordinateToPriceRef.current(point.y);
      if (!date || price === null) {
        return;
      }
      const roundedPrice = roundPrice(price);
      updateTextNotes(
        activeTextNotesRef.current.map((note) =>
          note.id === target.id ? { ...note, date, price: roundedPrice } : note,
        ),
      );
    };
    const handlePointerUp = () => endAnnotationPress();

    // pointerup 兜底之外，指针被系统取消、窗口失焦（拖到浏览器外面松手）也都收尾，
    // 免得残留一个还在跟鼠标的拖动。
    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerup", handlePointerUp, { once: true });
    window.addEventListener("pointercancel", handlePointerUp, { once: true });
    window.addEventListener("blur", handlePointerUp, { once: true });
    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerup", handlePointerUp);
      window.removeEventListener("pointercancel", handlePointerUp);
      window.removeEventListener("blur", handlePointerUp);
    };
  }, [
    candleOrder,
    dragging,
    endAnnotationPress,
    updatePriceBoxes,
    updatePriceLines,
    updateTextNotes,
    updateVerticalLines,
  ]);

  /** 短按 = 选中 + 弹编辑框。 */
  const openAnnotationEditor = (target: AnnotationTarget, x: number, y: number) => {
    if (target.kind === "line") {
      const line = activePriceLines.find((item) => item.id === target.id);
      if (!line) {
        return;
      }
      setActionMenu({ lineId: line.id, mode: "priceLine", price: line.price, x, y });
      return;
    }
    if (target.kind === "box") {
      const box = activePriceBoxes.find((item) => item.id === target.id);
      if (!box) {
        return;
      }
      setActionMenu({ boxId: box.id, mode: "box", price: box.top, x, y });
      return;
    }
    if (target.kind === "vline") {
      const line = activeVerticalLines.find((item) => item.id === target.id);
      if (!line) {
        return;
      }
      setActionMenu({
        mode: "vline",
        price: activePriceRef.current ?? undefined,
        vlineId: line.id,
        x,
        y,
      });
      return;
    }
    const note = activeTextNotes.find((item) => item.id === target.id);
    if (!note) {
      return;
    }
    setActionMenu({ mode: "text", price: note.price, textId: note.id, x, y });
  };

  /**
   * 按住标注：光标变手形（grab），继续按住 longPressMs 就进入拖动；
   * 短按松开则是"选中 + 编辑"。指针按下即捕获，保证松手一定回到这里收尾。
   */
  const handleAnnotationPointerDown = (
    event: ReactPointerEvent<HTMLElement>,
    target: AnnotationTarget,
  ) => {
    if (event.button !== 0) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.setPointerCapture(event.pointerId);
    endAnnotationPress();
    const rect = chartRef.current?.getBoundingClientRect();
    const startX = event.clientX - (rect?.left ?? 0);
    const startY = event.clientY - (rect?.top ?? 0);
    const timer = window.setTimeout(() => {
      const press = pressRef.current;
      if (!press || press.target.id !== target.id) {
        return;
      }
      press.longPressed = true;
      setActionMenu(null);
      setDragging(buildDragSession(target, startX, startY));
    }, longPressMs);
    pressRef.current = { longPressed: false, startX, startY, target, timer };
    setActionMenu(null);
  };

  const handleAnnotationPointerUp = (
    event: ReactPointerEvent<HTMLElement>,
    target: AnnotationTarget,
  ) => {
    event.stopPropagation();
    const press = pressRef.current;
    if (!press || press.target.id !== target.id) {
      endAnnotationPress();
      return;
    }
    const wasDragging = press.longPressed;
    endAnnotationPress();
    if (wasDragging) {
      return;
    }
    const rect = chartRef.current?.getBoundingClientRect();
    openAnnotationEditor(
      target,
      event.clientX - (rect?.left ?? 0),
      event.clientY - (rect?.top ?? 0),
    );
  };

  // 四个"添加"都是**点完即画**：用点击位置的价格 / 日期落一个默认标注，不再弹二次表单。
  // 想改就先点中画出来的那层，再进编辑面板（见各 mode 分支）。
  const handleAddPriceLine = () => {
    if (!actionMenu) {
      return;
    }
    const price = actionMenu.price;
    if (price === undefined || !Number.isFinite(price)) {
      return;
    }
    updatePriceLines([
      ...activePriceLines,
      {
        id: `price_line_${Date.now()}_${activePriceLines.length}`,
        kind: "price",
        color: lineColor,
        price: roundPrice(price),
        title: defaultLineName,
        width: lineWidth,
      },
    ]);
    setActionMenu(null);
  };

  const handleAddPriceBox = () => {
    if (!actionMenu) {
      return;
    }
    const price = actionMenu.price;
    if (price === undefined || !Number.isFinite(price)) {
      return;
    }
    const halfHeight = Math.max(Math.abs(price) * 0.03, 0.03);
    const { top, bottom } = normalizeBoxPrices(price + halfHeight, price - halfHeight);
    // 默认左右各留 defaultBoxHalfBars 根，四条边都能再拖；
    // 点在 K 线右侧空白处（没有对应的那一根）时贴着最后一根落，别落成"整幅图宽"
    const index =
      actionMenu.date === undefined
        ? candles.length - 1
        : (candleOrder.get(actionMenu.date) ?? candles.length - 1);
    const fromIndex = index < 0 ? -1 : Math.max(0, index - defaultBoxHalfBars);
    const toIndex = index < 0 ? -1 : Math.min(candles.length - 1, index + defaultBoxHalfBars);
    const from = fromIndex < 0 ? undefined : candles[fromIndex]?.date;
    const to = toIndex < 0 ? undefined : candles[toIndex]?.date;
    updatePriceBoxes([
      ...activePriceBoxes,
      {
        id: `price_box_${Date.now()}_${activePriceBoxes.length}`,
        bottom,
        color: boxColor,
        from,
        title: defaultBoxName,
        to,
        top,
        width: boxWidth,
      },
    ]);
    setActionMenu(null);
  };

  const handleAddVerticalLine = () => {
    const date = actionMenu?.date;
    if (!date || !candleKeys.has(date)) {
      return;
    }
    updateVerticalLines([
      ...activeVerticalLines,
      {
        id: `vline_${Date.now()}_${activeVerticalLines.length}`,
        color: vlineColor,
        date,
        title: defaultVerticalLineName,
        width: vlineWidth,
      },
    ]);
    setActionMenu(null);
  };

  const handleAddTextNote = () => {
    if (!actionMenu) {
      return;
    }
    const date = actionMenu.date;
    const price = actionMenu.price;
    if (!date || !candleKeys.has(date) || price === undefined || !Number.isFinite(price)) {
      return;
    }
    updateTextNotes([
      ...activeTextNotes,
      {
        id: `text_${Date.now()}_${activeTextNotes.length}`,
        bold: textBold,
        color: textColor,
        date,
        price: roundPrice(price),
        text: defaultTextNoteText,
      },
    ]);
    setActionMenu(null);
  };

  const handleViewIntraday = () => {
    const date = actionMenu?.date;
    if (!date || !viewIntradayRef.current) {
      return;
    }
    viewIntradayRef.current(date);
    setActionMenu(null);
  };

  const actionMenuMaxLeft = Math.max(8, (chartRef.current?.clientWidth ?? 720) - 232);
  const actionMenuMaxTop = Math.max(8, height - (actionMenu?.mode === "choose" ? 320 : 260));
  const hasDate = actionMenu?.date !== undefined;
  const vlineDateKey = axis.parseKey(vlineDate);
  const textNoteDateKey = axis.parseKey(textNoteDate);
  const vlineDateValid = vlineDateKey !== null && candleKeys.has(vlineDateKey);
  const textNoteDateValid = textNoteDateKey !== null && candleKeys.has(textNoteDateKey);
  /** 当前"选中"的标注：拖动中就是被拖的那层，否则是编辑框对应的那层。 */
  const selectedTarget: AnnotationTarget | null = dragging
    ? dragging.target
    : actionMenu?.lineId
      ? { id: actionMenu.lineId, kind: "line" }
      : actionMenu?.boxId
        ? { id: actionMenu.boxId, kind: "box" }
        : actionMenu?.vlineId
          ? { id: actionMenu.vlineId, kind: "vline" }
          : actionMenu?.textId
            ? { id: actionMenu.textId, kind: "text" }
            : null;
  const isSelected = (kind: AnnotationKind, id: string) =>
    selectedTarget?.kind === kind && selectedTarget.id === id;
  const isDragging = (kind: AnnotationKind, id: string) =>
    dragging?.target.kind === kind && dragging.target.id === id;

  return (
    <div className={cn("relative min-w-0 overflow-hidden", className)}>
      <div
        ref={chartRef}
        aria-label={ariaLabel}
        role="img"
        style={{ height }}
      />
      {/* 可拖拽的标注层统一 z-[3]：图表给每块 pane 的 topCanvas 设了 z-index: 2，
          压不过它就拿不到指针事件（垂直线曾经就是这个原因拖不动）。 */}
      {enablePriceLineActions
        ? boxPositions.map((position) => {
            const box = activePriceBoxes.find((item) => item.id === position.id);
            if (!box) {
              return null;
            }
            const color = box.color ?? defaultBoxColor;
            const strokeWidth = box.width ?? defaultBoxWidth;
            const selected = isSelected("box", box.id);
            const active = isDragging("box", box.id);
            const topPrice = formatPrice(Math.max(box.top, box.bottom));
            const bottomPrice = formatPrice(Math.min(box.top, box.bottom));
            // 有左右边界就按日期定位，否则退回整幅图宽（左右边界拖动时会实体化）
            const hasSides = position.left !== null && position.right !== null;
            const boxLeft = hasSides ? Number(position.left) : 12;
            const boxWidth = hasSides
              ? Math.max(2, Number(position.right) - Number(position.left))
              : "calc(100% - 76px)";
            // 抓取条平时完全透明（只负责接指针），hover / 拖动时才浮出来。
            // 注意别给它们加边框：Tailwind preflight 默认 border-style: solid，
            // 四条条各画一圈边，拼起来就是框外那一圈"重影"。
            const edgeClass = "absolute rounded opacity-0 transition-opacity hover:opacity-100";
            const edgeStyle = { backgroundColor: `${color}33` };
            const activeEdge = active ? dragging?.target.mode : null;
            return (
              <div
                key={box.id}
                aria-label={`${box.title ?? defaultBoxName} ${topPrice}-${bottomPrice}`}
                className={cn(
                  "absolute z-[3] touch-none select-none rounded",
                  active ? "cursor-grabbing" : "cursor-grab",
                )}
                onPointerCancel={endAnnotationPress}
                onPointerDown={(event) =>
                  handleAnnotationPointerDown(event, { id: box.id, kind: "box", mode: "move" })
                }
                onPointerUp={(event) =>
                  handleAnnotationPointerUp(event, { id: box.id, kind: "box" })
                }
                role="button"
                style={{
                  backgroundColor: `${color}1a`,
                  borderColor: color,
                  borderStyle: "solid",
                  borderWidth: strokeWidth,
                  boxShadow: selected ? `0 0 0 2px ${color}55` : undefined,
                  height: Math.max(10, position.bottom - position.top),
                  left: boxLeft,
                  top: position.top,
                  width: boxWidth,
                }}
                tabIndex={0}
              >
                <button
                  aria-label={`调整${box.title ?? defaultBoxName}上沿`}
                  className={cn(
                    edgeClass,
                    "left-0 right-0 top-0 h-3 -translate-y-1/2 cursor-ns-resize",
                    activeEdge === "top" ? "opacity-100" : null,
                  )}
                  onPointerDown={(event) =>
                    handleAnnotationPointerDown(event, { id: box.id, kind: "box", mode: "top" })
                  }
                  onPointerUp={(event) =>
                    handleAnnotationPointerUp(event, { id: box.id, kind: "box" })
                  }
                  style={edgeStyle}
                  type="button"
                />
                <button
                  aria-label={`调整${box.title ?? defaultBoxName}下沿`}
                  className={cn(
                    edgeClass,
                    "bottom-0 left-0 right-0 h-3 translate-y-1/2 cursor-ns-resize",
                    activeEdge === "bottom" ? "opacity-100" : null,
                  )}
                  onPointerDown={(event) =>
                    handleAnnotationPointerDown(event, { id: box.id, kind: "box", mode: "bottom" })
                  }
                  onPointerUp={(event) =>
                    handleAnnotationPointerUp(event, { id: box.id, kind: "box" })
                  }
                  style={edgeStyle}
                  type="button"
                />
                <button
                  aria-label={`调整${box.title ?? defaultBoxName}左边界`}
                  className={cn(
                    edgeClass,
                    "bottom-0 left-0 top-0 w-3 -translate-x-1/2 cursor-ew-resize",
                    activeEdge === "left" ? "opacity-100" : null,
                  )}
                  onPointerDown={(event) =>
                    handleAnnotationPointerDown(event, { id: box.id, kind: "box", mode: "left" })
                  }
                  onPointerUp={(event) =>
                    handleAnnotationPointerUp(event, { id: box.id, kind: "box" })
                  }
                  style={edgeStyle}
                  type="button"
                />
                <button
                  aria-label={`调整${box.title ?? defaultBoxName}右边界`}
                  className={cn(
                    edgeClass,
                    "bottom-0 right-0 top-0 w-3 translate-x-1/2 cursor-ew-resize",
                    activeEdge === "right" ? "opacity-100" : null,
                  )}
                  onPointerDown={(event) =>
                    handleAnnotationPointerDown(event, { id: box.id, kind: "box", mode: "right" })
                  }
                  onPointerUp={(event) =>
                    handleAnnotationPointerUp(event, { id: box.id, kind: "box" })
                  }
                  style={edgeStyle}
                  type="button"
                />
                <div
                  className="pointer-events-none absolute left-2 top-1 max-w-[calc(100%-16px)] truncate rounded border bg-white/85 px-1.5 py-0.5 text-[10px] font-semibold shadow-sm"
                  style={{ borderColor: color, color }}
                >
                  {box.title?.trim() || defaultBoxName}
                </div>
              </div>
            );
          })
        : null}
      {enablePriceLineActions
        ? linePositions.map((position) => {
            const line = activePriceLines.find((item) => item.id === position.id);
            if (!line) {
              return null;
            }
            const color = line.color ?? priceLineColor(line.title);
            const title = line.title?.trim() || defaultLineName;
            // 线上只写标题（价格看右侧价格轴），避免一条线上一串数字
            const ariaLabel = `${title} ${formatPrice(line.price)}`;
            const selected = isSelected("line", line.id);
            const active = isDragging("line", line.id);
            const top = Math.max(10, position.y);
            return (
              <div key={line.id}>
                <div
                  aria-label={ariaLabel}
                  className={cn(
                    "absolute left-0 right-16 z-[3] h-2 -translate-y-1/2 touch-none",
                    active ? "cursor-grabbing" : "cursor-grab",
                  )}
                  onPointerCancel={endAnnotationPress}
                  onPointerDown={(event) =>
                    handleAnnotationPointerDown(event, { id: line.id, kind: "line" })
                  }
                  onPointerUp={(event) =>
                    handleAnnotationPointerUp(event, { id: line.id, kind: "line" })
                  }
                  role="button"
                  style={{
                    backgroundColor: selected ? `${color}2e` : undefined,
                    boxShadow: selected ? `inset 0 0 0 1px ${color}` : undefined,
                    top,
                  }}
                  tabIndex={0}
                />
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      aria-label={ariaLabel}
                      className={cn(
                        "absolute left-3 z-10 h-5 max-w-[120px] -translate-y-1/2 truncate rounded border bg-white/80 px-1.5 text-[10px] font-semibold shadow-sm backdrop-blur-sm",
                        active ? "cursor-grabbing" : "cursor-grab",
                      )}
                      onPointerCancel={endAnnotationPress}
                      onPointerDown={(event) =>
                        handleAnnotationPointerDown(event, { id: line.id, kind: "line" })
                      }
                      onPointerUp={(event) =>
                        handleAnnotationPointerUp(event, { id: line.id, kind: "line" })
                      }
                      style={{
                        borderColor: selected ? color : `${color}88`,
                        color,
                        top,
                      }}
                      type="button"
                    >
                      {title}
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>{title}</TooltipContent>
                </Tooltip>
              </div>
            );
          })
        : null}
      {enablePriceLineActions
        ? vlinePositions.map((position) => {
            const line = activeVerticalLines.find((item) => item.id === position.id);
            if (!line) {
              return null;
            }
            const color = line.color ?? defaultVerticalLineColor;
            const strokeWidth = line.width ?? defaultVerticalLineWidth;
            const selected = isSelected("vline", line.id);
            const active = isDragging("vline", line.id);
            return (
              <div
                key={line.id}
                aria-label={`${line.title ?? defaultVerticalLineName} ${line.date}`}
                className={cn(
                  "absolute bottom-[30px] top-0 z-[3] w-2 -translate-x-1/2 touch-none rounded-full",
                  active ? "cursor-grabbing" : "cursor-grab",
                )}
                onPointerCancel={endAnnotationPress}
                onPointerDown={(event) =>
                  handleAnnotationPointerDown(event, { id: line.id, kind: "vline" })
                }
                onPointerUp={(event) =>
                  handleAnnotationPointerUp(event, { id: line.id, kind: "vline" })
                }
                role="button"
                style={{
                  backgroundColor: selected ? `${color}2e` : undefined,
                  left: position.x,
                }}
                tabIndex={0}
              >
                <span
                  className="pointer-events-none absolute inset-y-0 left-1/2 -translate-x-1/2 rounded-full"
                  style={{ backgroundColor: color, width: strokeWidth }}
                />
                <span
                  className="pointer-events-none absolute left-2 top-1 whitespace-nowrap rounded border bg-white/85 px-1.5 py-0.5 text-[10px] font-semibold shadow-sm"
                  style={{ borderColor: color, color }}
                >
                  {line.title?.trim() || defaultVerticalLineName}
                </span>
              </div>
            );
          })
        : null}
      {enablePriceLineActions
        ? textPositions.map((position) => {
            const note = activeTextNotes.find((item) => item.id === position.id);
            if (!note) {
              return null;
            }
            const color = note.color ?? defaultTextNoteColor;
            const selected = isSelected("text", note.id);
            const active = isDragging("text", note.id);
            return (
              <div
                key={note.id}
                aria-label={`文字 ${note.text}`}
                className={cn(
                  "absolute z-[3] touch-none",
                  active ? "cursor-grabbing" : "cursor-grab",
                )}
                onPointerCancel={endAnnotationPress}
                onPointerDown={(event) =>
                  handleAnnotationPointerDown(event, { id: note.id, kind: "text" })
                }
                onPointerUp={(event) =>
                  handleAnnotationPointerUp(event, { id: note.id, kind: "text" })
                }
                role="button"
                style={{ left: position.x, top: position.y }}
                tabIndex={0}
              >
                <span
                  className="pointer-events-none absolute left-0 top-0 h-1 w-1 -translate-x-1/2 -translate-y-1/2 rounded-full"
                  style={{ backgroundColor: color }}
                />
                <span
                  className={cn(
                    "block -translate-y-full whitespace-nowrap rounded border bg-white/90 px-1.5 py-0.5 text-[10px] shadow-sm",
                    note.bold ?? true ? "font-bold" : "font-normal",
                  )}
                  style={{
                    borderColor: color,
                    boxShadow: selected ? `0 0 0 2px ${color}55` : undefined,
                    color,
                  }}
                >
                  {note.text}
                </span>
              </div>
            );
          })
        : null}
      {enablePriceLineActions && actionMenu ? (
        <div
          className="absolute z-20 w-56 rounded-md border border-line bg-white p-2 text-xs shadow-lg"
          style={{
            left: Math.min(Math.max(8, actionMenu.x + 8), actionMenuMaxLeft),
            top: Math.min(Math.max(8, actionMenu.y - 12), actionMenuMaxTop),
          }}
        >
          {actionMenu.mode === "choose" ? (
            <>
              <div className="mb-2 flex items-center justify-between gap-2">
                <span className="font-semibold text-ink">添加标注</span>
                <span className="font-mono text-[11px] text-mutedText">
                  {formatPrice(actionMenu.price ?? 0)}
                </span>
              </div>
              <div className="grid gap-2">
                <Button
                  className="h-8 justify-start gap-2 text-xs"
                  onClick={handleAddPriceLine}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <Minus className="h-4 w-4" />
                  水平线
                </Button>
                <Button
                  className="h-8 justify-start gap-2 text-xs"
                  disabled={!hasDate}
                  onClick={handleAddVerticalLine}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <Minus className="h-4 w-4 rotate-90" />
                  垂直线
                </Button>
                <Button
                  className="h-8 justify-start gap-2 text-xs"
                  onClick={handleAddPriceBox}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <Square className="h-4 w-4" />
                  矩形
                </Button>
                <Button
                  className="h-8 justify-start gap-2 text-xs"
                  disabled={!hasDate}
                  onClick={handleAddTextNote}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <Type className="h-4 w-4" />
                  文字
                </Button>
                {onViewIntraday ? (
                  <Button
                    className="h-8 justify-start gap-2 text-xs"
                    disabled={!hasDate}
                    onClick={handleViewIntraday}
                    size="sm"
                    type="button"
                    variant="outline"
                  >
                    <LineChart className="h-4 w-4" />
                    查看分时
                  </Button>
                ) : null}
                <Button
                  className="h-8 justify-start gap-2 text-xs"
                  onClick={() => setActionMenu(null)}
                  size="sm"
                  type="button"
                  variant="ghost"
                >
                  <X className="h-4 w-4" />
                  取消
                </Button>
              </div>
            </>
          ) : null}

          {actionMenu.mode === "priceLine" ? (
            <>
              <div className="mb-2 flex items-center justify-between gap-2">
                <span className="font-semibold text-ink">水平线</span>
                <span className="font-mono text-[11px] text-mutedText">
                  {formatPrice(actionMenu.price ?? 0)}
                </span>
              </div>
              <TitleInput onChange={setLineTitle} value={lineTitle} />
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">颜色</span>
                <ColorSwatches onChange={setLineColor} value={lineColor} />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">粗细</span>
                <WidthOptions onChange={setLineWidth} value={lineWidth} />
              </div>
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
            </>
          ) : null}

          {actionMenu.mode === "box" ? (
            <>
              <div className="mb-2 flex items-center justify-between gap-2">
                <span className="font-semibold text-ink">矩形</span>
                <span className="font-mono text-[11px] text-mutedText">
                  {formatPrice(actionMenu.price ?? 0)}
                </span>
              </div>
              <div className="space-y-2">
                <TitleInput onChange={setBoxTitle} value={boxTitle} />
                <div className="grid grid-cols-2 gap-2">
                  <Input
                    className="h-8 text-xs"
                    inputMode="decimal"
                    onChange={(event) => setBoxTop(event.target.value)}
                    placeholder="上沿"
                    value={boxTop}
                  />
                  <Input
                    className="h-8 text-xs"
                    inputMode="decimal"
                    onChange={(event) => setBoxBottom(event.target.value)}
                    placeholder="下沿"
                    value={boxBottom}
                  />
                </div>
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">颜色</span>
                <ColorSwatches onChange={setBoxColor} value={boxColor} />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">粗细</span>
                <WidthOptions onChange={setBoxWidth} value={boxWidth} />

              </div>
              <div className="mt-2 grid grid-cols-3 gap-2">
                <Button
                  className="h-8 text-xs"
                  onClick={handleSavePriceBox}
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
                  onClick={() => handleRemovePriceBox(actionMenu.boxId as string)}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <X className="h-3.5 w-3.5" />
                  删除
                </Button>
              </div>
            </>
          ) : null}

          {actionMenu.mode === "vline" ? (
            <>
              <div className="mb-2 flex items-center justify-between gap-2">
                <span className="font-semibold text-ink">垂直线</span>
                <span className="font-mono text-[11px] text-mutedText">
                  {vlineDate.trim() ||
                    (actionMenu.date === undefined ? "--" : axis.formatKey(actionMenu.date))}
                </span>
              </div>
              <div className="space-y-2">
                <TitleInput onChange={setVlineTitle} value={vlineTitle} />
                <Input
                  className="h-8 text-xs"
                  onChange={(event) => setVlineDate(event.target.value)}
                  placeholder={axis.keyPlaceholder ?? "日期"}
                  value={vlineDate}
                />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">颜色</span>
                <ColorSwatches onChange={setVlineColor} value={vlineColor} />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">粗细</span>
                <WidthOptions onChange={setVlineWidth} value={vlineWidth} />

              </div>
              <div className="mt-2 grid grid-cols-3 gap-2">
                <Button
                  className="h-8 text-xs"
                  disabled={!vlineDateValid}
                  onClick={handleSaveVerticalLine}
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
                  onClick={() => handleRemoveVerticalLine(actionMenu.vlineId as string)}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <X className="h-3.5 w-3.5" />
                  删除
                </Button>
              </div>
            </>
          ) : null}

          {actionMenu.mode === "text" ? (
            <>
              <div className="mb-2 flex items-center justify-between gap-2">
                <span className="font-semibold text-ink">文字</span>
                <span className="font-mono text-[11px] text-mutedText">
                  {textNoteDate.trim() ||
                    (actionMenu.date === undefined ? "--" : axis.formatKey(actionMenu.date))}
                </span>
              </div>
              <div className="space-y-2">
                <Input
                  className="h-8 text-xs"
                  onChange={(event) => setTextNoteText(event.target.value)}
                  placeholder="输入文字"
                  value={textNoteText}
                />
                <Input
                  className="h-8 text-xs"
                  onChange={(event) => setTextNoteDate(event.target.value)}
                  placeholder={axis.keyPlaceholder ?? "日期"}
                  value={textNoteDate}
                />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">颜色</span>
                <ColorSwatches onChange={setTextColor} value={textColor} />
              </div>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-[11px] text-mutedText">粗细</span>
                <TextWeightOptions onChange={setTextBold} value={textBold} />
              </div>
              <div className="mt-2 grid grid-cols-3 gap-2">
                <Button
                  className="h-8 text-xs"
                  disabled={!textNoteDateValid}
                  onClick={handleSaveTextNote}
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
                  onClick={() => handleRemoveTextNote(actionMenu.textId as string)}
                  size="sm"
                  type="button"
                  variant="outline"
                >
                  <X className="h-3.5 w-3.5" />
                  删除
                </Button>
              </div>
            </>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

function TitleInput({
  value,
  onChange,
}: {
  value: string;
  onChange: (title: string) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-2">
      <span className="shrink-0 text-[11px] text-mutedText">标题</span>
      <Input
        className="h-8 max-w-[150px] text-xs"
        onChange={(event) => onChange(event.target.value)}
        placeholder="标题"
        value={value}
      />
    </div>
  );
}

function ColorSwatches({
  value,
  onChange,
}: {
  value: string;
  onChange: (color: string) => void;
}) {
  return (
    <div className="flex items-center gap-1.5">
      {annotationColors.map((color) => (
        <button
          key={color}
          aria-label={`颜色 ${color}`}
          className={cn(
            "h-5 w-5 rounded-full border-2 transition-transform",
            value === color ? "scale-110 border-ink" : "border-transparent",
          )}
          onClick={() => onChange(color)}
          style={{ backgroundColor: color }}
          type="button"
        />
      ))}
    </div>
  );
}

function WidthOptions({
  value,
  onChange,
}: {
  value: number;
  onChange: (width: number) => void;
}) {
  return (
    <div className="flex items-center gap-1">
      {annotationWidths.map((width) => (
        <button
          key={width}
          aria-label={`粗细 ${width}`}
          className={cn(
            "h-6 w-6 rounded border text-[10px] font-semibold",
            value === width
              ? "border-ink bg-ink/5 text-ink"
              : "border-line text-mutedText hover:border-ink/40",
          )}
          onClick={() => onChange(width)}
          type="button"
        >
          {width}
        </button>
      ))}
    </div>
  );
}

function TextWeightOptions({
  value,
  onChange,
}: {
  value: boolean;
  onChange: (bold: boolean) => void;
}) {
  return (
    <div className="flex items-center gap-1">
      {[
        { bold: false, label: "常规" },
        { bold: true, label: "加粗" },
      ].map((item) => (
        <button
          key={item.label}
          className={cn(
            "h-6 rounded border px-2 text-[10px] font-semibold",
            value === item.bold
              ? "border-ink bg-ink/5 text-ink"
              : "border-line text-mutedText hover:border-ink/40",
          )}
          onClick={() => onChange(item.bold)}
          type="button"
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}

/** 最新价虚线：训练图用来标"当前已经揭示到哪一根"的收盘价。 */
function createLastPriceLine(
  candleSeries: ISeriesApi<"Candlestick", Time>,
  lastPrice: LightweightKlineLastPrice,
): IPriceLine {
  return candleSeries.createPriceLine({
    price: lastPrice.price,
    color: lastPrice.color ?? defaultLineColor,
    lineWidth: 1,
    lineStyle: LineStyle.Dashed,
    axisLabelVisible: true,
    title: lastPrice.title ?? "",
  });
}

function toLightweightData(candles: LightweightKlineCandle[], axis: ChartTimeAxis) {
  const candleData: CandlestickData<Time>[] = candles.map((candle) => ({
    time: axis.toTime(candle.date),
    open: candle.open,
    high: candle.high,
    low: candle.low,
    close: candle.close,
  }));
  const volumeData: HistogramData<Time>[] = candles.map((candle) => ({
    time: axis.toTime(candle.date),
    value: candle.volume ?? 0,
    color: candle.close >= candle.open ? "rgba(225, 29, 72, 0.85)" : "rgba(22, 163, 74, 0.85)",
  }));
  return {
    candles: candleData,
    volume: volumeData,
    ma5: movingAverageData(candles, "ma5", axis),
    ma10: movingAverageData(candles, "ma10", axis),
    ma20: movingAverageData(candles, "ma20", axis),
    ma60: movingAverageData(candles, "ma60", axis),
  };
}

function movingAverageData(
  candles: LightweightKlineCandle[],
  key: "ma5" | "ma10" | "ma20" | "ma60",
  axis: ChartTimeAxis,
): LineData<Time>[] {
  return candles
    .filter((candle) => typeof candle[key] === "number" && Number.isFinite(candle[key]))
    .map((candle) => ({
      time: axis.toTime(candle.date),
      value: candle[key] as number,
    }));
}

function addLineSeries(
  chart: ReturnType<typeof createChart>,
  data: LineData<Time>[],
  color: string,
) {
  const series = chart.addSeries(LineSeries, {
    color,
    lineWidth: 1,
    priceLineVisible: false,
    lastValueVisible: false,
    crosshairMarkerVisible: false,
  });
  series.setData(data);
  return series;
}

function toLightweightMarkers(
  markers: LightweightKlineMarker[],
  axis: ChartTimeAxis,
): SeriesMarker<Time>[] {
  return markers.map((marker) => ({
    time: axis.toTime(marker.date),
    position: marker.side === "buy" ? "belowBar" : "aboveBar",
    shape: marker.side === "buy" ? "arrowUp" : "arrowDown",
    color: marker.side === "buy" ? downColor : upColor,
    text: marker.text ?? (marker.side === "buy" ? "B" : "S"),
    size: 1.2,
  }));
}

function nearestVerticalLine(
  x: number,
  vlinePositions: Array<{ id: string; x: number }>,
): { id: string; x: number } | null {
  let nearest: { id: string; x: number } | null = null;
  let nearestDistance = Number.POSITIVE_INFINITY;
  for (const position of vlinePositions) {
    const distance = Math.abs(position.x - x);
    if (distance < nearestDistance) {
      nearest = position;
      nearestDistance = distance;
    }
  }
  return nearest && nearestDistance <= 6 ? nearest : null;
}

function nearestTextNote(
  point: { x: number; y: number },
  textPositions: Array<{ id: string; x: number; y: number }>,
): { id: string; x: number; y: number } | null {
  let nearest: { id: string; x: number; y: number } | null = null;
  let nearestDistance = Number.POSITIVE_INFINITY;
  for (const position of textPositions) {
    // 文字气泡画在锚点上方，命中框跟着气泡走
    const dx = point.x - position.x;
    const dy = point.y - position.y;
    if (dx > 90 || dx < -6 || dy > 6 || dy < -22) {
      continue;
    }
    const distance = Math.hypot(Math.max(dx, 0), dy);
    if (distance < nearestDistance) {
      nearest = position;
      nearestDistance = distance;
    }
  }
  return nearest;
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

function nearestPriceBox(
  price: number,
  date: string | undefined,
  priceBoxes: LightweightKlinePriceBox[],
  candleOrder: Map<string, number>,
): LightweightKlinePriceBox | null {
  const padding = Math.max(Math.abs(price) * 0.003, 0.02);
  for (const box of priceBoxes) {
    const top = Math.max(box.top, box.bottom);
    const bottom = Math.min(box.top, box.bottom);
    if (price < bottom - padding || price > top + padding) {
      continue;
    }
    if (box.from !== undefined && box.to !== undefined && date !== undefined) {
      const order = candleOrder.get(date);
      const fromOrder = candleOrder.get(box.from);
      const toOrder = candleOrder.get(box.to);
      if (order === undefined || fromOrder === undefined || toOrder === undefined) {
        continue;
      }
      if (order < fromOrder || order > toOrder) {
        continue;
      }
    }
    return box;
  }
  return null;
}

/** 把矩形的左右边界按先后摆正（拖过头就互换）。 */
function normalizeBoxDates(first: string, second: string, candleOrder: Map<string, number>) {
  const firstOrder = candleOrder.get(first) ?? 0;
  const secondOrder = candleOrder.get(second) ?? 0;
  return firstOrder <= secondOrder ? { from: first, to: second } : { from: second, to: first };
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

function normalizeBoxPrices(firstPrice: number, secondPrice: number) {
  return {
    top: roundPrice(Math.max(firstPrice, secondPrice)),
    bottom: roundPrice(Math.min(firstPrice, secondPrice)),
  };
}

function formatPrice(value: number): string {
  return value.toFixed(2);
}

function formatEditablePrice(value: number): string {
  return Number.isFinite(value) ? roundPrice(value).toFixed(2) : "";
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
