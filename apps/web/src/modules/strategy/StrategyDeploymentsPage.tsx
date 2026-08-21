import {
  CalendarClock,
  CalendarX,
  Activity,
  ListChecks,
  MoreHorizontal,
  Pencil,
  Play,
  Plus,
  RadioTower,
  RefreshCw,
  ScrollText,
  Trash2,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
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
  createStrategyDeployment,
  deleteStrategyDeployment,
  deleteStrategyDeploymentSchedule,
  getStrategyVersion,
  listStrategies,
  listStrategyDeployments,
  listStrategySignals,
  triggerStrategyDeployment,
  updateStrategyDeployment,
  upsertStrategyDeploymentSchedule,
  type Project,
  type StrategyDeployment,
  type StrategyDeploymentJobInstance,
  type StrategyDeploymentMode,
  type StrategyJsonValue,
  type StrategySignal,
  type StrategySignalActionType,
  type StrategySignalListResponse,
  type StrategySummary,
  type StrategyVersion,
} from "@/shared/api";
import {
  listJobRuntimeInstances,
  type JobInstanceStatus,
  type JobRuntimeInstanceListResponse,
} from "@/shared/api/client";
import { notify } from "@/shared/notify";

type StrategyDeploymentsPageProps = {
  project: Project | null;
};

type DeploymentForm = {
  strategyVersionId: string;
  mode: StrategyDeploymentMode;
  name: string;
  symbols: string;
  lookbackBars: string;
  brokerId: string;
  requiresManualConfirm: boolean;
  paramValues: Record<string, string>;
};

type DeploymentFilters = {
  query: string;
  strategyId: string;
  mode: "all" | StrategyDeploymentMode;
  schedule: "all" | "scheduled" | "unscheduled";
  symbol: string;
};

type DeploymentInstanceStatusFilter = "all" | JobInstanceStatus;
type SignalActionFilter = "all" | StrategySignalActionType;

const defaultForm: DeploymentForm = {
  strategyVersionId: "",
  mode: "signal",
  name: "",
  symbols: "600519.SH",
  lookbackBars: "250",
  brokerId: "",
  requiresManualConfirm: false,
  paramValues: {},
};

const defaultFilters: DeploymentFilters = {
  query: "",
  strategyId: "all",
  mode: "all",
  schedule: "all",
  symbol: "",
};

const instanceStatusFilterOptions: {
  label: string;
  value: DeploymentInstanceStatusFilter;
}[] = [
  { label: "全部", value: "all" },
  { label: "等待", value: "waiting" },
  { label: "派发中", value: "dispatching" },
  { label: "运行中", value: "running" },
  { label: "完成", value: "completed" },
  { label: "失败", value: "failed" },
  { label: "取消", value: "cancelled" },
];

const signalActionFilterOptions: {
  label: string;
  value: SignalActionFilter;
}[] = [
  { label: "全部", value: "all" },
  { label: "买入", value: "buy" },
  { label: "卖出", value: "sell" },
  { label: "平仓", value: "close" },
  { label: "撤单", value: "cancel" },
];

export function StrategyDeploymentsPage({ project }: StrategyDeploymentsPageProps) {
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [deployments, setDeployments] = useState<StrategyDeployment[]>([]);
  const [form, setForm] = useState<DeploymentForm>(defaultForm);
  const [filters, setFilters] = useState<DeploymentFilters>(defaultFilters);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editDialogDeployment, setEditDialogDeployment] = useState<StrategyDeployment | null>(null);
  const [editStrategyVersion, setEditStrategyVersion] = useState<StrategyVersion | null>(null);
  const [editForm, setEditForm] = useState<DeploymentForm>(defaultForm);
  const [stateDialogDeployment, setStateDialogDeployment] =
    useState<StrategyDeployment | null>(null);
  const [deleteDialogDeployment, setDeleteDialogDeployment] =
    useState<StrategyDeployment | null>(null);
  const [scheduleDialogDeployment, setScheduleDialogDeployment] =
    useState<StrategyDeployment | null>(null);
  const [scheduleCron, setScheduleCron] = useState("0 15 * * 1-5");
  const [instancesDialogDeployment, setInstancesDialogDeployment] =
    useState<StrategyDeployment | null>(null);
  const [deploymentInstances, setDeploymentInstances] =
    useState<JobRuntimeInstanceListResponse | null>(null);
  const [instanceStatusFilter, setInstanceStatusFilter] =
    useState<DeploymentInstanceStatusFilter>("all");
  const [isLoadingInstances, setIsLoadingInstances] = useState(false);
  const [signalsDialogDeployment, setSignalsDialogDeployment] =
    useState<StrategyDeployment | null>(null);
  const [deploymentSignals, setDeploymentSignals] =
    useState<StrategySignalListResponse | null>(null);
  const [signalActionFilter, setSignalActionFilter] = useState<SignalActionFilter>("all");
  const [isLoadingSignals, setIsLoadingSignals] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [pendingDeploymentId, setPendingDeploymentId] = useState<string | null>(null);
  const [lastInstance, setLastInstance] = useState<StrategyDeploymentJobInstance | null>(null);

  const selectedStrategy = useMemo(
    () =>
      strategies.find((strategy) => strategy.strategy_version_id === form.strategyVersionId) ??
      null,
    [form.strategyVersionId, strategies],
  );
  const strategyNameById = useMemo(
    () => new Map(strategies.map((strategy) => [strategy.strategy_id, strategy.name])),
    [strategies],
  );
  const filteredDeployments = useMemo(
    () =>
      deployments.filter((deployment) => {
        const query = filters.query.trim().toLowerCase();
        const symbolQuery = filters.symbol.trim().toLowerCase();
        const strategyName = strategyNameById.get(deployment.strategy_id) ?? "";
        if (
          query &&
          ![
            deployment.name,
            deployment.id,
            strategyName,
            deployment.symbols.join(","),
            String(deployment.lookback_bars),
          ]
            .join(" ")
            .toLowerCase()
            .includes(query)
        ) {
          return false;
        }
        if (filters.strategyId !== "all" && deployment.strategy_id !== filters.strategyId) {
          return false;
        }
        if (filters.mode !== "all" && deployment.mode !== filters.mode) {
          return false;
        }
        if (filters.schedule === "scheduled" && !deployment.scheduled) {
          return false;
        }
        if (filters.schedule === "unscheduled" && deployment.scheduled) {
          return false;
        }
        if (
          symbolQuery &&
          !deployment.symbols.some((symbol) => symbol.toLowerCase().includes(symbolQuery))
        ) {
          return false;
        }
        return true;
      }),
    [deployments, filters, strategyNameById],
  );

  const loadPage = useCallback(async () => {
    if (!project) {
      setStrategies([]);
      setDeployments([]);
      return;
    }
    setIsLoading(true);
    try {
      const [strategyItems, deploymentItems] = await Promise.all([
        listStrategies(project.id),
        listStrategyDeployments(project.id),
      ]);
      setStrategies(strategyItems);
      setDeployments(deploymentItems);
      const firstStrategy = strategyItems[0];
      setForm((current) => ({
        ...current,
        strategyVersionId:
          current.strategyVersionId || firstStrategy?.strategy_version_id || "",
        name: current.name || (firstStrategy ? `${firstStrategy.name} 部署` : ""),
        paramValues:
          Object.keys(current.paramValues).length > 0
            ? current.paramValues
            : firstStrategy
              ? paramDefaults(firstStrategy)
              : {},
      }));
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "策略部署加载失败", "error");
    } finally {
      setIsLoading(false);
    }
  }, [project]);

  useEffect(() => {
    void loadPage();
  }, [loadPage]);

  const handleCreateDeployment = async () => {
    if (!project || !selectedStrategy) {
      notify("请选择一个策略版本", "error");
      return;
    }
    const symbols = parseSymbols(form.symbols);
    if (symbols.length === 0) {
      notify("至少填写一个标的", "error");
      return;
    }
    if (form.mode !== "signal" && !form.brokerId.trim()) {
      notify("模拟盘或实盘部署需要填写 broker ID", "error");
      return;
    }
    setPendingDeploymentId("create");
    try {
      const deployment = await createStrategyDeployment({
        project_id: project.id,
        strategy_id: selectedStrategy.strategy_id,
        strategy_version_id: selectedStrategy.strategy_version_id,
        name: form.name.trim() || `${selectedStrategy.name} 部署`,
        mode: form.mode,
        symbols,
        lookback_bars: parseLookbackBars(form.lookbackBars),
        params: parseParamValues(selectedStrategy, form.paramValues),
        broker_id: form.mode === "signal" ? null : form.brokerId.trim(),
        requires_manual_confirm: form.requiresManualConfirm,
        risk_config: {},
      });
      setDeployments((current) => [deployment, ...current]);
      setIsCreateOpen(false);
      setForm((current) => ({
        ...defaultForm,
        strategyVersionId: current.strategyVersionId,
        mode: current.mode,
        paramValues: current.paramValues,
      }));
      notify("策略部署已创建", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "创建部署失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const handleOpenEditDeployment = async (deployment: StrategyDeployment) => {
    setPendingDeploymentId(deployment.id);
    try {
      const version = await getStrategyVersion(deployment.strategy_version_id);
      setEditStrategyVersion(version);
      setEditForm(formFromDeployment(deployment, version));
      setEditDialogDeployment(deployment);
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "加载部署配置失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const handleUpdateDeployment = async () => {
    if (!editDialogDeployment || !editStrategyVersion) {
      return;
    }
    const symbols = parseSymbols(editForm.symbols);
    if (symbols.length === 0) {
      notify("至少填写一个标的", "error");
      return;
    }
    if (editForm.mode !== "signal" && !editForm.brokerId.trim()) {
      notify("模拟盘或实盘部署需要填写 broker ID", "error");
      return;
    }
    setPendingDeploymentId(editDialogDeployment.id);
    try {
      const updated = await updateStrategyDeployment(editDialogDeployment.id, {
        strategy_version_id: editStrategyVersion.id,
        name: editForm.name.trim() || editDialogDeployment.name,
        mode: editForm.mode,
        symbols,
        lookback_bars: parseLookbackBars(editForm.lookbackBars),
        params: parseParamValues(editStrategyVersion, editForm.paramValues),
        broker_id: editForm.mode === "signal" ? null : editForm.brokerId.trim(),
        requires_manual_confirm: editForm.requiresManualConfirm,
        risk_config: editDialogDeployment.risk_config,
      });
      setDeployments((current) =>
        current.map((deployment) => (deployment.id === updated.id ? updated : deployment)),
      );
      setEditDialogDeployment(null);
      setEditStrategyVersion(null);
      notify("部署配置已更新", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "更新部署失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const handleDeleteDeployment = async (deployment: StrategyDeployment) => {
    setPendingDeploymentId(deployment.id);
    try {
      const deleted = await deleteStrategyDeployment(deployment.id);
      setDeployments((current) => current.filter((item) => item.id !== deleted.id));
      if (lastInstance?.job_id === deleted.id) {
        setLastInstance(null);
      }
      notify("部署已删除，相关调度和实例已清理", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "删除部署失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const loadDeploymentInstances = async (
    deployment: StrategyDeployment,
    statusFilter: DeploymentInstanceStatusFilter,
  ) => {
    setIsLoadingInstances(true);
    try {
      const response = await listJobRuntimeInstances({
        job_type: "strategy_deployment_tick",
        job_id: deployment.id,
        status: statusFilter === "all" ? undefined : statusFilter,
        page: 1,
        page_size: 20,
      });
      setDeploymentInstances(response);
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "加载实例列表失败", "error");
    } finally {
      setIsLoadingInstances(false);
    }
  };

  const handleOpenInstances = async (deployment: StrategyDeployment) => {
    setInstancesDialogDeployment(deployment);
    setDeploymentInstances(null);
    setInstanceStatusFilter("all");
    await loadDeploymentInstances(deployment, "all");
  };

  const handleInstanceStatusFilterChange = async (
    statusFilter: DeploymentInstanceStatusFilter,
  ) => {
    setInstanceStatusFilter(statusFilter);
    if (instancesDialogDeployment) {
      await loadDeploymentInstances(instancesDialogDeployment, statusFilter);
    }
  };

  const loadDeploymentSignals = async (
    deployment: StrategyDeployment,
    actionFilter: SignalActionFilter,
  ) => {
    setIsLoadingSignals(true);
    try {
      const signals = await listStrategySignals(deployment.id, {
        limit: 100,
        action: actionFilter === "all" ? undefined : actionFilter,
      });
      setDeploymentSignals(signals);
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "加载信号列表失败", "error");
    } finally {
      setIsLoadingSignals(false);
    }
  };

  const handleOpenSignals = async (deployment: StrategyDeployment) => {
    setSignalsDialogDeployment(deployment);
    setDeploymentSignals(null);
    setSignalActionFilter("all");
    await loadDeploymentSignals(deployment, "all");
  };

  const handleSignalActionFilterChange = async (actionFilter: SignalActionFilter) => {
    setSignalActionFilter(actionFilter);
    if (signalsDialogDeployment) {
      await loadDeploymentSignals(signalsDialogDeployment, actionFilter);
    }
  };

  const handleTriggerDeployment = async (deployment: StrategyDeployment) => {
    setPendingDeploymentId(deployment.id);
    try {
      const instance = await triggerStrategyDeployment(deployment.id);
      setLastInstance(instance);
      notify("已创建部署运行实例", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "触发部署失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const handleDeleteSchedule = async (deployment: StrategyDeployment) => {
    setPendingDeploymentId(deployment.id);
    try {
      const updated = await deleteStrategyDeploymentSchedule(deployment.id);
      setDeployments((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
      notify("调度已取消", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "取消调度失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  const handleOpenSchedule = (deployment: StrategyDeployment) => {
    setScheduleCron(deployment.schedule_cron || "0 15 * * 1-5");
    setScheduleDialogDeployment(deployment);
  };

  const handleSaveSchedule = async () => {
    if (!scheduleDialogDeployment) {
      return;
    }
    setPendingDeploymentId(scheduleDialogDeployment.id);
    try {
      const updated = await upsertStrategyDeploymentSchedule(
        scheduleDialogDeployment.id,
        scheduleCron,
      );
      setDeployments((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
      setScheduleDialogDeployment(null);
      notify("调度已保存", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "保存调度失败", "error");
    } finally {
      setPendingDeploymentId(null);
    }
  };

  if (!project) {
    return <EmptyState title="暂无项目" description="先创建或选择一个项目后再管理策略部署。" />;
  }

  return (
    <section className="mx-auto flex w-full max-w-6xl flex-col gap-4" aria-label="策略部署">
      <header className="flex flex-wrap items-end justify-between gap-3 border-b border-line pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase text-mutedText">
            <RadioTower className="h-4 w-4" />
            Strategy Deployment
          </div>
          <h1 className="mt-1 text-xl font-black text-ink">策略部署</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" type="button" onClick={() => void loadPage()}>
            <RefreshCw className="h-4 w-4" />
            刷新
          </Button>
          <Button type="button" onClick={() => setIsCreateOpen(true)}>
            <Plus className="h-4 w-4" />
            新建部署
          </Button>
        </div>
      </header>

      <section className="rounded-lg border bg-panel">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-4 py-3">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-bold text-ink">部署列表</h2>
            <Badge variant="outline">
              {filteredDeployments.length}/{deployments.length}
            </Badge>
          </div>
          {lastInstance ? (
            <div className="font-mono text-[11px] text-mutedText">
              最近实例 {lastInstance.id} · {lastInstance.status}
            </div>
          ) : null}
        </div>

        <div className="flex flex-wrap items-center gap-2 border-b border-line px-4 py-3">
          <Input
            className="h-8 w-64 text-xs"
            placeholder="搜索名称 / ID / 策略"
            value={filters.query}
            onChange={(event) =>
              setFilters((current) => ({ ...current, query: event.target.value }))
            }
          />
          <select
            className="h-8 w-44 rounded-md border border-input bg-background px-2 text-xs"
            value={filters.strategyId}
            onChange={(event) =>
              setFilters((current) => ({ ...current, strategyId: event.target.value }))
            }
          >
            <option value="all">全部策略</option>
            {strategies.map((strategy) => (
              <option key={strategy.strategy_id} value={strategy.strategy_id}>
                {strategy.name}
              </option>
            ))}
          </select>
          <select
            className="h-8 w-28 rounded-md border border-input bg-background px-2 text-xs"
            value={filters.mode}
            onChange={(event) =>
              setFilters((current) => ({
                ...current,
                mode: event.target.value as DeploymentFilters["mode"],
              }))
            }
          >
            <option value="all">全部模式</option>
            <option value="signal">信号</option>
            <option value="paper">模拟盘</option>
            <option value="live">实盘</option>
          </select>
          <select
            className="h-8 w-28 rounded-md border border-input bg-background px-2 text-xs"
            value={filters.schedule}
            onChange={(event) =>
              setFilters((current) => ({
                ...current,
                schedule: event.target.value as DeploymentFilters["schedule"],
              }))
            }
          >
            <option value="all">全部状态</option>
            <option value="scheduled">已调度</option>
            <option value="unscheduled">未调度</option>
          </select>
          <Input
            className="h-8 w-40 text-xs"
            placeholder="按标的过滤"
            value={filters.symbol}
            onChange={(event) =>
              setFilters((current) => ({ ...current, symbol: event.target.value }))
            }
          />
        </div>

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="min-w-56">部署</TableHead>
              <TableHead className="min-w-40">策略</TableHead>
              <TableHead>模式</TableHead>
              <TableHead className="min-w-36">标的</TableHead>
              <TableHead>状态</TableHead>
              <TableHead className="text-right">操作</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="h-28 text-center text-sm text-mutedText">
                  部署加载中
                </TableCell>
              </TableRow>
            ) : null}
            {!isLoading && filteredDeployments.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-32 text-center">
                  <div className="text-sm font-semibold text-ink">暂无部署</div>
                  <div className="mt-1 text-xs text-mutedText">
                    没有匹配当前筛选条件的策略部署。
                  </div>
                </TableCell>
              </TableRow>
            ) : null}
            {!isLoading
              ? filteredDeployments.map((deployment) => (
                  <TableRow key={deployment.id}>
                    <TableCell>
                      <div className="font-bold text-ink">{deployment.name}</div>
                      <div className="mt-1 max-w-72 truncate font-mono text-[11px] text-mutedText">
                        {deployment.id}
                      </div>
                    </TableCell>
                    <TableCell className="max-w-48 truncate text-graphite">
                      {strategyNameById.get(deployment.strategy_id) ?? deployment.strategy_id}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{modeLabel(deployment.mode)}</Badge>
                    </TableCell>
                    <TableCell className="max-w-48 truncate font-mono text-xs text-mutedText">
                      {deployment.symbols.join(", ") || "-"} · {deployment.lookback_bars} bars
                    </TableCell>
                    <TableCell>
                      <div className="grid gap-1">
                        <Badge variant={deployment.scheduled ? "default" : "outline"}>
                          {deployment.scheduled ? "已调度" : "未调度"}
                        </Badge>
                        {deployment.schedule_cron ? (
                          <span className="font-mono text-[11px] text-mutedText">
                            {deployment.schedule_cron}
                          </span>
                        ) : null}
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          type="button"
                          disabled={pendingDeploymentId === deployment.id}
                          onClick={() => void handleOpenInstances(deployment)}
                        >
                          <ListChecks className="h-4 w-4" />
                          实例
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          type="button"
                          disabled={pendingDeploymentId === deployment.id}
                          onClick={() => void handleOpenSignals(deployment)}
                        >
                          <Activity className="h-4 w-4" />
                          信号
                        </Button>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              size="sm"
                              variant="outline"
                              type="button"
                              disabled={pendingDeploymentId === deployment.id}
                            >
                              <MoreHorizontal className="h-4 w-4" />
                              更多
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => setStateDialogDeployment(deployment)}>
                              <ScrollText className="h-4 w-4" />
                              查看 State
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() => void handleOpenEditDeployment(deployment)}
                            >
                              <Pencil className="h-4 w-4" />
                              编辑
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => handleOpenSchedule(deployment)}>
                              <CalendarClock className="h-4 w-4" />
                              配置调度
                            </DropdownMenuItem>
                            {deployment.scheduled ? (
                              <DropdownMenuItem
                                onClick={() => void handleDeleteSchedule(deployment)}
                              >
                                <CalendarX className="h-4 w-4" />
                                取消调度
                              </DropdownMenuItem>
                            ) : null}
                            <DropdownMenuItem
                              onClick={() => void handleTriggerDeployment(deployment)}
                            >
                              <Play className="h-4 w-4" />
                              手动触发
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              className="text-destructive focus:text-destructive"
                              onClick={() => setDeleteDialogDeployment(deployment)}
                            >
                              <Trash2 className="h-4 w-4" />
                              删除
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              : null}
          </TableBody>
        </Table>
      </section>

      <CreateDeploymentDialog
        form={form}
        isOpen={isCreateOpen}
        isSaving={pendingDeploymentId === "create"}
        selectedStrategy={selectedStrategy}
        strategies={strategies}
        onChange={setForm}
        onClose={() => setIsCreateOpen(false)}
        onSubmit={() => void handleCreateDeployment()}
      />
      <EditDeploymentDialog
        deployment={editDialogDeployment}
        form={editForm}
        isSaving={
          editDialogDeployment ? pendingDeploymentId === editDialogDeployment.id : false
        }
        strategyVersion={editStrategyVersion}
        onChange={setEditForm}
        onClose={() => {
          setEditDialogDeployment(null);
          setEditStrategyVersion(null);
        }}
        onSubmit={() => void handleUpdateDeployment()}
      />
      <DeploymentInstancesDialog
        deployment={instancesDialogDeployment}
        instances={deploymentInstances}
        isLoading={isLoadingInstances}
        statusFilter={instanceStatusFilter}
        onClose={() => {
          setInstancesDialogDeployment(null);
          setDeploymentInstances(null);
        }}
        onRefresh={() => {
          if (instancesDialogDeployment) {
            void loadDeploymentInstances(instancesDialogDeployment, instanceStatusFilter);
          }
        }}
        onStatusFilterChange={(statusFilter) => {
          void handleInstanceStatusFilterChange(statusFilter);
        }}
      />
      <DeploymentSignalsDialog
        deployment={signalsDialogDeployment}
        signals={deploymentSignals}
        isLoading={isLoadingSignals}
        actionFilter={signalActionFilter}
        onClose={() => {
          setSignalsDialogDeployment(null);
          setDeploymentSignals(null);
        }}
        onActionFilterChange={(actionFilter) => {
          void handleSignalActionFilterChange(actionFilter);
        }}
        onRefresh={() => {
          if (signalsDialogDeployment) {
            void loadDeploymentSignals(signalsDialogDeployment, signalActionFilter);
          }
        }}
      />
      <DeploymentStateDialog
        deployment={stateDialogDeployment}
        onClose={() => setStateDialogDeployment(null)}
      />
      <AlertDialog
        open={Boolean(deleteDialogDeployment)}
        onOpenChange={(open) => (open ? undefined : setDeleteDialogDeployment(null))}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              删除部署“{deleteDialogDeployment?.name ?? ""}”？
            </AlertDialogTitle>
            <AlertDialogDescription>
              删除后会同时清理该部署的调度、运行实例和生成的信号记录。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => {
                if (deleteDialogDeployment) {
                  void handleDeleteDeployment(deleteDialogDeployment);
                }
                setDeleteDialogDeployment(null);
              }}
            >
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      <ScheduleDialog
        cron={scheduleCron}
        deployment={scheduleDialogDeployment}
        isSaving={
          scheduleDialogDeployment
            ? pendingDeploymentId === scheduleDialogDeployment.id
            : false
        }
        onChange={setScheduleCron}
        onClose={() => setScheduleDialogDeployment(null)}
        onSubmit={() => void handleSaveSchedule()}
      />
    </section>
  );
}

type CreateDeploymentDialogProps = {
  form: DeploymentForm;
  isOpen: boolean;
  isSaving: boolean;
  selectedStrategy: StrategySummary | null;
  strategies: StrategySummary[];
  onChange: (form: DeploymentForm) => void;
  onClose: () => void;
  onSubmit: () => void;
};

function CreateDeploymentDialog({
  form,
  isOpen,
  isSaving,
  selectedStrategy,
  strategies,
  onChange,
  onClose,
  onSubmit,
}: CreateDeploymentDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>新建策略部署</DialogTitle>
          <DialogDescription>选择部署模式后，调度运行会统一进入 Job Runtime。</DialogDescription>
        </DialogHeader>
        <div className="grid gap-3">
          <label className="grid gap-1 text-xs font-semibold text-graphite">
            策略版本
            <select
              className="h-9 rounded-md border border-input bg-background px-3 text-sm"
              value={form.strategyVersionId}
              onChange={(event) => {
                const strategy = strategies.find(
                  (item) => item.strategy_version_id === event.target.value,
                );
                onChange({
                  ...form,
                  strategyVersionId: event.target.value,
                  name: strategy ? `${strategy.name} 部署` : form.name,
                  paramValues: strategy ? paramDefaults(strategy) : {},
                });
              }}
            >
              <option value="">选择策略</option>
              {strategies.map((strategy) => (
                <option key={strategy.strategy_version_id} value={strategy.strategy_version_id}>
                  {strategy.name} · V{strategy.version}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1 text-xs font-semibold text-graphite">
            部署模式
            <select
              className="h-9 rounded-md border border-input bg-background px-3 text-sm"
              value={form.mode}
              onChange={(event) => onChange(withModeDefaults(form, event.target.value))}
            >
              <option value="signal">信号</option>
              <option value="paper">模拟盘</option>
              <option value="live">实盘</option>
            </select>
          </label>
          <label className="grid gap-1 text-xs font-semibold text-graphite">
            部署名称
            <Input
              value={form.name}
              onChange={(event) => onChange({ ...form, name: event.target.value })}
            />
          </label>
          <div className="grid gap-3 md:grid-cols-2">
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              标的
              <Input
                value={form.symbols}
                onChange={(event) => onChange({ ...form, symbols: event.target.value })}
              />
            </label>
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              Bars
              <Input
                type="number"
                min={1}
                value={form.lookbackBars}
                onChange={(event) => onChange({ ...form, lookbackBars: event.target.value })}
              />
            </label>
          </div>
          {form.mode !== "signal" ? (
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              Broker ID
              <Input
                value={form.brokerId}
                onChange={(event) => onChange({ ...form, brokerId: event.target.value })}
              />
            </label>
          ) : null}
          <label className="flex items-center justify-between gap-3 rounded-md border border-line px-3 py-2 text-xs font-semibold text-graphite">
            人工确认
            <Switch
              checked={form.requiresManualConfirm}
              onCheckedChange={(checked) =>
                onChange({ ...form, requiresManualConfirm: checked })
              }
            />
          </label>
          {selectedStrategy?.custom_params.length ? (
            <div className="grid gap-3 border-t border-line pt-3 md:grid-cols-2">
              {selectedStrategy.custom_params.map((param) => (
                <label
                  key={param.name_en}
                  className="grid gap-1 text-xs font-semibold text-graphite"
                >
                  {param.name_cn || param.name_en}
                  <Input
                    value={form.paramValues[param.name_en] ?? ""}
                    onChange={(event) =>
                      onChange({
                        ...form,
                        paramValues: {
                          ...form.paramValues,
                          [param.name_en]: event.target.value,
                        },
                      })
                    }
                  />
                </label>
              ))}
            </div>
          ) : null}
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={!form.strategyVersionId || isSaving} onClick={onSubmit}>
            <Plus className="h-4 w-4" />
            创建
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type EditDeploymentDialogProps = {
  deployment: StrategyDeployment | null;
  form: DeploymentForm;
  isSaving: boolean;
  strategyVersion: StrategyVersion | null;
  onChange: (form: DeploymentForm) => void;
  onClose: () => void;
  onSubmit: () => void;
};

function EditDeploymentDialog({
  deployment,
  form,
  isSaving,
  strategyVersion,
  onChange,
  onClose,
  onSubmit,
}: EditDeploymentDialogProps) {
  return (
    <Dialog open={Boolean(deployment)} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>编辑策略部署</DialogTitle>
          <DialogDescription>
            {deployment ? `${deployment.id} · V${strategyVersion?.version ?? "-"}` : ""}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-3">
          <label className="grid gap-1 text-xs font-semibold text-graphite">
            部署模式
            <select
              className="h-9 rounded-md border border-input bg-background px-3 text-sm"
              value={form.mode}
              onChange={(event) => onChange(withModeDefaults(form, event.target.value))}
            >
              <option value="signal">信号</option>
              <option value="paper">模拟盘</option>
              <option value="live">实盘</option>
            </select>
          </label>
          <label className="grid gap-1 text-xs font-semibold text-graphite">
            部署名称
            <Input
              value={form.name}
              onChange={(event) => onChange({ ...form, name: event.target.value })}
            />
          </label>
          <div className="grid gap-3 md:grid-cols-2">
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              标的
              <Input
                value={form.symbols}
                onChange={(event) => onChange({ ...form, symbols: event.target.value })}
              />
            </label>
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              Bars
              <Input
                type="number"
                min={1}
                value={form.lookbackBars}
                onChange={(event) => onChange({ ...form, lookbackBars: event.target.value })}
              />
            </label>
          </div>
          {form.mode !== "signal" ? (
            <label className="grid gap-1 text-xs font-semibold text-graphite">
              Broker ID
              <Input
                value={form.brokerId}
                onChange={(event) => onChange({ ...form, brokerId: event.target.value })}
              />
            </label>
          ) : null}
          <label className="flex items-center justify-between gap-3 rounded-md border border-line px-3 py-2 text-xs font-semibold text-graphite">
            人工确认
            <Switch
              checked={form.requiresManualConfirm}
              onCheckedChange={(checked) =>
                onChange({ ...form, requiresManualConfirm: checked })
              }
            />
          </label>
          {strategyVersion?.custom_params.length ? (
            <div className="grid gap-3 border-t border-line pt-3 md:grid-cols-2">
              {strategyVersion.custom_params.map((param) => (
                <label
                  key={param.name_en}
                  className="grid gap-1 text-xs font-semibold text-graphite"
                >
                  {param.name_cn || param.name_en}
                  <Input
                    value={form.paramValues[param.name_en] ?? ""}
                    onChange={(event) =>
                      onChange({
                        ...form,
                        paramValues: {
                          ...form.paramValues,
                          [param.name_en]: event.target.value,
                        },
                      })
                    }
                  />
                </label>
              ))}
            </div>
          ) : null}
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={!deployment || isSaving} onClick={onSubmit}>
            <Pencil className="h-4 w-4" />
            保存
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type DeploymentInstancesDialogProps = {
  deployment: StrategyDeployment | null;
  instances: JobRuntimeInstanceListResponse | null;
  isLoading: boolean;
  statusFilter: DeploymentInstanceStatusFilter;
  onClose: () => void;
  onRefresh: () => void;
  onStatusFilterChange: (statusFilter: DeploymentInstanceStatusFilter) => void;
};

function DeploymentInstancesDialog({
  deployment,
  instances,
  isLoading,
  statusFilter,
  onClose,
  onRefresh,
  onStatusFilterChange,
}: DeploymentInstancesDialogProps) {
  const statusCountMap = new Map(
    (instances?.status_counts ?? []).map((item) => [item.status, item.count]),
  );
  const allInstanceCount = Array.from(statusCountMap.values()).reduce(
    (total, count) => total + count,
    0,
  );
  const instanceRows = instances?.items ?? [];

  return (
    <Dialog open={Boolean(deployment)} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent className="max-w-6xl">
        <DialogHeader>
          <DialogTitle>运行实例</DialogTitle>
          <DialogDescription>
            {deployment
              ? `${deployment.name} · ${instances?.total ?? 0}/${allInstanceCount} 条`
              : ""}
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Tabs
            className="min-w-[280px] flex-1"
            value={statusFilter}
            onValueChange={(value) =>
              onStatusFilterChange(value as DeploymentInstanceStatusFilter)
            }
          >
            <TabsList className="flex h-auto flex-wrap justify-start gap-1.5 bg-transparent p-0">
              {instanceStatusFilterOptions.map((option) => {
                const count =
                  option.value === "all"
                    ? allInstanceCount
                    : statusCountMap.get(option.value) ?? 0;
                return (
                  <TabsTrigger
                    key={option.value}
                    className="h-8 gap-1 border border-line bg-panel px-2 text-[11px] data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
                    disabled={isLoading}
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
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={!deployment || isLoading}
              onClick={onRefresh}
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
              刷新
            </Button>
          </div>
        </div>
        <div className="max-h-[60vh] overflow-auto rounded-md border border-line">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="min-w-44">实例</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>触发</TableHead>
                <TableHead className="min-w-40">计划时间</TableHead>
                <TableHead className="min-w-40">开始时间</TableHead>
                <TableHead className="min-w-40">结束时间</TableHead>
                <TableHead>Payload</TableHead>
                <TableHead className="min-w-48">摘要</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={8} className="h-24 text-center text-sm text-mutedText">
                    实例加载中
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading && instanceRows.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={8} className="h-24 text-center text-sm text-mutedText">
                    暂无运行实例
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading
                ? instanceRows.map((instance) => (
                    <TableRow key={instance.id}>
                      <TableCell>
                        <div className="font-mono text-xs font-semibold text-ink">
                          {instance.id}
                        </div>
                        <div className="mt-1 max-w-48 truncate font-mono text-[11px] text-mutedText">
                          {instance.trigger_key}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={instanceStatusVariant(instance.status)}>
                          {instanceStatusLabel(instance.status)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-xs text-graphite">
                        {triggerTypeLabel(instance.trigger_type)}
                      </TableCell>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {formatDateTime(instance.scheduled_for)}
                      </TableCell>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {formatDateTime(instance.started_at)}
                      </TableCell>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {formatDateTime(instance.completed_at)}
                      </TableCell>
                      <TableCell>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button size="sm" variant="outline" type="button">
                              Payload
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent className="max-h-80 max-w-xl overflow-auto p-3">
                            <pre className="whitespace-pre-wrap break-words font-mono text-[11px] leading-relaxed">
                              {formatPayload(instance.payload)}
                            </pre>
                          </TooltipContent>
                        </Tooltip>
                      </TableCell>
                      <TableCell className="max-w-64">
                        <div className="truncate text-xs text-graphite">
                          {instance.summary || instance.result_status || "-"}
                        </div>
                        {instance.error_message ? (
                          <div className="mt-1 truncate text-xs text-destructive">
                            {instance.error_message}
                          </div>
                        ) : null}
                      </TableCell>
                    </TableRow>
                  ))
                : null}
            </TableBody>
          </Table>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type DeploymentSignalsDialogProps = {
  deployment: StrategyDeployment | null;
  signals: StrategySignalListResponse | null;
  isLoading: boolean;
  actionFilter: SignalActionFilter;
  onClose: () => void;
  onActionFilterChange: (actionFilter: SignalActionFilter) => void;
  onRefresh: () => void;
};

function DeploymentSignalsDialog({
  deployment,
  signals,
  isLoading,
  actionFilter,
  onClose,
  onActionFilterChange,
  onRefresh,
}: DeploymentSignalsDialogProps) {
  const actionCountMap = new Map(
    (signals?.action_counts ?? []).map((item) => [item.action, item.count]),
  );
  const allSignalCount = Array.from(actionCountMap.values()).reduce(
    (total, count) => total + count,
    0,
  );
  const signalRows = signals?.items ?? [];

  return (
    <Dialog open={Boolean(deployment)} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent className="max-w-5xl">
        <DialogHeader>
          <DialogTitle>策略信号</DialogTitle>
          <DialogDescription>
            {deployment
              ? `${deployment.name} · ${signals?.total ?? 0}/${allSignalCount} 条`
              : ""}
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Tabs
            className="min-w-[260px] flex-1"
            value={actionFilter}
            onValueChange={(value) => onActionFilterChange(value as SignalActionFilter)}
          >
            <TabsList className="flex h-auto flex-wrap justify-start gap-1.5 bg-transparent p-0">
              {signalActionFilterOptions.map((option) => {
                const count =
                  option.value === "all"
                    ? allSignalCount
                    : actionCountMap.get(option.value) ?? 0;
                return (
                  <TabsTrigger
                    key={option.value}
                    className="h-8 gap-1 border border-line bg-panel px-2 text-[11px] data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
                    disabled={isLoading}
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
            <span className="text-[11px] text-mutedText">{signals?.total ?? 0} 条</span>
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={!deployment || isLoading}
              onClick={onRefresh}
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
              刷新
            </Button>
          </div>
        </div>
        <div className="max-h-[60vh] overflow-auto rounded-md border border-line">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="min-w-40">信号时间</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>动作</TableHead>
                <TableHead className="min-w-32">标的</TableHead>
                <TableHead className="min-w-32">数量 / 价格</TableHead>
                <TableHead className="min-w-48">原因</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center text-sm text-mutedText">
                    信号加载中
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading && signalRows.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center text-sm text-mutedText">
                    暂无信号
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading
                ? signalRows.map((signal) => (
                    <TableRow key={signal.id}>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {formatDateTime(signal.signal_datetime)}
                      </TableCell>
                      <TableCell>
                        <Badge variant={signalStatusVariant(signal.status)}>
                          {signalStatusLabel(signal.status)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-xs font-semibold text-graphite">
                        {signalActionLabel(signal.action.action)}
                      </TableCell>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {signal.action.symbol ?? "-"}
                      </TableCell>
                      <TableCell className="font-mono text-xs text-mutedText">
                        {formatSignalSizePrice(signal)}
                      </TableCell>
                      <TableCell className="max-w-64 truncate text-xs text-graphite">
                        {signal.reason || signal.action.reason || "-"}
                      </TableCell>
                      <TableCell>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button size="sm" variant="outline" type="button">
                              Action
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent className="max-h-80 max-w-xl overflow-auto p-3">
                            <pre className="whitespace-pre-wrap break-words font-mono text-[11px] leading-relaxed">
                              {formatPayload(signal.action)}
                            </pre>
                          </TooltipContent>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
                : null}
            </TableBody>
          </Table>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type DeploymentStateDialogProps = {
  deployment: StrategyDeployment | null;
  onClose: () => void;
};

function DeploymentStateDialog({ deployment, onClose }: DeploymentStateDialogProps) {
  return (
    <Dialog open={Boolean(deployment)} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>部署 State</DialogTitle>
          <DialogDescription>{deployment ? deployment.name : ""}</DialogDescription>
        </DialogHeader>
        <div className="max-h-[60vh] overflow-auto rounded-md border border-line bg-muted/20 p-3">
          <pre className="whitespace-pre-wrap break-words font-mono text-xs leading-relaxed text-graphite">
            {formatPayload(deployment?.state ?? {})}
          </pre>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type ScheduleDialogProps = {
  cron: string;
  deployment: StrategyDeployment | null;
  isSaving: boolean;
  onChange: (cron: string) => void;
  onClose: () => void;
  onSubmit: () => void;
};

function ScheduleDialog({
  cron,
  deployment,
  isSaving,
  onChange,
  onClose,
  onSubmit,
}: ScheduleDialogProps) {
  return (
    <Dialog open={Boolean(deployment)} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>配置调度</DialogTitle>
          <DialogDescription>{deployment?.name ?? ""}</DialogDescription>
        </DialogHeader>
        <label className="grid gap-1 text-xs font-semibold text-graphite">
          Cron
          <Input value={cron} onChange={(event) => onChange(event.target.value)} />
        </label>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={!cron.trim() || isSaving} onClick={onSubmit}>
            <CalendarClock className="h-4 w-4" />
            保存
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function parseSymbols(value: string): string[] {
  return value
    .split(/[,，\s]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseLookbackBars(value: string): number {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 250;
}

type StrategyParameterSource = {
  custom_params: StrategySummary["custom_params"];
};

function paramDefaults(strategy: StrategyParameterSource): Record<string, string> {
  return Object.fromEntries(
    strategy.custom_params.map((param) => [param.name_en, String(param.default)]),
  );
}

function parseParamValues(
  strategy: StrategyParameterSource,
  values: Record<string, string>,
): Record<string, StrategyJsonValue> {
  return Object.fromEntries(
    strategy.custom_params.map((param) => {
      const rawValue = values[param.name_en] ?? String(param.default);
      if (param.type === "integer") {
        return [param.name_en, Number.parseInt(rawValue, 10)];
      }
      if (param.type === "number") {
        return [param.name_en, Number.parseFloat(rawValue)];
      }
      if (param.type === "boolean") {
        return [param.name_en, ["true", "1", "yes", "on"].includes(rawValue.toLowerCase())];
      }
      return [param.name_en, rawValue];
    }),
  );
}

function formFromDeployment(
  deployment: StrategyDeployment,
  version: StrategyParameterSource,
): DeploymentForm {
  return {
    strategyVersionId: deployment.strategy_version_id,
    mode: deployment.mode,
    name: deployment.name,
    symbols: deployment.symbols.join(", "),
    lookbackBars: String(deployment.lookback_bars),
    brokerId: deployment.broker_id ?? "",
    requiresManualConfirm: deployment.requires_manual_confirm,
    paramValues: Object.fromEntries(
      version.custom_params.map((param) => [
        param.name_en,
        String(deployment.params[param.name_en] ?? param.default),
      ]),
    ),
  };
}

function withModeDefaults(form: DeploymentForm, modeValue: string): DeploymentForm {
  const mode = modeValue as StrategyDeploymentMode;
  return {
    ...form,
    mode,
    requiresManualConfirm: mode === "live" ? true : form.requiresManualConfirm,
  };
}

type DeploymentInstance = JobRuntimeInstanceListResponse["items"][number];

function instanceStatusVariant(
  status: DeploymentInstance["status"],
): "default" | "secondary" | "destructive" | "outline" {
  if (status === "completed") {
    return "default";
  }
  if (status === "failed" || status === "cancelled") {
    return "destructive";
  }
  return "outline";
}

function instanceStatusLabel(status: DeploymentInstance["status"]): string {
  if (status === "waiting") {
    return "等待";
  }
  if (status === "dispatching") {
    return "派发中";
  }
  if (status === "running") {
    return "运行中";
  }
  if (status === "completed") {
    return "完成";
  }
  if (status === "failed") {
    return "失败";
  }
  return "取消";
}

function triggerTypeLabel(triggerType: DeploymentInstance["trigger_type"]): string {
  if (triggerType === "schedule") {
    return "调度";
  }
  if (triggerType === "manual") {
    return "手动";
  }
  if (triggerType === "rerun") {
    return "重跑";
  }
  return "系统";
}

function signalStatusVariant(
  status: StrategySignal["status"],
): "default" | "secondary" | "destructive" | "outline" {
  if (status === "generated") {
    return "default";
  }
  if (status === "rejected" || status === "ignored") {
    return "destructive";
  }
  return "outline";
}

function signalStatusLabel(status: StrategySignal["status"]): string {
  if (status === "generated") {
    return "已生成";
  }
  if (status === "rejected") {
    return "已拒绝";
  }
  if (status === "converted") {
    return "已转换";
  }
  return "已忽略";
}

function signalActionLabel(action: StrategySignal["action"]["action"]): string {
  if (action === "buy") {
    return "买入";
  }
  if (action === "sell") {
    return "卖出";
  }
  if (action === "close") {
    return "平仓";
  }
  if (action === "cancel") {
    return "撤单";
  }
  return action || "未知";
}

function formatSignalSizePrice(signal: StrategySignal): string {
  const parts = [];
  if (signal.action.size !== undefined && signal.action.size !== null) {
    parts.push(String(signal.action.size));
  }
  if (signal.action.price !== undefined && signal.action.price !== null) {
    parts.push(`@ ${signal.action.price}`);
  }
  if (signal.action.ref !== undefined && signal.action.ref !== null) {
    parts.push(`ref ${signal.action.ref}`);
  }
  return parts.length ? parts.join(" ") : "-";
}

function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
}

function formatPayload(value: unknown): string {
  try {
    return JSON.stringify(value ?? {}, null, 2);
  } catch {
    return String(value ?? "");
  }
}

function modeLabel(mode: StrategyDeploymentMode): string {
  if (mode === "signal") {
    return "信号";
  }
  if (mode === "paper") {
    return "模拟盘";
  }
  return "实盘";
}
