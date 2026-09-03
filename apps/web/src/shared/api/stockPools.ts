import { API_BASE_URL } from "./client";

export type StockPool = {
  id: string;
  project_id: string;
  name: string;
  description?: string | null;
  stock_count: number;
  created_at: string;
  updated_at: string;
};

export type StockPoolStock = {
  id: string;
  pool_id: string;
  symbol: string;
  name?: string | null;
  tags: string[];
  note?: string | null;
  created_at: string;
  updated_at: string;
};

export type StockPoolDetail = StockPool & {
  stocks: StockPoolStock[];
  symbols: string[];
};

export type StockPoolCandidate = {
  symbol: string;
  name?: string | null;
  in_pool: boolean;
};

export type StockPoolListResponse = {
  items: StockPool[];
  total: number;
};

export type StockPoolCandidateListResponse = {
  items: StockPoolCandidate[];
  total: number;
};

export type StockPoolStockListResponse = {
  items: StockPoolStock[];
  total: number;
};

export type StockPoolCreatePayload = {
  project_id: string;
  name: string;
  description?: string | null;
};

export type StockPoolUpdatePayload = {
  name?: string;
  description?: string | null;
};

export type StockPoolStockCreatePayload = {
  symbol: string;
  name?: string | null;
  tags?: string[];
  note?: string | null;
};

export type StockPoolStockUpdatePayload = Partial<StockPoolStockCreatePayload>;

export type StockPoolBulkCreatePayload = {
  symbols: string;
};

export type StockPoolSnapshotImportPayload = {
  symbols?: string[];
};

export type StockPoolBulkCreateResult = {
  items: StockPoolStock[];
  created: number;
  skipped: number;
};

export type StockPoolSnapshotImportResult = StockPoolBulkCreateResult & {
  source_dataset: string;
};

export async function listStockPools(projectId?: string | null): Promise<StockPoolListResponse> {
  if (!projectId) {
    return { items: [], total: 0 };
  }
  const params = new URLSearchParams({ project_id: projectId });
  return stockPoolFetch<StockPoolListResponse>(`/api/stock-pools?${params.toString()}`);
}

export async function createStockPool(payload: StockPoolCreatePayload): Promise<StockPool> {
  return stockPoolFetch<StockPool>("/api/stock-pools", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getStockPool(
  poolId: string,
  options: { includeStocks?: boolean } = {},
): Promise<StockPoolDetail> {
  const params = new URLSearchParams();
  if (options.includeStocks === false) {
    params.set("include_stocks", "false");
  }
  const suffix = params.size ? `?${params.toString()}` : "";
  return stockPoolFetch<StockPoolDetail>(`/api/stock-pools/${poolId}${suffix}`);
}

export async function updateStockPool(
  poolId: string,
  payload: StockPoolUpdatePayload,
): Promise<StockPool> {
  return stockPoolFetch<StockPool>(`/api/stock-pools/${poolId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteStockPool(poolId: string): Promise<void> {
  await stockPoolFetch<void>(`/api/stock-pools/${poolId}`, {
    method: "DELETE",
  });
}

export async function listPoolStocks(
  poolId: string,
  options: {
    query?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<StockPoolStockListResponse> {
  const params = new URLSearchParams({
    limit: String(options.limit ?? 100),
    offset: String(options.offset ?? 0),
  });
  if (options.query?.trim()) {
    params.set("query", options.query.trim());
  }
  return stockPoolFetch<StockPoolStockListResponse>(
    `/api/stock-pools/${poolId}/stocks?${params.toString()}`,
  );
}

export async function searchStockPoolCandidates(
  poolId: string,
  query: string,
  limit = 50,
  offset = 0,
): Promise<StockPoolCandidateListResponse> {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (query.trim()) {
    params.set("query", query.trim());
  }
  return stockPoolFetch<StockPoolCandidateListResponse>(
    `/api/stock-pools/${poolId}/stock-candidates?${params.toString()}`,
  );
}

export async function addPoolStock(
  poolId: string,
  payload: StockPoolStockCreatePayload,
): Promise<StockPoolStock> {
  return stockPoolFetch<StockPoolStock>(`/api/stock-pools/${poolId}/stocks`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function bulkAddPoolStocks(
  poolId: string,
  payload: StockPoolBulkCreatePayload,
): Promise<StockPoolBulkCreateResult> {
  return stockPoolFetch<StockPoolBulkCreateResult>(`/api/stock-pools/${poolId}/stocks/bulk`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function importSnapshotInfoStocks(
  poolId: string,
  payload: StockPoolSnapshotImportPayload = {},
): Promise<StockPoolSnapshotImportResult> {
  return stockPoolFetch<StockPoolSnapshotImportResult>(
    `/api/stock-pools/${poolId}/stocks/import-snapshot-info`,
    {
      method: "POST",
      body: Object.keys(payload).length ? JSON.stringify(payload) : undefined,
    },
  );
}

export async function updatePoolStock(
  stockId: string,
  payload: StockPoolStockUpdatePayload,
): Promise<StockPoolStock> {
  return stockPoolFetch<StockPoolStock>(`/api/stock-pools/stocks/${stockId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deletePoolStock(stockId: string): Promise<void> {
  await stockPoolFetch<void>(`/api/stock-pools/stocks/${stockId}`, {
    method: "DELETE",
  });
}

async function stockPoolFetch<T>(path: string, init?: RequestInit): Promise<T> {
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

  if (response.status === 204) {
    return undefined as T;
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
