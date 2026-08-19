import { API_BASE_URL } from "./client";

export type StrategyParamValue = number | string | boolean;
export type StrategyMode = "single_symbol" | "multi_symbol" | "portfolio" | "universe_selection";
export type StrategyJsonValue =
  | string
  | number
  | boolean
  | null
  | StrategyJsonValue[]
  | { [key: string]: StrategyJsonValue };

export type StrategyCustomParameter = {
  name_cn: string;
  name_en: string;
  type: "integer" | "number" | "string" | "boolean";
  default: StrategyParamValue;
  required: boolean;
};

export type StrategySummary = {
  strategy_id: string;
  strategy_version_id: string;
  version: number;
  name: string;
  status: "active" | "archived" | "deleted";
  tags: string[];
  strategy_mode: StrategyMode;
  custom_params: StrategyCustomParameter[];
  updated_at: string;
};

export type StrategyRecord = {
  id: string;
  project_id: string;
  name: string;
  description?: string | null;
  tags: string[];
  current_version_id?: string | null;
  status: "active" | "archived" | "deleted";
  created_at: string;
  updated_at: string;
};

export type StrategyVersion = {
  id: string;
  strategy_id: string;
  version: number;
  source_code: string;
  strategy_mode: StrategyMode;
  custom_params: StrategyCustomParameter[];
  created_at: string;
};

export type StrategyCreatePayload = {
  name: string;
  description: string;
  source_code: string;
  strategy_mode: StrategyMode;
  custom_params?: StrategyCustomParameter[];
  risk_notes: string[];
};

export type StrategyVersionCreatePayload = Omit<StrategyCreatePayload, "name" | "description">;

export type StrategyCreateResult = {
  strategy_id: string;
};

export type StrategyDetail = {
  strategy: StrategyRecord;
};

export type StrategyMetadataUpdate = {
  name?: string;
  description?: string | null;
  tags?: string[];
  status?: StrategyRecord["status"];
};

export type StrategyBacktestConfig = {
  strategy_mode: StrategyMode;
  asset_class: "stock" | "etf" | "index" | "crypto" | "futures";
  market: "CN" | "US" | "HK";
  symbols: string[];
  universe?: string | null;
  benchmark_symbol?: string | null;
  start_date: string;
  end_date: string;
  timeframe?: "1d";
  initial_cash: string;
  commission: string;
  slippage?: string;
  notes?: string[];
  params?: Record<string, StrategyJsonValue>;
};

export type StrategyBacktestStatus = "pending" | "running" | "succeeded" | "failed" | "canceled";

export type StrategyBacktestRecord = {
  id: string;
  project_id: string;
  strategy_id: string;
  strategy_version_id: string;
  status: StrategyBacktestStatus;
  config: StrategyBacktestConfig;
  execution_engine?: string | null;
  result_id?: string | null;
  failure_code?: string | null;
  failure_message?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
};

export type StrategyBacktestMetrics = {
  initial_value: string;
  final_value: string;
  total_return_pct: string;
  annual_return_pct?: string | null;
  max_drawdown_pct: string;
  max_drawdown_start?: string | null;
  max_drawdown_end?: string | null;
  max_drawdown_duration_days?: number | null;
  sharpe_ratio?: string | null;
  win_rate_pct?: string | null;
  total_trades: number;
};

export type StrategyCurvePoint = {
  date: string;
  value: string;
  normalized_value?: string | null;
  extra?: Record<string, StrategyJsonValue>;
};

export type StrategyCurve = {
  id: string;
  strategy_backtest_id: string;
  strategy_backtest_result_id: string;
  curve_type: "equity" | "drawdown";
  point_count: number;
  start_date: string;
  end_date: string;
  points: StrategyCurvePoint[];
  created_at: string;
};

export type StrategyTradeRecord = {
  id: string;
  strategy_backtest_id: string;
  symbol: string;
  side: "buy" | "sell" | "short" | "cover";
  status: "opened" | "closed" | "partial";
  trade_datetime: string;
  price: string;
  size: string;
  value: string;
  commission: string;
  pnl?: string | null;
  pnl_pct?: string | null;
  metadata?: Record<string, StrategyJsonValue>;
};

export type StrategyMarketCandle = {
  symbol: string;
  date: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
};

export type StrategyMarketSeries = {
  symbol: string;
  candles: StrategyMarketCandle[];
};

export type StrategyBenchmarkPoint = {
  date: string;
  value: string;
  normalized_value: string;
};

export type StrategyBenchmarkSeries = {
  symbol: string;
  total_return_pct?: string | null;
  points: StrategyBenchmarkPoint[];
};

export type StrategyDailyPosition = {
  symbol: string;
  size: string;
  close_price: string;
  market_value: string;
  unrealized_pnl?: string | null;
};

export type StrategyDailyPortfolioSnapshot = {
  date: string;
  cash: string;
  total_value: string;
  daily_pnl: string;
  positions: StrategyDailyPosition[];
};

export type StrategyBacktestResult = {
  id: string;
  strategy_backtest_id: string;
  summary: string;
  metrics: StrategyBacktestMetrics;
  trades?: StrategyTradeRecord[];
  curves?: StrategyCurve[];
  market_data?: StrategyMarketSeries[];
  benchmark?: StrategyBenchmarkSeries | null;
  daily_positions?: StrategyDailyPortfolioSnapshot[];
  warnings: string[];
  engine: string;
  protocol: string;
  created_at: string;
};

export type StrategyBacktestDetail = {
  backtest: StrategyBacktestRecord;
  result?: StrategyBacktestResult | null;
};

export type StrategyBacktestPayload = {
  project_id: string;
  config: StrategyBacktestConfig;
  strategy_version_id?: string;
};

export type StrategyBacktestRerunPayload = {
  config: StrategyBacktestConfig;
};

export type StrategyCopySummary = {
  mode: "summary" | "new_strategy";
  source_strategy_version_id: string;
  summary: string;
  target_strategy_id?: string | null;
  copy_record_id: string;
};

type ApiFetchOptions = RequestInit & {
  projectId?: string;
};

export async function listStrategies(projectId?: string): Promise<StrategySummary[]> {
  if (!projectId) {
    return [];
  }
  const params = new URLSearchParams({ project_id: projectId });
  return apiFetch<StrategySummary[]>(`/api/strategies?${params.toString()}`);
}

export async function getStrategy(strategyId: string): Promise<StrategyDetail> {
  return apiFetch<StrategyDetail>(`/api/strategies/${strategyId}`);
}

export async function listStrategyVersions(
  strategyId: string,
): Promise<StrategyVersion[]> {
  return apiFetch<StrategyVersion[]>(`/api/strategies/${strategyId}/versions`);
}

export async function getStrategyVersion(versionId: string): Promise<StrategyVersion> {
  return apiFetch<StrategyVersion>(`/api/strategy-versions/${versionId}`);
}

export async function createStrategy(
  payload: StrategyCreatePayload,
  projectId: string,
): Promise<StrategyCreateResult> {
  return apiFetch<StrategyCreateResult>("/api/strategies", {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      project_id: projectId,
    }),
  });
}

export async function updateStrategyMetadata(
  strategyId: string,
  payload: StrategyMetadataUpdate,
): Promise<StrategyRecord> {
  return apiFetch<StrategyRecord>(`/api/strategies/${strategyId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteStrategy(strategyId: string): Promise<StrategyRecord> {
  return apiFetch<StrategyRecord>(`/api/strategies/${strategyId}`, {
    method: "DELETE",
  });
}

export async function createStrategyVersion(
  strategyId: string,
  payload: StrategyVersionCreatePayload,
): Promise<StrategyVersion> {
  return apiFetch<StrategyVersion>(`/api/strategies/${strategyId}/versions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function switchStrategyCurrentVersion(
  strategyId: string,
  versionId: string,
): Promise<StrategySummary> {
  return apiFetch<StrategySummary>(`/api/strategies/${strategyId}/current-version`, {
    method: "PATCH",
    body: JSON.stringify({ strategy_version_id: versionId }),
  });
}

export async function backtestStrategy(
  strategyId: string,
  payload: StrategyBacktestPayload,
): Promise<StrategyBacktestDetail> {
  return apiFetch<StrategyBacktestDetail>(`/api/strategies/${strategyId}/backtest`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listStrategyBacktests(
  strategyVersionId: string,
): Promise<StrategyBacktestRecord[]> {
  const params = new URLSearchParams({ strategy_version_id: strategyVersionId, limit: "20" });
  return apiFetch<StrategyBacktestRecord[]>(`/api/backtests?${params.toString()}`);
}

export async function getStrategyBacktest(backtestId: string): Promise<StrategyBacktestDetail> {
  return apiFetch<StrategyBacktestDetail>(`/api/backtests/${backtestId}`);
}

export async function rerunStrategyBacktest(
  backtestId: string,
  payload: StrategyBacktestRerunPayload,
): Promise<StrategyBacktestDetail> {
  return apiFetch<StrategyBacktestDetail>(`/api/backtests/${backtestId}/rerun`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function validateStrategyVersion(versionId: string): Promise<unknown> {
  return apiFetch(`/api/strategy-versions/${versionId}/validate`, {
    method: "POST",
  });
}

export async function copyStrategySummary(versionId: string): Promise<StrategyCopySummary> {
  return apiFetch<StrategyCopySummary>(`/api/strategy-versions/${versionId}/copy`, {
    method: "POST",
    body: JSON.stringify({ mode: "summary" }),
  });
}

async function apiFetch<T>(path: string, init?: ApiFetchOptions): Promise<T> {
  const { projectId, headers, ...requestInit } = init ?? {};
  void projectId;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...requestInit,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  });

  if (!response.ok) {
    const message = await readErrorMessage(response);
    throw new Error(message);
  }

  return response.json();
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
