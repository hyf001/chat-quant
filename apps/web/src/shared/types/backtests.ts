export type BacktestRunStatus = "pending" | "running" | "succeeded" | "failed" | "canceled";

export type BacktestConfig = {
  symbols: string[];
  universe_ref: string | null;
  market: string;
  benchmark_symbol: string | null;
  start_date: string;
  end_date: string;
  timeframe: string;
  data_source: string;
  data_adjust: string;
  data_as_of: string | null;
  initial_cash: string;
  commission: string;
  slippage: string;
  tax: string | null;
  order_size_mode: string;
  params: Record<string, string | number | boolean | null>;
  risk_free_rate: string;
  calendar: string;
  currency: string;
  assumptions: string[];
  symbol_order_mode: "preserve" | "sorted";
};

export type BacktestMetrics = {
  initial_value: string;
  final_value: string;
  total_return_pct: string;
  annual_return_pct: string | null;
  max_drawdown_pct: string;
  max_drawdown_abs_pct: string;
  max_drawdown_start: string | null;
  max_drawdown_end: string | null;
  max_drawdown_recovery_date: string | null;
  max_drawdown_duration_days: number | null;
  volatility_annual_pct: string | null;
  sharpe_ratio: string | null;
  sortino_ratio: string | null;
  calmar_ratio: string | null;
  win_rate_pct: string | null;
  total_trades: number;
  profit_factor: string | null;
  turnover_rate: string | null;
  annualization_basis: "calendar_days" | "trading_days";
  trade_count_basis: "closed_trade" | "order_fill";
};

export type BacktestRun = {
  id: string;
  project_id: string;
  strategy_id: string;
  strategy_version_id: string;
  parent_backtest_run_id: string | null;
  status: BacktestRunStatus;
  config: BacktestConfig;
  result_id: string | null;
  failure_code: string | null;
  failure_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
};

export type BacktestResult = {
  id: string;
  backtest_run_id: string;
  summary: string;
  metrics: BacktestMetrics;
  warnings: string[];
  config_snapshot: BacktestConfig;
  created_at: string;
};

export type TradeRecord = {
  id: string;
  symbol: string;
  side: "buy" | "sell" | "short" | "cover";
  status: "opened" | "closed" | "partial";
  trade_datetime: string;
  price: string;
  size: string;
  value: string;
  commission: string;
  pnl: string | null;
  pnl_pct: string | null;
  holding_days: number | null;
};

export type CurvePoint = {
  date: string;
  value: string;
  normalized_value: string | null;
  benchmark_value: string | null;
};

export type BacktestCurve = {
  id: string;
  curve_type: "equity" | "drawdown" | "benchmark_equity" | "benchmark_drawdown";
  point_count: number;
  start_date: string;
  end_date: string;
  sampling: "daily" | "weekly" | "monthly";
  points: CurvePoint[];
};

export type BacktestDetail = {
  run: BacktestRun;
  result: BacktestResult | null;
  trades: TradeRecord[];
  curves: BacktestCurve[];
};

export type CreateBacktestRunPayload = {
  strategy_version_id: string;
  symbols: string[];
  market: string;
  benchmark_symbol?: string;
  start_date: string;
  end_date: string;
  initial_cash: string;
  commission: string;
  slippage?: string;
  params?: Record<string, string | number | boolean | null>;
};
