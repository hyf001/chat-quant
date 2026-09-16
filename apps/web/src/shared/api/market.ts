import { API_BASE_URL } from "./client";

export type StockPreviewPeriod = "daily" | "weekly" | "monthly";

export type StockPreviewCandle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number | null;
  turnover?: number | null;
  ma5?: number | null;
  ma10?: number | null;
  ma20?: number | null;
  ma60?: number | null;
};

export type StockPreview = {
  symbol: string;
  name: string;
  period: StockPreviewPeriod;
  trade_date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  prev_close?: number | null;
  change?: number | null;
  pct_change?: number | null;
  volume?: number | null;
  turnover?: number | null;
  candles: StockPreviewCandle[];
  source_dataset: string;
};

export type StockIntradayPoint = {
  /** 分钟标签 ``HH:MM``。 */
  t: string;
  p: number;
  v: number;
};

export type StockIntraday = {
  symbol: string;
  trade_date: string;
  points: StockIntradayPoint[];
  source_dataset: string;
};

export async function getStockPreview(
  symbol: string,
  options: {
    period?: StockPreviewPeriod;
    limit?: number;
  } = {},
): Promise<StockPreview> {
  const params = new URLSearchParams({
    period: options.period ?? "daily",
    limit: String(options.limit ?? 120),
  });
  return marketFetch<StockPreview>(
    `/api/market/stocks/${encodeURIComponent(symbol)}/preview?${params.toString()}`,
  );
}

/** 某一天的 1 分钟分时（K 线上右键菜单的"查看分时"）。 */
export async function getStockIntraday(symbol: string, tradeDate: string): Promise<StockIntraday> {
  const params = new URLSearchParams({ date: tradeDate });
  return marketFetch<StockIntraday>(
    `/api/market/stocks/${encodeURIComponent(symbol)}/intraday?${params.toString()}`,
  );
}

async function marketFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const message = await readErrorMessage(response);
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as { detail?: { message?: string } | string };
    if (typeof payload.detail === "string") {
      return payload.detail;
    }
    return payload.detail?.message ?? `API request failed: ${response.status}`;
  } catch {
    return `API request failed: ${response.status}`;
  }
}
