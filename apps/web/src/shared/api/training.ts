import { API_BASE_URL } from "./client";

export type TrainingAction = "buy" | "sell" | "close" | "cancel" | "hold";
export type TrainingStatus = "active" | "finished";

export type TrainingBar = {
  i: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
};

export type TrainingRevealedBar = TrainingBar & { date: string };

export type TrainingMarker = {
  i: number;
  side: "buy" | "sell";
  text: string;
};

export type TrainingFill = {
  i: number;
  side: "buy" | "sell";
  price: string;
  size: number;
  value: string;
  commission: string;
};

export type TrainingOrderRejection = {
  i: number;
  side: "buy" | "sell";
  size: number;
  reason: string;
};

export type TrainingAccount = {
  initial_cash: string;
  cash: string;
  position_size: number;
  position_price: string;
  position_value: string;
  position_pct: string;
  total_return: string;
  open_return: string;
};

export type TrainingSessionView = {
  id: string;
  status: TrainingStatus;
  instrument_alias: string;
  started_at: string;
  elapsed_seconds: number;
  warmup_bars: number;
  training_bars: number;
  cursor_index: number;
  remaining: number;
  account: TrainingAccount;
};

export type TrainingSession = {
  session: TrainingSessionView;
  bars: TrainingBar[];
  markers: TrainingMarker[];
};

export type TrainingSessionSummary = {
  id: string;
  status: TrainingStatus;
  instrument_alias: string;
  initial_cash: string;
  started_at: string;
  finished_at: string | null;
  elapsed_seconds: number;
  warmup_bars: number;
  training_bars: number | null;
  cursor_index: number;
  remaining: number | null;
};

export type TrainingSessionList = {
  items: TrainingSessionSummary[];
  total: number;
};

export type TrainingReveal = {
  session: TrainingSessionView;
  bar: TrainingBar | null;
  markers: TrainingMarker[];
  fills: TrainingFill[];
  rejected: TrainingOrderRejection[];
};

export type TrainingIntradayPoint = {
  /** 分钟标签 ``HH:MM``：分时轴不带交易日（双盲口径）。 */
  t: string;
  p: number;
  v: number;
};

export type TrainingIntraday = {
  session_id: string;
  seq: number;
  available: boolean;
  bar: TrainingBar | null;
  /** 分时涨跌幅基准：切片里前一根的 close；第一根没有前一根时为 null。 */
  prev_close: string | null;
  points: TrainingIntradayPoint[];
};

export type TrainingConfig = {
  warmup_bars: number;
  training_bars_min: number;
  training_bars_max: number;
  initial_cash: string;
  commission: string;
  slippage: string;
  exclude_st: boolean;
  idle_ttl_seconds: number;
};

export type TrainingCurvePoint = {
  i: number;
  date: string | null;
  value: string;
  normalized_value: string | null;
};

export type TrainingCurve = {
  curve_type: "equity" | "drawdown";
  point_count: number;
  points: TrainingCurvePoint[];
};

export type TrainingClosedTrade = {
  date: string;
  size: number;
  price: string;
  value: string;
  pnl: string;
  pnl_pct: string | null;
};

export type TrainingMetrics = {
  initial_cash: string;
  final_value: string;
  total_return_pct: string;
  realized_pnl: string;
  unrealized_pnl: string;
  open_return_pct: string;
  position_size: number;
  position_pct: string;
  max_drawdown_pct: string;
  max_drawdown_start: string | null;
  max_drawdown_end: string | null;
  sharpe_ratio: string | null;
  win_rate_pct: string | null;
  total_trades: number;
  duration_seconds: number;
  settlement_note: string;
};

export type TrainingReport = {
  metrics: TrainingMetrics;
  equity_curve: TrainingCurve;
  drawdown_curve: TrainingCurve;
  bars: TrainingRevealedBar[];
  markers: TrainingMarker[];
  fills: TrainingFill[];
  closed_trades: TrainingClosedTrade[];
};

export type TrainingReportResponse = {
  session: TrainingSessionView;
  instrument: { symbol: string; name: string | null; instrument_alias: string };
  window: { start_date: string; end_date: string; warmup_bars: number; training_bars: number };
  report: TrainingReport;
};

export class TrainingApiError extends Error {
  code: string;
  status: number;
  detail: Record<string, unknown>;

  constructor(message: string, code: string, status: number, detail: Record<string, unknown> = {}) {
    super(message);
    this.name = "TrainingApiError";
    this.code = code;
    this.status = status;
    this.detail = detail;
  }
}

export async function createTrainingSession(payload: {
  project_id: string;
  config?: Partial<TrainingConfig>;
}): Promise<TrainingSession> {
  return trainingFetch<TrainingSession>("/api/training/sessions", {
    method: "POST",
    body: { mode: "daily", ...payload },
  });
}

export async function getTrainingSession(sessionId: string): Promise<TrainingSession> {
  return trainingFetch<TrainingSession>(
    `/api/training/sessions/${encodeURIComponent(sessionId)}`,
  );
}

export async function listTrainingSessions(
  projectId: string,
  options: {
    limit?: number;
    offset?: number;
    status?: TrainingStatus;
    keyword?: string;
  } = {},
): Promise<TrainingSessionList> {
  const params = new URLSearchParams({ project_id: projectId });
  if (options.limit !== undefined) {
    params.set("limit", String(options.limit));
  }
  if (options.offset !== undefined) {
    params.set("offset", String(options.offset));
  }
  if (options.status !== undefined) {
    params.set("status", options.status);
  }
  if (options.keyword) {
    params.set("keyword", options.keyword);
  }
  return trainingFetch<TrainingSessionList>(`/api/training/sessions?${params.toString()}`);
}

export async function revealTrainingBar(
  sessionId: string,
  payload: { seq: number; action: TrainingAction; size?: number },
): Promise<TrainingReveal> {
  return trainingFetch<TrainingReveal>(
    `/api/training/sessions/${encodeURIComponent(sessionId)}/reveal`,
    { method: "POST", body: payload },
  );
}

export async function finishTrainingSession(sessionId: string): Promise<TrainingReportResponse> {
  return trainingFetch<TrainingReportResponse>(
    `/api/training/sessions/${encodeURIComponent(sessionId)}/finish`,
    { method: "POST" },
  );
}

/** 第 ``seq`` 根日线当天的分时（只有已揭示的根可看）。 */
export async function getTrainingIntraday(
  sessionId: string,
  seq: number,
): Promise<TrainingIntraday> {
  return trainingFetch<TrainingIntraday>(
    `/api/training/sessions/${encodeURIComponent(sessionId)}/intraday?seq=${seq}`,
  );
}

export async function getTrainingReport(sessionId: string): Promise<TrainingReportResponse> {
  return trainingFetch<TrainingReportResponse>(
    `/api/training/sessions/${encodeURIComponent(sessionId)}/report`,
  );
}

async function trainingFetch<T>(
  path: string,
  options: { method?: "GET" | "POST"; body?: unknown } = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: { "Content-Type": "application/json" },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  });

  if (!response.ok) {
    const detail = await readErrorDetail(response);
    throw new TrainingApiError(
      String(detail.message ?? `请求失败：${response.status}`),
      String(detail.error_code ?? "TRAINING_REQUEST_FAILED"),
      response.status,
      detail,
    );
  }

  return response.json() as Promise<T>;
}

async function readErrorDetail(response: Response): Promise<Record<string, unknown>> {
  try {
    const payload = (await response.json()) as { detail?: unknown };
    if (typeof payload.detail === "object" && payload.detail !== null) {
      return payload.detail as Record<string, unknown>;
    }
    if (typeof payload.detail === "string") {
      return { message: payload.detail };
    }
  } catch {
    return { message: `请求失败：${response.status}` };
  }
  return { message: `请求失败：${response.status}` };
}
