import {
  CalendarClock,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Code2,
  Database,
  FolderOpen,
  Loader2,
  Play,
  Power,
  PowerOff,
  RefreshCw,
  RotateCcw,
  Save,
  Settings,
  Server,
  Trash2,
} from "lucide-react";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";

import {
  deleteJobRuntimeInstance,
  deleteMindgoDatasetSyncScheduler,
  getMindgoDatasetSyncStatus,
  getMindgoDatasetSchema,
  listJobRuntimeInstances,
  listMindgoDatasets,
  queryMindgoDataset,
  queryMindgoDatasetFromDuckDB,
  rerunJobRuntimeInstance,
  syncMindgoDataset,
  testMindgoConnection,
  upsertMindgoDatasetSyncScheduler,
  type AppSettings,
  type JobInstanceStatus,
  type JobRuntimeInstance,
  type JobRuntimeInstanceListResponse,
  type MindgoDatasetQueryResponse,
  type MindgoDatasetSchema,
  type MindgoDatasetSummary,
  type MindgoDatasetStorageSpec,
  type MindgoDatasetSyncStatusResponse,
  type MindgoDatasetSyncWriteMode,
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
type MindgoQueryMode = "mindgo" | "duckdb" | "sync";
type SyncInstanceStatusFilter = JobInstanceStatus | "all";
type SchedulerFrequency = "daily" | "workdays" | "weekly" | "monthly" | "custom";

type SchedulerScheduleDraft = {
  frequency: SchedulerFrequency;
  time: string;
  weekday: string;
  monthDay: string;
  customCron: string;
};

const today = formatLocalDate(new Date());
const defaultSyncTime = formatLocalTime(new Date());
const defaultSyncCron = "0 18 * * 1-5";
const defaultSyncWriteMode: MindgoDatasetSyncWriteMode = "overwrite";
const defaultSyncInstancePageSize = 8;
const syncInstanceStatusOptions: Array<{ value: SyncInstanceStatusFilter; label: string }> = [
  { value: "all", label: "全部" },
  { value: "waiting", label: "等待" },
  { value: "dispatching", label: "分发" },
  { value: "running", label: "运行" },
  { value: "completed", label: "完成" },
  { value: "failed", label: "失败" },
  { value: "cancelled", label: "取消" },
];
const defaultSchedulerSchedule: SchedulerScheduleDraft = {
  frequency: "workdays",
  time: "18:00",
  weekday: "1",
  monthDay: "1",
  customCron: defaultSyncCron,
};
const schedulerFrequencyOptions: Array<{ value: SchedulerFrequency; label: string }> = [
  { value: "daily", label: "每天" },
  { value: "workdays", label: "工作日" },
  { value: "weekly", label: "每周" },
  { value: "monthly", label: "每月" },
];
const schedulerWeekdayOptions = [
  { value: "1", label: "周一" },
  { value: "2", label: "周二" },
  { value: "3", label: "周三" },
  { value: "4", label: "周四" },
  { value: "5", label: "周五" },
  { value: "6", label: "周六" },
  { value: "0", label: "周日" },
];
const schedulerMonthDayOptions = Array.from({ length: 31 }, (_, index) => String(index + 1));

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
  const [queryMode, setQueryMode] = useState<MindgoQueryMode>("mindgo");
  const [duckdbSql, setDuckdbSql] = useState("");
  const [queryResult, setQueryResult] = useState<MindgoDatasetQueryResponse | null>(null);
  const [syncStatus, setSyncStatus] = useState<MindgoDatasetSyncStatusResponse | null>(null);
  const [syncInstances, setSyncInstances] = useState<JobRuntimeInstanceListResponse | null>(null);
  const [syncInstancePage, setSyncInstancePage] = useState(1);
  const [syncInstancePageSize, setSyncInstancePageSize] = useState(defaultSyncInstancePageSize);
  const [syncInstanceStatusFilter, setSyncInstanceStatusFilter] = useState<SyncInstanceStatusFilter>("all");
  const [cronDraft, setCronDraft] = useState(defaultSyncCron);
  const [manualWriteModeDraft, setManualWriteModeDraft] = useState<MindgoDatasetSyncWriteMode>(defaultSyncWriteMode);
  const [schedulerWriteModeDraft, setSchedulerWriteModeDraft] = useState<MindgoDatasetSyncWriteMode>(defaultSyncWriteMode);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [isConnectionOpen, setIsConnectionOpen] = useState(false);
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(false);
  const [isLoadingSchema, setIsLoadingSchema] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isDatasetSidebarCollapsed, setIsDatasetSidebarCollapsed] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isLoadingSyncStatus, setIsLoadingSyncStatus] = useState(false);
  const [isLoadingSyncInstances, setIsLoadingSyncInstances] = useState(false);
  const [mutatingInstanceId, setMutatingInstanceId] = useState<string | null>(null);
  const [isSavingScheduler, setIsSavingScheduler] = useState(false);
  const [isManualSyncOpen, setIsManualSyncOpen] = useState(false);
  const [isSchedulerSettingsOpen, setIsSchedulerSettingsOpen] = useState(false);
  const [syncStartDateDraft, setSyncStartDateDraft] = useState(today);
  const [syncEndDateDraft, setSyncEndDateDraft] = useState(today);
  const [syncTimeDraft, setSyncTimeDraft] = useState(defaultSyncTime);

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
    try {
      const nextSchema = await getMindgoDatasetSchema(datasetId);
      setSchema(nextSchema);
      setParams(defaultParamsFromSchema(nextSchema));
      setDuckdbSql(defaultDuckDBSql(nextSchema));
      setPage(1);
    } catch (caught) {
      setSchema(null);
      onToast(caught instanceof Error ? caught.message : "Schema 加载失败", "error");
    } finally {
      setIsLoadingSchema(false);
    }
  }, [onToast]);

  const loadSyncInstances = useCallback(async ({
    jobType,
    jobId,
    page: nextPage = 1,
    pageSize: nextPageSize = defaultSyncInstancePageSize,
    statusFilter = "all",
  }: {
    jobType: string;
    jobId: string;
    page?: number;
    pageSize?: number;
    statusFilter?: SyncInstanceStatusFilter;
  }) => {
    setIsLoadingSyncInstances(true);
    try {
      const response = await listJobRuntimeInstances({
        job_type: jobType,
        job_id: jobId,
        status: statusFilter === "all" ? undefined : statusFilter,
        page: nextPage,
        page_size: nextPageSize,
      });
      setSyncInstances(response);
      setSyncInstancePage(response.page);
      setSyncInstancePageSize(response.page_size);
    } catch (caught) {
      setSyncInstances(null);
      onToast(caught instanceof Error ? caught.message : "实例列表加载失败", "error");
    } finally {
      setIsLoadingSyncInstances(false);
    }
  }, [onToast]);

  const loadSyncStatus = useCallback(async (
    datasetId: string,
    statusFilter: SyncInstanceStatusFilter = "all",
  ) => {
    setIsLoadingSyncStatus(true);
    try {
      const response = await getMindgoDatasetSyncStatus(datasetId);
      setSyncStatus(response);
      setCronDraft(response.scheduler.cron ?? defaultSyncCron);
      setSchedulerWriteModeDraft(response.scheduler.write_mode ?? defaultSyncWriteMode);
      await loadSyncInstances({
        jobType: response.job_type,
        jobId: response.job_id,
        page: 1,
        statusFilter,
      });
    } catch (caught) {
      setSyncStatus(null);
      setSyncInstances(null);
      if (selectedDatasetId === datasetId) {
        onToast(caught instanceof Error ? caught.message : "同步状态加载失败", "error");
      }
    } finally {
      setIsLoadingSyncStatus(false);
    }
  }, [loadSyncInstances, onToast, selectedDatasetId]);

  useEffect(() => {
    void loadDatasets();
  }, [loadDatasets]);

  useEffect(() => {
    if (selectedDatasetId) {
      setSyncInstanceStatusFilter("all");
      void loadSchema(selectedDatasetId);
      void loadSyncStatus(selectedDatasetId, "all");
    }
  }, [loadSchema, loadSyncStatus, selectedDatasetId]);

  const updateParam = (name: string, value: MindgoJsonValue) => {
    setParams((current) => ({ ...current, [name]: value }));
    setQueryResult(null);
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
    if (queryMode === "duckdb") {
      await handleDuckDBQuery(nextPage);
      return;
    }
    await handleMindgoQuery(nextPage);
  };

  const handleMindgoQuery = async (nextPage = page) => {
    if (!schema) {
      return;
    }
    setIsQuerying(true);
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

  const handleDuckDBQuery = async (nextPage = page) => {
    if (!schema || !duckdbSql.trim()) {
      return;
    }
    setIsQuerying(true);
    setQueryResult(null);
    try {
      const response = await queryMindgoDatasetFromDuckDB(selectedDatasetId, {
        sql: duckdbSql,
        page: nextPage,
        page_size: pageSize,
      });
      setPage(response.page);
      setQueryResult(response);
      onToast(`DuckDB 查询完成：${response.total} 行`, "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "DuckDB 查询失败", "error");
    } finally {
      setIsQuerying(false);
    }
  };

  const handleSync = async () => {
    setIsSyncing(true);
    setQueryResult(null);
    try {
      const response = await syncMindgoDataset(selectedDatasetId, {
        trigger_start_date: syncStartDateDraft,
        trigger_end_date: syncEndDateDraft,
        trigger_time: syncTimeDraft,
        write_mode: manualWriteModeDraft,
        params: {},
      });
      const instances = response.instances.length > 0 ? response.instances : [response.instance];
      await loadSyncStatus(selectedDatasetId, syncInstanceStatusFilter);
      setIsManualSyncOpen(false);
      onToast(syncInstancesToast(instances), instances.some((instance) => instance.status === "failed") ? "error" : "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "同步失败", "error");
    } finally {
      setIsSyncing(false);
    }
  };

  const handleRefreshSyncRuntime = async () => {
    if (!selectedDatasetId) {
      return;
    }
    await loadSyncStatus(selectedDatasetId, syncInstanceStatusFilter);
  };

  const handleSyncInstancePageChange = async (nextPage: number) => {
    if (!syncStatus) {
      return;
    }
    await loadSyncInstances({
      jobType: syncStatus.job_type,
      jobId: syncStatus.job_id,
      page: nextPage,
      pageSize: syncInstancePageSize,
      statusFilter: syncInstanceStatusFilter,
    });
  };

  const handleSyncInstancePageSizeChange = async (nextPageSize: number) => {
    setSyncInstancePageSize(nextPageSize);
    if (!syncStatus) {
      return;
    }
    await loadSyncInstances({
      jobType: syncStatus.job_type,
      jobId: syncStatus.job_id,
      page: 1,
      pageSize: nextPageSize,
      statusFilter: syncInstanceStatusFilter,
    });
  };

  const handleSyncInstanceStatusFilterChange = async (nextStatus: SyncInstanceStatusFilter) => {
    setSyncInstanceStatusFilter(nextStatus);
    if (!syncStatus) {
      return;
    }
    await loadSyncInstances({
      jobType: syncStatus.job_type,
      jobId: syncStatus.job_id,
      page: 1,
      pageSize: syncInstancePageSize,
      statusFilter: nextStatus,
    });
  };

  const handleRerunInstance = async (instance: JobRuntimeInstance) => {
    setMutatingInstanceId(instance.id);
    try {
      await rerunJobRuntimeInstance(instance.id);
      if (syncStatus) {
        await loadSyncInstances({
          jobType: syncStatus.job_type,
          jobId: syncStatus.job_id,
          page: syncInstancePage,
          pageSize: syncInstancePageSize,
          statusFilter: syncInstanceStatusFilter,
        });
      }
      onToast("实例已重新加入等待队列", "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "重新执行失败", "error");
    } finally {
      setMutatingInstanceId(null);
    }
  };

  const handleDeleteInstance = async (instance: JobRuntimeInstance) => {
    if (!window.confirm(`删除实例 ${instance.id}？`)) {
      return;
    }
    setMutatingInstanceId(instance.id);
    try {
      await deleteJobRuntimeInstance(instance.id);
      if (syncStatus) {
        const nextPage =
          syncInstances?.items.length === 1
            ? Math.max(1, syncInstancePage - 1)
            : syncInstancePage;
        await loadSyncInstances({
          jobType: syncStatus.job_type,
          jobId: syncStatus.job_id,
          page: nextPage,
          pageSize: syncInstancePageSize,
          statusFilter: syncInstanceStatusFilter,
        });
      }
      onToast("实例已删除", "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "删除实例失败", "error");
    } finally {
      setMutatingInstanceId(null);
    }
  };

  const handleSaveScheduler = async () => {
    setIsSavingScheduler(true);
    try {
      const response = await upsertMindgoDatasetSyncScheduler(selectedDatasetId, {
        cron: cronDraft,
        write_mode: schedulerWriteModeDraft,
        params: {},
      });
      setSyncStatus(response);
      setCronDraft(response.scheduler.cron ?? defaultSyncCron);
      setSchedulerWriteModeDraft(response.scheduler.write_mode ?? defaultSyncWriteMode);
      onToast("周期同步已上线", "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "周期同步保存失败", "error");
    } finally {
      setIsSavingScheduler(false);
    }
  };

  const handleDeleteScheduler = async () => {
    setIsSavingScheduler(true);
    try {
      const response = await deleteMindgoDatasetSyncScheduler(selectedDatasetId);
      setSyncStatus(response);
      onToast("周期同步已下线", "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "周期同步下线失败", "error");
    } finally {
      setIsSavingScheduler(false);
    }
  };

  const handleOpenManualSyncDialog = () => {
    setSyncStartDateDraft(today);
    setSyncEndDateDraft(today);
    setSyncTimeDraft(formatLocalTime(new Date()));
    setIsManualSyncOpen(true);
  };

  const handleOpenSchedulerSettingsDialog = () => {
    setIsSchedulerSettingsOpen(true);
  };

  const canUseDataset = Boolean(schema && selectedDataset);
  const isBusy = isLoadingSchema || isQuerying || isSyncing || isTesting || isSavingScheduler;

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

      <section
        className={`grid gap-4 transition-[grid-template-columns] duration-200 ${
          isDatasetSidebarCollapsed
            ? "xl:grid-cols-[56px_minmax(0,1fr)]"
            : "xl:grid-cols-[280px_minmax(0,1fr)]"
        }`}
      >
        <div
          className={`rounded-md border border-line bg-soft xl:self-start ${
            isDatasetSidebarCollapsed ? "grid place-items-center gap-2 p-2" : "grid gap-3 p-3"
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            {isDatasetSidebarCollapsed ? null : (
              <h2 className="text-sm font-semibold text-ink">已接入数据集</h2>
            )}
            <div className="flex items-center gap-1.5">
              {isLoadingDatasets ? <Loader2 className="h-4 w-4 animate-spin text-muted" /> : null}
              <button
                className="grid h-8 w-8 shrink-0 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                type="button"
                title={isDatasetSidebarCollapsed ? "展开数据集" : "收起数据集"}
                aria-label={isDatasetSidebarCollapsed ? "展开数据集" : "收起数据集"}
                onClick={() => setIsDatasetSidebarCollapsed((current) => !current)}
              >
                {isDatasetSidebarCollapsed ? (
                  <ChevronRight className="h-3.5 w-3.5" />
                ) : (
                  <ChevronLeft className="h-3.5 w-3.5" />
                )}
              </button>
            </div>
          </div>
          {isDatasetSidebarCollapsed ? (
            <div
              className="grid h-10 w-10 place-items-center rounded-md border border-line bg-panel text-graphite"
              title={`已接入 ${datasets.length} 个数据集`}
              aria-label={`已接入 ${datasets.length} 个数据集`}
            >
              <Database className="h-4 w-4" />
            </div>
          ) : (
            <div className="grid gap-2">
              {datasets.map((dataset) => (
                <button
                  className={`group relative grid gap-1 rounded-md border py-2 pl-3 pr-9 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 ${
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
                  <StorageSummary storage={dataset.storage} compact />
                </button>
              ))}
            </div>
          )}
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
              <div className="grid gap-3">
                <div className="inline-grid w-fit grid-cols-3 rounded-md border border-line bg-soft p-1">
                  <button
                    className={`inline-flex h-8 items-center gap-1.5 rounded px-2.5 text-xs font-semibold transition-colors ${
                      queryMode === "mindgo"
                        ? "bg-panel text-ink shadow-sm"
                        : "text-muted hover:text-ink"
                    }`}
                    type="button"
                    onClick={() => {
                      setQueryMode("mindgo");
                      setQueryResult(null);
                      setPage(1);
                    }}
                  >
                    <Server className="h-3.5 w-3.5" />
                    MindGo 查询
                  </button>
                  <button
                    className={`inline-flex h-8 items-center gap-1.5 rounded px-2.5 text-xs font-semibold transition-colors ${
                      queryMode === "duckdb"
                        ? "bg-panel text-ink shadow-sm"
                        : "text-muted hover:text-ink"
                    }`}
                    type="button"
                    onClick={() => {
                      setQueryMode("duckdb");
                      setQueryResult(null);
                      setPage(1);
                    }}
                  >
                    <Database className="h-3.5 w-3.5" />
                    DuckDB SQL
                  </button>
                  <button
                    className={`inline-flex h-8 items-center gap-1.5 rounded px-2.5 text-xs font-semibold transition-colors ${
                      queryMode === "sync"
                        ? "bg-panel text-ink shadow-sm"
                        : "text-muted hover:text-ink"
                    }`}
                    type="button"
                    onClick={() => {
                      setQueryMode("sync");
                      setQueryResult(null);
                    }}
                  >
                    <RefreshCw className="h-3.5 w-3.5" />
                    数据同步
                  </button>
                </div>

                {queryMode === "mindgo" ? (
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
                ) : queryMode === "duckdb" ? (
                  <div className="grid gap-2">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-xs font-semibold text-graphite">SQL</span>
                      <span className="max-w-full truncate font-mono text-[11px] text-muted">
                        {schema.storage.path}
                      </span>
                    </div>
                    <textarea
                      className="min-h-40 resize-y rounded-md border border-line bg-soft p-3 font-mono text-[11px] leading-5 text-ink outline-none transition-colors focus:border-signal"
                      spellCheck={false}
                      value={duckdbSql}
                      onChange={(event) => {
                        setDuckdbSql(event.target.value);
                        setPage(1);
                      }}
                    />
                  </div>
                ) : (
                  <SyncRuntimePanel
                    disabled={!canUseDataset || isBusy || isLoadingSyncStatus || isLoadingSyncInstances}
                    instancePage={syncInstancePage}
                    instancePageSize={syncInstancePageSize}
                    instances={syncInstances}
                    isLoading={isLoadingSyncStatus || isLoadingSyncInstances}
                    isSyncing={isSyncing}
                    mutatingInstanceId={mutatingInstanceId}
                    statusFilter={syncInstanceStatusFilter}
                    status={syncStatus}
                    onDeleteInstance={handleDeleteInstance}
                    onInstancePageChange={(nextPage) => void handleSyncInstancePageChange(nextPage)}
                    onInstancePageSizeChange={(nextPageSize) => void handleSyncInstancePageSizeChange(nextPageSize)}
                    onInstanceStatusFilterChange={(nextStatus) => void handleSyncInstanceStatusFilterChange(nextStatus)}
                    onOpenManualSync={handleOpenManualSyncDialog}
                    onOpenSchedulerSettings={handleOpenSchedulerSettingsDialog}
                    onRefresh={() => void handleRefreshSyncRuntime()}
                    onRerunInstance={handleRerunInstance}
                  />
                )}
              </div>
            ) : null}

            {queryMode !== "sync" ? (
            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-3">
              <div className="flex flex-wrap items-center gap-2">
                <button
                  className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
                  type="button"
                  disabled={!canUseDataset || isBusy || (queryMode === "duckdb" && !duckdbSql.trim())}
                  onClick={() => void handleQuery(1)}
                >
                  {isQuerying ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : queryMode === "duckdb" ? <Code2 className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
                  {queryMode === "duckdb" ? "运行 SQL" : "查询"}
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
            ) : null}
          </section>

          {queryResult ? (
            <QueryResultTable
              result={queryResult}
              onPageChange={(nextPage) => void handleQuery(nextPage)}
              disabled={isBusy}
            />
          ) : null}
        </div>
      </section>
      {isManualSyncOpen ? (
        <ManualSyncDialog
          disabled={isSyncing || isSavingScheduler}
          endDate={syncEndDateDraft}
          isSyncing={isSyncing}
          startDate={syncStartDateDraft}
          triggerTime={syncTimeDraft}
          writeMode={manualWriteModeDraft}
          onCancel={() => setIsManualSyncOpen(false)}
          onEndDateChange={setSyncEndDateDraft}
          onStartDateChange={(value) => {
            setSyncStartDateDraft(value);
            setSyncEndDateDraft((current) => (current < value ? value : current));
          }}
          onSync={() => void handleSync()}
          onTriggerTimeChange={setSyncTimeDraft}
          onWriteModeChange={setManualWriteModeDraft}
        />
      ) : null}
      {isSchedulerSettingsOpen ? (
        <SchedulerSyncDialog
          cron={cronDraft}
          disabled={isSyncing || isSavingScheduler}
          isSavingScheduler={isSavingScheduler}
          lastRunAt={syncStatus?.scheduler.last_run_at ?? null}
          nextRunAt={syncStatus?.scheduler.next_run_at ?? null}
          schedulerConfigured={Boolean(syncStatus?.scheduler.configured)}
          writeMode={schedulerWriteModeDraft}
          onCancel={() => setIsSchedulerSettingsOpen(false)}
          onCronChange={setCronDraft}
          onDisableScheduler={() => void handleDeleteScheduler()}
          onEnableScheduler={() => void handleSaveScheduler()}
          onWriteModeChange={setSchedulerWriteModeDraft}
        />
      ) : null}
    </div>
  );
}

function StorageSummary({
  storage,
  compact = false,
}: {
  storage: MindgoDatasetStorageSpec;
  compact?: boolean;
}) {
  const partitionRange = partitionRangeText(storage);

  if (compact) {
    return (
      <span className="absolute right-2 top-2 z-10">
        <span
          className="grid h-5 w-5 place-items-center rounded-full border border-line bg-soft font-mono text-[11px] font-bold text-muted transition-colors group-hover:border-signal group-hover:text-ink group-focus-visible:border-signal group-focus-visible:text-ink"
          aria-hidden="true"
        >
          !
        </span>
        <span className="pointer-events-none absolute right-0 top-7 z-30 hidden w-72 rounded-md border border-line bg-panel p-3 text-left shadow-lift group-hover:grid group-focus-visible:grid">
          <span className="text-xs font-semibold text-ink">本地存储</span>
          <span className="mt-1 break-all font-mono text-[11px] leading-4 text-ink">
            {storage.path}
          </span>
          <span className="mt-2 grid grid-cols-2 gap-1.5">
            <StorageBadge label="分区数量" value={String(storage.partition_count)} />
            <StorageBadge label="格式" value={storage.format} />
            <StorageBadge label="最小分区" value={storage.min_partition ?? "-"} />
            <StorageBadge label="最大分区" value={storage.max_partition ?? "-"} />
          </span>
          <span className="mt-2 font-mono text-[11px] text-muted">
            {storage.partitioned_by.join(", ") || "-"}
            {partitionRange ? ` · ${partitionRange}` : ""}
          </span>
        </span>
      </span>
    );
  }

  return (
    <div className="grid gap-2 rounded-md border border-line bg-soft px-3 py-2">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-semibold text-graphite">本地存储</span>
        <span className="font-mono text-[11px] text-muted">{storage.format}</span>
      </div>
      <div className="min-w-0 truncate font-mono text-[11px] text-ink">{storage.path}</div>
      <div className="flex flex-wrap gap-1.5">
        <StorageBadge label="分区字段" value={storage.partitioned_by.join(", ") || "-"} />
        <StorageBadge label="分区数量" value={String(storage.partition_count)} />
        <StorageBadge label="最小分区" value={storage.min_partition ?? "-"} />
        <StorageBadge label="最大分区" value={storage.max_partition ?? "-"} />
      </div>
    </div>
  );
}

function StorageBadge({ label, value }: { label: string; value: string }) {
  return (
    <span className="inline-flex min-h-6 items-center gap-1 rounded border border-line bg-panel px-2 text-[11px] text-muted">
      {label}
      <span className="font-mono font-semibold text-ink">{value}</span>
    </span>
  );
}

function partitionRangeText(storage: MindgoDatasetStorageSpec): string {
  if (!storage.min_partition || !storage.max_partition) {
    return "";
  }
  if (storage.min_partition === storage.max_partition) {
    return storage.min_partition;
  }
  return `${storage.min_partition}..${storage.max_partition}`;
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

function ManualSyncDialog({
  disabled,
  endDate,
  isSyncing,
  startDate,
  triggerTime,
  writeMode,
  onCancel,
  onEndDateChange,
  onStartDateChange,
  onSync,
  onTriggerTimeChange,
  onWriteModeChange,
}: {
  disabled: boolean;
  endDate: string;
  isSyncing: boolean;
  startDate: string;
  triggerTime: string;
  writeMode: MindgoDatasetSyncWriteMode;
  onCancel: () => void;
  onEndDateChange: (value: string) => void;
  onStartDateChange: (value: string) => void;
  onSync: () => void;
  onTriggerTimeChange: (value: string) => void;
  onWriteModeChange: (value: MindgoDatasetSyncWriteMode) => void;
}) {
  const invalidRange = !startDate || !endDate || startDate > endDate || !triggerTime;
  return (
    <div className="fixed inset-0 z-40 grid place-items-center bg-ink/20 p-4">
      <div className="grid w-full max-w-md gap-4 rounded-md border border-line bg-panel p-4 shadow-lift">
        <div className="flex items-center justify-between gap-2">
          <h2 className="text-sm font-semibold text-ink">手动同步</h2>
          <Play className="h-4 w-4 text-muted" />
        </div>
        <div className="grid gap-3 rounded-md border border-line bg-soft p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="text-xs font-semibold text-graphite">写入方式</span>
            <WriteModeSwitch
              disabled={disabled}
              value={writeMode}
              onChange={onWriteModeChange}
            />
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <label className="grid gap-1.5">
              <span className="text-xs font-semibold text-graphite">开始日期</span>
              <input
                className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
                type="date"
                value={startDate}
                onChange={(event) => onStartDateChange(event.target.value)}
              />
            </label>
            <label className="grid gap-1.5">
              <span className="text-xs font-semibold text-graphite">结束日期</span>
              <input
                className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
                min={startDate}
                type="date"
                value={endDate}
                onChange={(event) => onEndDateChange(event.target.value)}
              />
            </label>
            <label className="grid gap-1.5">
              <span className="text-xs font-semibold text-graphite">触发时间</span>
              <input
                className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal"
                step={1}
                type="time"
                value={triggerTime}
                onChange={(event) => onTriggerTimeChange(event.target.value)}
              />
            </label>
          </div>
          <div className="flex flex-wrap justify-end gap-2">
            <button
              className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={disabled || invalidRange || isSyncing}
              onClick={onSync}
            >
              {isSyncing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
              创建实例
            </button>
          </div>
        </div>
        <div className="flex flex-wrap justify-end gap-2 border-t border-line pt-3">
          <button
            className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            disabled={disabled}
            onClick={onCancel}
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  );
}

function parseSchedulerCron(cron: string): SchedulerScheduleDraft {
  const trimmedCron = cron.trim();
  const parts = trimmedCron.split(/\s+/);
  if (parts.length !== 5) {
    return {
      ...defaultSchedulerSchedule,
      frequency: "custom",
      customCron: trimmedCron,
    };
  }

  const [minute, hour, dayOfMonth, month, dayOfWeek] = parts;
  const hourNumber = Number(hour);
  const minuteNumber = Number(minute);
  const hasSingleTime =
    /^\d+$/.test(hour) &&
    /^\d+$/.test(minute) &&
    hourNumber >= 0 &&
    hourNumber <= 23 &&
    minuteNumber >= 0 &&
    minuteNumber <= 59;

  if (!hasSingleTime || month !== "*") {
    return {
      ...defaultSchedulerSchedule,
      frequency: "custom",
      customCron: trimmedCron,
    };
  }

  const time = `${String(hourNumber).padStart(2, "0")}:${String(minuteNumber).padStart(2, "0")}`;
  if (dayOfMonth === "*" && dayOfWeek === "*") {
    return {
      ...defaultSchedulerSchedule,
      frequency: "daily",
      time,
      customCron: trimmedCron,
    };
  }
  if (dayOfMonth === "*" && (dayOfWeek === "1-5" || dayOfWeek === "1,2,3,4,5")) {
    return {
      ...defaultSchedulerSchedule,
      frequency: "workdays",
      time,
      customCron: trimmedCron,
    };
  }
  if (
    dayOfMonth === "*" &&
    schedulerWeekdayOptions.some((option) => option.value === dayOfWeek)
  ) {
    return {
      ...defaultSchedulerSchedule,
      frequency: "weekly",
      time,
      weekday: dayOfWeek,
      customCron: trimmedCron,
    };
  }
  if (dayOfWeek === "*" && schedulerMonthDayOptions.includes(dayOfMonth)) {
    return {
      ...defaultSchedulerSchedule,
      frequency: "monthly",
      time,
      monthDay: dayOfMonth,
      customCron: trimmedCron,
    };
  }
  return {
    ...defaultSchedulerSchedule,
    frequency: "custom",
    time,
    customCron: trimmedCron,
  };
}

function buildSchedulerCron(schedule: SchedulerScheduleDraft): string {
  if (schedule.frequency === "custom") {
    return schedule.customCron.trim();
  }

  const [hour = "18", minute = "00"] = schedule.time.split(":");
  const normalizedHour = String(Math.min(23, Math.max(0, Number(hour) || 0)));
  const normalizedMinute = String(Math.min(59, Math.max(0, Number(minute) || 0)));

  switch (schedule.frequency) {
    case "daily":
      return `${normalizedMinute} ${normalizedHour} * * *`;
    case "workdays":
      return `${normalizedMinute} ${normalizedHour} * * 1-5`;
    case "weekly":
      return `${normalizedMinute} ${normalizedHour} * * ${schedule.weekday}`;
    case "monthly":
      return `${normalizedMinute} ${normalizedHour} ${schedule.monthDay} * *`;
    default:
      return schedule.customCron.trim();
  }
}

function schedulerDescription(schedule: SchedulerScheduleDraft): string {
  const time = schedule.time || defaultSchedulerSchedule.time;
  switch (schedule.frequency) {
    case "daily":
      return `每天 ${time} 执行`;
    case "workdays":
      return `每个工作日 ${time} 执行`;
    case "weekly": {
      const weekdayLabel =
        schedulerWeekdayOptions.find((option) => option.value === schedule.weekday)?.label ?? "周一";
      return `每${weekdayLabel} ${time} 执行`;
    }
    case "monthly":
      return `每月 ${schedule.monthDay} 日 ${time} 执行`;
    case "custom":
      return "使用自定义 Cron";
    default:
      return "使用周期设置";
  }
}

function SchedulerSyncDialog({
  cron,
  disabled,
  isSavingScheduler,
  lastRunAt,
  nextRunAt,
  schedulerConfigured,
  writeMode,
  onCancel,
  onCronChange,
  onDisableScheduler,
  onEnableScheduler,
  onWriteModeChange,
}: {
  cron: string;
  disabled: boolean;
  isSavingScheduler: boolean;
  lastRunAt: string | null;
  nextRunAt: string | null;
  schedulerConfigured: boolean;
  writeMode: MindgoDatasetSyncWriteMode;
  onCancel: () => void;
  onCronChange: (value: string) => void;
  onDisableScheduler: () => void;
  onEnableScheduler: () => void;
  onWriteModeChange: (value: MindgoDatasetSyncWriteMode) => void;
}) {
  const schedule = parseSchedulerCron(cron);
  const generatedCron = buildSchedulerCron(schedule);
  const updateSchedule = (patch: Partial<SchedulerScheduleDraft>) => {
    const nextSchedule = {
      ...schedule,
      ...patch,
      customCron: patch.customCron ?? schedule.customCron ?? cron,
    };
    onCronChange(buildSchedulerCron(nextSchedule));
  };

  return (
    <div className="fixed inset-0 z-40 grid place-items-center bg-ink/20 p-4">
      <div className="grid w-full max-w-xl gap-4 rounded-md border border-line bg-panel p-4 shadow-lift">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-ink">周期同步设置</h2>
            <StatusBadge tone={schedulerConfigured ? "success" : "muted"}>
              {schedulerConfigured ? "已开启同步" : "未开启同步"}
            </StatusBadge>
          </div>
          <CalendarClock className="h-4 w-4 text-muted" />
        </div>
        <div className="grid gap-3 rounded-md border border-line bg-soft p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="text-xs font-semibold text-graphite">写入方式</span>
            <WriteModeSwitch
              disabled={disabled}
              value={writeMode}
              onChange={onWriteModeChange}
            />
          </div>
          <div className="grid gap-3 border-t border-line pt-3">
            <div className="grid gap-1.5">
              <span className="text-xs font-semibold text-graphite">执行周期</span>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                {schedulerFrequencyOptions.map((option) => {
                  const isActive = schedule.frequency === option.value;
                  return (
                    <button
                      className={`inline-flex h-9 items-center justify-center rounded-md border px-2 text-xs font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-60 ${
                        isActive
                          ? "border-ink bg-ink text-panel"
                          : "border-line bg-panel text-graphite hover:border-signal hover:text-ink"
                      }`}
                      key={option.value}
                      type="button"
                      disabled={disabled}
                      onClick={() => updateSchedule({ frequency: option.value })}
                    >
                      {option.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {schedule.frequency === "custom" ? (
              <label className="grid gap-1.5">
                <span className="text-xs font-semibold text-graphite">自定义 Cron</span>
                <input
                  className="h-10 rounded-md border border-line bg-panel px-2.5 font-mono text-xs text-ink outline-none focus:border-signal"
                  value={schedule.customCron}
                  disabled={disabled}
                  onChange={(event) => updateSchedule({ customCron: event.target.value })}
                />
              </label>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                <label className="grid gap-1.5">
                  <span className="text-xs font-semibold text-graphite">触发时间</span>
                  <input
                    className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-ink outline-none focus:border-signal"
                    type="time"
                    step={60}
                    value={schedule.time}
                    disabled={disabled}
                    onChange={(event) => updateSchedule({ time: event.target.value })}
                  />
                </label>
                {schedule.frequency === "weekly" ? (
                  <label className="grid gap-1.5">
                    <span className="text-xs font-semibold text-graphite">执行日</span>
                    <select
                      className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-ink outline-none focus:border-signal"
                      value={schedule.weekday}
                      disabled={disabled}
                      onChange={(event) => updateSchedule({ weekday: event.target.value })}
                    >
                      {schedulerWeekdayOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </label>
                ) : null}
                {schedule.frequency === "monthly" ? (
                  <label className="grid gap-1.5">
                    <span className="text-xs font-semibold text-graphite">执行日</span>
                    <select
                      className="h-10 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-ink outline-none focus:border-signal"
                      value={schedule.monthDay}
                      disabled={disabled}
                      onChange={(event) => updateSchedule({ monthDay: event.target.value })}
                    >
                      {schedulerMonthDayOptions.map((day) => (
                        <option key={day} value={day}>
                          {day} 日
                        </option>
                      ))}
                    </select>
                  </label>
                ) : null}
              </div>
            )}

            <div className="grid gap-1 rounded-md border border-line bg-panel px-3 py-2 text-[11px] text-muted">
              <span className="font-semibold text-graphite">{schedulerDescription(schedule)}</span>
              <span>
                生成 Cron：
                <code className="ml-1 rounded bg-soft px-1.5 py-0.5 font-mono text-ink">{generatedCron || "-"}</code>
              </span>
            </div>
          </div>
          <div className="grid gap-1 rounded-md border border-line bg-panel px-3 py-2 text-[11px] text-muted">
            <span>最近调度：{formatDateTime(lastRunAt)}</span>
            <span>下次调度：{formatDateTime(nextRunAt)}</span>
          </div>
          <div className="flex flex-wrap justify-end gap-2">
            <button
              className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={disabled || !schedulerConfigured || isSavingScheduler}
              onClick={onDisableScheduler}
            >
              {isSavingScheduler ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <PowerOff className="h-3.5 w-3.5" />}
              下线
            </button>
            <button
              className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={disabled || !generatedCron.trim() || isSavingScheduler}
              onClick={onEnableScheduler}
            >
              {isSavingScheduler ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : schedulerConfigured ? <CalendarClock className="h-3.5 w-3.5" /> : <Power className="h-3.5 w-3.5" />}
              {schedulerConfigured ? "更新周期" : "上线"}
            </button>
          </div>
        </div>
        <div className="flex flex-wrap justify-end gap-2 border-t border-line pt-3">
          <button
            className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            disabled={disabled}
            onClick={onCancel}
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  );
}

function WriteModeSwitch({
  disabled,
  value,
  onChange,
}: {
  disabled: boolean;
  value: MindgoDatasetSyncWriteMode;
  onChange: (value: MindgoDatasetSyncWriteMode) => void;
}) {
  return (
    <div className="inline-grid w-fit grid-cols-2 rounded-md border border-line bg-panel p-1">
      {[
        ["overwrite", "覆盖"],
        ["skip", "跳过"],
      ].map(([optionValue, label]) => (
        <button
          className={`inline-flex h-8 items-center justify-center rounded px-3 text-xs font-semibold transition-colors ${
            value === optionValue ? "bg-ink text-panel shadow-sm" : "text-muted hover:text-ink"
          }`}
          key={optionValue}
          type="button"
          disabled={disabled}
          onClick={() => onChange(optionValue as MindgoDatasetSyncWriteMode)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

function SyncRuntimePanel({
  disabled,
  instancePage,
  instancePageSize,
  instances,
  isLoading,
  isSyncing,
  mutatingInstanceId,
  statusFilter,
  status,
  onDeleteInstance,
  onInstancePageChange,
  onInstancePageSizeChange,
  onInstanceStatusFilterChange,
  onOpenManualSync,
  onOpenSchedulerSettings,
  onRefresh,
  onRerunInstance,
}: {
  disabled: boolean;
  instancePage: number;
  instancePageSize: number;
  instances: JobRuntimeInstanceListResponse | null;
  isLoading: boolean;
  isSyncing: boolean;
  mutatingInstanceId: string | null;
  statusFilter: SyncInstanceStatusFilter;
  status: MindgoDatasetSyncStatusResponse | null;
  onDeleteInstance: (instance: JobRuntimeInstance) => void;
  onInstancePageChange: (page: number) => void;
  onInstancePageSizeChange: (pageSize: number) => void;
  onInstanceStatusFilterChange: (status: SyncInstanceStatusFilter) => void;
  onOpenManualSync: () => void;
  onOpenSchedulerSettings: () => void;
  onRefresh: () => void;
  onRerunInstance: (instance: JobRuntimeInstance) => void;
}) {
  const schedulerConfigured = Boolean(status?.scheduler.configured);
  const instanceRows = instances?.items ?? [];
  const totalPages = instances?.total_pages ?? 0;
  const canGoPrev = instancePage > 1;
  const canGoNext = totalPages > 0 && instancePage < totalPages;
  const statusCountMap = new Map(
    (instances?.status_counts ?? []).map((item) => [item.status, item.count]),
  );
  const allInstanceCount = Array.from(statusCountMap.values()).reduce(
    (total, count) => total + count,
    0,
  );

  return (
    <div className="grid gap-4">
      <div className="flex flex-wrap items-center gap-2">
        <button
          className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          disabled={disabled || isSyncing}
          onClick={onOpenManualSync}
        >
          {isSyncing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
          手动同步
        </button>
        <button
          className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          disabled={disabled}
          onClick={onOpenSchedulerSettings}
        >
          <CalendarClock className="h-3.5 w-3.5" />
          周期同步设置
        </button>
        <span
          className={`px-2 text-xs font-semibold ${
            schedulerConfigured ? "text-brand" : "text-muted"
          }`}
        >
          {schedulerConfigured ? "已开启同步" : "未开启同步"}
        </span>
        {isLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin text-muted" /> : null}
      </div>

      <div className="grid gap-2 border-t border-line pt-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-xs font-semibold text-graphite">实例记录</span>
          <div className="flex min-w-[220px] flex-1 flex-wrap items-center gap-1.5">
            {syncInstanceStatusOptions.map((option) => {
              const isActive = statusFilter === option.value;
              const count =
                option.value === "all"
                  ? allInstanceCount
                  : statusCountMap.get(option.value) ?? 0;
              return (
                <button
                  className={`inline-flex h-8 items-center gap-1 rounded-md border px-2 text-[11px] font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
                    isActive
                      ? "border-ink bg-ink text-panel"
                      : "border-line bg-panel text-graphite hover:border-signal hover:text-ink"
                  }`}
                  key={option.value}
                  type="button"
                  disabled={disabled}
                  onClick={() => onInstanceStatusFilterChange(option.value)}
                >
                  <span>{option.label}</span>
                  <span className={isActive ? "text-panel/75" : "text-muted"}>{count}</span>
                </button>
              );
            })}
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] text-muted">{instances?.total ?? 0} 条</span>
            <label className="flex items-center gap-1 text-[11px] font-semibold text-muted">
              每页
              <select
                className="h-8 rounded-md border border-line bg-panel px-2 text-[11px] outline-none focus:border-signal"
                value={instancePageSize}
                disabled={disabled}
                onChange={(event) => onInstancePageSizeChange(Number(event.target.value))}
              >
                {[8, 20, 50, 100].map((size) => (
                  <option key={size} value={size}>
                    {size}
                  </option>
                ))}
              </select>
            </label>
            <button
              className="grid h-8 w-8 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
              type="button"
              title="刷新同步状态"
              aria-label="刷新同步状态"
              disabled={disabled}
              onClick={onRefresh}
            >
              <RefreshCw className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1180px] border-separate border-spacing-y-1.5 text-left text-xs">
            <thead className="text-[11px] font-semibold text-muted">
              <tr>
                <th className="px-2 py-1">id</th>
                <th className="px-2 py-1">触发方式</th>
                <th className="px-2 py-1">触发时间</th>
                <th className="px-2 py-1">开始时间</th>
                <th className="px-2 py-1">结束时间</th>
                <th className="px-2 py-1">创建时间</th>
                <th className="px-2 py-1">更新时间</th>
                <th className="px-2 py-1">状态</th>
                <th className="px-2 py-1">结果</th>
                <th className="px-2 py-1">summary</th>
                <th className="px-2 py-1 text-right">操作</th>
              </tr>
            </thead>
            <tbody>
              {instanceRows.map((instance) => {
                const isMutating = mutatingInstanceId === instance.id;
                return (
                  <tr className="bg-soft text-graphite" key={instance.id}>
                    <td className="rounded-l-md px-2 py-2 font-mono text-[11px] text-ink">{instance.id}</td>
                    <td className="px-2 py-2">{triggerTypeLabel(instance.trigger_type)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-muted">{formatDateTime(instance.scheduled_for)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-muted">{formatDateTime(instance.started_at)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-muted">{formatDateTime(instance.completed_at)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-muted">{formatDateTime(instance.created_at)}</td>
                    <td className="px-2 py-2 font-mono text-[11px] text-muted">{formatDateTime(instance.updated_at)}</td>
                    <td className="px-2 py-2">
                      <StatusBadge tone={instance.status === "completed" ? "success" : instance.status === "failed" ? "danger" : "muted"}>
                        {instanceStatusLabel(instance.status)}
                      </StatusBadge>
                    </td>
                    <td className="px-2 py-2">{instance.result_status || "-"}</td>
                    <td className="max-w-[260px] truncate px-2 py-2 text-ink" title={instance.summary || instance.error_message || ""}>
                      {instance.summary || instance.error_message || "-"}
                    </td>
                    <td className="rounded-r-md px-2 py-2">
                      <div className="flex justify-end gap-1">
                        <button
                          className="grid h-7 w-7 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
                          type="button"
                          title="重新执行"
                          aria-label={`重新执行实例 ${instance.id}`}
                          disabled={disabled || Boolean(mutatingInstanceId)}
                          onClick={() => onRerunInstance(instance)}
                        >
                          {isMutating ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RotateCcw className="h-3.5 w-3.5" />}
                        </button>
                        <button
                          className="grid h-7 w-7 place-items-center rounded-md border border-line bg-panel text-muted transition-colors hover:border-risk hover:text-risk disabled:cursor-not-allowed disabled:opacity-50"
                          type="button"
                          title="删除"
                          aria-label={`删除实例 ${instance.id}`}
                          disabled={disabled || Boolean(mutatingInstanceId)}
                          onClick={() => onDeleteInstance(instance)}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {instanceRows.length === 0 ? (
            <div className="rounded-md bg-soft px-3 py-6 text-center text-xs text-muted">暂无实例</div>
          ) : null}
        </div>
        <div className="flex flex-wrap items-center justify-end gap-2">
          <span className="font-mono text-[11px] text-muted">
            {totalPages > 0 ? `${instancePage} / ${totalPages}` : "0 / 0"}
          </span>
          <button
            className="grid h-8 w-8 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            title="上一页"
            aria-label="上一页"
            disabled={disabled || !canGoPrev}
            onClick={() => onInstancePageChange(instancePage - 1)}
          >
            <ChevronLeft className="h-3.5 w-3.5" />
          </button>
          <button
            className="grid h-8 w-8 place-items-center rounded-md border border-line bg-panel text-graphite transition-colors hover:border-signal hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            title="下一页"
            aria-label="下一页"
            disabled={disabled || !canGoNext}
            onClick={() => onInstancePageChange(instancePage + 1)}
          >
            <ChevronRight className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({
  children,
  tone,
}: {
  children: ReactNode;
  tone: "success" | "danger" | "muted";
}) {
  const className =
    tone === "success"
      ? "border-brand/25 bg-gainSoft text-brand"
      : tone === "danger"
        ? "border-risk/25 bg-riskSoft text-risk"
        : "border-line bg-panel text-muted";
  return (
    <span className={`inline-flex h-6 items-center rounded border px-2 text-[11px] font-semibold ${className}`}>
      {children}
    </span>
  );
}

function syncInstancesToast(instances: JobRuntimeInstance[]): string {
  const failed = instances.find((instance) => instance.status === "failed");
  if (failed) {
    return failed.error_message || "同步任务失败";
  }
  if (instances.length > 1) {
    return `已创建 ${instances.length} 个同步实例`;
  }
  return instances[0]?.summary || "同步任务已创建";
}

function instanceStatusLabel(status: JobRuntimeInstance["status"]): string {
  switch (status) {
    case "waiting":
      return "等待";
    case "dispatching":
      return "分发";
    case "running":
      return "运行";
    case "completed":
      return "完成";
    case "failed":
      return "失败";
    case "cancelled":
      return "取消";
    default:
      return status;
  }
}

function triggerTypeLabel(triggerType: JobRuntimeInstance["trigger_type"]): string {
  switch (triggerType) {
    case "schedule":
      return "周期";
    case "manual":
      return "手动";
    case "rerun":
      return "重新执行";
    case "system":
      return "系统";
    default:
      return triggerType;
  }
}

function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  const second = String(date.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

function formatLocalDate(value: Date): string {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatLocalTime(value: Date): string {
  const hour = String(value.getHours()).padStart(2, "0");
  const minute = String(value.getMinutes()).padStart(2, "0");
  const second = String(value.getSeconds()).padStart(2, "0");
  return `${hour}:${minute}:${second}`;
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

function defaultDuckDBSql(schema: MindgoDatasetSchema): string {
  const parquetPath =
    schema.storage.partitioned_by.length > 0
      ? `${schema.storage.path}/${schema.storage.partitioned_by
          .map((partition) => `${partition}=*`)
          .join("/")}/data.parquet`
      : `${schema.storage.path}/*.parquet`;
  return [
    "SELECT *",
    `FROM read_parquet('${sqlStringLiteral(parquetPath)}')`,
    "LIMIT 200",
  ].join("\n");
}

function sqlStringLiteral(value: string): string {
  return value.replaceAll("'", "''");
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
