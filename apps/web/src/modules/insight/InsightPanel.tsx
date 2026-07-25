import { Copy, PlayCircle, RefreshCw, ShieldCheck, Sparkles } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import {
  buildDemoStrategyPackage,
  copyStrategySummary,
  createStrategy,
  getStrategyVersion,
  listStrategies,
  validateStrategyVersion,
  type StrategyCopySummary,
  type StrategySummary,
  type StrategyVersion,
} from "../../shared/api";

type LoadState = "loading" | "ready" | "empty" | "error";

const statusLabel: Record<StrategySummary["version_status"], string> = {
  draft: "草稿",
  validating: "校验中",
  validated: "已校验",
  invalid: "未通过",
  archived: "已归档",
};

export function InsightPanel() {
  const [state, setState] = useState<LoadState>("loading");
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [currentVersion, setCurrentVersion] = useState<StrategyVersion | null>(null);
  const [copyResult, setCopyResult] = useState<StrategyCopySummary | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [isWorking, setIsWorking] = useState(false);

  const selectedStrategy = strategies[0] ?? null;
  const params = useMemo(() => {
    if (!currentVersion) {
      return [];
    }
    return Object.entries(currentVersion.params_schema).map(([key, schema]) => ({
      key,
      schema,
      value: currentVersion.default_params[key],
    }));
  }, [currentVersion]);

  useEffect(() => {
    void refreshStrategies();
  }, []);

  async function refreshStrategies() {
    try {
      setState("loading");
      setActionError(null);
      const items = await listStrategies();
      setStrategies(items);
      setCopyResult(null);
      if (items.length === 0) {
        setCurrentVersion(null);
        setState("empty");
        return;
      }

      const version = await getStrategyVersion(items[0].strategy_version_id);
      setCurrentVersion(version);
      setState("ready");
    } catch (error) {
      setState("error");
      setActionError(error instanceof Error ? error.message : "策略资产加载失败");
    }
  }

  async function handleCreateDemoStrategy() {
    try {
      setIsWorking(true);
      setActionError(null);
      await createStrategy("conv_demo_strategy", buildDemoStrategyPackage());
      await refreshStrategies();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "策略创建失败");
    } finally {
      setIsWorking(false);
    }
  }

  async function handleValidateVersion() {
    if (!selectedStrategy) {
      return;
    }
    try {
      setIsWorking(true);
      setActionError(null);
      await validateStrategyVersion(selectedStrategy.strategy_version_id);
      await refreshStrategies();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "策略校验失败");
    } finally {
      setIsWorking(false);
    }
  }

  async function handleCopySummary() {
    if (!selectedStrategy) {
      return;
    }
    try {
      setIsWorking(true);
      setActionError(null);
      const result = await copyStrategySummary(selectedStrategy.strategy_version_id);
      setCopyResult(result);
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "复制摘要失败");
    } finally {
      setIsWorking(false);
    }
  }

  return (
    <aside
      className="hidden min-h-0 overflow-auto border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <div className="text-sm font-semibold">策略资产</div>
          <div className="mt-1 text-xs text-muted">M5 StrategyVersion</div>
        </div>
        <button
          className="grid size-9 place-items-center rounded-lg border border-line bg-soft text-ink transition hover:border-strong hover:bg-panel disabled:cursor-not-allowed disabled:opacity-50"
          type="button"
          aria-label="刷新策略资产"
          onClick={refreshStrategies}
          disabled={isWorking}
        >
          <RefreshCw size={16} />
        </button>
      </div>

      {state === "loading" ? <PanelNotice text="正在读取策略资产" /> : null}

      {state === "empty" ? (
        <section className="rounded-lg border border-dashed border-line bg-soft p-4">
          <div className="flex items-start gap-3">
            <div className="grid size-9 shrink-0 place-items-center rounded-lg bg-brand text-white">
              <Sparkles size={16} />
            </div>
            <div className="min-w-0">
              <div className="text-sm font-semibold">暂无策略资产</div>
              <button
                className="mt-3 inline-flex h-9 items-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white transition hover:bg-brand disabled:cursor-not-allowed disabled:opacity-50"
                type="button"
                onClick={handleCreateDemoStrategy}
                disabled={isWorking}
              >
                <PlayCircle size={16} />
                生成示例策略
              </button>
            </div>
          </div>
        </section>
      ) : null}

      {state === "error" ? <PanelNotice text={actionError ?? "策略资产加载失败"} tone="risk" /> : null}

      {selectedStrategy && currentVersion ? (
        <div className="grid gap-4">
          <section className="rounded-lg border border-line bg-panel p-4 shadow-panel">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <h2 className="truncate text-base font-semibold">{selectedStrategy.name}</h2>
                <div className="mt-2 flex flex-wrap gap-2">
                  <Pill text={`V${selectedStrategy.version}`} />
                  <Pill text={statusLabel[selectedStrategy.version_status]} />
                  <Pill text={selectedStrategy.strategy_type} />
                </div>
              </div>
              <ShieldCheck className="shrink-0 text-brand" size={20} />
            </div>
            <p className="mt-3 text-sm leading-6 text-muted">
              {currentVersion.logic_summary ?? selectedStrategy.logic_summary}
            </p>
          </section>

          <section className="rounded-lg border border-line bg-panel p-4">
            <div className="mb-3 text-sm font-semibold">参数快照</div>
            <div className="grid gap-2">
              {params.map(({ key, schema, value }) => (
                <div
                  className="grid min-h-12 grid-cols-[minmax(0,1fr)_auto] items-center gap-3 rounded-lg border border-line bg-soft px-3 py-2"
                  key={key}
                >
                  <div className="min-w-0">
                    <div className="truncate text-sm font-medium">{schema.title}</div>
                    <div className="truncate text-xs text-muted">{key}</div>
                  </div>
                  <div className="max-w-28 truncate text-right text-sm font-semibold text-ink">
                    {String(value)}
                    {schema.ui.unit ? (
                      <span className="ml-1 text-xs text-muted">{schema.ui.unit}</span>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-panel p-4">
            <div className="mb-3 text-sm font-semibold">版本入口</div>
            <div className="grid gap-2 text-sm">
              <InfoRow label="入口类" value={currentVersion.entrypoint} />
              <InfoRow label="代码产物" value={currentVersion.code_artifact_id} />
              <InfoRow label="校验时间" value={currentVersion.validated_at ?? "未校验"} />
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2">
              <button
                className="inline-flex h-9 items-center justify-center gap-2 rounded-lg bg-brand px-3 text-sm font-semibold text-white transition hover:bg-ink disabled:cursor-not-allowed disabled:opacity-50"
                type="button"
                onClick={handleValidateVersion}
                disabled={isWorking}
              >
                <ShieldCheck size={15} />
                校验
              </button>
              <button
                className="inline-flex h-9 items-center justify-center gap-2 rounded-lg border border-line bg-soft px-3 text-sm font-semibold text-ink transition hover:border-strong hover:bg-panel disabled:cursor-not-allowed disabled:opacity-50"
                type="button"
                onClick={handleCopySummary}
                disabled={isWorking}
              >
                <Copy size={15} />
                摘要
              </button>
            </div>
          </section>

          {copyResult ? (
            <section className="rounded-lg border border-line bg-soft p-4">
              <div className="mb-2 text-sm font-semibold">复制摘要</div>
              <pre className="max-h-48 overflow-auto whitespace-pre-wrap break-words text-xs leading-5 text-muted">
                {copyResult.summary}
              </pre>
            </section>
          ) : null}
        </div>
      ) : null}

      {actionError && state !== "error" ? <PanelNotice text={actionError} tone="risk" /> : null}
    </aside>
  );
}

function Pill({ text }: { text: string }) {
  return (
    <span className="rounded-full border border-line bg-soft px-2.5 py-1 text-xs text-muted">
      {text}
    </span>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid grid-cols-[72px_minmax(0,1fr)] gap-2">
      <span className="text-muted">{label}</span>
      <span className="truncate font-medium">{value}</span>
    </div>
  );
}

function PanelNotice({ text, tone = "muted" }: { text: string; tone?: "muted" | "risk" }) {
  const toneClass = tone === "risk" ? "border-risk/40 text-risk" : "border-line text-muted";
  return <div className={`rounded-lg border bg-soft p-4 text-sm ${toneClass}`}>{text}</div>;
}
