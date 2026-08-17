import {
  Check,
  ChevronLeft,
  ChevronRight,
  Code2,
  Database,
  FilePlus2,
  Play,
  RefreshCw,
  Search,
  Settings2,
  Trash2,
  X,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import {
  createDataset,
  deleteDataset,
  getDataset,
  listDatasets,
  listMindgoSources,
  queryDatasets,
  updateDataset,
  type Dataset,
  type DatasetDetail,
  type DatasetPayload,
  type DatasetQueryResponse,
  type MindgoSourceSummary,
  type MindgoJsonValue,
} from "../../shared/api";

type DatasetForm = {
  name: string;
  description: string;
  categoryPath: string;
  exposedToAgent: boolean;
  createSql: string;
};

type ToastState = {
  message: string;
  tone: "success" | "error" | "info";
};

const emptyForm: DatasetForm = {
  name: "",
  description: "",
  categoryPath: "股票 / A股",
  exposedToAgent: true,
  createSql: "",
};

type DatasetPageProps = {
  embedded?: boolean;
};

export function DatasetPage({ embedded = false }: DatasetPageProps) {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DatasetDetail | null>(null);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [isDatasetListCollapsed, setIsDatasetListCollapsed] = useState(false);
  const [form, setForm] = useState<DatasetForm>(emptyForm);
  const [editDraft, setEditDraft] = useState<DatasetForm>(emptyForm);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [sql, setSql] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [queryResult, setQueryResult] = useState<DatasetQueryResponse | null>(null);
  const [sources, setSources] = useState<MindgoSourceSummary[]>([]);
  const [isSourcesLoading, setIsSourcesLoading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);

  const filteredDatasets = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    if (!keyword) {
      return datasets;
    }
    return datasets.filter((dataset) =>
      [
        dataset.id,
        dataset.name,
        dataset.description,
        dataset.category_path.join("/"),
      ]
        .join(" ")
        .toLowerCase()
        .includes(keyword),
    );
  }, [datasets, query]);

  const selectedDataset =
    datasets.find((dataset) => dataset.id === selectedId) ?? filteredDatasets[0] ?? null;

  const showToast = useCallback((message: string, tone: ToastState["tone"] = "info") => {
    setToast({ message, tone });
  }, []);

  const loadDatasets = useCallback(async (preferredId?: string | null) => {
    setIsLoading(true);
    try {
      const response = await listDatasets();
      setDatasets(response.datasets);
      setSelectedId((current) => {
        const next =
          response.datasets.find((dataset) => dataset.id === preferredId)?.id ??
          response.datasets.find((dataset) => dataset.id === current)?.id ??
          response.datasets[0]?.id ??
          null;
        return next;
      });
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "数据集加载失败", "error");
    } finally {
      setIsLoading(false);
    }
  }, [showToast]);

  const loadSources = useCallback(async () => {
    setIsSourcesLoading(true);
    try {
      const response = await listMindgoSources();
      setSources(response.sources);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "数据源加载失败", "error");
    } finally {
      setIsSourcesLoading(false);
    }
  }, [showToast]);

  const loadDetail = useCallback(async (datasetId: string) => {
    setIsDetailLoading(true);
    try {
      const nextDetail = await getDataset(datasetId);
      setDetail(nextDetail);
      setEditDraft(formFromDetail(nextDetail));
      setSql((current) => current.trim() || `SELECT * FROM ${nextDetail.name}`);
      setQueryResult(null);
      setPage(1);
    } catch (caught) {
      setDetail(null);
      showToast(caught instanceof Error ? caught.message : "数据集详情加载失败", "error");
    } finally {
      setIsDetailLoading(false);
    }
  }, [showToast]);

  useEffect(() => {
    void loadDatasets();
    void loadSources();
  }, [loadDatasets, loadSources]);

  useEffect(() => {
    if (selectedDataset?.id) {
      void loadDetail(selectedDataset.id);
    } else {
      setDetail(null);
      setEditDraft(emptyForm);
      setSql("");
      setQueryResult(null);
    }
  }, [loadDetail, selectedDataset?.id]);

  useEffect(() => {
    if (!toast) {
      return undefined;
    }
    const timeoutId = window.setTimeout(() => setToast(null), 2600);
    return () => window.clearTimeout(timeoutId);
  }, [toast]);

  const handleOpenCreate = () => {
    setForm(emptyForm);
    setIsCreateOpen(true);
    setToast(null);
  };

  const handleOpenDetail = async (dataset: Dataset) => {
    setSelectedId(dataset.id);
    setIsDetailOpen(true);
    if (detail?.id !== dataset.id) {
      await loadDetail(dataset.id);
    }
  };

  const handleCreate = async () => {
    const payload = payloadFromForm(form);
    if (!payload.name || !payload.create_sql) {
      showToast("view name 和 create_sql 不能为空", "error");
      return;
    }
    setIsSubmitting(true);
    try {
      const created = await createDataset(payload);
      setIsCreateOpen(false);
      showToast("数据集已创建", "success");
      await loadDatasets(created.id);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "创建数据集失败", "error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSave = async () => {
    if (!detail) {
      return;
    }
    setIsSubmitting(true);
    try {
      await updateDataset(detail.id, {
        description: editDraft.description.trim(),
        category_path: categoryPathFromText(editDraft.categoryPath),
        exposed_to_agent: editDraft.exposedToAgent,
      });
      showToast("数据集已保存", "success");
      await loadDatasets(detail.id);
      await loadDetail(detail.id);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "保存数据集失败", "error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!detail || !window.confirm(`删除数据集“${detail.description || detail.name}”？`)) {
      return;
    }
    setIsSubmitting(true);
    try {
      await deleteDataset(detail.id);
      setIsDetailOpen(false);
      showToast("数据集已删除", "success");
      await loadDatasets(null);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "删除数据集失败", "error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRunQuery = async (nextPage = page) => {
    if (!sql.trim()) {
      showToast("SQL 不能为空", "error");
      return;
    }
    setIsQuerying(true);
    try {
      const result = await queryDatasets({
        sql,
        page: nextPage,
        page_size: pageSize,
      });
      setQueryResult(result);
      setPage(result.page);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "SQL 查询失败", "error");
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <section
      className={`flex w-full min-w-0 flex-col gap-3 ${embedded ? "" : "h-full"}`}
      aria-label="数据集"
    >
      {toast ? <DatasetToast toast={toast} /> : null}

      <div
        className={`grid min-h-0 gap-3 transition-[grid-template-columns] duration-200 ${
          isDatasetListCollapsed
            ? "grid-cols-[56px_minmax(0,1fr)]"
            : "grid-cols-1 xl:grid-cols-[300px_minmax(0,1fr)]"
        } ${
          embedded ? "min-h-[720px]" : "flex-1"
        }`}
      >
        <aside
          className={`flex min-h-0 flex-col rounded-lg border border-line bg-panel shadow-sm ${
            isDatasetListCollapsed ? "self-start p-2" : ""
          }`}
        >
          <div className={isDatasetListCollapsed ? "grid place-items-center gap-2" : "border-b border-line p-3"}>
            <div className="flex items-center justify-between gap-2">
              {isDatasetListCollapsed ? null : (
                <div className="min-w-0">
                  <h2 className="truncate text-sm font-semibold text-ink">数据集</h2>
                  <p className="mt-0.5 truncate text-xs text-muted">DuckDB views · {datasets.length}</p>
                </div>
              )}
              <button
                className="grid h-8 w-8 shrink-0 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                type="button"
                title={isDatasetListCollapsed ? "展开数据集列表" : "收起数据集列表"}
                aria-label={isDatasetListCollapsed ? "展开数据集列表" : "收起数据集列表"}
                onClick={() => setIsDatasetListCollapsed((current) => !current)}
              >
                {isDatasetListCollapsed ? (
                  <ChevronRight className="h-3.5 w-3.5" />
                ) : (
                  <ChevronLeft className="h-3.5 w-3.5" />
                )}
              </button>
            </div>
            {isDatasetListCollapsed ? (
              <div
                className="grid h-10 w-10 place-items-center rounded-md border border-line bg-soft text-brandBlue"
                title={`共 ${datasets.length} 个数据集`}
                aria-label={`共 ${datasets.length} 个数据集`}
              >
                <Database className="h-4 w-4" />
              </div>
            ) : (
              <div className="mt-3 grid gap-3">
                <div className="flex items-center gap-2">
                  <IconAction
                    label="刷新"
                    icon={<RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />}
                    disabled={isLoading}
                    onClick={() => void loadDatasets(selectedId)}
                  />
                  <button
                    className="inline-flex h-9 min-w-0 flex-1 items-center justify-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25"
                    type="button"
                    onClick={handleOpenCreate}
                  >
                    <FilePlus2 className="h-4 w-4 shrink-0" />
                    <span className="truncate">新建数据集</span>
                  </button>
                </div>
                <div className="relative">
                  <Search className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted" />
                  <input
                    className="h-9 w-full rounded-md border border-line bg-panel pl-8 pr-3 text-xs text-ink outline-none placeholder:text-muted/70 focus:border-signal"
                    placeholder="搜索数据集"
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                  />
                </div>
              </div>
            )}
          </div>
          {isDatasetListCollapsed ? null : (
            <div className="min-h-0 flex-1 overflow-y-auto p-2">
              {isLoading ? <Notice text="加载中" /> : null}
              {!isLoading && filteredDatasets.length === 0 ? <Notice text="暂无数据集" /> : null}
              <div className="grid gap-2">
                {filteredDatasets.map((dataset) => (
                  <article
                    className={`overflow-hidden rounded-md border p-2 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 ${
                      selectedDataset?.id === dataset.id
                        ? "border-ink bg-panel text-ink"
                        : "border-line bg-panel/60 text-graphite hover:border-signal"
                    }`}
                    key={dataset.id}
                  >
                    <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-2">
                      <button
                        className="flex min-w-0 items-start gap-2 text-left focus:outline-none"
                        type="button"
                        onClick={() => setSelectedId(dataset.id)}
                      >
                        <span className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-md border border-line bg-panel text-brandBlue">
                          <Database className="h-3.5 w-3.5" />
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className="block truncate text-sm font-semibold text-ink">
                            {dataset.description || dataset.name}
                          </span>
                          <span className="mt-1 block truncate font-mono text-[10px] text-muted">
                            {dataset.name}
                          </span>
                        </span>
                      </button>
                      <button
                        className="inline-flex h-7 shrink-0 items-center gap-1 rounded-md border border-line bg-soft px-2 text-[10px] font-semibold text-muted transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                        type="button"
                        onClick={() => void handleOpenDetail(dataset)}
                      >
                        <Settings2 className="h-3 w-3 shrink-0" />
                        详情
                      </button>
                    </div>
                    <button
                      className="mt-3 flex min-h-5 w-full min-w-0 flex-wrap items-center gap-1.5 overflow-hidden text-left focus:outline-none"
                      type="button"
                      onClick={() => setSelectedId(dataset.id)}
                    >
                      {dataset.category_path.map((part) => (
                        <span
                          className="inline-flex max-w-full rounded bg-compareSoft px-1.5 py-0.5 text-[10px] text-brandBlue"
                          key={part}
                        >
                          <span className="truncate">{part}</span>
                        </span>
                      ))}
                      {dataset.exposed_to_agent ? (
                        <span className="inline-flex max-w-full rounded bg-gainSoft px-1.5 py-0.5 text-[10px] text-brand">
                          <span className="truncate">agent</span>
                        </span>
                      ) : null}
                    </button>
                  </article>
                ))}
              </div>
            </div>
          )}
        </aside>

        <section className="flex min-h-0 flex-col rounded-lg border border-line bg-panel shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line p-3">
            <div className="min-w-0">
              <div className="font-mono text-[10px] font-bold uppercase text-muted">SQL</div>
              <h2 className="mt-1 truncate text-base font-semibold text-ink">查询数据</h2>
            </div>
            <div className="flex items-center gap-2">
              <select
                className="h-9 rounded-md border border-line bg-panel px-2 text-xs text-ink outline-none focus:border-signal"
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
              <button
                className="inline-flex h-9 items-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:bg-strong"
                type="button"
                disabled={isQuerying}
                onClick={() => void handleRunQuery(1)}
              >
                {isQuerying ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                执行
              </button>
            </div>
          </div>
          <div className="grid min-h-0 flex-1 grid-rows-[220px_minmax(0,1fr)]">
            <div className="border-b border-line p-3">
              <textarea
                className="h-full w-full resize-none rounded-md border border-line bg-soft p-3 font-mono text-xs leading-5 text-ink outline-none focus:border-signal"
                spellCheck={false}
                value={sql}
                onChange={(event) => setSql(event.target.value)}
              />
            </div>
            <QueryResultTable
              result={queryResult}
              isLoading={isQuerying}
              onPrev={() => void handleRunQuery(Math.max(1, page - 1))}
              onNext={() => void handleRunQuery(page + 1)}
            />
          </div>
        </section>
      </div>

      {isCreateOpen ? (
        <DatasetDialog
          form={form}
          sources={sources}
          isSourcesLoading={isSourcesLoading}
          isSubmitting={isSubmitting}
          onChange={setForm}
          onClose={() => setIsCreateOpen(false)}
          onSubmit={() => void handleCreate()}
        />
      ) : null}
      {isDetailOpen ? (
        <DatasetMetadataDialog
          detail={detail}
          draft={editDraft}
          isLoading={isDetailLoading}
          isSubmitting={isSubmitting}
          onChange={setEditDraft}
          onClose={() => setIsDetailOpen(false)}
          onDelete={() => void handleDelete()}
          onSave={() => void handleSave()}
        />
      ) : null}
    </section>
  );
}

function DatasetDialog({
  form,
  sources,
  isSourcesLoading,
  isSubmitting,
  onChange,
  onClose,
  onSubmit,
}: {
  form: DatasetForm;
  sources: MindgoSourceSummary[];
  isSourcesLoading: boolean;
  isSubmitting: boolean;
  onChange: (form: DatasetForm) => void;
  onClose: () => void;
  onSubmit: () => void;
}) {
  const updateName = (name: string) => {
    const nextSql =
      form.createSql.trim() && !form.createSql.includes("sample_value")
        ? form.createSql
        : `CREATE VIEW ${name || "dataset_view"} AS\nSELECT 1 AS sample_value`;
    onChange({
      ...form,
      name,
      createSql: nextSql,
    });
  };

  const applySourceExample = (source: MindgoSourceSummary) => {
    const viewName = form.name.trim() || sanitizeDuckDBIdentifier(`${source.id}_view`);
    onChange({
      ...form,
      name: viewName,
      description: form.description.trim() || source.description || source.name,
      categoryPath:
        form.categoryPath.trim() && form.categoryPath !== emptyForm.categoryPath
          ? form.categoryPath
          : source.category_path.join(" / "),
      createSql: sourceCreateSql(viewName, source),
    });
  };

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
      role="dialog"
      aria-modal="true"
      aria-label="新建数据集"
    >
      <div className="flex max-h-[calc(100vh-48px)] w-full max-w-6xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line p-4">
          <div className="min-w-0">
            <div className="font-mono text-[10px] font-bold uppercase text-signal">Dataset</div>
            <h2 className="mt-1 truncate text-base font-semibold text-ink">新建数据集</h2>
          </div>
          <button
            className="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="关闭"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="grid min-h-0 gap-4 overflow-y-auto p-4 lg:grid-cols-[280px_minmax(0,0.85fr)_minmax(0,1.15fr)]">
          <section className="flex min-h-0 flex-col rounded-lg border border-line bg-soft">
            <div className="flex items-center justify-between gap-2 border-b border-line px-3 py-2">
              <div className="min-w-0">
                <div className="font-mono text-[10px] font-bold uppercase text-muted">Sources</div>
                <div className="truncate text-xs font-semibold text-ink">数据源样例</div>
              </div>
              <RefreshCw className={`h-3.5 w-3.5 text-muted ${isSourcesLoading ? "animate-spin" : ""}`} />
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto p-2">
              {isSourcesLoading ? <Notice text="数据源加载中" /> : null}
              {!isSourcesLoading && sources.length === 0 ? <Notice text="暂无数据源" /> : null}
              <div className="grid gap-2">
                {sources.map((source) => (
                  <button
                    className="rounded-md border border-line bg-panel p-2 text-left transition-colors hover:border-strong hover:bg-soft focus:outline-none focus:ring-2 focus:ring-signal/20"
                    key={source.id}
                    type="button"
                    onClick={() => applySourceExample(source)}
                  >
                    <div className="flex items-start gap-2">
                      <span className="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded border border-line bg-soft text-brandBlue">
                        <Code2 className="h-3.5 w-3.5" />
                      </span>
                      <span className="min-w-0">
                        <span className="block truncate text-xs font-semibold text-ink">
                          {source.name}
                        </span>
                        <span className="mt-0.5 block truncate font-mono text-[10px] text-muted">
                          {source.id}
                        </span>
                      </span>
                    </div>
                    <div className="mt-2 truncate font-mono text-[10px] text-muted">
                      {source.storage.path}
                    </div>
                    <pre className="mt-2 max-h-20 overflow-hidden rounded bg-soft p-2 font-mono text-[10px] leading-4 text-graphite">
                      {sourceSelectSql(source)}
                    </pre>
                  </button>
                ))}
              </div>
            </div>
          </section>
          <div className="grid content-start gap-3">
            <TextField label="view name" value={form.name} onChange={updateName} />
            <TextField
              label="中文名"
              value={form.description}
              onChange={(description) => onChange({ ...form, description })}
            />
            <TextField
              label="分类路径"
              value={form.categoryPath}
              onChange={(categoryPath) => onChange({ ...form, categoryPath })}
            />
            <label className="flex items-center justify-between rounded-md border border-line bg-soft px-3 py-2 text-xs">
              <span className="font-semibold text-ink">暴露给智能体</span>
              <input
                className="h-4 w-4 accent-ink"
                type="checkbox"
                checked={form.exposedToAgent}
                onChange={(event) => onChange({ ...form, exposedToAgent: event.target.checked })}
              />
            </label>
          </div>
          <Textarea
            label="CREATE VIEW"
            value={form.createSql}
            rows={18}
            onChange={(createSql) => onChange({ ...form, createSql })}
          />
        </div>
        <div className="flex justify-end gap-2 border-t border-line p-4">
          <button
            className="inline-flex h-9 items-center gap-2 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-strong hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
            取消
          </button>
          <button
            className="inline-flex h-9 items-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:bg-strong"
            type="button"
            disabled={isSubmitting}
            onClick={onSubmit}
          >
            {isSubmitting ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4" />}
            创建
          </button>
        </div>
      </div>
    </div>
  );
}

function DatasetMetadataDialog({
  detail,
  draft,
  isLoading,
  isSubmitting,
  onChange,
  onClose,
  onDelete,
  onSave,
}: {
  detail: DatasetDetail | null;
  draft: DatasetForm;
  isLoading: boolean;
  isSubmitting: boolean;
  onChange: (form: DatasetForm) => void;
  onClose: () => void;
  onDelete: () => void;
  onSave: () => void;
}) {
  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
      role="dialog"
      aria-modal="true"
      aria-label="数据集详情"
    >
      <div className="flex max-h-[calc(100vh-48px)] w-full max-w-3xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line p-4">
          <div className="min-w-0">
            <div className="font-mono text-[10px] font-bold uppercase text-muted">Metadata</div>
            <h2 className="mt-1 truncate text-base font-semibold text-ink">
              {detail?.description || detail?.name || "数据集详情"}
            </h2>
          </div>
          <button
            className="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="关闭"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="min-h-0 overflow-y-auto p-4">
          {isLoading ? <Notice text="详情加载中" /> : null}
          {detail ? (
            <div className="grid gap-3">
              <ReadOnlyField label="id" value={detail.id} />
              <ReadOnlyField label="view name" value={detail.name} />
              <TextField
                label="中文名"
                value={draft.description}
                onChange={(description) => onChange({ ...draft, description })}
              />
              <TextField
                label="分类路径"
                value={draft.categoryPath}
                onChange={(categoryPath) => onChange({ ...draft, categoryPath })}
              />
              <label className="flex items-center justify-between rounded-md border border-line bg-soft px-3 py-2 text-xs">
                <span className="font-semibold text-ink">暴露给智能体</span>
                <input
                  className="h-4 w-4 accent-ink"
                  type="checkbox"
                  checked={draft.exposedToAgent}
                  onChange={(event) =>
                    onChange({
                      ...draft,
                      exposedToAgent: event.target.checked,
                    })
                  }
                />
              </label>
              <Textarea label="CREATE VIEW" value={detail.create_sql} rows={10} readOnly />
            </div>
          ) : (
            <Notice text="未加载数据集详情" />
          )}
        </div>

        <div className="flex flex-wrap justify-between gap-2 border-t border-line p-4">
          <button
            className="inline-flex h-9 items-center gap-1.5 rounded-md border border-risk/25 bg-riskSoft px-3 text-xs font-semibold text-risk transition-colors hover:border-risk/50 disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            disabled={!detail || isSubmitting}
            onClick={onDelete}
          >
            <Trash2 className="h-3.5 w-3.5" />
            删除
          </button>
          <div className="flex items-center gap-2">
            <button
              className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={isSubmitting}
              onClick={onClose}
            >
              关闭
            </button>
            <button
              className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={!detail || isSubmitting}
              onClick={onSave}
            >
              {isSubmitting ? <RefreshCw className="h-3.5 w-3.5 animate-spin" /> : <Check className="h-3.5 w-3.5" />}
              保存
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function QueryResultTable({
  result,
  isLoading,
  onPrev,
  onNext,
}: {
  result: DatasetQueryResponse | null;
  isLoading: boolean;
  onPrev: () => void;
  onNext: () => void;
}) {
  if (isLoading && !result) {
    return <Notice text="查询中" />;
  }
  if (!result) {
    return <Notice text="暂无结果" />;
  }
  return (
    <div className="flex min-h-0 flex-col">
      <div className="flex items-center justify-between gap-3 border-b border-line px-3 py-2">
        <div className="truncate font-mono text-[10px] font-bold text-muted">
          {result.total} rows · page {result.page}/{Math.max(1, result.total_pages)}
        </div>
        <div className="flex items-center gap-2">
          <button
            className="h-7 rounded-md border border-line px-2 text-xs font-semibold text-graphite transition-colors hover:border-strong hover:text-ink disabled:cursor-not-allowed disabled:text-muted"
            type="button"
            disabled={result.page <= 1 || isLoading}
            onClick={onPrev}
          >
            上一页
          </button>
          <button
            className="h-7 rounded-md border border-line px-2 text-xs font-semibold text-graphite transition-colors hover:border-strong hover:text-ink disabled:cursor-not-allowed disabled:text-muted"
            type="button"
            disabled={result.page >= result.total_pages || result.total_pages === 0 || isLoading}
            onClick={onNext}
          >
            下一页
          </button>
        </div>
      </div>
      <div className="min-h-0 flex-1 overflow-auto">
        <table className="min-w-full border-separate border-spacing-0 text-left text-xs">
          <thead className="sticky top-0 z-10 bg-soft text-[10px] uppercase text-muted">
            <tr>
              {result.columns.map((column) => (
                <th className="border-b border-line px-3 py-2 font-mono font-bold" key={column.name}>
                  <span className="block max-w-48 truncate">{column.name}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.rows.length === 0 ? (
              <tr>
                <td className="px-3 py-6 text-center text-muted" colSpan={Math.max(1, result.columns.length)}>
                  无数据
                </td>
              </tr>
            ) : (
              result.rows.map((row, rowIndex) => (
                <tr className="odd:bg-panel even:bg-soft/45" key={rowIndex}>
                  {result.columns.map((column) => (
                    <td className="max-w-64 border-b border-line/70 px-3 py-2 font-mono text-[11px] text-ink" key={column.name}>
                      <span className="block truncate" title={formatValue(row[column.name])}>
                        {formatValue(row[column.name])}
                      </span>
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function TextField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="grid gap-1.5">
      <span className="font-mono text-[10px] font-bold uppercase text-muted">{label}</span>
      <input
        className="h-9 rounded-md border border-line bg-panel px-3 text-xs text-ink outline-none placeholder:text-muted/70 focus:border-signal"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function Textarea({
  label,
  value,
  rows,
  readOnly,
  onChange,
}: {
  label: string;
  value: string;
  rows: number;
  readOnly?: boolean;
  onChange?: (value: string) => void;
}) {
  return (
    <label className="grid gap-1.5">
      <span className="font-mono text-[10px] font-bold uppercase text-muted">{label}</span>
      <textarea
        className="w-full resize-none rounded-md border border-line bg-soft p-3 font-mono text-xs leading-5 text-ink outline-none focus:border-signal disabled:text-muted"
        readOnly={readOnly}
        rows={rows}
        spellCheck={false}
        value={value}
        onChange={(event) => onChange?.(event.target.value)}
      />
    </label>
  );
}

function ReadOnlyField({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1.5">
      <div className="font-mono text-[10px] font-bold uppercase text-muted">{label}</div>
      <div className="truncate rounded-md border border-line bg-soft px-3 py-2 font-mono text-xs text-ink">
        {value}
      </div>
    </div>
  );
}

function IconAction({
  label,
  icon,
  danger,
  disabled,
  onClick,
}: {
  label: string;
  icon: React.ReactNode;
  danger?: boolean;
  disabled?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className={`grid h-9 w-9 place-items-center rounded-md border transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:opacity-50 ${
        danger
          ? "border-risk/25 bg-riskSoft text-risk hover:border-risk/50"
          : "border-line bg-soft text-ink hover:border-strong hover:bg-panel"
      }`}
      type="button"
      aria-label={label}
      title={label}
      disabled={disabled}
      onClick={onClick}
    >
      {icon}
    </button>
  );
}

function DatasetToast({ toast }: { toast: ToastState }) {
  const toneClass =
    toast.tone === "success"
      ? "border-brand/25 bg-gainSoft text-brand"
      : toast.tone === "error"
        ? "border-risk/25 bg-riskSoft text-risk"
        : "border-line bg-panel text-muted";

  return (
    <div
      className={`fixed right-4 top-4 z-50 max-w-sm rounded-md border px-3 py-2 text-xs font-medium shadow-xl ${toneClass}`}
      role="status"
      aria-live="polite"
    >
      {toast.message}
    </div>
  );
}

function Notice({ text }: { text: string }) {
  return (
    <div className="m-3 rounded-md border border-dashed border-line bg-soft px-3 py-5 text-center text-xs text-muted">
      {text}
    </div>
  );
}

function formFromDetail(detail: DatasetDetail): DatasetForm {
  return {
    name: detail.name,
    description: detail.description,
    categoryPath: detail.category_path.join(" / "),
    exposedToAgent: detail.exposed_to_agent,
    createSql: detail.create_sql,
  };
}

function payloadFromForm(form: DatasetForm): DatasetPayload {
  return {
    name: form.name.trim(),
    description: form.description.trim(),
    category_path: categoryPathFromText(form.categoryPath),
    exposed_to_agent: form.exposedToAgent,
    create_sql: form.createSql.trim(),
  };
}

function categoryPathFromText(value: string): string[] {
  return value
    .split(/[、,/]/)
    .map((part) => part.trim())
    .filter(Boolean);
}

function sourceCreateSql(viewName: string, source: MindgoSourceSummary): string {
  return `CREATE VIEW ${sanitizeDuckDBIdentifier(viewName)} AS
SELECT *
FROM read_parquet('${escapeSqlString(sourceParquetGlob(source))}')`;
}

function sourceSelectSql(source: MindgoSourceSummary): string {
  return `SELECT *
FROM read_parquet('${escapeSqlString(sourceParquetGlob(source))}')
LIMIT 100`;
}

function sourceParquetGlob(source: MindgoSourceSummary): string {
  const path = source.storage.path.replace(/\/+$/, "");
  return path.endsWith(".parquet") ? path : `${path}/**/*.parquet`;
}

function sanitizeDuckDBIdentifier(value: string): string {
  const identifier = value.trim().replace(/[^A-Za-z0-9_]/g, "_") || "dataset_view";
  return /^[A-Za-z_]/.test(identifier) ? identifier : `dataset_${identifier}`;
}

function escapeSqlString(value: string): string {
  return value.replace(/'/g, "''");
}

function formatValue(value: MindgoJsonValue | undefined): string {
  if (value === undefined || value === null) {
    return "";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}
