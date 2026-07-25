import {
  Copy,
  Download,
  Eye,
  FileCode2,
  PlayCircle,
  RefreshCw,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import {
  API_BASE_URL,
  buildDemoStrategyPackage,
  copyStrategySummary,
  createStrategy,
  getStrategyVersion,
  listStrategies,
  validateStrategyVersion,
  type BacktestDetail,
  type CodeArtifact,
  type ExecutionResult,
  type RuntimeHealth,
  type StrategyCopySummary,
  type StrategySummary,
  type StrategyVersion,
} from "../../shared/api";
import type { AssetLink, ChatSession, JsonValue } from "../../shared/api/types";

type InsightPanelProps = {
  session: ChatSession | null;
  assets: AssetLink[];
  artifact: CodeArtifact | null;
  health: RuntimeHealth | null;
  result: ExecutionResult | null;
  backtestDetail: BacktestDetail | null;
};

type LoadState = "loading" | "ready" | "empty" | "error";

const formatter = new Intl.DateTimeFormat("zh-CN", {
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});

const statusLabel: Record<StrategySummary["version_status"], string> = {
  draft: "草稿",
  validating: "校验中",
  validated: "已校验",
  invalid: "未通过",
  archived: "已归档",
};

function snapshotTitle(snapshot: JsonValue | null): string | null {
  if (snapshot && typeof snapshot === "object" && !Array.isArray(snapshot)) {
    const title = snapshot.title;
    return typeof title === "string" ? title : null;
  }
  return null;
}

export function InsightPanel({
  session,
  assets,
  artifact,
  health,
  result,
  backtestDetail,
}: InsightPanelProps) {
  return (
    <aside
      className="hidden min-h-0 overflow-auto border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      <div className="grid gap-4">
        {artifact ? (
          <ArtifactDetail artifact={artifact} />
        ) : result ? (
          <RuntimeDetail health={health} result={result} />
        ) : backtestDetail ? (
          <BacktestDetailCard detail={backtestDetail} />
        ) : (
          <SessionDetail assets={assets} session={session} />
        )}
        <StrategyAssetPanel />
      </div>
    </aside>
  );
}

function ArtifactDetail({ artifact }: { artifact: CodeArtifact }) {
  return (
    <div className="grid gap-3">
      <section className="rounded-lg border border-line bg-panel p-4">
        <div className="mb-3 flex items-start gap-3">
          <div className="grid size-9 shrink-0 place-items-center rounded-lg bg-brand/10 text-brand">
            <FileCode2 size={17} />
          </div>
          <div className="min-w-0">
            <div className="truncate text-sm font-semibold">{artifact.title}</div>
            <div className="mt-1 text-xs text-muted">
              {artifact.artifact_type} · v{artifact.version}
            </div>
          </div>
        </div>
        <dl className="grid gap-2 text-xs">
          <DetailRow label="状态" value={artifact.status} />
          <DetailRow label="会话" value={artifact.chat_session_id} />
          <DetailRow label="入口" value={artifact.entrypoint ?? "-"} />
          <DetailRow label="Checksum" value={artifact.checksum} />
          <DetailRow label="更新时间" value={formatter.format(new Date(artifact.updated_at))} />
        </dl>
      </section>

      <section className="rounded-lg border border-line bg-panel p-4">
        <div className="mb-3 text-sm font-semibold">文件清单</div>
        <div className="grid gap-2">
          {artifact.files.map((file) => (
            <div key={file.file_id} className="rounded-lg border border-line bg-soft p-3">
              <div className="min-w-0 text-xs font-semibold">
                <span className="break-all">{file.relative_path}</span>
              </div>
              <div className="mt-2 flex flex-wrap items-center gap-2 text-[11px] text-muted">
                <span>{file.file_role}</span>
                <span>{Math.ceil(file.size_bytes / 1024)} KB</span>
                {file.is_entrypoint ? <span>entrypoint</span> : null}
              </div>
              <div className="mt-3 flex items-center gap-2">
                {file.preview_url ? (
                  <a
                    className="grid size-8 place-items-center rounded-lg border border-line bg-panel text-muted hover:text-brand focus:outline-none focus:ring-2 focus:ring-brand/30"
                    href={`${API_BASE_URL}${file.preview_url}`}
                    target="_blank"
                    rel="noreferrer"
                    aria-label={`预览 ${file.relative_path}`}
                    title="预览"
                  >
                    <Eye size={15} />
                  </a>
                ) : null}
                <a
                  className="grid size-8 place-items-center rounded-lg border border-line bg-panel text-muted hover:text-brand focus:outline-none focus:ring-2 focus:ring-brand/30"
                  href={`${API_BASE_URL}${file.download_url}`}
                  aria-label={`下载 ${file.relative_path}`}
                  title="下载"
                >
                  <Download size={15} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function RuntimeDetail({ health, result }: { health: RuntimeHealth | null; result: ExecutionResult }) {
  return (
    <div className="grid gap-3">
      <DetailCard label="运行 ID" value={result.run_id} />
      <DetailCard label="Python" value={health?.python_version ?? result.python_version} />
      <DetailCard label="exit code" value={result.exit_code === null ? "-" : String(result.exit_code)} />
      <DetailCard label="输出目录" value={result.output_dir} />
    </div>
  );
}

function BacktestDetailCard({ detail }: { detail: BacktestDetail }) {
  const metrics = detail.result?.metrics;
  return (
    <div className="grid gap-3">
      <DetailCard label="回测 ID" value={detail.run.id} />
      <DetailCard label="状态" value={detail.run.status} />
      <DetailCard label="年化收益" value={metrics?.annual_return_pct ? `${metrics.annual_return_pct}%` : "-"} />
      <DetailCard label="最大回撤" value={metrics?.max_drawdown_pct ? `${metrics.max_drawdown_pct}%` : "-"} />
    </div>
  );
}

function SessionDetail({ session, assets }: { session: ChatSession | null; assets: AssetLink[] }) {
  return (
    <div className="grid gap-3">
      <section className="rounded-lg border border-line bg-soft p-4">
        <div className="text-xs font-semibold text-muted">当前会话</div>
        <div className="mt-2 truncate text-sm font-semibold">{session?.title ?? "未选择会话"}</div>
        <div className="mt-2 grid gap-1 text-xs text-muted">
          <div>SDK Session: {session?.sdk_session_id ?? "未建立"}</div>
          <div>策略版本: {session?.current_strategy_version_id ?? "无"}</div>
          <div>回测结果: {session?.current_backtest_run_id ?? "无"}</div>
        </div>
      </section>

      <section className="rounded-lg border border-line bg-soft p-4">
        <div className="text-xs font-semibold text-muted">关联资产</div>
        <div className="mt-3 grid gap-2">
          {assets.length === 0 ? (
            <div className="text-sm text-muted">暂无资产</div>
          ) : (
            assets.map((asset) => (
              <div className="rounded-lg border border-line bg-panel p-3" key={asset.id}>
                <div className="truncate text-sm font-medium">
                  {snapshotTitle(asset.display_snapshot) ?? asset.asset_id}
                </div>
                <div className="mt-1 text-xs text-muted">
                  {asset.asset_type} · {asset.relation_type}
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}

function StrategyAssetPanel() {
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
    <section className="rounded-lg border border-line bg-panel p-4">
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
        <div className="rounded-lg border border-dashed border-line bg-soft p-4">
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
        </div>
      ) : null}

      {state === "error" ? <PanelNotice text={actionError ?? "策略资产加载失败"} tone="risk" /> : null}

      {selectedStrategy && currentVersion ? (
        <div className="grid gap-3">
          <div className="rounded-lg border border-line bg-soft p-3">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <div className="truncate text-sm font-semibold">{selectedStrategy.name}</div>
                <div className="mt-2 flex flex-wrap gap-1">
                  <Pill text={`V${selectedStrategy.version}`} />
                  <Pill text={statusLabel[selectedStrategy.version_status]} />
                  <Pill text={selectedStrategy.strategy_type} />
                </div>
              </div>
              <ShieldCheck className="shrink-0 text-brand" size={18} />
            </div>
            <p className="mt-3 text-sm leading-6 text-muted">
              {currentVersion.logic_summary ?? selectedStrategy.logic_summary}
            </p>
          </div>

          <div className="grid gap-2">
            {params.slice(0, 3).map(({ key, schema, value }) => (
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
                  {schema.ui.unit ? <span className="ml-1 text-xs text-muted">{schema.ui.unit}</span> : null}
                </div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-2">
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

          {copyResult ? (
            <pre className="max-h-48 overflow-auto whitespace-pre-wrap break-words rounded-lg border border-line bg-soft p-3 text-xs leading-5 text-muted">
              {copyResult.summary}
            </pre>
          ) : null}
        </div>
      ) : null}

      {actionError && state !== "error" ? <PanelNotice text={actionError} tone="risk" /> : null}
    </section>
  );
}

function Pill({ text }: { text: string }) {
  return (
    <span className="rounded-full border border-line bg-panel px-2 py-0.5 text-xs text-muted">
      {text}
    </span>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1">
      <dt className="text-muted">{label}</dt>
      <dd className="break-all font-medium text-ink">{value}</dd>
    </div>
  );
}

function DetailCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-line bg-soft p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 truncate text-xs font-semibold">{value}</div>
    </div>
  );
}

function PanelNotice({ text, tone = "muted" }: { text: string; tone?: "muted" | "risk" }) {
  const toneClass = tone === "risk" ? "border-risk/40 text-risk" : "border-line text-muted";
  return <div className={`rounded-lg border bg-soft p-4 text-sm ${toneClass}`}>{text}</div>;
}
