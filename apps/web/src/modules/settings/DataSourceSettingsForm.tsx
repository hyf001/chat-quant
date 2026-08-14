import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Download,
  FolderOpen,
  Loader2,
  Play,
  Save,
  Settings,
  Server,
} from "lucide-react";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";

import {
  getMindgoDatasetSchema,
  listMindgoDatasets,
  queryMindgoDataset,
  syncMindgoDataset,
  testMindgoConnection,
  type AppSettings,
  type MindgoDatasetQueryResponse,
  type MindgoDatasetSchema,
  type MindgoDatasetSummary,
  type MindgoDatasetSyncResult,
  type MindgoJsonValue,
  type MindgoParameterSpec,
  type MindgoSettings,
} from "../../shared/api";

type DataSourceSettingsFormProps = {
  draft: AppSettings;
  onChange: (settings: AppSettings) => void;
  onSaveMindgoSettings: (settings: Partial<MindgoSettings>, message: string) => void;
  onToast: (message: string, tone?: "success" | "error" | "info") => void;
};

type MindgoParamDraft = Record<string, MindgoJsonValue>;

const today = new Date().toISOString().slice(0, 10);

export function DataSourceSettingsForm({
  draft,
  onChange,
  onSaveMindgoSettings,
  onToast,
}: DataSourceSettingsFormProps) {
  const [datasets, setDatasets] = useState<MindgoDatasetSummary[]>([]);
  const [selectedDatasetId, setSelectedDatasetId] = useState("stock_a_daily_price");
  const [schema, setSchema] = useState<MindgoDatasetSchema | null>(null);
  const [params, setParams] = useState<MindgoParamDraft>({});
  const [queryResult, setQueryResult] = useState<MindgoDatasetQueryResponse | null>(null);
  const [syncResult, setSyncResult] = useState<MindgoDatasetSyncResult | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [isConnectionOpen, setIsConnectionOpen] = useState(false);
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(false);
  const [isLoadingSchema, setIsLoadingSchema] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  const selectedDataset = useMemo(
    () => datasets.find((dataset) => dataset.id === selectedDatasetId) ?? datasets[0] ?? null,
    [datasets, selectedDatasetId],
  );

  const loadDatasets = useCallback(async () => {
    setIsLoadingDatasets(true);
    try {
      const response = await listMindgoDatasets();
      setDatasets(response.datasets);
      if (response.datasets.length > 0) {
        setSelectedDatasetId((current) =>
          response.datasets.some((dataset) => dataset.id === current)
            ? current
            : response.datasets[0].id,
        );
      }
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "数据集加载失败", "error");
    } finally {
      setIsLoadingDatasets(false);
    }
  }, [onToast]);

  const loadSchema = useCallback(async (datasetId: string) => {
    setIsLoadingSchema(true);
    setQueryResult(null);
    setSyncResult(null);
    try {
      const nextSchema = await getMindgoDatasetSchema(datasetId);
      setSchema(nextSchema);
      setParams(defaultParamsFromSchema(nextSchema));
      setPage(1);
    } catch (caught) {
      setSchema(null);
      onToast(caught instanceof Error ? caught.message : "Schema 加载失败", "error");
    } finally {
      setIsLoadingSchema(false);
    }
  }, [onToast]);

  useEffect(() => {
    void loadDatasets();
  }, [loadDatasets]);

  useEffect(() => {
    if (selectedDatasetId) {
      void loadSchema(selectedDatasetId);
    }
  }, [loadSchema, selectedDatasetId]);

  const updateParam = (name: string, value: MindgoJsonValue) => {
    setParams((current) => ({ ...current, [name]: value }));
    setQueryResult(null);
    setSyncResult(null);
    setPage(1);
  };

  const updateMindgoSettings = (patch: Partial<MindgoSettings>) => {
    onChange({
      ...draft,
      mindgo: normalizeMindgoSettings({
        ...draft.mindgo,
        ...patch,
      }),
    });
  };

  const handleSaveMindgoSettings = () => {
    const normalized = normalizeMindgoSettings(draft.mindgo);
    onSaveMindgoSettings(
      {
        ...normalized,
        jupyter_url: normalized.jupyter_url ?? "",
        jupyter_token: normalized.jupyter_token ?? "",
        kernel_id: normalized.kernel_id ?? "",
      },
      "MindGo 连接配置已保存",
    );
    setIsConnectionOpen(false);
  };

  const handleSelectMindgoStorageRoot = async () => {
    const selected = await selectDirectory({
      title: "选择 MindGo 数据根目录",
      buttonLabel: "选择",
      defaultPath: draft.mindgo.storage_root,
      prompt: "输入 MindGo 数据根目录",
    });
    if (selected) {
      updateMindgoSettings({ storage_root: selected });
    }
  };

  const handleTestConnection = async () => {
    setIsTesting(true);
    try {
      const result = await testMindgoConnection();
      onToast(result.message, result.ok ? "success" : "error");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "连接测试失败", "error");
    } finally {
      setIsTesting(false);
    }
  };

  const handleQuery = async (nextPage = page) => {
    if (!schema) {
      return;
    }
    setIsQuerying(true);
    setSyncResult(null);
    try {
      const response = await queryMindgoDataset(selectedDatasetId, {
        params: cleanParams(params),
        page: nextPage,
        page_size: pageSize,
      });
      setPage(response.page);
      setQueryResult(response);
      onToast(`查询完成：${response.total} 行`, "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "查询失败", "error");
    } finally {
      setIsQuerying(false);
    }
  };

  const handleSync = async () => {
    const baseDay = stringParam(params.baseDay) || today;
    setIsSyncing(true);
    setQueryResult(null);
    try {
      const response = await syncMindgoDataset(selectedDatasetId, {
        start_date: baseDay,
        end_date: baseDay,
        params: cleanParams(params),
      });
      setSyncResult(response);
      onToast(`导入完成：${response.synced_count} 行`, "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "导入失败", "error");
    } finally {
      setIsSyncing(false);
    }
  };

  const canUseDataset = Boolean(schema && selectedDataset);
  const isBusy = isLoadingSchema || isQuerying || isSyncing || isTesting;

  return (
    <div className="grid gap-5">
      <section className="grid gap-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-sm font-semibold text-ink">MindGo 数据源</h2>
            <p className="mt-1 text-xs text-muted">连接配置保存到系统设置；Token 手动维护。</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <button
                className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                type="button"
                aria-expanded={isConnectionOpen}
                onClick={() => setIsConnectionOpen((current) => !current)}
              >
                <Settings className="h-3.5 w-3.5" />
                连接配置
                <ChevronDown
                  className={`h-3.5 w-3.5 transition-transform ${
                    isConnectionOpen ? "rotate-180" : ""
                  }`}
                />
              </button>
              {isConnectionOpen ? (
                <div className="absolute right-0 z-20 mt-2 w-[min(760px,calc(100vw-2rem))] rounded-md border border-line bg-panel p-3 shadow-lift">
                  <div className="grid gap-3 md:grid-cols-2">
                    <TextInput
                      label="Notebook 地址"
                      value={draft.mindgo.jupyter_url ?? ""}
                      onChange={(jupyter_url) => updateMindgoSettings({ jupyter_url })}
                    />
                    <TextInput
                      label="访问 Token"
                      type="password"
                      value={draft.mindgo.jupyter_token ?? ""}
                      onChange={(jupyter_token) => updateMindgoSettings({ jupyter_token })}
                    />
                    <TextInput
                      label="Notebook 路径"
                      value={draft.mindgo.notebook_path}
                      onChange={(notebook_path) => updateMindgoSettings({ notebook_path })}
                    />
                    <TextInput
                      label="数据根目录"
                      value={draft.mindgo.storage_root}
                      onChange={(storage_root) => updateMindgoSettings({ storage_root })}
                      action={
                        <button
                          className="inline-flex h-10 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                          type="button"
                          onClick={() => void handleSelectMindgoStorageRoot()}
                        >
                          <FolderOpen className="h-3.5 w-3.5" />
                          浏览
                        </button>
                      }
                    />
                    <NumberInput
                      label="超时 秒"
                      value={draft.mindgo.timeout_seconds}
                      onChange={(timeout_seconds) => updateMindgoSettings({ timeout_seconds })}
                    />
                  </div>
                  <div className="mt-3 flex flex-wrap justify-end gap-2 border-t border-line pt-3">
                    <button
                      className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink"
                      type="button"
                      onClick={handleSaveMindgoSettings}
                    >
                      <Save className="h-3.5 w-3.5" />
                      保存配置
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
            <button
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={isTesting}
              onClick={handleTestConnection}
            >
              {isTesting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Server className="h-3.5 w-3.5" />}
              测试连接
            </button>
          </div>
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-[280px_minmax(0,1fr)]">
        <div className="grid gap-3 rounded-md border border-line bg-soft p-3 xl:self-start">
          <div className="flex items-center justify-between gap-2">
            <h2 className="text-sm font-semibold text-ink">已接入数据集</h2>
            {isLoadingDatasets ? <Loader2 className="h-4 w-4 animate-spin text-muted" /> : null}
          </div>
          <div className="grid gap-2">
            {datasets.map((dataset) => (
              <button
                className={`grid gap-1 rounded-md border px-3 py-2 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 ${
                  selectedDatasetId === dataset.id
                    ? "border-ink bg-panel text-ink"
                    : "border-line bg-panel/60 text-graphite hover:border-signal"
                }`}
                key={dataset.id}
                type="button"
                onClick={() => setSelectedDatasetId(dataset.id)}
              >
                <span className="text-xs font-semibold">{dataset.name}</span>
                <span className="text-[11px] leading-4 text-muted">
                  {dataset.category_path.join(" / ")}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div className="grid min-w-0 gap-4">
          <section className="grid gap-3 rounded-md border border-line bg-panel p-3">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="min-w-0">
                <h2 className="truncate text-sm font-semibold text-ink">
                  {selectedDataset?.name ?? "数据集"}
                </h2>
                <p className="mt-1 text-xs leading-5 text-muted">
                  {selectedDataset?.description ?? "选择一个数据集后开始查询。"}
                </p>
              </div>
            </div>

            {schema ? (
              <div className="grid gap-3 md:grid-cols-2">
                {schema.query_params.map((param) => (
                  <ParamField
                    key={param.name}
                    param={param}
                    value={params[param.name]}
                    onChange={(value) => updateParam(param.name, value)}
                  />
                ))}
              </div>
            ) : null}

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-3">
              <div className="flex flex-wrap items-center gap-2">
                <button
                  className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
                  type="button"
                  disabled={!canUseDataset || isBusy}
                  onClick={() => void handleQuery(1)}
                >
                  {isQuerying ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
                  查询
                </button>
                <button
                  className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
                  type="button"
                  disabled={!canUseDataset || isBusy}
                  onClick={() => void handleSync()}
                >
                  {isSyncing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Download className="h-3.5 w-3.5" />}
                  导入
                </button>
              </div>
              <label className="flex items-center gap-2 text-xs font-semibold text-graphite">
                每页
                <select
                  className="h-8 rounded-md border border-line bg-panel px-2 text-xs outline-none focus:border-signal"
                  value={pageSize}
                  onChange={(event) => {
                    setPageSize(Number(event.target.value));
                    setPage(1);
                  }}
                >
                  {[20, 50, 100, 200].map((size) => (
                    <option key={size} value={size}>
                      {size}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </section>

          {queryResult ? (
            <QueryResultTable
              result={queryResult}
              onPageChange={(nextPage) => void handleQuery(nextPage)}
              disabled={isBusy}
            />
          ) : null}
          {syncResult ? <SyncResultPanel result={syncResult} /> : null}
        </div>
      </section>
    </div>
  );
}

function TextInput({
  label,
  value,
  onChange,
  type = "text",
  action,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: "text" | "password";
  action?: ReactNode;
}) {
  return (
    <div className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <span className="flex gap-2">
        <input
          className="h-10 min-w-0 flex-1 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
          type={type}
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
        {action}
      </span>
    </div>
  );
}

function NumberInput({
  label,
  value,
  onChange,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <input
        className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
        min={1}
        type="number"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </label>
  );
}

function ParamField({
  param,
  value,
  onChange,
}: {
  param: MindgoParameterSpec;
  value: MindgoJsonValue;
  onChange: (value: MindgoJsonValue) => void;
}) {
  if (param.value_type === "string[]" && param.options.length > 0) {
    const selected = Array.isArray(value) ? value.map(String) : [];
    return (
      <div className="grid gap-1.5 md:col-span-2">
        <span className="text-xs font-semibold text-graphite">{param.label}</span>
        <div className="flex max-h-32 flex-wrap gap-1.5 overflow-auto rounded-md border border-line bg-soft p-2">
          {param.options.map((option) => {
            const optionValue = String(option.value);
            const checked = selected.includes(optionValue);
            return (
              <label
                className={`inline-flex h-7 items-center gap-1.5 rounded border px-2 text-[11px] ${
                  checked
                    ? "border-brand/35 bg-gainSoft text-brand"
                    : "border-line bg-panel text-graphite"
                }`}
                key={optionValue}
              >
                <input
                  className="h-3 w-3 accent-brand"
                  type="checkbox"
                  checked={checked}
                  onChange={(event) => {
                    const nextValue = event.target.checked
                      ? [...selected, optionValue]
                      : selected.filter((item) => item !== optionValue);
                    onChange(nextValue);
                  }}
                />
                {option.label}
              </label>
            );
          })}
        </div>
      </div>
    );
  }

  if (param.value_type === "enum" && param.options.length > 0) {
    return (
      <label className="grid gap-1.5">
        <span className="text-xs font-semibold text-graphite">{param.label}</span>
        <select
          className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
          value={stringParam(value)}
          onChange={(event) => onChange(event.target.value)}
        >
          {param.options.map((option) => (
            <option key={String(option.value)} value={String(option.value)}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
    );
  }

  if (param.value_type === "boolean") {
    return (
      <label className="flex min-h-10 items-center justify-between gap-3 rounded-md border border-line bg-soft px-3 py-2">
        <span className="text-xs font-semibold text-graphite">{param.label}</span>
        <input
          className="h-4 w-4 accent-brand"
          type="checkbox"
          checked={Boolean(value)}
          onChange={(event) => onChange(event.target.checked)}
        />
      </label>
    );
  }

  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{param.label}</span>
      <input
        className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
        type={param.value_type === "date" ? "date" : param.value_type === "integer" || param.value_type === "number" ? "number" : "text"}
        value={stringParam(value)}
        onChange={(event) => {
          if (param.value_type === "integer") {
            onChange(Number.parseInt(event.target.value, 10));
            return;
          }
          if (param.value_type === "number") {
            onChange(Number(event.target.value));
            return;
          }
          onChange(event.target.value);
        }}
      />
    </label>
  );
}

function QueryResultTable({
  result,
  disabled,
  onPageChange,
}: {
  result: MindgoDatasetQueryResponse;
  disabled: boolean;
  onPageChange: (page: number) => void;
}) {
  const visibleColumns = result.columns.filter((column) =>
    result.rows.some((row) => row[column.name] !== null && row[column.name] !== undefined),
  );
  const columns = visibleColumns.length > 0 ? visibleColumns : result.columns.slice(0, 8);

  return (
    <section className="grid gap-3 rounded-md border border-line bg-panel p-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-ink">查询结果</h2>
        <div className="flex items-center gap-2 text-xs text-muted">
          <span>
            {result.total} 行 · 第 {result.page}/{Math.max(result.total_pages, 1)} 页
          </span>
          <button
            className="grid h-8 w-8 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            title="上一页"
            aria-label="上一页"
            disabled={disabled || result.page <= 1}
            onClick={() => onPageChange(result.page - 1)}
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            className="grid h-8 w-8 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            title="下一页"
            aria-label="下一页"
            disabled={disabled || result.total_pages === 0 || result.page >= result.total_pages}
            onClick={() => onPageChange(result.page + 1)}
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
      <div className="max-w-full overflow-auto rounded-md border border-line">
        <table className="min-w-full border-collapse text-left text-xs">
          <thead className="bg-soft text-graphite">
            <tr>
              {columns.map((column) => (
                <th className="whitespace-nowrap border-b border-line px-2.5 py-2 font-semibold" key={column.name}>
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.rows.map((row, rowIndex) => (
              <tr className="odd:bg-panel even:bg-soft/55" key={`${result.page}-${rowIndex}`}>
                {columns.map((column) => (
                  <td className="whitespace-nowrap border-b border-line px-2.5 py-2 font-mono text-[11px] text-ink" key={column.name}>
                    {formatCell(row[column.name])}
                  </td>
                ))}
              </tr>
            ))}
            {result.rows.length === 0 ? (
              <tr>
                <td className="px-3 py-8 text-center text-xs text-muted" colSpan={columns.length || 1}>
                  暂无数据
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function SyncResultPanel({ result }: { result: MindgoDatasetSyncResult }) {
  return (
    <section className="flex flex-wrap items-center justify-between gap-3 rounded-md border border-brand/25 bg-gainSoft px-3 py-2 text-xs text-brand">
      <span className="font-semibold">导入完成</span>
      <span className="font-mono">
        rows={result.synced_count} · elapsed={result.elapsed_ms}ms
      </span>
    </section>
  );
}

function defaultParamsFromSchema(schema: MindgoDatasetSchema): MindgoParamDraft {
  const draft: MindgoParamDraft = {};
  for (const param of schema.query_params) {
    if (param.default !== null && param.default !== undefined) {
      draft[param.name] = param.default;
    } else if (param.value_type === "date") {
      draft[param.name] = today;
    } else if (param.value_type === "string[]") {
      draft[param.name] = [];
    } else if (param.value_type === "boolean") {
      draft[param.name] = false;
    } else {
      draft[param.name] = "";
    }
  }
  return draft;
}

function cleanParams(params: MindgoParamDraft): Record<string, MindgoJsonValue> {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => {
      if (value === "") {
        return false;
      }
      if (Array.isArray(value) && value.length === 0) {
        return false;
      }
      return value !== undefined;
    }),
  );
}

function normalizeMindgoSettings(settings: MindgoSettings): MindgoSettings {
  return {
    ...settings,
    jupyter_url: settings.jupyter_url?.trim() || null,
    auth_scheme: settings.auth_scheme.trim() || "Bearer",
    jupyter_token: settings.jupyter_token?.trim() || null,
    notebook_path: settings.notebook_path.trim() || "deepsolo_v3/少标的分时实时.ipynb",
    kernel_id: settings.kernel_id?.trim() || null,
    timeout_seconds: Math.max(1, Number(settings.timeout_seconds) || 120),
    storage_root: settings.storage_root.trim() || "data/mindgo/parquet",
  };
}

async function selectDirectory({
  title,
  buttonLabel,
  defaultPath,
  prompt,
}: {
  title: string;
  buttonLabel: string;
  defaultPath: string;
  prompt: string;
}): Promise<string | null> {
  if (window.chatqDesktop?.selectDirectory) {
    return window.chatqDesktop.selectDirectory({ title, buttonLabel, defaultPath });
  }
  return window.prompt(prompt, defaultPath)?.trim() || null;
}

function stringParam(value: MindgoJsonValue): string {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return "";
}

function formatCell(value: MindgoJsonValue | undefined): string {
  if (value === null || value === undefined) {
    return "-";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}
