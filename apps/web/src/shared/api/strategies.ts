import { API_BASE_URL, API_PROJECT_ID, API_USER_ID } from "./client";

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
  status: "active" | "archived" | "deleted";
  tags: string[];
  default_params: Record<string, StrategyParamValue>;
  updated_at: string;
};

export type StrategyVersion = {
  id: string;
  strategy_id: string;
  version: number;
  entrypoint: string;
  python_file: StrategyPythonFile;
  params_schema: Record<string, StrategyParameterSchema>;
  default_params: Record<string, StrategyParamValue>;
  code_checksum: string;
  created_at: string;
};

export type StrategyPythonFile = {
  path: string;
  content: string;
};

export type StrategyPackage = {
  name: string;
  description: string;
  entrypoint: string;
  python_file: StrategyPythonFile;
  params_schema: Record<string, StrategyParameterSchema>;
  default_params: Record<string, StrategyParamValue>;
  risk_notes: string[];
};

export type StrategyCreateResult = {
  strategy_id: string;
  entrypoint: string;
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
  return apiFetch<StrategySummary[]>("/api/strategies", { projectId });
}

export async function getStrategyVersion(versionId: string): Promise<StrategyVersion> {
  return apiFetch<StrategyVersion>(`/api/strategy-versions/${versionId}`);
}

export async function createStrategy(strategyPackage: StrategyPackage): Promise<StrategyCreateResult> {
  return apiFetch<StrategyCreateResult>("/api/strategies", {
    method: "POST",
    body: JSON.stringify({
      package: strategyPackage,
      user_id: API_USER_ID,
      project_id: API_PROJECT_ID,
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
    body: JSON.stringify({
      mode: "summary",
      user_id: API_USER_ID,
      project_id: API_PROJECT_ID,
    }),
  });
}

async function apiFetch<T>(path: string, init?: ApiFetchOptions): Promise<T> {
  const { projectId, headers, ...requestInit } = init ?? {};
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...requestInit,
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": API_USER_ID,
      "X-Project-Id": projectId ?? API_PROJECT_ID,
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
