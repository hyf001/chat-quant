import type { BacktestDetail, BacktestRun, CreateBacktestRunPayload } from "../types/backtests";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(payload?.detail ?? `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getHealth(): Promise<{ status: string }> {
  return fetchJson<{ status: string }>("/api/health");
}

export async function createBacktestRun(payload: CreateBacktestRunPayload): Promise<BacktestRun> {
  return fetchJson<BacktestRun>("/api/backtests", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function runBacktest(backtestRunId: string): Promise<BacktestDetail> {
  return fetchJson<BacktestDetail>(`/api/backtests/${backtestRunId}/run`, {
    method: "POST",
    body: JSON.stringify({ mode: "sync" }),
  });
}

export async function getBacktest(backtestRunId: string): Promise<BacktestDetail> {
  return fetchJson<BacktestDetail>(
    `/api/backtests/${backtestRunId}?include_trades=true&include_curves=true`,
  );
}
