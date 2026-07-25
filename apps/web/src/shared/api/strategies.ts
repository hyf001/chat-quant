const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type StrategyParamValue = number | string | boolean;

export type StrategyParameterSchema = {
  type: "integer" | "number" | "string" | "boolean";
  title: string;
  description?: string | null;
  default: StrategyParamValue;
  minimum?: number | null;
  maximum?: number | null;
  enum?: StrategyParamValue[] | null;
  required: boolean;
  ui: {
    control: "number" | "select" | "checkbox" | "text";
    unit?: string | null;
  };
};

export type StrategySummary = {
  strategy_id: string;
  strategy_version_id: string;
  version: number;
  name: string;
  strategy_type: string;
  status: "active" | "archived" | "deleted";
  version_status: "draft" | "validating" | "validated" | "invalid" | "archived";
  tags: string[];
  logic_summary?: string | null;
  default_params: Record<string, StrategyParamValue>;
  updated_at: string;
};

export type StrategyVersion = {
  id: string;
  strategy_id: string;
  version: number;
  version_name?: string | null;
  parent_version_id?: string | null;
  code_artifact_id: string;
  entrypoint: string;
  params_schema: Record<string, StrategyParameterSchema>;
  default_params: Record<string, StrategyParamValue>;
  logic_summary?: string | null;
  change_summary?: string | null;
  code_checksum: string;
  status: StrategySummary["version_status"];
  validation_error?: string | null;
  validated_at?: string | null;
  created_at: string;
};

export type StrategyPackage = {
  name: string;
  description: string;
  strategy_type: string;
  entrypoint: string;
  code_artifact_id: string;
  params_schema: Record<string, StrategyParameterSchema>;
  default_params: Record<string, StrategyParamValue>;
  logic_summary: string;
  risk_notes: string[];
};

export type StrategyCreateResult = {
  strategy_id: string;
  strategy_version_id: string;
  version: number;
  status: StrategySummary["version_status"];
  entrypoint: string;
};

export type StrategyCopySummary = {
  mode: "summary" | "new_strategy";
  source_strategy_version_id: string;
  summary: string;
  target_strategy_id?: string | null;
  copy_record_id: string;
};

export async function listStrategies(): Promise<StrategySummary[]> {
  return apiFetch<StrategySummary[]>("/api/strategies");
}

export async function getStrategyVersion(versionId: string): Promise<StrategyVersion> {
  return apiFetch<StrategyVersion>(`/api/strategy-versions/${versionId}`);
}

export async function createStrategy(
  chatSessionId: string,
  strategyPackage: StrategyPackage,
): Promise<StrategyCreateResult> {
  return apiFetch<StrategyCreateResult>("/api/strategies", {
    method: "POST",
    body: JSON.stringify({
      chat_session_id: chatSessionId,
      package: strategyPackage,
    }),
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

export function buildDemoStrategyPackage(): StrategyPackage {
  return {
    name: "沪深300 均线突破策略",
    description: "短期均线上穿长期均线买入，下穿卖出，并加入波动过滤。",
    strategy_type: "ma_cross",
    entrypoint: "strategy.py:GeneratedStrategy",
    code_artifact_id: "code_demo_ma_cross",
    params_schema: {
      fast_period: {
        type: "integer",
        title: "短期均线周期",
        default: 20,
        minimum: 2,
        maximum: 250,
        required: true,
        ui: { control: "number", unit: "日" },
      },
      slow_period: {
        type: "integer",
        title: "长期均线周期",
        default: 60,
        minimum: 5,
        maximum: 500,
        required: true,
        ui: { control: "number", unit: "日" },
      },
      volatility_filter: {
        type: "string",
        title: "波动过滤",
        enum: ["off", "medium", "strong"],
        default: "medium",
        required: true,
        ui: { control: "select" },
      },
    },
    default_params: {
      fast_period: 20,
      slow_period: 60,
      volatility_filter: "medium",
    },
    logic_summary: "MA 20/60 突破并使用中等波动过滤",
    risk_notes: ["历史回测不代表未来收益，不构成投资建议"],
  };
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
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
