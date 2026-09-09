import {
  CalendarClock,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Database,
  Eye,
  FolderOpen,
  Loader2,
  Play,
  Power,
  PowerOff,
  RefreshCw,
  Save,
  Settings,
  Server,
  Trash2,
} from "lucide-react";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { EmptyState } from "@/shared/components";

import {
  deleteJobRuntimeInstance,
  deleteMindgoSourceSyncScheduler,
  getMindgoSourceSyncStatus,
  getMindgoSourceSchema,
  listJobRuntimeInstances,
  listMindgoSources,
  queryMindgoSource,
  rerunJobRuntimeInstance,
  syncMindgoSource,
  testMindgoConnection,
  upsertMindgoSourceSyncScheduler,
  type AppSettings,
  type JobInstanceStatus,
  type JobRuntimeInstance,
  type JobRuntimeInstanceListResponse,
  type MindgoSourceQueryResponse,
  type MindgoSourceSchema,
  type MindgoSourceSummary,
  type MindgoSourceStorageSpec,
  type MindgoSourceSyncQueryWindow,
  type MindgoSourceSyncSpec,
  type MindgoSourceSyncStatusResponse,
  type MindgoSourceSyncWriteMode,
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

type MindgoSourceMode = "mindgo" | "sync";
type MindgoParamDraft = Record<string, MindgoJsonValue>;
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
const defaultSyncWriteMode: MindgoSourceSyncWriteMode = "overwrite";
const defaultSyncInstancePageSize = 8;
type MindgoSourceUiMeta = {
  badge: string;
};
const hiddenMindgoQueryParamNames = new Set(["fields", "fq"]);
const hiddenMindgoSyncParamNames = new Set([
  ...hiddenMindgoQueryParamNames,
  "date",
  "baseDay",
  "start_date",
  "end_date",
  "bar_count",
]);
const mindgoSourceUiMeta: Record<string, MindgoSourceUiMeta> = {
  a_stock_daily_price: { badge: "1015 日行情" },
  a_stock_daily_adjust_factor: { badge: "1016 复权因子" },
  a_stock_daily_valuation_metrics: { badge: "345 估值指标" },
  a_index_daily_price: { badge: "指数日行情" },
  a_stock_snapshot_info: { badge: "1018 快照维表" },
  a_stock_minute_price: { badge: "分钟行情" },
};
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
  const [sources, setSources] = useState<MindgoSourceSummary[]>([]);
  const [selectedSourceId, setSelectedSourceId] = useState("a_stock_daily_price");
  const [schema, setSchema] = useState<MindgoSourceSchema | null>(null);
  const [queryParamsBySource, setQueryParamsBySource] = useState<Record<string, MindgoParamDraft>>({});
  const [syncParamsBySource, setSyncParamsBySource] = useState<Record<string, MindgoParamDraft>>({});
  const queryParams = queryParamsBySource[selectedSourceId] ?? {};
  const syncParams = syncParamsBySource[selectedSourceId] ?? {};
  const [queryMode, setQueryMode] = useState<MindgoSourceMode>("sync");
  const [queryResult, setQueryResult] = useState<MindgoSourceQueryResponse | null>(null);
  const [syncStatus, setSyncStatus] = useState<MindgoSourceSyncStatusResponse | null>(null);
  const [syncInstances, setSyncInstances] = useState<JobRuntimeInstanceListResponse | null>(null);
  const [syncInstancePage, setSyncInstancePage] = useState(1);
  const [syncInstancePageSize, setSyncInstancePageSize] = useState(defaultSyncInstancePageSize);
  const [syncInstanceStatusFilter, setSyncInstanceStatusFilter] = useState<SyncInstanceStatusFilter>("all");
  const [cronDraft, setCronDraft] = useState(defaultSyncCron);
  const [manualWriteModeDraft, setManualWriteModeDraft] = useState<MindgoSourceSyncWriteMode>(defaultSyncWriteMode);
  const [schedulerWriteModeDraft, setSchedulerWriteModeDraft] = useState<MindgoSourceSyncWriteMode>(defaultSyncWriteMode);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [isConnectionOpen, setIsConnectionOpen] = useState(false);
  const [isLoadingSources, setIsLoadingSources] = useState(false);
  const [isLoadingSchema, setIsLoadingSchema] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isSourceSidebarCollapsed, setIsSourceSidebarCollapsed] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isLoadingSyncStatus, setIsLoadingSyncStatus] = useState(false);
  const [isLoadingSyncInstances, setIsLoadingSyncInstances] = useState(false);
  const [mutatingInstanceId, setMutatingInstanceId] = useState<string | null>(null);
  const [isSavingScheduler, setIsSavingScheduler] = useState(false);
  const [isManualSyncOpen, setIsManualSyncOpen] = useState(false);
  const [isSchedulerSettingsOpen, setIsSchedulerSettingsOpen] = useState(false);
  const [storageDialog, setStorageDialog] = useState<{
    sourceName: string;
    storage: MindgoSourceStorageSpec;
  } | null>(null);
  const [syncStartDateDraft, setSyncStartDateDraft] = useState(today);
  const [syncEndDateDraft, setSyncEndDateDraft] = useState(today);
  const [syncTimeDraft, setSyncTimeDraft] = useState(defaultSyncTime);
  const [manualQueryWindowDraft, setManualQueryWindowDraft] =
    useState<MindgoSourceSyncQueryWindow>({
      start_offset_days: 0,
      end_offset_days: 0,
    });

  const selectedSource = useMemo(
    () => sources.find((source) => source.id === selectedSourceId) ?? sources[0] ?? null,
    [sources, selectedSourceId],
  );

  const loadSources = useCallback(async () => {
    setIsLoadingSources(true);
    try {
      const response = await listMindgoSources();
      setSources(response.sources);
      if (response.sources.length > 0) {
        setSelectedSourceId((current) =>
          response.sources.some((source) => source.id === current)
            ? current
            : response.sources[0].id,
        );
      }
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "数据源加载失败", "error");
    } finally {
      setIsLoadingSources(false);
    }
  }, [onToast]);

  const loadSchema = useCallback(async (sourceId: string) => {
    setIsLoadingSchema(true);
    setSchema(null);
    setQueryResult(null);
    try {
      const nextSchema = await getMindgoSourceSchema(sourceId);
      setSchema(nextSchema);
      setQueryParamsBySource((current) => ({
        ...current,
        [sourceId]: current[sourceId] ?? defaultParamsFromSchema(nextSchema),
      }));
      setSyncParamsBySource((current) => ({
        ...current,
        [sourceId]: current[sourceId] ?? defaultParamsFromSchema(nextSchema),
      }));
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
    sourceId: string,
    statusFilter: SyncInstanceStatusFilter = "all",
  ) => {
    setIsLoadingSyncStatus(true);
    try {
      const response = await getMindgoSourceSyncStatus(sourceId);
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
      if (selectedSourceId === sourceId) {
        onToast(caught instanceof Error ? caught.message : "同步状态加载失败", "error");
      }
    } finally {
      setIsLoadingSyncStatus(false);
    }
  }, [loadSyncInstances, onToast, selectedSourceId]);

  useEffect(() => {
    void loadSources();
  }, [loadSources]);

  useEffect(() => {
    if (selectedSourceId) {
      setSyncInstanceStatusFilter("all");
      void loadSchema(selectedSourceId);
      void loadSyncStatus(selectedSourceId, "all");
    }
  }, [loadSchema, loadSyncStatus, selectedSourceId]);

  const updateQueryParam = (name: string, value: MindgoJsonValue) => {
    setQueryParamsBySource((current) => ({
      ...current,
      [selectedSourceId]: { ...queryParams, [name]: value },
    }));
    setQueryResult(null);
    setPage(1);
  };

  const updateSyncParam = (name: string, value: MindgoJsonValue) => {
    setSyncParamsBySource((current) => ({
      ...current,
      [selectedSourceId]: { ...syncParams, [name]: value },
    }));
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
    await handleMindgoQuery(nextPage);
  };

  const handleMindgoQuery = async (nextPage = page) => {
    if (!schema) {
      return;
    }
    setIsQuerying(true);
    try {
      const response = await queryMindgoSource(selectedSourceId, {
        params: cleanVisibleParams(queryParams),
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
    setIsSyncing(true);
    setQueryResult(null);
    try {
      const response = await syncMindgoSource(selectedSourceId, {
        trigger_start_date: syncStartDateDraft,
        trigger_end_date: syncEndDateDraft,
        trigger_time: syncTimeDraft,
        write_mode: manualWriteModeDraft,
        query_window: normalizeQueryWindow(manualQueryWindowDraft, schema?.sync ?? null),
        params: cleanVisibleSyncParams(syncParams),
      });
      const instances = response.instances.length > 0 ? response.instances : [response.instance];
      await loadSyncStatus(selectedSourceId, syncInstanceStatusFilter);
      setIsManualSyncOpen(false);
      onToast(syncInstancesToast(instances), instances.some((instance) => instance.status === "failed") ? "error" : "success");
    } catch (caught) {
      onToast(caught instanceof Error ? caught.message : "同步失败", "error");
    } finally {
      setIsSyncing(false);
    }
  };

  const handleRefreshSyncRuntime = async () => {
    if (!selectedSourceId) {
      return;
    }
    await loadSyncStatus(selectedSourceId, syncInstanceStatusFilter);
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
      const response = await upsertMindgoSourceSyncScheduler(selectedSourceId, {
        cron: cronDraft,
        write_mode: schedulerWriteModeDraft,
        query_window: schema?.sync.default_query_window ?? {
          start_offset_days: 0,
          end_offset_days: 0,
        },
        params: cleanVisibleSyncParams(syncParams),
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
      const response = await deleteMindgoSourceSyncScheduler(selectedSourceId);
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
    setManualQueryWindowDraft(
      schema?.sync.default_query_window ?? {
        start_offset_days: 0,
        end_offset_days: 0,
      },
    );
    setIsManualSyncOpen(true);
  };

  const handleOpenSchedulerSettingsDialog = () => {
    setIsSchedulerSettingsOpen(true);
  };

  const canUseSource = Boolean(schema && selectedSource);
  const isBusy = isLoadingSchema || isQuerying || isSyncing || isTesting || isSavingScheduler;

  return (
    <div className="grid gap-5">
      <section className="grid gap-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-sm font-semibold text-ink">MindGo 数据源</h2>
            <p className="mt-1 text-xs text-mutedText">连接配置保存到系统设置；Token 手动维护。</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Popover open={isConnectionOpen} onOpenChange={setIsConnectionOpen}>
              <PopoverTrigger asChild>
                <Button
                  size="sm"
                  variant="outline"
                  type="button"
                  aria-expanded={isConnectionOpen}
                >
                  <Settings className="h-3.5 w-3.5" />
                  连接配置
                  <ChevronDown
                    className={`h-3.5 w-3.5 transition-transform ${
                      isConnectionOpen ? "rotate-180" : ""
                    }`}
                  />
                </Button>
              </PopoverTrigger>
              <PopoverContent align="end" className="w-[min(760px,calc(100vw-2rem))] p-3">
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
                        <Button
                          className="h-10"
                          size="sm"
                          variant="outline"
                          type="button"
                          onClick={() => void handleSelectMindgoStorageRoot()}
                        >
                          <FolderOpen className="h-3.5 w-3.5" />
                          浏览
                        </Button>
                      }
                    />
                    <NumberInput
                      label="超时 秒"
                      value={draft.mindgo.timeout_seconds}
                      onChange={(timeout_seconds) => updateMindgoSettings({ timeout_seconds })}
                    />
                  </div>
                  <div className="mt-3 flex flex-wrap justify-end gap-2 border-t border-line pt-3">
                    <Button
                      size="sm"
                      variant="outline"
                      type="button"
                      onClick={handleSaveMindgoSettings}
                    >
                      <Save className="h-3.5 w-3.5" />
                      保存配置
                    </Button>
                  </div>
              </PopoverContent>
            </Popover>
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={isTesting}
              onClick={handleTestConnection}
            >
              {isTesting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Server className="h-3.5 w-3.5" />}
              测试连接
            </Button>
          </div>
        </div>
      </section>

      <section
        className={`grid gap-4 transition-[grid-template-columns] duration-200 ${
          isSourceSidebarCollapsed
            ? "xl:grid-cols-[56px_minmax(0,1fr)]"
            : "xl:grid-cols-[280px_minmax(0,1fr)]"
        }`}
      >
        <div
          className={`rounded-md border border-line bg-soft xl:self-start ${
            isSourceSidebarCollapsed ? "grid place-items-center gap-2 p-2" : "grid gap-3 p-3"
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            {isSourceSidebarCollapsed ? null : (
              <h2 className="text-sm font-semibold text-ink">已接入数据源</h2>
            )}
            <div className="flex items-center gap-1.5">
              {isLoadingSources ? <Loader2 className="h-4 w-4 animate-spin text-mutedText" /> : null}
              <Button
                size="iconSm"
                variant="outline"
                type="button"
                title={isSourceSidebarCollapsed ? "展开数据源" : "收起数据源"}
                aria-label={isSourceSidebarCollapsed ? "展开数据源" : "收起数据源"}
                onClick={() => setIsSourceSidebarCollapsed((current) => !current)}
              >
                {isSourceSidebarCollapsed ? (
                  <ChevronRight className="h-3.5 w-3.5" />
                ) : (
                  <ChevronLeft className="h-3.5 w-3.5" />
                )}
              </Button>
            </div>
          </div>
          {isSourceSidebarCollapsed ? (
            <div
              className="grid h-10 w-10 place-items-center rounded-md border border-line bg-panel text-graphite"
              title={`已接入 ${sources.length} 个数据源`}
              aria-label={`已接入 ${sources.length} 个数据源`}
            >
              <Database className="h-4 w-4" />
            </div>
          ) : (
            <div className="grid gap-2">
              {sources.map((source) => (
                <div className="relative" key={source.id}>
                  <Button
                    className={`h-auto w-full justify-start rounded-md border py-2 pl-3 pr-14 text-left ${
                    selectedSourceId === source.id
                      ? "border-ink bg-panel text-ink"
                      : "border-line bg-panel/60 text-graphite hover:border-signal"
                    }`}
                    variant="ghost"
                    type="button"
                    onClick={() => setSelectedSourceId(source.id)}
                  >
                    <span className="grid min-w-0 gap-1">
                      <span className="flex min-w-0 items-center gap-1.5">
                        <span className="truncate text-xs font-semibold">{source.name}</span>
                        <SourceBadge sourceId={source.id} />
                      </span>
                      <span className="text-[11px] leading-4 text-mutedText">
                        {source.category_path.join(" / ")}
                      </span>
                    </span>
                  </Button>
                  <StorageSummary
                    storage={source.storage}
                    compact
                    onOpen={() =>
                      setStorageDialog({
                        sourceName: source.name,
                        storage: source.storage,
                      })
                    }
                  />
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="grid min-w-0 gap-4">
          <section className="grid gap-3 rounded-md border border-line bg-panel p-3">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="min-w-0">
                <div className="flex min-w-0 flex-wrap items-center gap-2">
                  <h2 className="truncate text-sm font-semibold text-ink">
                    {selectedSource?.name ?? "数据源"}
                  </h2>
                  {selectedSource ? <SourceBadge sourceId={selectedSource.id} /> : null}
                </div>
                <p className="mt-1 text-xs leading-5 text-mutedText">
                  {selectedSource?.description ?? "选择一个数据源后开始查询。"}
                </p>
              </div>
            </div>

            {schema ? (
              <div className="grid gap-3">
                <Tabs
                  value={queryMode}
                  onValueChange={(value) => {
                    const nextMode = value as MindgoSourceMode;
                    setQueryMode(nextMode);
                    setQueryResult(null);
                    if (nextMode === "mindgo") {
                      setPage(1);
                    }
                  }}
                >
                  <TabsList className="h-9 w-fit border bg-muted p-1">
                    <TabsTrigger className="h-7 gap-2 px-3 text-xs" value="mindgo">
                      <Server className="h-3.5 w-3.5" />
                      MindGo 查询
                    </TabsTrigger>
                    <TabsTrigger className="h-7 gap-2 px-3 text-xs" value="sync">
                      <RefreshCw className="h-3.5 w-3.5" />
                      数据同步
                    </TabsTrigger>
                  </TabsList>
                </Tabs>

                {queryMode === "mindgo" ? (
                  <div className="grid gap-3 md:grid-cols-2">
                    {(isMinuteSource(selectedSourceId)
                      ? visibleMindgoQueryParams(schema).filter((param) => !["start_date", "end_date"].includes(param.name))
                      : visibleMindgoQueryParams(schema)
                    ).map((param) => (
                      <ParamField key={param.name} param={param} value={queryParams[param.name]} onChange={(value) => updateQueryParam(param.name, value)} />
                    ))}
                    {isMinuteSource(selectedSourceId) ? (["start_date", "end_date"] as const).map((name) => (
                      <Label className="grid gap-1.5" key={name}>
                        <span>{name === "start_date" ? "起始时间" : "结束时间"}</span>
                        <DateTimePicker
                          mode="datetime"
                          value={String(queryParams[name] ?? "")}
                          onChange={(value) => updateQueryParam(name, value)}
                        />
                      </Label>
                    )) : null}
                  </div>
                ) : (
                  <div className="grid gap-4">
                    {visibleMindgoSyncParams(schema).length > 0 ? (
                      <div className="grid gap-3 rounded-md border border-line bg-soft p-3 md:grid-cols-2">
                        {visibleMindgoSyncParams(schema).map((param) => (
                          <ParamField
                            key={param.name}
                            param={param}
                            value={syncParams[param.name]}
                            onChange={(value) => updateSyncParam(param.name, value)}
                          />
                        ))}
                      </div>
                    ) : null}
                    <SyncRuntimePanel
                      disabled={!canUseSource || isBusy || isLoadingSyncStatus || isLoadingSyncInstances}
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
                  </div>
                )}
              </div>
            ) : null}

            {queryMode !== "sync" ? (
            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-3">
              <div className="flex flex-wrap items-center gap-2">
                <Button
                  size="sm"
                  type="button"
                  disabled={!canUseSource || isBusy}
                  onClick={() => void handleQuery(1)}
                >
                  {isQuerying ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
                  查询
                </Button>
              </div>
              <Label className="flex items-center gap-2">
                每页
                <Select
                  value={String(pageSize)}
                  onValueChange={(value) => {
                    setPageSize(Number(value));
                    setPage(1);
                  }}
                >
                  <SelectTrigger className="h-8 w-20 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[20, 50, 100, 200].map((size) => (
                      <SelectItem key={size} value={String(size)}>
                        {size}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </Label>
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
          queryWindow={manualQueryWindowDraft}
          startDate={syncStartDateDraft}
          syncSpec={schema?.sync ?? null}
          triggerTime={syncTimeDraft}
          writeMode={manualWriteModeDraft}
          onCancel={() => setIsManualSyncOpen(false)}
          onEndDateChange={setSyncEndDateDraft}
          onQueryWindowChange={setManualQueryWindowDraft}
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
      {storageDialog ? (
        <SourceStorageDialog
          sourceName={storageDialog.sourceName}
          storage={storageDialog.storage}
          onClose={() => setStorageDialog(null)}
        />
      ) : null}
    </div>
  );
}

function SourceBadge({ sourceId }: { sourceId: string }) {
  return (
    <Badge className="h-5 shrink-0 rounded border-line bg-soft px-1.5 font-mono text-[10px] text-mutedText" variant="outline">
      {mindgoSourceUiMeta[sourceId]?.badge ?? sourceId}
    </Badge>
  );
}

function isMinuteSource(sourceId: string): boolean {
  return sourceId === "a_stock_minute_price";
}

function StorageSummary({
  storage,
  compact = false,
  onOpen,
}: {
  storage: MindgoSourceStorageSpec;
  compact?: boolean;
  onOpen?: () => void;
}) {
  const isSnapshot = isSnapshotStorage(storage);
  if (compact) {
    return (
      <span className="absolute right-2 top-2 z-10">
        <Button
          className="h-6 px-1.5 text-[10px] text-mutedText hover:border-signal hover:text-ink"
          size="sm"
          variant="outline"
          type="button"
          onClick={(event) => {
            event.stopPropagation();
            onOpen?.();
          }}
        >
          {isSnapshot ? "快照" : "存储"}
        </Button>
      </span>
    );
  }

  return (
    <div className="grid gap-2 rounded-md border border-line bg-soft px-3 py-2">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-semibold text-graphite">本地存储</span>
        <span className="font-mono text-[11px] text-mutedText">{storage.format}</span>
      </div>
      <div className="min-w-0 truncate font-mono text-[11px] text-ink">{storage.path}</div>
      <div className="flex flex-wrap gap-1.5">
        {isSnapshot ? (
          <StorageBadge label="存储类型" value="快照文件" />
        ) : (
          <>
            <StorageBadge label="分区字段" value={storage.partitioned_by.join(", ")} />
            <StorageBadge label="分区数量" value={String(storage.partition_count)} />
            <StorageBadge label="最小分区" value={storage.min_partition ?? "-"} />
            <StorageBadge label="最大分区" value={storage.max_partition ?? "-"} />
          </>
        )}
      </div>
    </div>
  );
}

function SourceStorageDialog({
  sourceName,
  storage,
  onClose,
}: {
  sourceName: string;
  storage: MindgoSourceStorageSpec;
  onClose: () => void;
}) {
  const partitionRange = partitionRangeText(storage);
  const isSnapshot = isSnapshotStorage(storage);

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-xl overflow-hidden p-0">
        <DialogHeader className="border-b p-4">
          <div className="font-mono text-[10px] font-bold uppercase text-muted-foreground">Storage</div>
          <DialogTitle className="truncate text-base">{sourceName}</DialogTitle>
          <DialogDescription className="sr-only">数据源本地存储信息</DialogDescription>
        </DialogHeader>
        <div className="grid gap-3 p-4">
          <div className="rounded-md border bg-muted p-3">
            <div className="text-xs font-semibold">本地存储</div>
            <div className="mt-2 break-all font-mono text-[11px] leading-5 text-ink">
              {storage.path}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <StorageBadge label="格式" value={storage.format} />
            {isSnapshot ? (
              <StorageBadge label="存储类型" value="快照文件" />
            ) : (
              <>
                <StorageBadge label="分区数量" value={String(storage.partition_count)} />
                <StorageBadge label="最小分区" value={storage.min_partition ?? "-"} />
                <StorageBadge label="最大分区" value={storage.max_partition ?? "-"} />
                <StorageBadge label="分区字段" value={storage.partitioned_by.join(", ")} />
                <StorageBadge label="分区范围" value={partitionRange || "-"} />
              </>
            )}
          </div>
        </div>
        <DialogFooter className="border-t p-4">
          <Button size="sm" variant="outline" type="button" onClick={onClose}>
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function StorageBadge({ label, value }: { label: string; value: string }) {
  return (
    <Badge className="min-h-6 justify-start gap-1 text-[11px]" variant="secondary">
      {label}
      <span className="font-mono font-semibold text-ink">{value}</span>
    </Badge>
  );
}

function partitionRangeText(storage: MindgoSourceStorageSpec): string {
  if (!storage.min_partition || !storage.max_partition) {
    return "";
  }
  if (storage.min_partition === storage.max_partition) {
    return storage.min_partition;
  }
  return `${storage.min_partition}..${storage.max_partition}`;
}

function isSnapshotStorage(storage: MindgoSourceStorageSpec): boolean {
  return storage.partitioned_by.length === 0 && storage.path.endsWith(".parquet");
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
      <Label>{label}</Label>
      <span className="flex gap-2">
        <Input
          className="h-10 min-w-0 flex-1 text-xs"
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
    <Label className="grid gap-1.5">
      <span>{label}</span>
      <Input
        className="h-10 text-xs"
        min={1}
        type="number"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </Label>
  );
}

type DateTimePickerMode = "date" | "time" | "datetime";

function DateTimePicker({
  mode,
  value,
  onChange,
  min,
  disabled = false,
}: {
  mode: DateTimePickerMode;
  value: string;
  onChange: (value: string) => void;
  min?: string;
  disabled?: boolean;
}) {
  const [date = "", time = ""] = value.split(" ");
  const [hour = "00", minute = "00"] = time.split(":");
  const isDateMode = mode === "date" || mode === "datetime";
  const isTimeMode = mode === "time" || mode === "datetime";
  const update = (nextDate = date, nextHour = hour, nextMinute = minute) => {
    if (mode === "date") return onChange(nextDate);
    if (mode === "time") return onChange(`${nextHour}:${nextMinute}`);
    onChange(nextDate ? `${nextDate} ${nextHour}:${nextMinute}` : "");
  };

  if (!isDateMode) {
    return (
      <div className="grid grid-cols-2 gap-1.5">
        <TimePartSelect label="时" value={hour} count={24} disabled={disabled} onChange={(next) => update(date, next, minute)} />
        <TimePartSelect label="分" value={minute} count={60} disabled={disabled} onChange={(next) => update(date, hour, next)} />
      </div>
    );
  }

  const [open, setOpen] = useState(false);
  const selected = parseDateValue(value) ?? new Date();
  const [month, setMonth] = useState(new Date(selected.getFullYear(), selected.getMonth(), 1));
  const firstDay = new Date(month.getFullYear(), month.getMonth(), 1).getDay();
  const daysInMonth = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
  const minDate = min ? parseDateValue(min) : null;
  const dayCells = Array.from({ length: firstDay + daysInMonth }, (_, index) =>
    index < firstDay ? null : index - firstDay + 1,
  );
  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button type="button" variant="outline" disabled={disabled} className="h-10 w-full justify-start text-left text-xs font-normal">
          <CalendarClock className="mr-2 h-3.5 w-3.5" />
          {date || "选择日期"}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-72 p-3" align="start">
        <div className="mb-2 flex items-center justify-between">
          <Button type="button" size="iconSm" variant="ghost" onClick={() => setMonth(new Date(month.getFullYear(), month.getMonth() - 1, 1))}><ChevronLeft className="h-4 w-4" /></Button>
          <span className="text-xs font-semibold">{month.getFullYear()}年{month.getMonth() + 1}月</span>
          <Button type="button" size="iconSm" variant="ghost" onClick={() => setMonth(new Date(month.getFullYear(), month.getMonth() + 1, 1))}><ChevronRight className="h-4 w-4" /></Button>
        </div>
        <div className="grid grid-cols-7 gap-1 text-center text-[11px] text-mutedText">
          {['日', '一', '二', '三', '四', '五', '六'].map((day) => <span key={day}>{day}</span>)}
          {dayCells.map((day, index) => {
            if (day === null) return <span key={`empty-${index}`} />;
            const date = new Date(month.getFullYear(), month.getMonth(), day);
            const dateValue = formatLocalDate(date);
            const isDisabled = Boolean(minDate && date < minDate);
            const isSelected = dateValue === value;
            return <Button key={dateValue} type="button" size="iconSm" variant={isSelected ? "default" : "ghost"} disabled={isDisabled} onClick={() => { update(dateValue); if (mode === "date") setOpen(false); }}>{day}</Button>;
          })}
        </div>
        {mode === "datetime" ? (
          <div className="mt-3 grid grid-cols-2 gap-1.5 border-t pt-3">
            <TimePartSelect label="时" value={hour} count={24} onChange={(next) => update(date, next, minute)} />
            <TimePartSelect label="分" value={minute} count={60} onChange={(next) => update(date, hour, next)} />
          </div>
        ) : null}
      </PopoverContent>
    </Popover>
  );
}

function TimePartSelect({ label, value, count, disabled = false, onChange }: { label: string; value: string; count: number; disabled?: boolean; onChange: (value: string) => void }) {
  return (
    <Select value={value || "00"} disabled={disabled} onValueChange={onChange}>
      <SelectTrigger className="h-10 text-xs"><SelectValue /></SelectTrigger>
      <SelectContent>{Array.from({ length: count }, (_, index) => { const item = String(index).padStart(2, "0"); return <SelectItem key={item} value={item}>{item}{label}</SelectItem>; })}</SelectContent>
    </Select>
  );
}

function parseDateValue(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);
  if (!match) return null;
  return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
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
        <Label>{param.label}</Label>
        <div className="flex max-h-32 flex-wrap gap-1.5 overflow-auto rounded-md border bg-muted p-2">
          {param.options.map((option) => {
            const optionValue = String(option.value);
            const checked = selected.includes(optionValue);
            return (
              <label
                className="inline-flex h-7 items-center gap-1.5 rounded-md border bg-background px-2 text-[11px]"
                key={optionValue}
              >
                <Switch
                  className="scale-75"
                  checked={checked}
                  onCheckedChange={(nextChecked) => {
                    const nextValue = nextChecked
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
      <Label className="grid gap-1.5">
        <span>{param.label}</span>
        <Select
          value={stringParam(value)}
          onValueChange={onChange}
        >
          <SelectTrigger className="h-10 text-xs">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {param.options.map((option) => (
              <SelectItem key={String(option.value)} value={String(option.value)}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </Label>
    );
  }

  if (param.value_type === "boolean") {
    return (
      <Label className="flex min-h-10 items-center justify-between gap-3 rounded-md border bg-card px-3 py-2 shadow-sm">
        <span>{param.label}</span>
        <Switch
          checked={Boolean(value)}
          onCheckedChange={onChange}
        />
      </Label>
    );
  }

  return (
    <Label className="grid gap-1.5">
      <span>{param.label}</span>
      <Input
        className="h-10 text-xs"
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
    </Label>
  );
}

function QueryResultTable({
  result,
  disabled,
  onPageChange,
}: {
  result: MindgoSourceQueryResponse;
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
        <div className="flex items-center gap-2 text-xs text-mutedText">
          <span>
            {result.total} 行 · 第 {result.page}/{Math.max(result.total_pages, 1)} 页
          </span>
          <Pagination className="mx-0 w-auto">
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  disabled={disabled || result.page <= 1}
                  onClick={() => onPageChange(result.page - 1)}
                />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext
                  disabled={disabled || result.total_pages === 0 || result.page >= result.total_pages}
                  onClick={() => onPageChange(result.page + 1)}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </div>
      <div className="max-w-full overflow-auto rounded-md border border-line">
        <Table className="min-w-full border-collapse text-xs">
          <TableHeader className="bg-soft text-graphite">
            <TableRow>
              {columns.map((column) => (
                <TableHead className="whitespace-nowrap border-b border-line px-2.5 py-2 font-semibold" key={column.name}>
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {result.rows.map((row, rowIndex) => (
              <TableRow className="odd:bg-panel even:bg-soft/55" key={`${result.page}-${rowIndex}`}>
                {columns.map((column) => (
                  <TableCell className="whitespace-nowrap border-b border-line px-2.5 py-2 font-mono text-[11px] text-ink" key={column.name}>
                    {formatCell(row[column.name])}
                  </TableCell>
                ))}
              </TableRow>
            ))}
            {result.rows.length === 0 ? (
              <TableRow>
                <TableCell className="px-3 py-8 text-center text-xs text-mutedText" colSpan={columns.length || 1}>
                  暂无数据
                </TableCell>
              </TableRow>
            ) : null}
          </TableBody>
        </Table>
      </div>
    </section>
  );
}

function ManualSyncDialog({
  disabled,
  endDate,
  isSyncing,
  queryWindow,
  startDate,
  syncSpec,
  triggerTime,
  writeMode,
  onCancel,
  onEndDateChange,
  onQueryWindowChange,
  onStartDateChange,
  onSync,
  onTriggerTimeChange,
  onWriteModeChange,
}: {
  disabled: boolean;
  endDate: string;
  isSyncing: boolean;
  queryWindow: MindgoSourceSyncQueryWindow;
  startDate: string;
  syncSpec: MindgoSourceSyncSpec | null;
  triggerTime: string;
  writeMode: MindgoSourceSyncWriteMode;
  onCancel: () => void;
  onEndDateChange: (value: string) => void;
  onQueryWindowChange: (value: MindgoSourceSyncQueryWindow) => void;
  onStartDateChange: (value: string) => void;
  onSync: () => void;
  onTriggerTimeChange: (value: string) => void;
  onWriteModeChange: (value: MindgoSourceSyncWriteMode) => void;
}) {
  const supportsQueryWindow = Boolean(syncSpec?.supports_query_window);
  const minStartOffset = syncSpec?.min_start_offset_days ?? 0;
  const maxEndOffset = syncSpec?.max_end_offset_days ?? 0;
  const queryWindowError = supportsQueryWindow
    ? queryWindowValidationError(queryWindow, minStartOffset, maxEndOffset)
    : null;
  const invalidQueryWindow = Boolean(queryWindowError);
  const invalidRange =
    !startDate || !endDate || startDate > endDate || !triggerTime || invalidQueryWindow;
  return (
    <Dialog open onOpenChange={(open) => !open && onCancel()}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-sm">
            <Play className="h-4 w-4" />
            手动同步
          </DialogTitle>
          <DialogDescription>创建一次数据同步运行实例。</DialogDescription>
        </DialogHeader>
        <div className="grid gap-3 rounded-md border bg-muted p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <Label>写入方式</Label>
            <WriteModeSwitch
              disabled={disabled}
              value={writeMode}
              onChange={onWriteModeChange}
            />
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <Label className="grid gap-1.5">
              <span>开始日期</span>
              <DateTimePicker mode="date" value={startDate} onChange={onStartDateChange} />
            </Label>
            <Label className="grid gap-1.5">
              <span>结束日期</span>
              <DateTimePicker mode="date" min={startDate} value={endDate} onChange={onEndDateChange} />
            </Label>
            <Label className="grid gap-1.5">
              <span>触发时间</span>
              <DateTimePicker mode="time" value={triggerTime} onChange={onTriggerTimeChange} />
            </Label>
          </div>
          {supportsQueryWindow ? (
            <div className="grid gap-3 border-t border-line pt-3 sm:grid-cols-2">
              <Label className="grid gap-1.5">
                <span>开始偏移</span>
                <Input
                  className="h-10 text-xs"
                  max={inputNumberValue(queryWindow.end_offset_days)}
                  min={minStartOffset}
                  step={1}
                  type="number"
                  value={inputNumberValue(queryWindow.start_offset_days)}
                  onChange={(event) =>
                    onQueryWindowChange({
                      ...queryWindow,
                      start_offset_days: numberInputValue(event.currentTarget.value),
                    })
                  }
                />
              </Label>
              <Label className="grid gap-1.5">
                <span>结束偏移</span>
                <Input
                  className="h-10 text-xs"
                  max={maxEndOffset}
                  min={inputNumberValue(queryWindow.start_offset_days)}
                  step={1}
                  type="number"
                  value={inputNumberValue(queryWindow.end_offset_days)}
                  onChange={(event) =>
                    onQueryWindowChange({
                      ...queryWindow,
                      end_offset_days: numberInputValue(event.currentTarget.value),
                    })
                  }
                />
              </Label>
              <div className="sm:col-span-2">
                <p className="text-[11px] text-mutedText">
                  允许范围：{minStartOffset} 到 {maxEndOffset}
                </p>
                {queryWindowError ? (
                  <p className="mt-1 text-[11px] font-semibold text-risk">{queryWindowError}</p>
                ) : null}
              </div>
            </div>
          ) : null}
          <div className="flex flex-wrap justify-end gap-2">
            <Button
              size="sm"
              type="button"
              disabled={disabled || invalidRange || isSyncing}
              onClick={onSync}
            >
              {isSyncing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
              创建实例
            </Button>
          </div>
        </div>
        <DialogFooter>
          <Button
            size="sm"
            variant="outline"
            type="button"
            disabled={disabled}
            onClick={onCancel}
          >
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
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
  writeMode: MindgoSourceSyncWriteMode;
  onCancel: () => void;
  onCronChange: (value: string) => void;
  onDisableScheduler: () => void;
  onEnableScheduler: () => void;
  onWriteModeChange: (value: MindgoSourceSyncWriteMode) => void;
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
    <Dialog open onOpenChange={(open) => !open && onCancel()}>
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-sm">
            <CalendarClock className="h-4 w-4" />
            周期同步设置
            <StatusBadge tone={schedulerConfigured ? "success" : "muted"}>
              {schedulerConfigured ? "已开启同步" : "未开启同步"}
            </StatusBadge>
          </DialogTitle>
          <DialogDescription>配置数据源同步调度和写入方式。</DialogDescription>
        </DialogHeader>
        <div className="grid gap-3 rounded-md border bg-muted p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <Label>写入方式</Label>
            <WriteModeSwitch
              disabled={disabled}
              value={writeMode}
              onChange={onWriteModeChange}
            />
          </div>
          <div className="grid gap-3 border-t border-line pt-3">
            <div className="grid gap-1.5">
              <Label>执行周期</Label>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                {schedulerFrequencyOptions.map((option) => {
                  const isActive = schedule.frequency === option.value;
                  return (
                    <Button
                      key={option.value}
                      size="sm"
                      variant={isActive ? "default" : "outline"}
                      type="button"
                      disabled={disabled}
                      onClick={() => updateSchedule({ frequency: option.value })}
                    >
                      {option.label}
                    </Button>
                  );
                })}
              </div>
            </div>

            {schedule.frequency === "custom" ? (
              <Label className="grid gap-1.5">
                <span>自定义 Cron</span>
                <Input
                  className="h-10 font-mono text-xs"
                  value={schedule.customCron}
                  disabled={disabled}
                  onChange={(event) => updateSchedule({ customCron: event.target.value })}
                />
              </Label>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                <Label className="grid gap-1.5">
                  <span>触发时间</span>
                  <DateTimePicker
                    mode="time"
                    value={schedule.time}
                    disabled={disabled}
                    onChange={(time) => updateSchedule({ time })}
                  />
                </Label>
                {schedule.frequency === "weekly" ? (
                  <Label className="grid gap-1.5">
                    <span>执行日</span>
                    <Select
                      value={schedule.weekday}
                      disabled={disabled}
                      onValueChange={(weekday) => updateSchedule({ weekday })}
                    >
                      <SelectTrigger className="h-10 text-xs font-semibold">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {schedulerWeekdayOptions.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </Label>
                ) : null}
                {schedule.frequency === "monthly" ? (
                  <Label className="grid gap-1.5">
                    <span>执行日</span>
                    <Select
                      value={schedule.monthDay}
                      disabled={disabled}
                      onValueChange={(monthDay) => updateSchedule({ monthDay })}
                    >
                      <SelectTrigger className="h-10 text-xs font-semibold">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {schedulerMonthDayOptions.map((day) => (
                          <SelectItem key={day} value={day}>
                            {day} 日
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </Label>
                ) : null}
              </div>
            )}

            <div className="grid gap-1 rounded-md border border-line bg-panel px-3 py-2 text-[11px] text-mutedText">
              <span className="font-semibold text-graphite">{schedulerDescription(schedule)}</span>
              <span>
                生成 Cron：
                <code className="ml-1 rounded bg-soft px-1.5 py-0.5 font-mono text-ink">{generatedCron || "-"}</code>
              </span>
            </div>
          </div>
          <div className="grid gap-1 rounded-md border border-line bg-panel px-3 py-2 text-[11px] text-mutedText">
            <span>最近调度：{formatDateTime(lastRunAt)}</span>
            <span>下次调度：{formatDateTime(nextRunAt)}</span>
          </div>
          <div className="flex flex-wrap justify-end gap-2">
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={disabled || !schedulerConfigured || isSavingScheduler}
              onClick={onDisableScheduler}
            >
              {isSavingScheduler ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <PowerOff className="h-3.5 w-3.5" />}
              下线
            </Button>
            <Button
              size="sm"
              type="button"
              disabled={disabled || !generatedCron.trim() || isSavingScheduler}
              onClick={onEnableScheduler}
            >
              {isSavingScheduler ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : schedulerConfigured ? <CalendarClock className="h-3.5 w-3.5" /> : <Power className="h-3.5 w-3.5" />}
              {schedulerConfigured ? "更新周期" : "上线"}
            </Button>
          </div>
        </div>
        <DialogFooter>
          <Button
            size="sm"
            variant="outline"
            type="button"
            disabled={disabled}
            onClick={onCancel}
          >
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function WriteModeSwitch({
  disabled,
  value,
  onChange,
}: {
  disabled: boolean;
  value: MindgoSourceSyncWriteMode;
  onChange: (value: MindgoSourceSyncWriteMode) => void;
}) {
  return (
    <Tabs
      value={value}
      onValueChange={(nextValue) => onChange(nextValue as MindgoSourceSyncWriteMode)}
    >
      <TabsList className="h-9 w-fit border bg-background p-1">
        {[
          ["overwrite", "覆盖"],
          ["skip", "跳过"],
        ].map(([optionValue, label]) => (
          <TabsTrigger
            className="h-7 px-3 text-xs"
            disabled={disabled}
            key={optionValue}
            value={optionValue}
          >
            {label}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
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
  status: MindgoSourceSyncStatusResponse | null;
  onDeleteInstance: (instance: JobRuntimeInstance) => void;
  onInstancePageChange: (page: number) => void;
  onInstancePageSizeChange: (pageSize: number) => void;
  onInstanceStatusFilterChange: (status: SyncInstanceStatusFilter) => void;
  onOpenManualSync: () => void;
  onOpenSchedulerSettings: () => void;
  onRefresh: () => void;
  onRerunInstance: (instance: JobRuntimeInstance) => void;
}) {
  const [detailInstance, setDetailInstance] = useState<JobRuntimeInstance | null>(null);
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
        <Button
          size="sm"
          type="button"
          disabled={disabled || isSyncing}
          onClick={onOpenManualSync}
        >
          {isSyncing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
          手动同步
        </Button>
        <Button
          size="sm"
          variant="outline"
          type="button"
          disabled={disabled}
          onClick={onOpenSchedulerSettings}
        >
          <CalendarClock className="h-3.5 w-3.5" />
          周期同步设置
        </Button>
        <StatusBadge tone={schedulerConfigured ? "success" : "muted"}>
          {schedulerConfigured ? "已开启同步" : "未开启同步"}
        </StatusBadge>
        {isLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin text-mutedText" /> : null}
      </div>

      <div className="grid gap-2 border-t border-line pt-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-xs font-semibold text-graphite">实例记录</span>
          <Tabs
            className="min-w-[220px] flex-1"
            value={statusFilter}
            onValueChange={(value) => onInstanceStatusFilterChange(value as SyncInstanceStatusFilter)}
          >
            <TabsList className="flex h-auto flex-wrap justify-start gap-1.5 bg-transparent p-0">
              {syncInstanceStatusOptions.map((option) => {
                const count =
                  option.value === "all"
                    ? allInstanceCount
                    : statusCountMap.get(option.value) ?? 0;
                return (
                  <TabsTrigger
                    key={option.value}
                    className="h-8 gap-1 border border-line bg-panel px-2 text-[11px] data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
                    disabled={disabled}
                    value={option.value}
                  >
                    <span>{option.label}</span>
                    <span className="opacity-75">{count}</span>
                  </TabsTrigger>
                );
              })}
            </TabsList>
          </Tabs>
          <div className="flex items-center gap-2">
            <span className="text-[11px] text-mutedText">{instances?.total ?? 0} 条</span>
            <Label className="flex items-center gap-1 text-[11px] text-mutedText">
              每页
              <Select
                value={String(instancePageSize)}
                disabled={disabled}
                onValueChange={(value) => onInstancePageSizeChange(Number(value))}
              >
                <SelectTrigger className="h-8 w-20 text-[11px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {[8, 20, 50, 100].map((size) => (
                    <SelectItem key={size} value={String(size)}>
                      {size}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Label>
            <Button
              size="iconSm"
              variant="outline"
              type="button"
              title="刷新同步状态"
              aria-label="刷新同步状态"
              disabled={disabled}
              onClick={onRefresh}
            >
              <RefreshCw className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <Table className="w-full min-w-[1180px] border-separate border-spacing-y-1.5 text-xs">
            <TableHeader className="text-[11px] font-semibold text-mutedText">
              <TableRow>
                <TableHead className="px-2 py-1">id</TableHead>
                <TableHead className="px-2 py-1">触发方式</TableHead>
                <TableHead className="px-2 py-1">触发时间</TableHead>
                <TableHead className="px-2 py-1">开始时间</TableHead>
                <TableHead className="px-2 py-1">结束时间</TableHead>
                <TableHead className="px-2 py-1">创建时间</TableHead>
                <TableHead className="px-2 py-1">更新时间</TableHead>
                <TableHead className="px-2 py-1">状态</TableHead>
                <TableHead className="px-2 py-1">结果</TableHead>
                <TableHead className="px-2 py-1">summary</TableHead>
                <TableHead className="px-2 py-1 text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {instanceRows.map((instance) => {
                const isMutating = mutatingInstanceId === instance.id;
                return (
                  <TableRow className="bg-soft text-graphite" key={instance.id}>
                    <TableCell className="rounded-l-md px-2 py-2 font-mono text-[11px] text-ink">{instance.id}</TableCell>
                    <TableCell className="px-2 py-2">{triggerTypeLabel(instance.trigger_type)}</TableCell>
                    <TableCell className="px-2 py-2 font-mono text-[11px] text-mutedText">{formatDateTime(instance.scheduled_for)}</TableCell>
                    <TableCell className="px-2 py-2 font-mono text-[11px] text-mutedText">{formatDateTime(instance.started_at)}</TableCell>
                    <TableCell className="px-2 py-2 font-mono text-[11px] text-mutedText">{formatDateTime(instance.completed_at)}</TableCell>
                    <TableCell className="px-2 py-2 font-mono text-[11px] text-mutedText">{formatDateTime(instance.created_at)}</TableCell>
                    <TableCell className="px-2 py-2 font-mono text-[11px] text-mutedText">{formatDateTime(instance.updated_at)}</TableCell>
                    <TableCell className="px-2 py-2">
                      <StatusBadge tone={instance.status === "completed" ? "success" : instance.status === "failed" ? "danger" : "muted"}>
                        {instanceStatusLabel(instance.status)}
                      </StatusBadge>
                    </TableCell>
                    <TableCell className="px-2 py-2">{instance.result_status || "-"}</TableCell>
                    <TableCell className="max-w-[260px] truncate px-2 py-2 text-ink" title={instance.summary || instance.error_message || ""}>
                      {instance.summary || instance.error_message || "-"}
                    </TableCell>
                    <TableCell className="rounded-r-md px-2 py-2">
                      <div className="flex justify-end gap-1">
                        <Button
                          className="h-7 w-7"
                          size="iconSm"
                          variant="outline"
                          type="button"
                          title="详情"
                          aria-label={`查看实例 ${instance.id} 详情`}
                          disabled={disabled}
                          onClick={() => setDetailInstance(instance)}
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          className="h-7 w-7"
                          size="iconSm"
                          variant="outline"
                          type="button"
                          title="重新执行"
                          aria-label={`重新执行实例 ${instance.id}`}
                          disabled={disabled || Boolean(mutatingInstanceId)}
                          onClick={() => onRerunInstance(instance)}
                        >
                          {isMutating ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button
                              className="h-7 w-7 text-mutedText hover:text-destructive"
                              size="iconSm"
                              variant="outline"
                              type="button"
                              title="删除"
                              aria-label={`删除实例 ${instance.id}`}
                              disabled={disabled || Boolean(mutatingInstanceId)}
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>删除实例 {instance.id}？</AlertDialogTitle>
                              <AlertDialogDescription>
                                删除后该运行实例记录将从当前同步任务中移除。
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>取消</AlertDialogCancel>
                              <AlertDialogAction
                                className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                                onClick={() => onDeleteInstance(instance)}
                              >
                                删除
                              </AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          {instanceRows.length === 0 ? (
            <EmptyState className="mt-2 bg-soft" title="暂无实例" />
          ) : null}
        </div>
        <div className="flex flex-wrap items-center justify-end gap-2">
          <span className="font-mono text-[11px] text-mutedText">
            {totalPages > 0 ? `${instancePage} / ${totalPages}` : "0 / 0"}
          </span>
          <Pagination className="mx-0 w-auto">
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  disabled={disabled || !canGoPrev}
                  onClick={() => onInstancePageChange(instancePage - 1)}
                />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext
                  disabled={disabled || !canGoNext}
                  onClick={() => onInstancePageChange(instancePage + 1)}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </div>
      {detailInstance ? (
        <JobInstanceDetailDialog
          instance={detailInstance}
          onClose={() => setDetailInstance(null)}
        />
      ) : null}
    </div>
  );
}

function JobInstanceDetailDialog({
  instance,
  onClose,
}: {
  instance: JobRuntimeInstance;
  onClose: () => void;
}) {
  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-h-[calc(100vh-48px)] max-w-3xl overflow-hidden p-0">
        <DialogHeader className="border-b p-4">
          <div className="font-mono text-[10px] font-bold uppercase text-muted-foreground">Job Instance</div>
          <DialogTitle className="truncate font-mono text-base">{instance.id}</DialogTitle>
          <DialogDescription className="sr-only">同步任务实例详情</DialogDescription>
        </DialogHeader>
        <div className="min-h-0 overflow-y-auto p-4">
          <div className="grid gap-3">
            <div className="grid gap-2 sm:grid-cols-2">
              <InstanceDetailField label="触发方式" value={triggerTypeLabel(instance.trigger_type)} />
              <InstanceDetailField label="状态" value={instanceStatusLabel(instance.status)} />
              <InstanceDetailField label="job_type" value={instance.job_type} />
              <InstanceDetailField label="job_id" value={instance.job_id} />
              <InstanceDetailField label="trigger_key" value={instance.trigger_key} />
              <InstanceDetailField label="priority" value={String(instance.priority)} />
              <InstanceDetailField label="触发时间" value={formatDateTime(instance.scheduled_for)} />
              <InstanceDetailField label="创建时间" value={formatDateTime(instance.created_at)} />
              <InstanceDetailField label="开始时间" value={formatDateTime(instance.started_at)} />
              <InstanceDetailField label="结束时间" value={formatDateTime(instance.completed_at)} />
              <InstanceDetailField label="更新时间" value={formatDateTime(instance.updated_at)} />
              <InstanceDetailField label="结果" value={instance.result_status || "-"} />
            </div>
            {instance.summary || instance.error_message ? (
              <div className="rounded-md border border-line bg-soft p-3">
                <div className="text-xs font-semibold text-graphite">
                  {instance.error_message ? "错误信息" : "summary"}
                </div>
                <div className="mt-2 whitespace-pre-wrap break-words text-xs leading-5 text-ink">
                  {instance.error_message || instance.summary}
                </div>
              </div>
            ) : null}
            <div className="rounded-md border border-line bg-soft p-3">
              <div className="text-xs font-semibold text-graphite">payload</div>
              <pre className="mt-2 max-h-[42vh] overflow-auto whitespace-pre-wrap break-words rounded-md bg-panel p-3 font-mono text-[11px] leading-5 text-ink">
                {formatJson(instance.payload)}
              </pre>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

function InstanceDetailField({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-md border border-line bg-soft px-3 py-2">
      <div className="text-[10px] font-semibold uppercase text-mutedText">{label}</div>
      <div className="mt-1 break-all font-mono text-[11px] leading-5 text-ink">{value}</div>
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
        : "border-line bg-panel text-mutedText";
  return (
    <Badge className={`h-6 rounded px-2 text-[11px] ${className}`} variant="outline">
      {children}
    </Badge>
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

function defaultParamsFromSchema(schema: MindgoSourceSchema): MindgoParamDraft {
  const draft: MindgoParamDraft = {};
  for (const param of schema.query_params) {
    if (param.default !== null && param.default !== undefined) draft[param.name] = param.default;
    else if (param.value_type === "date") draft[param.name] = today;
    else if (param.value_type === "string[]") draft[param.name] = [];
    else if (param.value_type === "boolean") draft[param.name] = false;
    else draft[param.name] = "";
  }
  return draft;
}

function visibleMindgoQueryParams(schema: MindgoSourceSchema): MindgoParameterSpec[] {
  return schema.query_params.filter((param) => !hiddenMindgoQueryParamNames.has(param.name));
}

function visibleMindgoSyncParams(schema: MindgoSourceSchema): MindgoParameterSpec[] {
  return schema.query_params.filter((param) => !hiddenMindgoSyncParamNames.has(param.name));
}

function cleanVisibleParams(params: MindgoParamDraft): Record<string, MindgoJsonValue> {
  return cleanParams(
    Object.fromEntries(
      Object.entries(params).filter(([name]) => !hiddenMindgoQueryParamNames.has(name)),
    ),
  );
}

function cleanVisibleSyncParams(params: MindgoParamDraft): Record<string, MindgoJsonValue> {
  return cleanParams(
    Object.fromEntries(
      Object.entries(params).filter(([name]) => !hiddenMindgoSyncParamNames.has(name)),
    ),
  );
}

function normalizeQueryWindow(
  queryWindow: MindgoSourceSyncQueryWindow,
  syncSpec: MindgoSourceSyncSpec | null,
): MindgoSourceSyncQueryWindow {
  if (!syncSpec?.supports_query_window) {
    return {
      start_offset_days: 0,
      end_offset_days: 0,
    };
  }
  return {
    start_offset_days: toInteger(queryWindow.start_offset_days),
    end_offset_days: toInteger(queryWindow.end_offset_days),
  };
}

function queryWindowValidationError(
  queryWindow: MindgoSourceSyncQueryWindow,
  minStartOffset: number,
  maxEndOffset: number,
): string | null {
  if (!Number.isFinite(queryWindow.start_offset_days) || !Number.isFinite(queryWindow.end_offset_days)) {
    return "偏移量必须是整数";
  }
  if (!Number.isInteger(queryWindow.start_offset_days) || !Number.isInteger(queryWindow.end_offset_days)) {
    return "偏移量必须是整数";
  }
  if (queryWindow.start_offset_days > queryWindow.end_offset_days) {
    return "开始偏移不能大于结束偏移";
  }
  if (queryWindow.start_offset_days < minStartOffset) {
    return `开始偏移不能小于 ${minStartOffset}`;
  }
  if (queryWindow.end_offset_days > maxEndOffset) {
    return `结束偏移不能大于 ${maxEndOffset}`;
  }
  return null;
}

function numberInputValue(value: string): number {
  if (value.trim() === "") {
    return Number.NaN;
  }
  return Number(value);
}

function inputNumberValue(value: number): number | "" {
  return Number.isFinite(value) ? value : "";
}

function toInteger(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.trunc(value);
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

function formatJson(value: MindgoJsonValue | Record<string, MindgoJsonValue>): string {
  return JSON.stringify(value, null, 2);
}
