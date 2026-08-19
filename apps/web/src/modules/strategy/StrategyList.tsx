import {
  AlertCircle,
  Check,
  Code2,
  FileCode2,
  GitCompare,
  History,
  Pencil,
  Play,
  Plus,
  RefreshCw,
  Search,
  Settings2,
  Tag,
  Trash2,
  UploadCloud,
  X,
} from "lucide-react";
import * as echarts from "echarts";
import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import type { EChartsOption } from "echarts";

import {
  backtestStrategy,
  createStrategy,
  createStrategyVersion,
  deleteStrategy,
  getStrategyBacktest,
  getStrategy,
  listStrategyBacktests,
  listStrategyVersions,
  listStrategies,
  switchStrategyCurrentVersion,
  updateStrategyMetadata,
  type Project,
  type StrategyBacktestConfig,
  type StrategyBacktestDetail,
  type StrategyBacktestRecord,
  type StrategyBenchmarkSeries,
  type StrategyCreatePayload,
  type StrategyCurvePoint,
  type StrategyCustomParameter,
  type StrategyDailyPortfolioSnapshot,
  type StrategyMarketCandle,
  type StrategyMode,
  type StrategyRecord,
  type StrategySummary,
  type StrategyTradeRecord,
  type StrategyVersion,
  type StrategyVersionCreatePayload,
} from "../../shared/api";

type StrategyListProps = {
  project: Project | null;
};

type StrategyForm = {
  name: string;
  description: string;
  tags: string;
  strategyMode: StrategyMode;
  code: string;
  riskNote: string;
};

type BacktestForm = {
  strategyMode: StrategyBacktestConfig["strategy_mode"];
  assetClass: StrategyBacktestConfig["asset_class"];
  market: StrategyBacktestConfig["market"];
  symbols: string;
  universe: string;
  benchmarkPreset: string;
  benchmarkSymbol: string;
  startDate: string;
  endDate: string;
  initialCash: string;
  commission: string;
  slippage: string;
  notes: string;
  customParamValues: Record<string, string>;
};

type SelectOption = string | { value: string; label: string };

type DialogState =
  | { kind: "create" }
  | {
      kind: "edit";
      strategy: StrategySummary;
      currentVersion: StrategyVersion | null;
      record: StrategyRecord;
    }
  | { kind: "version"; strategy: StrategySummary }
  | null;

type VersionPanelState = {
  strategy: StrategySummary;
  versions: StrategyVersion[];
  selectedVersionId: string | null;
  backtests: BacktestRecordView[];
  isLoading: boolean;
  isBacktesting: boolean;
  error: string | null;
} | null;

type RecordsPanelState = {
  strategy: StrategySummary;
  records: BacktestRecordView[];
  isLoading: boolean;
  error: string | null;
} | null;

type BacktestDialogState = {
  strategy: StrategySummary;
  version: StrategyVersion | null;
} | null;

type BacktestRecordView = {
  backtest: StrategyBacktestRecord;
  version: StrategyVersion;
};

type StatusFilter = "all" | StrategySummary["status"];
type ResultTab = "profile" | "trades" | "positions" | "signals";

const statusFilters: { label: string; value: StatusFilter }[] = [
  { label: "全部", value: "all" },
  { label: "启用", value: "active" },
];

const resultTabs: { label: string; value: ResultTab }[] = [
  { label: "收益概述", value: "profile" },
  { label: "交易详情", value: "trades" },
  { label: "每日持仓&收益", value: "positions" },
  { label: "买卖点分析", value: "signals" },
];

const strategyModeOptions: SelectOption[] = [
  { value: "single_symbol", label: "单股票" },
  { value: "multi_symbol", label: "多股票" },
  { value: "portfolio", label: "固定组合" },
  { value: "universe_selection", label: "股票池选股" },
];

const marketOptions: SelectOption[] = [
  { value: "CN", label: "A股" },
  { value: "HK", label: "港股" },
  { value: "US", label: "美股" },
];

const customBenchmarkValue = "__custom__";

const benchmarkOptionsByMarket: Record<StrategyBacktestConfig["market"], SelectOption[]> = {
  CN: [
    { value: "000016.SH", label: "上证50 (000016.SH)" },
    { value: "000300.SH", label: "沪深300 (000300.SH)" },
    { value: "000905.SH", label: "中证500 (000905.SH)" },
    { value: "000852.SH", label: "中证1000 (000852.SH)" },
    { value: "000001.SH", label: "上证指数 (000001.SH)" },
    { value: "399001.SZ", label: "深证成指 (399001.SZ)" },
    { value: "399006.SZ", label: "创业板指 (399006.SZ)" },
    { value: customBenchmarkValue, label: "其他" },
  ],
  HK: [
    { value: "HSI.HK", label: "恒生指数 (HSI.HK)" },
    { value: "HSCEI.HK", label: "恒生中国企业指数 (HSCEI.HK)" },
    { value: "HSTECH.HK", label: "恒生科技指数 (HSTECH.HK)" },
    { value: customBenchmarkValue, label: "其他" },
  ],
  US: [
    { value: "SPX.US", label: "标普500 (SPX.US)" },
    { value: "IXIC.US", label: "纳斯达克综合 (IXIC.US)" },
    { value: "DJI.US", label: "道琼斯工业指数 (DJI.US)" },
    { value: customBenchmarkValue, label: "其他" },
  ],
};

const cnAssetClassOptions: SelectOption[] = [
  { value: "stock", label: "股票" },
  { value: "etf", label: "ETF" },
  { value: "index", label: "指数" },
];

const stockOnlyAssetClassOptions: SelectOption[] = [{ value: "stock", label: "股票" }];

const backtestDateRangePresets = [
  { years: 1, label: "最近1年" },
  { years: 2, label: "最近2年" },
  { years: 3, label: "最近3年" },
  { years: 5, label: "最近5年" },
];

const defaultCode = [
  "import backtrader as bt",
  "",
  "class GeneratedStrategy(bt.Strategy):",
  "    @classmethod",
  "    def chatq_params(cls):",
  "        return [",
  '            {"name": "fast_period", "type": "integer", "default": 20, "label": "短期均线周期"},',
  '            {"name": "slow_period", "type": "integer", "default": 60, "label": "长期均线周期"},',
  "        ]",
  "",
  "    def __init__(self):",
  "        close = self.datas[0].close",
  "        self.fast_ma = bt.ind.SMA(close, period=self.p.fast_period)",
  "        self.slow_ma = bt.ind.SMA(close, period=self.p.slow_period)",
  "",
  "    def next(self):",
  "        if not self.position and self.fast_ma[0] > self.slow_ma[0]:",
  "            self.order_target_percent(target=0.95)",
  "        elif self.position and self.fast_ma[0] < self.slow_ma[0]:",
  "            self.order_target_percent(target=0)",
].join("\n");

export function StrategyList({ project }: StrategyListProps) {
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [dialog, setDialog] = useState<DialogState>(null);
  const [versionPanel, setVersionPanel] = useState<VersionPanelState>(null);
  const [recordsPanel, setRecordsPanel] = useState<RecordsPanelState>(null);
  const [backtestDialog, setBacktestDialog] = useState<BacktestDialogState>(null);
  const [resultDetail, setResultDetail] = useState<StrategyBacktestDetail | null>(null);
  const [form, setForm] = useState<StrategyForm>(() => newStrategyForm());
  const [backtestForm, setBacktestForm] = useState<BacktestForm>(() => newBacktestForm([]));
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [pendingStrategyId, setPendingStrategyId] = useState<string | null>(null);
  const [runningBacktestKey, setRunningBacktestKey] = useState<string | null>(null);
  const [switchingVersionId, setSwitchingVersionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const filteredStrategies = useMemo(() => {
    const text = query.trim().toLowerCase();
    return strategies.filter((strategy) => {
      const matchesStatus = statusFilter === "all" || strategy.status === statusFilter;
      const matchesText =
        !text ||
        strategy.name.toLowerCase().includes(text) ||
        strategy.tags.some((tag) => tag.toLowerCase().includes(text));
      return matchesStatus && matchesText;
    });
  }, [query, statusFilter, strategies]);

  const loadStrategies = useCallback(async (): Promise<StrategySummary[]> => {
    if (!project) {
      setStrategies([]);
      setError(null);
      return [];
    }

    setIsLoading(true);
    setError(null);
    try {
      const nextStrategies = await listStrategies(project.id);
      setStrategies(nextStrategies);
      return nextStrategies;
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "策略列表加载失败");
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [project]);

  useEffect(() => {
    void loadStrategies();
  }, [loadStrategies]);

  const openCreateDialog = () => {
    setForm(newStrategyForm());
    setDialog({ kind: "create" });
    setError(null);
    setNotice(null);
  };

  const openEditDialog = async (strategy: StrategySummary) => {
    setError(null);
    setNotice(null);
    setPendingStrategyId(strategy.strategy_id);
    try {
      const latestStrategies = await loadStrategies();
      const latestStrategy =
        latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
        strategy;
      const [detail, versions] = await Promise.all([
        getStrategy(latestStrategy.strategy_id),
        listStrategyVersions(latestStrategy.strategy_id),
      ]);
      const currentVersion =
        versions.find((version) => version.id === latestStrategy.strategy_version_id) ??
        versions.at(-1) ??
        null;
      setForm({
        ...versionToForm(currentVersion, latestStrategy.name),
        name: latestStrategy.name,
        description: detail.strategy.description ?? "",
        tags: detail.strategy.tags.join(", "),
      });
      setDialog({ kind: "edit", strategy: latestStrategy, currentVersion, record: detail.strategy });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "策略详情加载失败");
    } finally {
      setPendingStrategyId(null);
    }
  };

  const openVersionDialog = async (strategy: StrategySummary) => {
    setError(null);
    setNotice(null);
    const latestStrategies = await loadStrategies();
    const latestStrategy =
      latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
      strategy;
    setForm({
      ...newStrategyForm(latestStrategy.name),
      strategyMode: latestStrategy.strategy_mode,
    });
    setDialog({ kind: "version", strategy: latestStrategy });
  };

  const openVersionPanel = async (
    strategy: StrategySummary,
    preferredVersionId?: string | null,
  ) => {
    setVersionPanel({
      strategy,
      versions: [],
      selectedVersionId: null,
      backtests: [],
      isLoading: true,
      isBacktesting: false,
      error: null,
    });
    setError(null);
    setNotice(null);
    try {
      const latestStrategies = await loadStrategies();
      const latestStrategy =
        latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
        strategy;
      const versions = await listStrategyVersions(latestStrategy.strategy_id);
      const selectedVersionId =
        versions.find((version) => version.id === preferredVersionId)?.id ??
        versions.find((version) => version.id === latestStrategy.strategy_version_id)?.id ??
        versions.at(-1)?.id ??
        null;
      const selectedVersion = versions.find((version) => version.id === selectedVersionId) ?? null;
      const backtests = selectedVersion
        ? await loadVersionBacktests(selectedVersion)
        : [];
      setVersionPanel({
        strategy: latestStrategy,
        versions,
        selectedVersionId,
        backtests,
        isLoading: false,
        isBacktesting: false,
        error: null,
      });
    } catch (caught) {
      setVersionPanel((current) =>
        current
          ? {
              ...current,
              isLoading: false,
              error: caught instanceof Error ? caught.message : "版本列表加载失败",
            }
          : current,
      );
    }
  };

  const openRecordsPanel = async (strategy: StrategySummary) => {
    setRecordsPanel({
      strategy,
      records: [],
      isLoading: true,
      error: null,
    });
    setError(null);
    setNotice(null);
    try {
      const latestStrategies = await loadStrategies();
      const latestStrategy =
        latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
        strategy;
      const versions = await listStrategyVersions(latestStrategy.strategy_id);
      const records = await loadStrategyBacktestRecords(versions);
      setRecordsPanel({
        strategy: latestStrategy,
        records,
        isLoading: false,
        error: null,
      });
    } catch (caught) {
      setRecordsPanel((current) =>
        current
          ? {
              ...current,
              isLoading: false,
              error: caught instanceof Error ? caught.message : "回测记录加载失败",
            }
          : current,
      );
    }
  };

  const handleCreate = async () => {
    if (!project) {
      setError("请先创建或选择项目");
      return;
    }
    const payload = buildCreatePayload(form);
    if (!payload.ok) {
      setError(payload.message);
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      await createStrategy(payload.value, project.id);
      setDialog(null);
      setNotice("策略已创建");
      await loadStrategies();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "创建策略失败");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = async () => {
    if (!project || dialog?.kind !== "edit") {
      return;
    }
    const name = form.name.trim();
    if (!name) {
      setError("策略名称不能为空");
      return;
    }
    const versionPayload = buildVersionPayload(form);
    if (!versionPayload.ok) {
      setError(versionPayload.message);
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      const metadataChanged =
        name !== dialog.strategy.name ||
        form.description.trim() !== (dialog.record.description ?? "") ||
        parseTags(form.tags).join("\n") !== dialog.strategy.tags.join("\n");
      const shouldCreateVersion = hasVersionChanges(dialog.currentVersion, versionPayload.value);

      await updateStrategyMetadata(
        dialog.strategy.strategy_id,
        {
          name,
          description: form.description.trim() || null,
          tags: parseTags(form.tags),
        },
      );
      if (shouldCreateVersion) {
        const version = await createStrategyVersion(
          dialog.strategy.strategy_id,
          versionPayload.value,
        );
        setNotice(metadataChanged ? `策略已保存，并发布 V${version.version}` : `已发布 V${version.version}`);
      } else {
        setNotice("策略已保存");
      }
      setDialog(null);
      await loadStrategies();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "保存策略失败");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCreateVersion = async () => {
    if (!project || dialog?.kind !== "version") {
      return;
    }
    const payload = buildVersionPayload(form);
    if (!payload.ok) {
      setError(payload.message);
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      const version = await createStrategyVersion(dialog.strategy.strategy_id, payload.value);
      setDialog(null);
      setNotice(`已发布 V${version.version}`);
      await loadStrategies();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "发布新版本失败");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (strategy: StrategySummary) => {
    if (!project || !window.confirm(`删除策略“${strategy.name}”？`)) {
      return;
    }

    setPendingStrategyId(strategy.strategy_id);
    setError(null);
    setNotice(null);
    try {
      await deleteStrategy(strategy.strategy_id);
      setNotice("策略已删除");
      await loadStrategies();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "删除策略失败");
    } finally {
      setPendingStrategyId(null);
    }
  };

  const openBacktestDialog = async (strategy: StrategySummary, version?: StrategyVersion) => {
    setError(null);
    setNotice(null);
    try {
      const latestStrategies = await loadStrategies();
      const latestStrategy =
        latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
        strategy;
      const versions = version ? await listStrategyVersions(latestStrategy.strategy_id) : [];
      const latestVersion = version
        ? versions.find((item) => item.id === version.id) ?? version
        : null;
      const params = latestVersion?.custom_params ?? latestStrategy.custom_params;
      const strategyMode = latestVersion?.strategy_mode ?? latestStrategy.strategy_mode;
      setBacktestForm(newBacktestForm(params, strategyMode));
      setBacktestDialog({ strategy: latestStrategy, version: latestVersion });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "回测配置加载失败");
    }
  };

  const handleSubmitBacktest = async () => {
    if (!project) {
      return;
    }
    if (!backtestDialog) {
      return;
    }

    setError(null);
    setNotice(null);
    try {
      const { strategy, version } = backtestDialog;
      const latestStrategies = await loadStrategies();
      const latestStrategy =
        latestStrategies.find((item) => item.strategy_id === strategy.strategy_id) ??
        strategy;
      const versions = version ? await listStrategyVersions(latestStrategy.strategy_id) : [];
      const latestVersion = version
        ? versions.find((item) => item.id === version.id) ?? version
        : null;
      const config = buildBacktestConfig(
        backtestForm,
        latestVersion?.custom_params ?? latestStrategy.custom_params,
      );
      if (!config.ok) {
        setError(config.message);
        return;
      }

      const backtestKey = latestVersion
        ? `version:${latestVersion.id}`
        : `strategy:${latestStrategy.strategy_id}`;
      setPendingStrategyId(latestStrategy.strategy_id);
      setRunningBacktestKey(backtestKey);
      if (versionPanel) {
        setVersionPanel({ ...versionPanel, isBacktesting: true, error: null });
      }
      const detail = await backtestStrategy(
        latestStrategy.strategy_id,
        {
          project_id: project.id,
          config: config.value,
          strategy_version_id: latestVersion?.id,
        },
      );
      const freshDetail = await getStrategyBacktest(detail.backtest.id);
      setBacktestDialog(null);
      setResultDetail(freshDetail);
      await loadStrategies();
      if (latestVersion && versionPanel) {
        await openVersionPanel(versionPanel.strategy, latestVersion.id);
      }
      if (recordsPanel) {
        await openRecordsPanel(recordsPanel.strategy);
      }
      setNotice(`回测已完成：${freshDetail.backtest.status}`);
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "回测失败";
      if (versionPanel) {
        setVersionPanel({ ...versionPanel, isBacktesting: false, error: message });
      } else {
        setError(message);
      }
    } finally {
      setRunningBacktestKey(null);
      setPendingStrategyId(null);
    }
  };

  const handleSelectVersion = async (versionId: string) => {
    if (!project || !versionPanel) {
      return;
    }
    setVersionPanel({
      ...versionPanel,
      selectedVersionId: versionId,
      backtests: [],
      isLoading: true,
      error: null,
    });
    try {
      const versions = await listStrategyVersions(versionPanel.strategy.strategy_id);
      const version = versions.find((item) => item.id === versionId);
      const backtests = version ? await loadVersionBacktests(version) : [];
      setVersionPanel({
        ...versionPanel,
        versions,
        selectedVersionId: versionId,
        backtests,
        isLoading: false,
        error: null,
      });
    } catch (caught) {
      setVersionPanel({
        ...versionPanel,
        selectedVersionId: versionId,
        isLoading: false,
        error: caught instanceof Error ? caught.message : "回测记录加载失败",
      });
    }
  };

  const handleSwitchVersion = async (version: StrategyVersion) => {
    if (!project || !versionPanel || version.id === versionPanel.strategy.strategy_version_id) {
      return;
    }

    setSwitchingVersionId(version.id);
    setVersionPanel({ ...versionPanel, error: null });
    setError(null);
    setNotice(null);
    try {
      const summary = await switchStrategyCurrentVersion(versionPanel.strategy.strategy_id, version.id);
      const nextStrategies = await loadStrategies();
      const nextSummary =
        nextStrategies.find((strategy) => strategy.strategy_id === summary.strategy_id) ??
        summary;
      await openVersionPanel(nextSummary, version.id);
      setNotice(`已切换到 V${summary.version}`);
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "版本切换失败";
      setVersionPanel((current) =>
        current ? { ...current, error: message } : current,
      );
    } finally {
      setSwitchingVersionId(null);
    }
  };

  const handleViewResult = async (backtestId: string) => {
    if (!project) {
      return;
    }
    setError(null);
    try {
      setResultDetail(await getStrategyBacktest(backtestId));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "回测结果加载失败");
    }
  };

  return (
    <section className="mx-auto flex w-full max-w-6xl flex-col gap-5" aria-label="策略列表">
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-line bg-panel/85 p-4 shadow-sm">
        <div className="min-w-0">
          <div className="font-mono text-[10px] font-bold uppercase text-signal">Strategies</div>
          <h1 className="mt-1 truncate text-xl font-black text-ink">策略档案</h1>
          <p className="mt-1 truncate text-xs text-muted">
            当前项目：{project?.name ?? "未选择项目"}
          </p>
        </div>
        <IconButton
          label="刷新"
          icon={<RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />}
          disabled={!project || isLoading}
          onClick={() => void loadStrategies()}
        />
      </div>

      {!project ? <Notice text="请先创建或选择项目" /> : null}
      {project && error ? <Feedback tone="error" text={error} /> : null}
      {project && notice ? <Feedback tone="success" text={notice} /> : null}

      <div className="flex flex-wrap items-center gap-3">
        <div className="relative min-w-64 flex-1">
          <Search className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted" />
          <input
            className="h-9 w-full rounded-md border border-line bg-panel pl-8 pr-3 text-xs text-ink outline-none placeholder:text-muted/70 focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
            disabled={!project}
            placeholder="搜索策略或标签"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>
        <StatusFilterControl value={statusFilter} onChange={setStatusFilter} />
      </div>

      {project && isLoading ? <Notice text="策略加载中" /> : null}
      {project && !isLoading && strategies.length > 0 && filteredStrategies.length === 0 ? (
        <Notice text="没有匹配的策略" />
      ) : null}

      {project && !isLoading ? (
        <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
          <NewStrategyCard onClick={openCreateDialog} />
          {filteredStrategies.map((strategy) => (
            <StrategyCard
              key={strategy.strategy_id}
              strategy={strategy}
              isPending={pendingStrategyId === strategy.strategy_id}
              isBacktesting={runningBacktestKey === `strategy:${strategy.strategy_id}`}
              onEdit={() => void openEditDialog(strategy)}
              onVersions={() => void openVersionPanel(strategy)}
              onRecords={() => void openRecordsPanel(strategy)}
              onBacktest={() => void openBacktestDialog(strategy)}
              onDelete={() => void handleDelete(strategy)}
            />
          ))}
        </div>
      ) : null}

      {versionPanel ? (
        <VersionPanel
          panel={versionPanel}
          currentVersionId={versionPanel.strategy.strategy_version_id}
          runningBacktestKey={runningBacktestKey}
          switchingVersionId={switchingVersionId}
          onClose={() => setVersionPanel(null)}
          onSelectVersion={(versionId) => void handleSelectVersion(versionId)}
          onSwitchVersion={(version) => void handleSwitchVersion(version)}
          onCreateVersion={() => {
            void openVersionDialog(versionPanel.strategy);
            setVersionPanel(null);
          }}
          onBacktest={(version) => void openBacktestDialog(versionPanel.strategy, version)}
          onViewResult={(backtestId) => void handleViewResult(backtestId)}
        />
      ) : null}

      {recordsPanel ? (
        <BacktestRecordsPanel
          panel={recordsPanel}
          onClose={() => setRecordsPanel(null)}
          onViewResult={(backtestId) => void handleViewResult(backtestId)}
        />
      ) : null}

      {backtestDialog ? (
        <BacktestRunDialog
          dialog={backtestDialog}
          error={error}
          form={backtestForm}
          disabled={runningBacktestKey !== null}
          onChange={setBacktestForm}
          onClose={() => setBacktestDialog(null)}
          onSubmit={() => void handleSubmitBacktest()}
        />
      ) : null}

      {resultDetail ? (
        <BacktestResultDialog detail={resultDetail} onClose={() => setResultDetail(null)} />
      ) : null}

      {dialog ? (
        <Dialog
          title={dialogTitle(dialog)}
          submitLabel={isSubmitting ? "处理中" : dialogSubmitLabel(dialog)}
          submitIcon={dialog.kind === "edit" ? <Check className="h-4 w-4" /> : <UploadCloud className="h-4 w-4" />}
          isSubmitting={isSubmitting}
          onClose={() => setDialog(null)}
          onSubmit={() => {
            if (dialog.kind === "create") {
              void handleCreate();
            } else if (dialog.kind === "edit") {
              void handleEdit();
            } else {
              void handleCreateVersion();
            }
          }}
        >
          <StrategyFormFields
            mode={dialog.kind}
            form={form}
            disabled={isSubmitting}
            onChange={setForm}
          />
        </Dialog>
      ) : null}
    </section>
  );
}

function NewStrategyCard({ onClick }: { onClick: () => void }) {
  return (
    <button
      className="flex min-h-[230px] flex-col items-center justify-center rounded-lg border border-dashed border-strong bg-soft p-4 text-center text-muted transition-all hover:-translate-y-0.5 hover:border-signal hover:bg-panel hover:text-ink hover:shadow-lift focus:outline-none focus:ring-2 focus:ring-signal/20"
      type="button"
      onClick={onClick}
    >
      <span className="grid h-10 w-10 place-items-center rounded-md border border-line bg-panel text-signal">
        <Plus className="h-5 w-5" />
      </span>
      <span className="mt-3 text-sm font-semibold">新建策略</span>
      <span className="mt-1 text-xs text-muted">创建一个可回测的策略卡片</span>
    </button>
  );
}

function StrategyCard({
  strategy,
  isPending,
  isBacktesting,
  onEdit,
  onVersions,
  onRecords,
  onBacktest,
  onDelete,
}: {
  strategy: StrategySummary;
  isPending: boolean;
  isBacktesting: boolean;
  onEdit: () => void;
  onVersions: () => void;
  onRecords: () => void;
  onBacktest: () => void;
  onDelete: () => void;
}) {
  return (
    <article className="flex min-h-[230px] flex-col rounded-lg border border-line bg-panel p-4 shadow-sm transition-all hover:-translate-y-0.5 hover:border-strong hover:shadow-lift">
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <span className="grid h-8 w-8 shrink-0 place-items-center rounded-md border border-line bg-soft text-brandBlue">
            <FileCode2 className="h-4 w-4" />
          </span>
          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-ink">{strategy.name}</h2>
            <div className="mt-0.5 text-[11px] text-muted">
              V{strategy.version} · {strategyModeLabel(strategy.strategy_mode)}
            </div>
          </div>
        </div>
        <StatusBadge status={strategy.status} />
      </div>

      <div className="mt-4 flex min-h-6 flex-wrap items-center gap-1.5">
        {strategy.tags.length > 0 ? (
          strategy.tags.slice(0, 4).map((tag) => (
            <span
              className="inline-flex max-w-28 items-center gap-1 rounded bg-compareSoft px-1.5 py-0.5 text-[10px] text-brandBlue"
              key={tag}
            >
              <Tag className="h-2.5 w-2.5 shrink-0" />
              <span className="truncate">{tag}</span>
            </span>
          ))
        ) : (
          <span className="font-mono text-[11px] text-muted">无标签</span>
        )}
      </div>

      <div className="mt-4 grid gap-2">
        {strategy.custom_params
          .slice(0, 3)
          .map((param) => (
            <div className="grid grid-cols-[minmax(0,1fr)_auto] gap-3 text-[11px]" key={param.name_en}>
              <span className="truncate font-mono text-muted">{param.name_en}</span>
              <span className="max-w-28 truncate font-mono font-semibold text-ink">
                {String(param.default)}
              </span>
            </div>
          ))}
      </div>

      <div className="mt-auto pt-4">
        <div className="mb-3 font-mono text-[10px] text-muted">
          {formatDate(strategy.updated_at)}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <SmallButton icon={<Pencil className="h-3.5 w-3.5" />} label="编辑" disabled={isPending} onClick={onEdit} />
          <SmallButton icon={<Code2 className="h-3.5 w-3.5" />} label="版本" disabled={isPending} onClick={onVersions} />
          <SmallButton
            icon={
              isBacktesting ? (
                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Play className="h-3.5 w-3.5" />
              )
            }
            label={isBacktesting ? "回测中" : "回测"}
            disabled={isPending || strategy.status !== "active"}
            onClick={onBacktest}
          />
          <SmallButton icon={<History className="h-3.5 w-3.5" />} label="记录" disabled={isPending} onClick={onRecords} />
          <IconButton icon={<Trash2 className="h-3.5 w-3.5" />} label="删除" danger disabled={isPending} onClick={onDelete} />
        </div>
      </div>
    </article>
  );
}

function VersionPanel({
  panel,
  currentVersionId,
  runningBacktestKey,
  switchingVersionId,
  onClose,
  onSelectVersion,
  onSwitchVersion,
  onCreateVersion,
  onBacktest,
  onViewResult,
}: {
  panel: Exclude<VersionPanelState, null>;
  currentVersionId: string;
  runningBacktestKey: string | null;
  switchingVersionId: string | null;
  onClose: () => void;
  onSelectVersion: (versionId: string) => void;
  onSwitchVersion: (version: StrategyVersion) => void;
  onCreateVersion: () => void;
  onBacktest: (version: StrategyVersion) => void;
  onViewResult: (backtestId: string) => void;
}) {
  const selectedVersion =
    panel.versions.find((version) => version.id === panel.selectedVersionId) ??
    panel.versions.at(-1) ??
    null;
  const selectedIndex = selectedVersion
    ? panel.versions.findIndex((version) => version.id === selectedVersion.id)
    : -1;
  const previousVersion = selectedIndex > 0 ? panel.versions[selectedIndex - 1] : null;
  const diffItems = selectedVersion ? summarizeVersionDiff(previousVersion, selectedVersion) : [];

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-ink/35 p-4">
      <section className="flex max-h-[88vh] w-full max-w-5xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-zinc-900">
              {panel.strategy.name} 版本
            </h2>
            <p className="mt-0.5 font-mono text-[11px] text-zinc-500">
              当前版本 V{panel.strategy.version}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <SmallButton
              icon={<Code2 className="h-3.5 w-3.5" />}
              label="新增版本"
              disabled={panel.strategy.status !== "active"}
              onClick={onCreateVersion}
            />
            <IconButton label="关闭" icon={<X className="h-4 w-4" />} onClick={onClose} />
          </div>
        </div>

        <div className="grid min-h-0 flex-1 grid-cols-[260px_minmax(0,1fr)] max-md:grid-cols-1">
          <aside className="min-h-0 overflow-y-auto border-r border-line bg-soft p-3 max-md:border-b max-md:border-r-0">
            {panel.isLoading && panel.versions.length === 0 ? <Notice text="版本加载中" /> : null}
            <div className="grid gap-2">
              {panel.versions.map((version) => {
                const isCurrent = version.id === currentVersionId;
                const isSwitching = switchingVersionId === version.id;
                return (
                  <div
                    className={`flex items-center gap-2 rounded-md border bg-white px-3 py-2 transition-colors ${
                      selectedVersion?.id === version.id
                        ? "border-zinc-900 text-zinc-900"
                        : "border-zinc-200 text-zinc-600 hover:border-zinc-300"
                    }`}
                    key={version.id}
                  >
                    <button
                      className="min-w-0 flex-1 text-left focus:outline-none"
                      type="button"
                      onClick={() => onSelectVersion(version.id)}
                    >
                      <span className="block font-mono text-xs font-semibold">V{version.version}</span>
                      <span className="mt-1 block truncate text-[11px] text-zinc-400">
                        {strategyModeLabel(version.strategy_mode)} · {formatDate(version.created_at)}
                      </span>
                    </button>
                    {isCurrent ? (
                      <span className="shrink-0 rounded border border-emerald-200 bg-emerald-50 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-700">
                        当前
                      </span>
                    ) : (
                      <button
                        className="inline-flex h-7 shrink-0 items-center gap-1 rounded-md border border-zinc-300 bg-white px-2 text-[11px] font-semibold text-zinc-700 transition-colors hover:border-zinc-400 hover:bg-zinc-50 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-300"
                        type="button"
                        disabled={
                          switchingVersionId !== null ||
                          panel.isBacktesting ||
                          panel.strategy.status !== "active"
                        }
                        onClick={() => onSwitchVersion(version)}
                      >
                        {isSwitching ? (
                          <RefreshCw className="h-3 w-3 animate-spin" />
                        ) : (
                          <Check className="h-3 w-3" />
                        )}
                        {isSwitching ? "切换中" : "切换"}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </aside>

          <div className="min-h-0 overflow-y-auto p-4">
            {panel.error ? <Feedback tone="error" text={panel.error} /> : null}
            {!selectedVersion ? (
              <Notice text="暂无版本" />
            ) : (
              <div className="grid gap-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="min-w-0">
                    <div className="font-mono text-xs font-semibold text-zinc-900">
                      V{selectedVersion.version}
                    </div>
                    <div className="mt-1 text-xs text-zinc-500">
                      {strategyModeLabel(selectedVersion.strategy_mode)}
                      {selectedVersion.custom_params.length > 0 ? " · " : ""}
                      {selectedVersion.custom_params
                        .map((param) => `${param.name_en}=${String(param.default)}`)
                        .join(", ")}
                    </div>
                  </div>
                  <SmallButton
                    icon={
                      runningBacktestKey === `version:${selectedVersion.id}` ? (
                        <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                      ) : (
                        <Play className="h-3.5 w-3.5" />
                      )
                    }
                    label={runningBacktestKey === `version:${selectedVersion.id}` ? "回测中" : "回测"}
                    disabled={panel.isBacktesting || panel.strategy.status !== "active"}
                    onClick={() => onBacktest(selectedVersion)}
                  />
                </div>

                <section className="rounded-md border border-zinc-200 p-3">
                  <div className="mb-3 flex items-center gap-2 text-xs font-semibold text-zinc-700">
                    <GitCompare className="h-3.5 w-3.5" />
                    版本比对
                  </div>
                  <div className="grid gap-2">
                    {diffItems.map((item) => (
                      <div className="grid grid-cols-[120px_minmax(0,1fr)] gap-3 text-xs" key={item.label}>
                        <span className="text-zinc-500">{item.label}</span>
                        <span className="min-w-0 break-words font-mono text-zinc-800">{item.value}</span>
                      </div>
                    ))}
                  </div>
                </section>

                <section className="rounded-md border border-zinc-200 p-3">
                  <div className="mb-3 flex items-center gap-2 text-xs font-semibold text-zinc-700">
                    <History className="h-3.5 w-3.5" />
                    回测记录
                  </div>
                  {panel.isLoading ? <Notice text="记录加载中" /> : null}
                  {!panel.isLoading && panel.backtests.length === 0 ? <Notice text="暂无回测记录" /> : null}
                  <BacktestRecordList records={panel.backtests} onViewResult={onViewResult} />
                </section>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

function BacktestRecordsPanel({
  panel,
  onClose,
  onViewResult,
}: {
  panel: Exclude<RecordsPanelState, null>;
  onClose: () => void;
  onViewResult: (backtestId: string) => void;
}) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-ink/35 p-4">
      <section className="flex max-h-[86vh] w-full max-w-4xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-zinc-900">
              {panel.strategy.name} 回测记录
            </h2>
            <p className="mt-0.5 font-mono text-[11px] text-zinc-500">
              当前版本 V{panel.strategy.version}
            </p>
          </div>
          <IconButton label="关闭" icon={<X className="h-4 w-4" />} onClick={onClose} />
        </div>
        <div className="min-h-0 overflow-y-auto p-4">
          {panel.error ? <Feedback tone="error" text={panel.error} /> : null}
          {panel.isLoading ? <Notice text="记录加载中" /> : null}
          {!panel.isLoading && panel.records.length === 0 ? <Notice text="暂无回测记录" /> : null}
          <BacktestRecordList records={panel.records} onViewResult={onViewResult} />
        </div>
      </section>
    </div>
  );
}

function BacktestRecordList({
  records,
  onViewResult,
}: {
  records: BacktestRecordView[];
  onViewResult: (backtestId: string) => void;
}) {
  if (records.length === 0) {
    return null;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[820px] table-fixed border-collapse text-left text-xs">
        <thead className="border-b border-zinc-200 bg-zinc-50 text-zinc-500">
          <tr>
            <th className="w-20 px-3 py-2 font-semibold">版本</th>
            <th className="w-28 px-3 py-2 font-semibold">模式</th>
            <th className="w-28 px-3 py-2 font-semibold">状态</th>
            <th className="px-3 py-2 font-semibold">开始时间</th>
            <th className="px-3 py-2 font-semibold">结束时间</th>
            <th className="w-32 px-3 py-2 font-semibold">标的</th>
            <th className="w-24 px-3 py-2 font-semibold">结果</th>
          </tr>
        </thead>
        <tbody>
          {records.map(({ backtest, version }) => (
            <tr className="border-b border-zinc-100 last:border-b-0" key={backtest.id}>
              <td className="px-3 py-2 font-mono font-semibold text-zinc-800">V{version.version}</td>
              <td className="px-3 py-2 text-zinc-600">{strategyModeLabel(version.strategy_mode)}</td>
              <td className="px-3 py-2">
                <StatusText status={backtest.status} />
              </td>
              <td className="px-3 py-2 font-mono text-zinc-600">
                {backtest.started_at ? formatDate(backtest.started_at) : "-"}
              </td>
              <td className="px-3 py-2 font-mono text-zinc-600">
                {backtest.completed_at ? formatDate(backtest.completed_at) : "-"}
              </td>
              <td className="truncate px-3 py-2 text-zinc-600">
                {backtest.config.symbols.join(", ")}
              </td>
              <td className="px-3 py-2">
                <button
                  className="rounded border border-zinc-300 px-2 py-1 font-semibold text-zinc-700 transition-colors hover:border-zinc-400 hover:bg-zinc-50 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-300"
                  type="button"
                  disabled={!backtest.result_id}
                  onClick={() => onViewResult(backtest.id)}
                >
                  查看
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function BacktestRunDialog({
  dialog,
  error,
  form,
  disabled,
  onChange,
  onClose,
  onSubmit,
}: {
  dialog: Exclude<BacktestDialogState, null>;
  error: string | null;
  form: BacktestForm;
  disabled?: boolean;
  onChange: (form: BacktestForm) => void;
  onClose: () => void;
  onSubmit: () => void;
}) {
  const [showMore, setShowMore] = useState(false);
  const customParams = dialog.version?.custom_params ?? dialog.strategy.custom_params;
  const setField = <Key extends keyof BacktestForm>(field: Key, value: BacktestForm[Key]) => {
    onChange(applyBacktestFieldUpdate(form, field, value));
  };
  const setDateRangePreset = (years: number) => {
    onChange({
      ...form,
      ...backtestDateRangeForYears(years),
    });
  };
  const setParamValue = (name: string, value: string) => {
    onChange({
      ...form,
      customParamValues: { ...form.customParamValues, [name]: value },
    });
  };

  return (
    <div className="fixed inset-0 z-[60] grid place-items-center bg-ink/35 p-4">
      <section className="flex max-h-[88vh] w-full max-w-3xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-zinc-900">回测参数</h2>
            <p className="mt-0.5 truncate font-mono text-[11px] text-zinc-500">
              {dialog.strategy.name} · V{dialog.version?.version ?? dialog.strategy.version}
            </p>
          </div>
          <IconButton label="关闭" icon={<X className="h-4 w-4" />} disabled={disabled} onClick={onClose} />
        </div>
        <div className="min-h-0 overflow-y-auto p-4">
          <div className="grid gap-4">
            {error ? <Feedback tone="error" text={error} /> : null}
            <section className="grid gap-3 rounded-md border border-zinc-200 p-3">
              <div className="text-xs font-semibold text-zinc-700">通用回测参数</div>
              <div className="grid grid-cols-3 gap-3 max-md:grid-cols-2 max-sm:grid-cols-1">
                <ReadOnlyField label="策略模式" value={strategyModeLabel(form.strategyMode)} />
                <Select label="市场" required value={form.market} disabled={disabled} options={marketOptions} onChange={(value) => setField("market", value as BacktestForm["market"])} />
                <Select label="资产类别" required value={form.assetClass} disabled={disabled} options={assetClassOptionsForMarket(form.market)} onChange={(value) => setField("assetClass", value as BacktestForm["assetClass"])} />
                <Input label={symbolInputLabel(form.strategyMode)} required value={form.symbols} disabled={disabled} onChange={(value) => setField("symbols", value)} />
                {form.strategyMode === "universe_selection" ? (
                  <Input label="股票池" required value={form.universe} disabled={disabled} onChange={(value) => setField("universe", value)} />
                ) : null}
                <Select label="基准" value={form.benchmarkPreset} disabled={disabled} options={benchmarkOptionsForMarket(form.market)} onChange={(value) => setField("benchmarkPreset", value)} />
                {form.benchmarkPreset === customBenchmarkValue ? (
                  <Input label="其他基准代码" required value={form.benchmarkSymbol} disabled={disabled} onChange={(value) => setField("benchmarkSymbol", value)} />
                ) : null}
                <DateRangeField
                  startDate={form.startDate}
                  endDate={form.endDate}
                  disabled={disabled}
                  onStartChange={(value) => setField("startDate", value)}
                  onEndChange={(value) => setField("endDate", value)}
                  onPreset={setDateRangePreset}
                />
                <Input label="初始资金" required value={form.initialCash} disabled={disabled} onChange={(value) => setField("initialCash", value)} />
                <Input label="手续费" required value={form.commission} disabled={disabled} onChange={(value) => setField("commission", value)} />
              </div>
              <div>
                <SmallButton
                  icon={<Settings2 className="h-3.5 w-3.5" />}
                  label={showMore ? "收起设置" : "更多设置"}
                  disabled={disabled}
                  onClick={() => setShowMore(!showMore)}
                />
              </div>
              {showMore ? (
                <div className="grid gap-3 border-t border-zinc-100 pt-3">
                  <div className="grid grid-cols-3 gap-3 max-md:grid-cols-2 max-sm:grid-cols-1">
                    <Input label="滑点" value={form.slippage} disabled={disabled} onChange={(value) => setField("slippage", value)} />
                  </div>
                  <Textarea label="备注" value={form.notes} rows={2} disabled={disabled} onChange={(value) => setField("notes", value)} />
                </div>
              ) : null}
            </section>

            <section className="grid gap-3 rounded-md border border-zinc-200 p-3">
              <div className="text-xs font-semibold text-zinc-700">本次策略参数</div>
              {customParams.length === 0 ? <Notice text="当前版本没有自定义参数" /> : null}
              <div className="grid grid-cols-2 gap-3 max-sm:grid-cols-1">
                {customParams.map((param) => (
                  <Input
                    key={param.name_en}
                    label={param.name_cn}
                    required={param.required}
                    value={form.customParamValues[param.name_en] ?? String(param.default)}
                    disabled={disabled}
                    onChange={(value) => setParamValue(param.name_en, value)}
                  />
                ))}
              </div>
            </section>
          </div>
        </div>
        <div className="flex justify-end gap-2 border-t border-line bg-soft px-4 py-3">
          <button
            className="h-9 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:bg-soft focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:text-muted/50"
            type="button"
            disabled={disabled}
            onClick={onClose}
          >
            取消
          </button>
          <button
            className="inline-flex h-9 items-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:bg-strong"
            type="button"
            disabled={disabled}
            onClick={onSubmit}
          >
            {disabled ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            {disabled ? "回测中" : "开始回测"}
          </button>
        </div>
      </section>
    </div>
  );
}

function BacktestResultDialog({
  detail,
  onClose,
}: {
  detail: StrategyBacktestDetail;
  onClose: () => void;
}) {
  const [activeResultTab, setActiveResultTab] = useState<ResultTab>("profile");
  const metrics = detail.result?.metrics;
  const result = detail.result;
  const drawdownCurve = detail.result?.curves?.find((curve) => curve.curve_type === "drawdown");
  const equityCurve = detail.result?.curves?.find((curve) => curve.curve_type === "equity");
  const marketSeries = result?.market_data?.[0] ?? null;
  const trades = result?.trades ?? [];
  const benchmarkReturn = result?.benchmark?.total_return_pct;
  const excessReturn =
    metrics && benchmarkReturn !== null && benchmarkReturn !== undefined
      ? (Number(metrics.total_return_pct) - Number(benchmarkReturn)).toFixed(4)
      : null;
  const deepestDrawdown = drawdownCurve
    ? drawdownCurve.points.reduce<null | { date: string; value: string }>((lowest, point) => {
        if (!lowest || Number(point.value) < Number(lowest.value)) {
          return { date: point.date, value: point.value };
        }
        return lowest;
      }, null)
    : null;

  return (
    <div className="fixed inset-0 z-[60] grid place-items-center bg-ink/35 p-4">
      <section className="flex max-h-[88vh] w-full max-w-6xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-zinc-900">回测结果</h2>
            <p className="mt-0.5 truncate font-mono text-[11px] text-zinc-500">
              {detail.backtest.id} · {detail.backtest.status}
            </p>
          </div>
          <IconButton label="关闭" icon={<X className="h-4 w-4" />} onClick={onClose} />
        </div>
        <ResultTabBar value={activeResultTab} onChange={setActiveResultTab} />
        <div className="min-h-0 overflow-y-auto p-4">
          {!result || !metrics ? (
            <Notice text={detail.backtest.failure_message ?? "暂无回测结果"} />
          ) : (
            <div className="grid gap-4">
              {activeResultTab === "profile" ? (
                <>
                  <div className="grid gap-3 sm:grid-cols-4 lg:grid-cols-6">
                    <MetricBox label="策略收益" value={`${metrics.total_return_pct}%`} />
                    <MetricBox label="策略年化收益" value={metrics.annual_return_pct ? `${metrics.annual_return_pct}%` : "-"} />
                    <MetricBox label="超额收益" value={excessReturn ? `${excessReturn}%` : "-"} />
                    <MetricBox label="基准收益" value={benchmarkReturn !== null && benchmarkReturn !== undefined ? `${benchmarkReturn}%` : "-"} />
                    <MetricBox label="阿尔法" value="-" />
                    <MetricBox label="贝塔" value="-" />
                    <MetricBox label="夏普比率" value={metrics.sharpe_ratio ?? "-"} />
                    <MetricBox label="胜率" value={metrics.win_rate_pct ? `${metrics.win_rate_pct}%` : "-"} />
                    <MetricBox label="盈亏比" value="-" />
                    <MetricBox label="最大回撤" value={`${metrics.max_drawdown_pct}%`} />
                    <MetricBox label="索提诺比率" value="-" />
                    <MetricBox label="日均超额收益" value="-" />
                    <MetricBox label="盈利次数" value="-" />
                    <MetricBox label="亏损次数" value="-" />
                    <MetricBox label="信息比率" value="-" />
                    <MetricBox label="策略波动率" value="-" />
                    <MetricBox label="基准波动率" value="-" />
                    <MetricBox label="最大回撤区间" value={metrics.max_drawdown_start && metrics.max_drawdown_end ? `${metrics.max_drawdown_start},${metrics.max_drawdown_end}` : "-"} />
                  </div>
                  {equityCurve && result.benchmark ? (
                    <BenchmarkComparisonChart
                      equityPoints={equityCurve.points}
                      benchmark={result.benchmark}
                      initialCash={metrics.initial_value}
                      dailyPositions={result.daily_positions ?? []}
                      trades={trades}
                    />
                  ) : (
                    <Notice text="暂无基准对比数据" />
                  )}
                  <section className="rounded-md border border-zinc-200 p-3 text-xs">
                    <div className="mb-3 font-semibold text-zinc-800">回撤结果</div>
                    <div className="grid gap-2 sm:grid-cols-2">
                      <InfoLine label="回撤开始" value={metrics.max_drawdown_start ?? "-"} />
                      <InfoLine label="回撤结束" value={metrics.max_drawdown_end ?? "-"} />
                      <InfoLine
                        label="持续天数"
                        value={
                          metrics.max_drawdown_duration_days === null ||
                          metrics.max_drawdown_duration_days === undefined
                            ? "-"
                            : `${metrics.max_drawdown_duration_days} 天`
                        }
                      />
                      <InfoLine
                        label="曲线低点"
                        value={
                          deepestDrawdown
                            ? `${deepestDrawdown.date} / ${deepestDrawdown.value}%`
                            : "-"
                        }
                      />
                    </div>
                  </section>
                  {result.warnings.length > 0 ? (
                    <Feedback tone="error" text={result.warnings.join("；")} />
                  ) : null}
                  <section className="rounded-md border border-zinc-200 p-3 text-xs text-zinc-600">
                    {result.summary}
                  </section>
                </>
              ) : null}
              {activeResultTab === "trades" ? (
                <section className="rounded-md border border-zinc-200 p-3 text-xs">
                  <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
                    <div className="font-semibold text-zinc-800">交易详情</div>
                    <span className="rounded border border-zinc-200 px-2 py-1 font-semibold text-zinc-600">Group by day</span>
                  </div>
                  {trades.length === 0 ? <Notice text="暂无交易详情" /> : <TradeExecutionTable trades={trades} />}
                </section>
              ) : null}
              {activeResultTab === "positions" ? (
                <section className="rounded-md border border-zinc-200 p-3 text-xs">
                  <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
                    <div className="font-semibold text-zinc-800">每日持仓&收益</div>
                    <span className="rounded border border-zinc-200 px-2 py-1 font-semibold text-zinc-600">Group by day</span>
                  </div>
                  {(result.daily_positions ?? []).length === 0 ? (
                    <Notice text="暂无每日持仓数据" />
                  ) : (
                    <DailyPositionsTable snapshots={result.daily_positions ?? []} />
                  )}
                </section>
              ) : null}
              {activeResultTab === "signals" ? (
                marketSeries ? (
                  <CandlestickChart
                    title={`${marketSeries.symbol} K线与买卖点`}
                    candles={marketSeries.candles}
                    trades={tradesForSeries(trades, marketSeries.symbol)}
                    equityPoints={equityCurve?.points ?? []}
                    initialCash={metrics.initial_value}
                    dailyPositions={result.daily_positions ?? []}
                  />
                ) : (
                  <Notice text="暂无K线数据" />
                )
              ) : null}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function ResultTabBar({
  value,
  onChange,
}: {
  value: ResultTab;
  onChange: (value: ResultTab) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2 border-b border-zinc-200 bg-zinc-50 px-4 py-2">
      {resultTabs.map((tab) => (
        <button
          className={`h-8 rounded-md px-3 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-900/20 ${
            value === tab.value
              ? "bg-zinc-900 text-white"
              : "border border-zinc-200 bg-white text-zinc-600 hover:border-zinc-300 hover:text-zinc-900"
          }`}
          key={tab.value}
          type="button"
          onClick={() => onChange(tab.value)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

function CandlestickChart({
  title,
  candles,
  trades,
  equityPoints,
  initialCash,
  dailyPositions,
}: {
  title: string;
  candles: StrategyMarketCandle[];
  trades: StrategyTradeRecord[];
  equityPoints: StrategyCurvePoint[];
  initialCash: string;
  dailyPositions: StrategyDailyPortfolioSnapshot[];
}) {
  if (candles.length === 0) {
    return <Notice text="暂无K线数据" />;
  }

  const dates = candles.map((candle) => candle.date);
  const buyPoints = trades
    .filter((trade) => trade.side === "buy")
    .map((trade) => tradeToChartPoint(trade, dates))
    .filter((point): point is TradeChartPoint => point !== null);
  const sellPoints = trades
    .filter((trade) => trade.side !== "buy")
    .map((trade) => tradeToChartPoint(trade, dates))
    .filter((point): point is TradeChartPoint => point !== null);
  const strategyReturnByDate = new Map(
    equityPoints.map((point) => [
      point.date,
      (toNumber(point.value) / Math.max(1, toNumber(initialCash)) - 1) * 100,
    ]),
  );
  const dailyMap = new Map(dailyPositions.map((snapshot) => [snapshot.date, snapshot]));
  const option: EChartsOption = {
    animation: false,
    color: ["#16a34a", "#dc2626"],
    grid: { left: 48, right: 48, top: 24, bottom: 42 },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
      borderColor: "#2563eb",
      formatter: (params: unknown) =>
        formatKlineTooltip(params, candles, trades, strategyReturnByDate, dailyMap),
    },
    xAxis: {
      type: "category",
      data: dates,
      boundaryGap: true,
      axisLine: { lineStyle: { color: "#d4d4d8" } },
      axisLabel: { color: "#71717a", fontSize: 10 },
      splitLine: { show: true, lineStyle: { color: "#e4e4e7" } },
    },
    yAxis: {
      type: "value",
      scale: true,
      axisLabel: { color: "#71717a", fontSize: 10 },
      splitLine: { lineStyle: { color: "#e4e4e7" } },
    },
    dataZoom: [
      { type: "inside", start: 0, end: 100 },
      { type: "slider", height: 18, bottom: 8, start: 0, end: 100 },
    ],
    series: [
      {
        name: "K线",
        type: "candlestick",
        data: candles.map((candle) => [
          toNumber(candle.open),
          toNumber(candle.close),
          toNumber(candle.low),
          toNumber(candle.high),
        ]),
        itemStyle: {
          color: "#16a34a",
          color0: "#dc2626",
          borderColor: "#16a34a",
          borderColor0: "#dc2626",
        },
      },
      {
        name: "买入",
        type: "scatter",
        symbol: "triangle",
        symbolSize: 14,
        z: 20,
        label: {
          show: true,
          formatter: "B",
          position: "bottom",
          color: "#16a34a",
          fontSize: 11,
          fontWeight: 700,
        },
        itemStyle: { color: "#16a34a" },
        data: buyPoints.map((point) => point.value),
      },
      {
        name: "卖出",
        type: "scatter",
        symbol: "triangle",
        symbolRotate: 180,
        symbolSize: 14,
        z: 20,
        label: {
          show: true,
          formatter: "S",
          position: "top",
          color: "#dc2626",
          fontSize: 11,
          fontWeight: 700,
        },
        itemStyle: { color: "#dc2626" },
        data: sellPoints.map((point) => point.value),
      },
    ],
  };

  return (
    <section className="rounded-md border border-zinc-200 p-3">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div className="text-xs font-semibold text-zinc-800">{title}</div>
        <div className="flex items-center gap-3 text-[11px] text-zinc-500">
          <span className="inline-flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-emerald-600" />买入</span>
          <span className="inline-flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-red-600" />卖出</span>
        </div>
      </div>
      <EChartsPanel option={option} height={360} ariaLabel={title} />
    </section>
  );
}

function BenchmarkComparisonChart({
  equityPoints,
  benchmark,
  initialCash,
  dailyPositions,
  trades,
}: {
  equityPoints: StrategyCurvePoint[];
  benchmark: StrategyBenchmarkSeries;
  initialCash: string;
  dailyPositions: StrategyDailyPortfolioSnapshot[];
  trades: StrategyTradeRecord[];
}) {
  const strategySeries = equityPoints.map((point) => ({
    date: point.date,
    value: (toNumber(point.value) / Math.max(1, toNumber(initialCash)) - 1) * 100,
  }));
  const benchmarkSeries = benchmark.points.map((point) => ({
    date: point.date,
    value: toNumber(point.normalized_value),
  }));
  const allValues = [...strategySeries, ...benchmarkSeries]
    .map((point) => point.value)
    .filter(Number.isFinite);
  if (allValues.length === 0) {
    return <Notice text="暂无基准对比数据" />;
  }

  const dates = strategySeries.map((point) => point.date);
  const dailyMap = new Map(dailyPositions.map((snapshot) => [snapshot.date, snapshot]));
  const tradesByDate = groupTradesByDate(trades);
  const strategyMap = new Map(strategySeries.map((point) => [point.date, point.value]));
  const benchmarkMap = new Map(benchmarkSeries.map((point) => [point.date, point.value]));
  const buyPoints = trades
    .filter((trade) => trade.side === "buy")
    .map((trade) => tradeToReturnPoint(trade, dates, strategyMap))
    .filter((point): point is TradeChartPoint => point !== null);
  const sellPoints = trades
    .filter((trade) => trade.side !== "buy")
    .map((trade) => tradeToReturnPoint(trade, dates, strategyMap))
    .filter((point): point is TradeChartPoint => point !== null);
  const option: EChartsOption = {
    animation: false,
    color: ["#2563eb", "#b45309", "#f97316", "#16a34a", "#dc2626"],
    grid: { left: 50, right: 48, top: 24, bottom: 42 },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
      borderColor: "#2563eb",
      formatter: (params: unknown) =>
        formatReturnTooltip(params, strategySeries, strategyMap, benchmarkMap, dailyMap, tradesByDate),
    },
    legend: {
      top: 0,
      right: 0,
      data: ["策略收益", "基准收益", "超额收益", "买入", "卖出"],
      itemWidth: 10,
      itemHeight: 10,
      textStyle: { color: "#52525b", fontSize: 11 },
    },
    xAxis: {
      type: "category",
      data: dates,
      axisLine: { lineStyle: { color: "#d4d4d8" } },
      axisLabel: { color: "#71717a", fontSize: 10 },
      splitLine: { show: true, lineStyle: { color: "#e4e4e7" } },
    },
    yAxis: {
      type: "value",
      axisLabel: { color: "#71717a", fontSize: 10, formatter: "{value}%" },
      splitLine: { lineStyle: { color: "#e4e4e7" } },
    },
    dataZoom: [
      { type: "inside", start: 0, end: 100 },
      { type: "slider", height: 18, bottom: 8, start: 0, end: 100 },
    ],
    series: [
      {
        name: "策略收益",
        type: "line",
        smooth: false,
        symbol: "none",
        itemStyle: { color: "#2563eb" },
        lineStyle: { width: 2.5, color: "#2563eb" },
        areaStyle: { color: "rgba(37, 99, 235, 0.12)" },
        data: strategySeries.map((point) => roundNumber(point.value, 4)),
      },
      {
        name: "基准收益",
        type: "line",
        smooth: false,
        symbol: "none",
        itemStyle: { color: "#b45309" },
        lineStyle: { width: 2.5, color: "#b45309" },
        data: dates.map((date) => roundNumber(benchmarkMap.get(date) ?? 0, 4)),
      },
      {
        name: "超额收益",
        type: "line",
        smooth: false,
        symbol: "none",
        itemStyle: { color: "#f97316" },
        lineStyle: { width: 1.8, color: "#f97316", type: "dashed" },
        data: strategySeries.map((point) =>
          roundNumber(point.value - (benchmarkMap.get(point.date) ?? 0), 4),
        ),
      },
      {
        name: "买入",
        type: "scatter",
        symbol: "triangle",
        symbolSize: 14,
        z: 20,
        label: {
          show: true,
          formatter: "B",
          position: "bottom",
          color: "#16a34a",
          fontSize: 11,
          fontWeight: 700,
        },
        itemStyle: { color: "#16a34a" },
        data: buyPoints.map((point) => point.value),
      },
      {
        name: "卖出",
        type: "scatter",
        symbol: "triangle",
        symbolRotate: 180,
        symbolSize: 14,
        z: 20,
        label: {
          show: true,
          formatter: "S",
          position: "top",
          color: "#dc2626",
          fontSize: 11,
          fontWeight: 700,
        },
        itemStyle: { color: "#dc2626" },
        data: sellPoints.map((point) => point.value),
      },
    ],
  };

  return (
    <section className="rounded-md border border-zinc-200 p-3">
      <div className="mb-3">
        <div className="text-xs font-semibold text-zinc-800">策略收益 vs 基准</div>
      </div>
      <EChartsPanel option={option} height={300} ariaLabel="策略收益与基准收益对比" />
    </section>
  );
}

function EChartsPanel({
  option,
  height,
  ariaLabel,
}: {
  option: EChartsOption;
  height: number;
  ariaLabel: string;
}) {
  const chartRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!chartRef.current) {
      return undefined;
    }
    const chart = echarts.init(chartRef.current, undefined, { renderer: "canvas" });
    chart.setOption(option, true);
    const resizeObserver = new ResizeObserver(() => chart.resize());
    resizeObserver.observe(chartRef.current);
    return () => {
      resizeObserver.disconnect();
      chart.dispose();
    };
  }, [option]);

  return (
    <div
      ref={chartRef}
      aria-label={ariaLabel}
      role="img"
      className="w-full min-w-[760px]"
      style={{ height }}
    />
  );
}

type ReturnPoint = {
  date: string;
  value: number;
};

type TooltipParam = {
  dataIndex?: number;
  axisValue?: string | number;
  axisValueLabel?: string;
};

type TradeChartPoint = {
  trade: StrategyTradeRecord;
  value: [string, number];
};

function tradesForSeries(
  trades: StrategyTradeRecord[],
  symbol: string,
): StrategyTradeRecord[] {
  const normalizedSymbol = normalizeSymbolKey(symbol);
  const matched = trades.filter((trade) => normalizeSymbolKey(trade.symbol) === normalizedSymbol);
  return matched.length > 0 ? matched : trades;
}

function tradeToChartPoint(
  trade: StrategyTradeRecord,
  candleDates: string[],
): TradeChartPoint | null {
  const alignedDate = alignTradeDateToCandle(trade.trade_datetime.slice(0, 10), candleDates);
  if (!alignedDate) {
    return null;
  }
  return {
    trade,
    value: [alignedDate, toNumber(trade.price)],
  };
}

function tradeToReturnPoint(
  trade: StrategyTradeRecord,
  returnDates: string[],
  returnMap: Map<string, number>,
): TradeChartPoint | null {
  const alignedDate = alignTradeDateToCandle(trade.trade_datetime.slice(0, 10), returnDates);
  if (!alignedDate) {
    return null;
  }
  const returnValue = returnMap.get(alignedDate);
  if (returnValue === undefined) {
    return null;
  }
  return {
    trade,
    value: [alignedDate, roundNumber(returnValue, 4)],
  };
}

function alignTradeDateToCandle(tradeDate: string, candleDates: string[]): string | null {
  if (candleDates.includes(tradeDate)) {
    return tradeDate;
  }
  const tradeTime = new Date(tradeDate).getTime();
  if (Number.isNaN(tradeTime)) {
    return null;
  }
  let bestDate: string | null = null;
  let bestDistance = Number.POSITIVE_INFINITY;
  for (const candleDate of candleDates) {
    const candleTime = new Date(candleDate).getTime();
    const distance = Math.abs(candleTime - tradeTime);
    if (distance < bestDistance) {
      bestDate = candleDate;
      bestDistance = distance;
    }
  }
  return bestDistance <= 1000 * 60 * 60 * 24 * 7 ? bestDate : null;
}

function normalizeSymbolKey(symbol: string): string {
  return symbol.replace(/[^A-Za-z0-9]/g, "").toUpperCase();
}

function formatReturnTooltip(
  params: unknown,
  strategySeries: ReturnPoint[],
  strategyMap: Map<string, number>,
  benchmarkMap: Map<string, number>,
  dailyMap: Map<string, StrategyDailyPortfolioSnapshot>,
  tradesByDate: Map<string, StrategyTradeRecord[]>,
): string {
  const tooltipParams = toTooltipParams(params);
  const first = tooltipParams[0];
  const index = first?.dataIndex ?? 0;
  const date = String(first?.axisValueLabel ?? first?.axisValue ?? strategySeries[index]?.date ?? "");
  const strategyReturn = strategyMap.get(date) ?? strategySeries[index]?.value ?? 0;
  const benchmarkReturn = benchmarkMap.get(date) ?? 0;
  const excessReturn = strategyReturn - benchmarkReturn;
  const snapshot = dailyMap.get(date);
  const dayTrades = tradesByDate.get(date) ?? [];
  const buyCount = dayTrades.filter((trade) => trade.side === "buy").length;
  const sellCount = dayTrades.length - buyCount;

  return [
    `<div style="min-width:180px;font-size:12px;line-height:1.6;color:#27272a">`,
    `<div style="margin-bottom:4px;color:#52525b">${formatTooltipDate(date)}</div>`,
    tooltipRow("#2563eb", "策略收益", `${formatSigned(strategyReturn)}%`),
    tooltipRow("#b45309", "基准收益", `${formatSigned(benchmarkReturn)}%`),
    tooltipRow("#f97316", "超额收益", `${formatSigned(excessReturn)}%`),
    tooltipRow("#65a30d", "当日盈亏", snapshot ? formatMoney(snapshot.daily_pnl) : "-"),
    tooltipRow("#0891b2", "当日开仓", String(buyCount)),
    tooltipRow("#7c3aed", "当日平仓", String(sellCount)),
    `</div>`,
  ].join("");
}

function formatKlineTooltip(
  params: unknown,
  candles: StrategyMarketCandle[],
  trades: StrategyTradeRecord[],
  strategyReturnByDate: Map<string, number>,
  dailyMap: Map<string, StrategyDailyPortfolioSnapshot>,
): string {
  const tooltipParams = toTooltipParams(params);
  const first = tooltipParams[0];
  const index = first?.dataIndex ?? 0;
  const date = String(first?.axisValueLabel ?? first?.axisValue ?? candles[index]?.date ?? "");
  const candle = candles.find((item) => item.date === date) ?? candles[index];
  const dayTrades = trades.filter((trade) => trade.trade_datetime.startsWith(date));
  const strategyReturn = strategyReturnByDate.get(date);
  const snapshot = dailyMap.get(date);
  return [
    `<div style="min-width:180px;font-size:12px;line-height:1.6;color:#27272a">`,
    `<div style="margin-bottom:4px;color:#52525b">${formatTooltipDate(date)}</div>`,
    tooltipRow("#2563eb", "策略收益", strategyReturn === undefined ? "-" : `${formatSigned(strategyReturn)}%`),
    tooltipRow("#65a30d", "当日收益", snapshot ? formatMoney(snapshot.daily_pnl) : "-"),
    tooltipRow("#52525b", "开盘", candle?.open ?? "-"),
    tooltipRow("#52525b", "最高", candle?.high ?? "-"),
    tooltipRow("#52525b", "最低", candle?.low ?? "-"),
    tooltipRow("#52525b", "收盘", candle?.close ?? "-"),
    tooltipRow("#16a34a", "买入", String(dayTrades.filter((trade) => trade.side === "buy").length)),
    tooltipRow("#dc2626", "卖出", String(dayTrades.filter((trade) => trade.side !== "buy").length)),
    `</div>`,
  ].join("");
}

function tooltipRow(color: string, label: string, value: string): string {
  return `<div><span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:${color};margin-right:6px"></span>${label}: <strong>${value}</strong></div>`;
}

function toTooltipParams(params: unknown): TooltipParam[] {
  const values = Array.isArray(params) ? params : [params];
  return values.filter(isTooltipParam);
}

function isTooltipParam(value: unknown): value is TooltipParam {
  if (!value || typeof value !== "object") {
    return false;
  }
  const candidate = value as Record<string, unknown>;
  return (
    candidate.dataIndex === undefined ||
    typeof candidate.dataIndex === "number"
  );
}

function groupTradesByDate(trades: StrategyTradeRecord[]): Map<string, StrategyTradeRecord[]> {
  const grouped = new Map<string, StrategyTradeRecord[]>();
  for (const trade of trades) {
    const date = trade.trade_datetime.slice(0, 10);
    grouped.set(date, [...(grouped.get(date) ?? []), trade]);
  }
  return grouped;
}

function TradeExecutionTable({ trades }: { trades: StrategyTradeRecord[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[920px] table-fixed border-collapse text-left">
        <thead className="border-b border-zinc-200 bg-zinc-50 text-zinc-500">
          <tr>
            <th className="w-28 px-3 py-2 font-semibold">日期</th>
            <th className="w-24 px-3 py-2 font-semibold">委托时间</th>
            <th className="w-36 px-3 py-2 font-semibold">标的</th>
            <th className="w-20 px-3 py-2 font-semibold">方向</th>
            <th className="w-24 px-3 py-2 font-semibold">下单类型</th>
            <th className="px-3 py-2 font-semibold">成交数量</th>
            <th className="px-3 py-2 font-semibold">成交价</th>
            <th className="px-3 py-2 font-semibold">成交额</th>
            <th className="px-3 py-2 font-semibold">手续费</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade) => (
            <tr className="border-b border-zinc-100 last:border-b-0" key={trade.id}>
              <td className="px-3 py-2 font-mono text-zinc-600">{trade.trade_datetime.slice(0, 10)}</td>
              <td className="px-3 py-2 font-mono text-zinc-600">{formatTradeTime(trade.trade_datetime)}</td>
              <td className="truncate px-3 py-2 font-mono text-zinc-700">{trade.symbol}</td>
              <td className={trade.side === "buy" ? "px-3 py-2 font-semibold text-emerald-700" : "px-3 py-2 font-semibold text-red-700"}>
                {trade.side === "buy" ? "买入" : "卖出"}
              </td>
              <td className="px-3 py-2 text-zinc-600">市价单</td>
              <td className="px-3 py-2 font-mono text-zinc-700">{trade.size}</td>
              <td className="px-3 py-2 font-mono text-zinc-700">{trade.price}</td>
              <td className="px-3 py-2 font-mono text-zinc-700">{trade.value}</td>
              <td className="px-3 py-2 font-mono text-zinc-700">{trade.commission}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function DailyPositionsTable({ snapshots }: { snapshots: StrategyDailyPortfolioSnapshot[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[860px] table-fixed border-collapse text-left">
        <thead className="border-b border-zinc-200 bg-zinc-50 text-zinc-500">
          <tr>
            <th className="w-44 px-3 py-2 font-semibold">标的</th>
            <th className="px-3 py-2 font-semibold">数量</th>
            <th className="px-3 py-2 font-semibold">收盘价/结算价</th>
            <th className="px-3 py-2 font-semibold">市值/价值</th>
            <th className="px-3 py-2 font-semibold">盈亏/逐笔浮盈</th>
          </tr>
        </thead>
        <tbody>
          {snapshots.map((snapshot) => (
            <DailyPositionRows key={snapshot.date} snapshot={snapshot} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

function DailyPositionRows({ snapshot }: { snapshot: StrategyDailyPortfolioSnapshot }) {
  return (
    <>
      <tr className="border-t border-zinc-200 bg-zinc-50">
        <td className="px-3 py-2 font-mono text-sm font-semibold text-zinc-800" colSpan={5}>
          {snapshot.date}
        </td>
      </tr>
      {snapshot.positions.map((position) => (
        <tr className="border-b border-zinc-100" key={`${snapshot.date}-${position.symbol}`}>
          <td className="px-3 py-2 font-mono text-zinc-700">{position.symbol}</td>
          <td className="px-3 py-2 font-mono text-zinc-700">{position.size}</td>
          <td className="px-3 py-2 font-mono text-zinc-700">{position.close_price}</td>
          <td className="px-3 py-2 font-mono text-zinc-700">{formatMoney(position.market_value)}</td>
          <td className={toNumber(position.unrealized_pnl) >= 0 ? "px-3 py-2 font-mono text-emerald-700" : "px-3 py-2 font-mono text-red-700"}>
            {formatMoney(position.unrealized_pnl)}
          </td>
        </tr>
      ))}
      <tr className="border-b border-zinc-100">
        <td className="px-3 py-2">
          <span className="rounded bg-emerald-600 px-1.5 py-0.5 text-[11px] font-semibold text-white">Cash</span>
        </td>
        <td className="px-3 py-2 font-mono text-zinc-500">-</td>
        <td className="px-3 py-2 font-mono text-zinc-500">-</td>
        <td className="px-3 py-2 font-mono text-zinc-700">{formatMoney(snapshot.cash)}</td>
        <td className="px-3 py-2 font-mono text-zinc-500">0.00</td>
      </tr>
      <tr className="border-b border-zinc-200 bg-zinc-50">
        <td className="px-3 py-2 font-semibold text-zinc-800" colSpan={3}>
          总共
        </td>
        <td className="px-3 py-2 font-mono font-semibold text-zinc-900">
          {formatMoney(snapshot.total_value)}
        </td>
        <td className={toNumber(snapshot.daily_pnl) >= 0 ? "px-3 py-2 font-mono font-semibold text-emerald-700" : "px-3 py-2 font-mono font-semibold text-red-700"}>
          {formatMoney(snapshot.daily_pnl)}
        </td>
      </tr>
    </>
  );
}

function StrategyFormFields({
  mode,
  form,
  disabled,
  onChange,
}: {
  mode: "create" | "edit" | "version";
  form: StrategyForm;
  disabled?: boolean;
  onChange: (form: StrategyForm) => void;
}) {
  const setField = <Key extends keyof StrategyForm>(field: Key, value: StrategyForm[Key]) => {
    onChange({ ...form, [field]: value });
  };

  return (
    <div className="grid gap-4">
      {mode !== "version" ? (
        <>
          <Input label="名称" value={form.name} disabled={disabled} onChange={(value) => setField("name", value)} />
          <Input label="描述" value={form.description} disabled={disabled} onChange={(value) => setField("description", value)} />
          <Input label="标签" value={form.tags} disabled={disabled} onChange={(value) => setField("tags", value)} />
        </>
      ) : null}

      <section className="grid gap-3 rounded-md border border-zinc-200 p-3">
        <div className="text-xs font-semibold text-zinc-700">策略模式</div>
        <Select
          label="股票模式"
          required
          value={form.strategyMode}
          disabled={disabled}
          options={strategyModeOptions}
          onChange={(value) => setField("strategyMode", value as StrategyMode)}
        />
      </section>

      <>
        <Textarea label="策略代码" value={form.code} rows={14} monospace disabled={disabled} onChange={(value) => setField("code", value)} />
        <Textarea label="风险说明" value={form.riskNote} rows={3} disabled={disabled} onChange={(value) => setField("riskNote", value)} />
      </>
    </div>
  );
}

function Dialog({
  title,
  children,
  submitLabel,
  submitIcon,
  isSubmitting,
  onClose,
  onSubmit,
}: {
  title: string;
  children: ReactNode;
  submitLabel: string;
  submitIcon: ReactNode;
  isSubmitting: boolean;
  onClose: () => void;
  onSubmit: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-ink/35 p-4">
      <section className="flex max-h-[86vh] w-full max-w-2xl flex-col overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
          <h2 className="truncate text-sm font-semibold text-zinc-900">{title}</h2>
          <IconButton label="关闭" icon={<X className="h-4 w-4" />} disabled={isSubmitting} onClick={onClose} />
        </div>
        <div className="min-h-0 overflow-y-auto p-4">{children}</div>
        <div className="flex justify-end gap-2 border-t border-line bg-soft px-4 py-3">
          <button
            className="h-9 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:bg-soft focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:text-muted/50"
            type="button"
            disabled={isSubmitting}
            onClick={onClose}
          >
            取消
          </button>
          <button
            className="inline-flex h-9 items-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:bg-strong"
            type="button"
            disabled={isSubmitting}
            onClick={onSubmit}
          >
            {submitIcon}
            {submitLabel}
          </button>
        </div>
      </section>
    </div>
  );
}

function StatusFilterControl({ value, onChange }: { value: StatusFilter; onChange: (value: StatusFilter) => void }) {
  return (
    <div className="grid h-9 grid-cols-2 overflow-hidden rounded-md border border-line bg-panel text-[11px] font-semibold">
      {statusFilters.map((filter) => (
        <button
          className={`min-w-12 px-2 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-signal/20 ${value === filter.value ? "bg-ink text-panel" : "text-muted hover:bg-soft hover:text-ink"}`}
          key={filter.value}
          type="button"
          onClick={() => onChange(filter.value)}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}

function FieldLabel({ label, required }: { label: string; required?: boolean }) {
  return (
    <span className="font-semibold text-muted">
      {label}
      {required ? <span className="ml-0.5 text-risk">*</span> : null}
    </span>
  );
}

function Input({ label, value, type = "text", required, disabled, onChange }: { label: string; value: string; type?: "text" | "date"; required?: boolean; disabled?: boolean; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-1 text-xs">
      <FieldLabel label={label} required={required} />
      <input
        className="h-9 rounded-md border border-line bg-panel px-3 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
        disabled={disabled}
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function DateRangeField({
  startDate,
  endDate,
  disabled,
  onStartChange,
  onEndChange,
  onPreset,
}: {
  startDate: string;
  endDate: string;
  disabled?: boolean;
  onStartChange: (value: string) => void;
  onEndChange: (value: string) => void;
  onPreset: (years: number) => void;
}) {
  return (
    <fieldset className="col-span-3 grid gap-2 text-xs max-md:col-span-2 max-sm:col-span-1">
      <FieldLabel label="回测区间" required />
      <div className="grid gap-2 rounded-md border border-line bg-panel p-2">
        <div className="grid grid-cols-[1fr_auto_1fr] items-end gap-2 max-sm:grid-cols-1">
          <DateInput label="开始" value={startDate} disabled={disabled} onChange={onStartChange} />
          <span className="pb-2 text-center font-semibold text-muted max-sm:hidden">至</span>
          <DateInput label="结束" value={endDate} disabled={disabled} onChange={onEndChange} />
        </div>
        <div className="flex flex-wrap gap-1.5">
          {backtestDateRangePresets.map((preset) => (
            <button
              className="h-7 rounded border border-line bg-soft px-2 text-[11px] font-semibold text-graphite transition-colors hover:border-strong hover:bg-panel hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:text-muted/50"
              key={preset.years}
              type="button"
              disabled={disabled}
              onClick={() => onPreset(preset.years)}
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>
    </fieldset>
  );
}

function DateInput({ label, value, disabled, onChange }: { label: string; value: string; disabled?: boolean; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-1">
      <span className="font-semibold text-muted">{label}</span>
      <input
        className="h-9 rounded-md border border-line bg-panel px-3 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
        disabled={disabled}
        type="date"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function ReadOnlyField({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1 text-xs">
      <FieldLabel label={label} />
      <div className="flex h-9 items-center rounded-md border border-line bg-soft px-3 text-xs font-semibold text-graphite">
        {value}
      </div>
    </div>
  );
}

function Select({
  label,
  value,
  options,
  required,
  disabled,
  onChange,
}: {
  label: string;
  value: string;
  options: SelectOption[];
  required?: boolean;
  disabled?: boolean;
  onChange: (value: string) => void;
}) {
  return (
    <label className="grid gap-1 text-xs">
      <FieldLabel label={label} required={required} />
      <select
        className="h-9 rounded-md border border-line bg-panel px-3 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
        disabled={disabled}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        {options.map((option) => {
          const normalized = normalizeSelectOption(option);
          return (
          <option key={normalized.value} value={normalized.value}>
            {normalized.label}
          </option>
          );
        })}
      </select>
    </label>
  );
}

function Textarea({ label, value, rows, monospace, required, disabled, onChange }: { label: string; value: string; rows: number; monospace?: boolean; required?: boolean; disabled?: boolean; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-1 text-xs">
      <FieldLabel label={label} required={required} />
      <textarea
        className={`w-full resize-y rounded-md border border-line bg-panel p-3 text-xs leading-5 text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted ${monospace ? "font-mono text-[11px]" : ""}`}
        disabled={disabled}
        rows={rows}
        spellCheck={!monospace}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function SmallButton({ icon, label, disabled, onClick }: { icon: ReactNode; label: string; disabled?: boolean; onClick: () => void }) {
  return (
    <button
      className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-strong hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20 disabled:cursor-not-allowed disabled:border-line disabled:text-muted/50"
      type="button"
      disabled={disabled}
      onClick={onClick}
    >
      {icon}
      {label}
    </button>
  );
}

function IconButton({ icon, label, danger, disabled, onClick }: { icon: ReactNode; label: string; danger?: boolean; disabled?: boolean; onClick: () => void }) {
  return (
    <button
      className={`grid h-9 w-9 place-items-center rounded-md border bg-panel transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed ${danger ? "border-risk/25 text-risk hover:border-risk/40 hover:bg-riskSoft focus:ring-risk/10 disabled:border-risk/10 disabled:text-risk/30" : "border-line text-graphite hover:border-strong hover:bg-soft hover:text-ink focus:ring-signal/20 disabled:border-line disabled:text-muted/50"}`}
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

function StatusBadge({ status }: { status: StrategySummary["status"] }) {
  const className =
    status === "active"
      ? "border-brand/30 bg-gainSoft text-brand"
      : status === "deleted"
        ? "border-risk/30 bg-riskSoft text-risk"
        : "border-line bg-soft text-muted";
  return <span className={`inline-flex rounded border px-2 py-0.5 font-mono text-[10px] ${className}`}>{status}</span>;
}

function Feedback({ tone, text }: { tone: "error" | "success"; text: string }) {
  const isError = tone === "error";
  return (
    <div className={`flex items-start gap-3 rounded-md border px-3 py-2 text-xs ${isError ? "border-risk/30 bg-riskSoft text-risk" : "border-brand/30 bg-gainSoft text-brand"}`}>
      {isError ? <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-risk" /> : <Check className="mt-0.5 h-4 w-4 shrink-0 text-brand" />}
      <span className="min-w-0 break-words">{text}</span>
    </div>
  );
}

function Notice({ text }: { text: string }) {
  return <div className="rounded-md border border-dashed border-line bg-panel px-3 py-3 text-xs text-muted">{text}</div>;
}

function StatusText({ status }: { status: StrategyBacktestRecord["status"] }) {
  const className =
    status === "succeeded"
      ? "text-brand"
      : status === "failed"
        ? "text-risk"
        : status === "running"
          ? "text-brandBlue"
          : "text-muted";
  return <span className={`font-mono text-[11px] font-semibold ${className}`}>{status}</span>;
}

function MetricBox({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-soft p-3">
      <div className="text-[11px] font-semibold text-muted">{label}</div>
      <div className="mt-1 truncate font-mono text-sm font-semibold text-ink">{value}</div>
    </div>
  );
}

function InfoLine({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid grid-cols-[80px_minmax(0,1fr)] gap-2">
      <span className="text-muted">{label}</span>
      <span className="min-w-0 break-words font-mono text-graphite">{value}</span>
    </div>
  );
}

function toNumber(value: string | number | null | undefined): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function roundNumber(value: number, digits: number): number {
  return Number(value.toFixed(digits));
}

function formatSigned(value: number): string {
  return `${value >= 0 ? "+" : ""}${value.toFixed(2)}`;
}

function formatMoney(value: string | number | null | undefined): string {
  return toNumber(value).toLocaleString("zh-CN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2,
  });
}

function formatTooltipDate(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat("zh-CN", {
    weekday: "short",
    month: "short",
    day: "numeric",
  }).format(date);
}

function formatTradeTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value.slice(11, 19) || "-";
  }
  return new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function normalizeSelectOption(option: SelectOption): { value: string; label: string } {
  return typeof option === "string" ? { value: option, label: option } : option;
}

function strategyModeLabel(mode: StrategyMode): string {
  return (
    strategyModeOptions
      .map(normalizeSelectOption)
      .find((option) => option.value === mode)?.label ?? mode
  );
}

function newStrategyForm(name = "均线突破策略"): StrategyForm {
  return {
    name,
    description: "短期均线上穿长期均线买入，下穿卖出",
    tags: "",
    strategyMode: "single_symbol",
    code: defaultCode,
    riskNote: "历史回测不代表未来收益，不构成投资建议",
  };
}

function newBacktestForm(
  params: StrategyCustomParameter[],
  strategyMode: StrategyMode = "single_symbol",
): BacktestForm {
  const defaultDateRange = defaultBacktestDateRange();
  const benchmarkSymbol = defaultBenchmarkFor("CN");
  const form: BacktestForm = {
    strategyMode,
    assetClass: "stock",
    market: "CN",
    symbols: strategyMode === "single_symbol" ? "600519.SH" : "600519.SH, 000001.SZ",
    universe: "",
    benchmarkPreset: benchmarkSymbol,
    benchmarkSymbol,
    startDate: defaultDateRange.startDate,
    endDate: defaultDateRange.endDate,
    initialCash: "100000",
    commission: "0.0005",
    slippage: "0.0002",
    notes: "",
    customParamValues: Object.fromEntries(
      params.map((param) => [param.name_en, String(param.default)]),
    ),
  };
  if (strategyMode === "universe_selection") {
    form.universe = "沪深300";
  }
  return form;
}

function defaultBacktestDateRange(): { startDate: string; endDate: string } {
  return backtestDateRangeForYears(1);
}

function backtestDateRangeForYears(years: number): { startDate: string; endDate: string } {
  const end = new Date();
  const start = new Date(end);
  const endMonth = end.getMonth();
  start.setFullYear(end.getFullYear() - years);
  if (start.getMonth() !== endMonth) {
    start.setDate(0);
  }
  return {
    startDate: formatDateInput(start),
    endDate: formatDateInput(end),
  };
}

function formatDateInput(value: Date): string {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function applyBacktestFieldUpdate<Key extends keyof BacktestForm>(
  form: BacktestForm,
  field: Key,
  value: BacktestForm[Key],
): BacktestForm {
  const next = { ...form, [field]: value };

  if (field === "strategyMode") {
    const strategyMode = value as BacktestForm["strategyMode"];
    if (strategyMode === "single_symbol") {
      next.symbols = splitList(form.symbols).at(0) ?? form.symbols;
    }
    if (strategyMode === "universe_selection" && !form.universe.trim()) {
      next.universe = "沪深300";
    }
  }

  if (field === "market") {
    const market = value as BacktestForm["market"];
    if (market !== "CN") {
      next.assetClass = "stock";
    }
    if (isDefaultBacktestSymbol(form.symbols)) {
      next.symbols = defaultSymbolFor(market, next.assetClass);
    }
    if (form.benchmarkPreset !== customBenchmarkValue) {
      const benchmarkSymbol = defaultBenchmarkFor(market);
      next.benchmarkPreset = benchmarkSymbol;
      next.benchmarkSymbol = benchmarkSymbol;
    }
  }

  if (field === "benchmarkPreset") {
    const benchmarkPreset = value as string;
    if (benchmarkPreset !== customBenchmarkValue) {
      next.benchmarkSymbol = benchmarkPreset;
    } else if (isDefaultBenchmarkSymbol(form.benchmarkSymbol)) {
      next.benchmarkSymbol = "";
    }
  }

  if (field === "assetClass") {
    const assetClass = value as BacktestForm["assetClass"];
    if (assetClass !== "stock") {
      next.market = "CN";
    }
    if (isDefaultBacktestSymbol(form.symbols)) {
      next.symbols = defaultSymbolFor(next.market, assetClass);
    }
  }

  return next;
}

function assetClassOptionsForMarket(market: BacktestForm["market"]): SelectOption[] {
  return market === "CN" ? cnAssetClassOptions : stockOnlyAssetClassOptions;
}

function benchmarkOptionsForMarket(market: BacktestForm["market"]): SelectOption[] {
  return benchmarkOptionsByMarket[market];
}

function symbolInputLabel(strategyMode: BacktestForm["strategyMode"]): string {
  if (strategyMode === "single_symbol") {
    return "股票代码";
  }
  if (strategyMode === "portfolio") {
    return "组合标的";
  }
  if (strategyMode === "universe_selection") {
    return "已解析标的";
  }
  return "标的列表";
}

function defaultSymbolFor(
  market: BacktestForm["market"],
  assetClass: BacktestForm["assetClass"],
): string {
  if (market === "HK") {
    return "00700.HK";
  }
  if (market === "US") {
    return "105.MSFT";
  }
  if (assetClass === "index") {
    return "000300.SH";
  }
  if (assetClass === "etf") {
    return "510300.SH";
  }
  return "600519.SH";
}

function defaultBenchmarkFor(market: BacktestForm["market"]): string {
  if (market === "HK") {
    return "HSI.HK";
  }
  if (market === "US") {
    return "SPX.US";
  }
  return "000016.SH";
}

function isDefaultBacktestSymbol(value: string): boolean {
  return ["600519.SH", "000300.SH", "510300.SH", "00700.HK", "105.MSFT"].includes(
    value.trim().toUpperCase(),
  );
}

function isDefaultBenchmarkSymbol(value: string): boolean {
  return Object.values(benchmarkOptionsByMarket)
    .flat()
    .map(normalizeSelectOption)
    .some((option) => option.value !== customBenchmarkValue && option.value === value.trim().toUpperCase());
}

function versionToForm(version: StrategyVersion | null, name = "均线突破策略"): StrategyForm {
  return {
    ...newStrategyForm(name),
    code: version?.source_code ?? defaultCode,
    strategyMode: version?.strategy_mode ?? "single_symbol",
  };
}

function parseCustomParamValue(
  param: StrategyCustomParameter,
  rawValue: string,
): { ok: true; value: string | number | boolean } | { ok: false; message: string } {
  const value = rawValue.trim();
  if (!value && param.required) {
    return { ok: false, message: `${param.name_cn}不能为空` };
  }
  if (!value) {
    return { ok: true, value: param.default };
  }
  if (param.type === "integer") {
    const parsed = Number(value);
    return Number.isInteger(parsed)
      ? { ok: true, value: parsed }
      : { ok: false, message: `${param.name_en} 必须是整数` };
  }
  if (param.type === "number") {
    const parsed = Number(value);
    return Number.isFinite(parsed)
      ? { ok: true, value: parsed }
      : { ok: false, message: `${param.name_en} 必须是数字` };
  }
  if (param.type === "boolean") {
    if (value === "true" || value === "false") {
      return { ok: true, value: value === "true" };
    }
    return { ok: false, message: `${param.name_en} 必须是 true 或 false` };
  }
  return { ok: true, value };
}

function customParamDefaults(params: StrategyCustomParameter[]): Record<string, string | number | boolean> {
  return Object.fromEntries(params.map((param) => [param.name_en, param.default]));
}

function splitList(value: string): string[] {
  return value
    .split(/[,，\n]/)
    .map((item) => item.trim().toUpperCase())
    .filter(Boolean);
}

function isFinitePositiveNumber(value: string): boolean {
  const parsed = Number(value.trim());
  return Number.isFinite(parsed) && parsed > 0;
}

function isFiniteNonNegativeNumber(value: string): boolean {
  const parsed = Number(value.trim());
  return Number.isFinite(parsed) && parsed >= 0;
}

function buildCreatePayload(form: StrategyForm): { ok: true; value: StrategyCreatePayload } | { ok: false; message: string } {
  const base = buildVersionPayload(form);
  if (!base.ok) {
    return base;
  }
  const name = form.name.trim();
  if (!name) {
    return { ok: false, message: "策略名称不能为空" };
  }
  return {
    ok: true,
    value: {
      ...base.value,
      name,
      description: form.description.trim(),
    },
  };
}

function buildVersionPayload(form: StrategyForm): { ok: true; value: StrategyVersionCreatePayload } | { ok: false; message: string } {
  const code = form.code.trim();
  if (!code) {
    return { ok: false, message: "策略代码不能为空" };
  }
  return {
    ok: true,
    value: {
      source_code: code,
      strategy_mode: form.strategyMode,
      risk_notes: form.riskNote.split("\n").map((note) => note.trim()).filter(Boolean),
    },
  };
}

function hasVersionChanges(
  currentVersion: StrategyVersion | null,
  nextPayload: StrategyVersionCreatePayload,
): boolean {
  if (!currentVersion) {
    return true;
  }
  return (
    normalizeCode(currentVersion.source_code) !== normalizeCode(nextPayload.source_code) ||
    currentVersion.strategy_mode !== nextPayload.strategy_mode
  );
}

function buildBacktestConfig(
  form: BacktestForm,
  customParams: StrategyCustomParameter[],
): { ok: true; value: StrategyBacktestConfig } | { ok: false; message: string } {
  const requiredFields = [
    ["股票模式", form.strategyMode],
    ["市场", form.market],
    ["资产类别", form.assetClass],
    ["开始日期", form.startDate],
    ["结束日期", form.endDate],
    ["初始资金", form.initialCash],
    ["手续费", form.commission],
  ] as const;
  for (const [label, value] of requiredFields) {
    if (!String(value).trim()) {
      return { ok: false, message: `请填写${label}` };
    }
  }
  if (Number.isNaN(Date.parse(form.startDate)) || Number.isNaN(Date.parse(form.endDate))) {
    return { ok: false, message: "开始日期和结束日期格式不正确" };
  }
  if (new Date(form.startDate) >= new Date(form.endDate)) {
    return { ok: false, message: "开始日期必须早于结束日期" };
  }
  if (!isFinitePositiveNumber(form.initialCash)) {
    return { ok: false, message: "初始资金必须大于 0" };
  }
  if (!isFiniteNonNegativeNumber(form.commission)) {
    return { ok: false, message: "手续费不能小于 0" };
  }
  if (form.slippage.trim() && !isFiniteNonNegativeNumber(form.slippage)) {
    return { ok: false, message: "滑点不能小于 0" };
  }
  const symbols = splitList(form.symbols);
  if (symbols.length === 0) {
    return { ok: false, message: "请填写回测标的" };
  }
  if (form.strategyMode === "single_symbol" && symbols.length !== 1) {
    return { ok: false, message: "单股票模式只能填写一个标的" };
  }
  if ((form.strategyMode === "multi_symbol" || form.strategyMode === "portfolio") && symbols.length < 2) {
    return { ok: false, message: "多股票或组合模式至少填写两个标的" };
  }
  if (form.strategyMode === "universe_selection" && !form.universe.trim()) {
    return { ok: false, message: "请选择或填写股票池" };
  }
  if (form.benchmarkPreset === customBenchmarkValue && !form.benchmarkSymbol.trim()) {
    return { ok: false, message: "请填写其他基准代码" };
  }

  const params: Record<string, string | number | boolean> = {};
  for (const param of customParams) {
    const parsed = parseCustomParamValue(
      param,
      form.customParamValues[param.name_en] ?? String(param.default),
    );
    if (!parsed.ok) {
      return parsed;
    }
    params[param.name_en] = parsed.value;
  }

  return {
    ok: true,
    value: {
      strategy_mode: form.strategyMode,
      asset_class: form.assetClass,
      market: form.market,
      symbols,
      universe: form.strategyMode === "universe_selection" ? form.universe.trim() : null,
      benchmark_symbol: form.benchmarkSymbol.trim() || null,
      start_date: form.startDate,
      end_date: form.endDate,
      timeframe: "1d",
      initial_cash: form.initialCash,
      commission: form.commission,
      slippage: form.slippage.trim() || "0",
      notes: form.notes.split("\n").map((note) => note.trim()).filter(Boolean),
      params,
    },
  };
}

async function loadVersionBacktests(version: StrategyVersion): Promise<BacktestRecordView[]> {
  const backtests = await listStrategyBacktests(version.id);
  return backtests.map((backtest) => ({ backtest, version }));
}

async function loadStrategyBacktestRecords(versions: StrategyVersion[]): Promise<BacktestRecordView[]> {
  const recordGroups = await Promise.all(
    versions.map((version) => loadVersionBacktests(version)),
  );
  return recordGroups
    .flat()
    .sort((left, right) => right.backtest.created_at.localeCompare(left.backtest.created_at));
}

function summarizeVersionDiff(
  previousVersion: StrategyVersion | null,
  selectedVersion: StrategyVersion,
): { label: string; value: string }[] {
  if (!previousVersion) {
    return [
      { label: "比较对象", value: "初始版本" },
      { label: "策略模式", value: strategyModeLabel(selectedVersion.strategy_mode) },
      { label: "代码行数", value: `${selectedVersion.source_code.split("\n").length}` },
      { label: "参数", value: formatParams(customParamDefaults(selectedVersion.custom_params)) },
    ];
  }

  const previousLines = previousVersion.source_code.split("\n");
  const selectedLines = selectedVersion.source_code.split("\n");
  const changedLines = Math.abs(selectedLines.length - previousLines.length) + countChangedLines(previousLines, selectedLines);
  return [
    { label: "比较对象", value: `V${previousVersion.version} -> V${selectedVersion.version}` },
    {
      label: "策略模式",
      value:
        previousVersion.strategy_mode === selectedVersion.strategy_mode
          ? strategyModeLabel(selectedVersion.strategy_mode)
          : `${strategyModeLabel(previousVersion.strategy_mode)} -> ${strategyModeLabel(selectedVersion.strategy_mode)}`,
    },
    { label: "代码变化", value: changedLines === 0 ? "无明显行级变化" : `${changedLines} 行差异` },
    {
      label: "参数变化",
      value:
        stableJson(previousVersion.custom_params) === stableJson(selectedVersion.custom_params)
          ? "默认参数未变"
          : `${formatParams(customParamDefaults(previousVersion.custom_params))} -> ${formatParams(customParamDefaults(selectedVersion.custom_params))}`,
    },
  ];
}

function countChangedLines(previousLines: string[], selectedLines: string[]): number {
  const comparableLength = Math.min(previousLines.length, selectedLines.length);
  let changed = 0;
  for (let index = 0; index < comparableLength; index += 1) {
    if (previousLines[index] !== selectedLines[index]) {
      changed += 1;
    }
  }
  return changed;
}

function normalizeCode(value: string): string {
  return value.trim().replace(/\r\n/g, "\n");
}

function stableJson(value: unknown): string {
  if (Array.isArray(value)) {
    return `[${value.map(stableJson).join(",")}]`;
  }
  if (value && typeof value === "object") {
    return `{${Object.entries(value)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, item]) => `${JSON.stringify(key)}:${stableJson(item)}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

function formatParams(params: Record<string, string | number | boolean>): string {
  const entries = Object.entries(params);
  if (entries.length === 0) {
    return "-";
  }
  return entries.map(([key, value]) => `${key}=${String(value)}`).join(", ");
}

function parseTags(value: string): string[] {
  const tags: string[] = [];
  value
    .split(/[,，]/)
    .map((tag) => tag.trim())
    .filter(Boolean)
    .forEach((tag) => {
      if (!tags.includes(tag)) {
        tags.push(tag);
      }
    });
  return tags;
}

function dialogTitle(dialog: Exclude<DialogState, null>): string {
  if (dialog.kind === "create") {
    return "新建策略";
  }
  if (dialog.kind === "edit") {
    return "编辑策略";
  }
  return "发布新版本";
}

function dialogSubmitLabel(dialog: Exclude<DialogState, null>): string {
  if (dialog.kind === "create") {
    return "创建";
  }
  if (dialog.kind === "edit") {
    return "保存";
  }
  return "发布";
}

function formatDate(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}
