import {
  BarChart3,
  Code2,
  ExternalLink,
  FileCode2,
  GitBranch,
  LineChart,
  Loader2,
} from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import type { PointerEvent as ReactPointerEvent, ReactNode } from "react";

import {
  getStrategy,
  getStrategyBacktest,
  getStrategyVersion,
  listStrategyVersions,
  type AssetLink,
  type ChatSession,
  type InspectorObject,
  type JsonValue,
  type StrategyBacktestDetail,
  type StrategyCurvePoint,
  type StrategyDetail,
  type StrategyVersion,
} from "../../shared/api";

type InsightPanelProps = {
  session: ChatSession | null;
  assets: AssetLink[];
  activeObject: InspectorObject | null;
  onOpenObject: (object: InspectorObject) => void;
};

type InspectorState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; message: string }
  | {
      status: "ready";
      object: InspectorObject;
      backtest?: StrategyBacktestDetail;
      strategy?: StrategyDetail;
      versions?: StrategyVersion[];
      version?: StrategyVersion;
    };

const minPanelWidth = 320;
const maxPanelWidth = 720;
const defaultPanelWidth = 392;

export function InsightPanel({
  session,
  assets,
  activeObject,
  onOpenObject,
}: InsightPanelProps) {
  const [panelWidth, setPanelWidth] = useState(() => storedPanelWidth());
  const [state, setState] = useState<InspectorState>({ status: "idle" });

  useEffect(() => {
    if (!activeObject) {
      setState({ status: "idle" });
      return;
    }

    let isCancelled = false;
    setState({ status: "loading" });

    loadInspectorObject(activeObject)
      .then((nextState) => {
        if (!isCancelled) {
          setState(nextState);
        }
      })
      .catch((caught) => {
        if (!isCancelled) {
          setState({
            status: "error",
            message: caught instanceof Error ? caught.message : "对象加载失败",
          });
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [activeObject]);

  const startResize = useCallback((event: ReactPointerEvent<HTMLDivElement>) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    const startX = event.clientX;
    const startWidth = panelWidth;

    const handleMove = (moveEvent: PointerEvent) => {
      const nextWidth = clampPanelWidth(startWidth + startX - moveEvent.clientX);
      setPanelWidth(nextWidth);
      window.localStorage.setItem("chatq.insight.width", String(nextWidth));
    };
    const handleUp = () => {
      window.removeEventListener("pointermove", handleMove);
      window.removeEventListener("pointerup", handleUp);
    };

    window.addEventListener("pointermove", handleMove);
    window.addEventListener("pointerup", handleUp);
  }, [panelWidth]);

  return (
    <aside
      className="glass-panel relative hidden shrink-0 overflow-auto border-l border-line px-4 py-5 xl:block"
      style={{ width: panelWidth }}
      aria-label="对象详情"
    >
      <div
        className="absolute left-0 top-0 h-full w-1 cursor-col-resize border-l border-transparent transition-colors hover:border-signal"
        role="separator"
        aria-orientation="vertical"
        onPointerDown={startResize}
      />
      <PanelHeader />
      {state.status === "idle" ? (
        <SessionAssets session={session} assets={assets} onOpenObject={onOpenObject} />
      ) : state.status === "loading" ? (
        <LoadingState />
      ) : state.status === "error" ? (
        <ErrorState message={state.message} />
      ) : (
        <ObjectDetail state={state} onOpenObject={onOpenObject} />
      )}
    </aside>
  );
}

async function loadInspectorObject(object: InspectorObject): Promise<InspectorState> {
  if (object.type === "backtest") {
    const backtest = await getStrategyBacktest(object.id);
    return { status: "ready", object, backtest };
  }
  if (object.type === "strategy") {
    const strategy = await getStrategy(object.id);
    const versions = await listStrategyVersions(object.id);
    return { status: "ready", object, strategy, versions };
  }
  const version = await getStrategyVersion(object.id);
  return { status: "ready", object, version };
}

function PanelHeader() {
  return (
    <div className="mb-4 flex items-center justify-between">
      <div>
        <div className="font-mono text-[10px] font-bold uppercase text-muted">Inspector</div>
        <div className="mt-1 text-sm font-semibold text-ink">对象详情</div>
      </div>
      <span className="rounded border border-brand/30 bg-gainSoft px-2 py-1 font-mono text-[10px] font-bold text-brand">
        READY
      </span>
    </div>
  );
}

function ObjectDetail({
  state,
  onOpenObject,
}: {
  state: Extract<InspectorState, { status: "ready" }>;
  onOpenObject: (object: InspectorObject) => void;
}) {
  if (state.backtest) {
    return <BacktestInspector detail={state.backtest} onOpenObject={onOpenObject} />;
  }
  if (state.strategy) {
    return (
      <StrategyInspector
        detail={state.strategy}
        versions={state.versions ?? []}
        onOpenObject={onOpenObject}
      />
    );
  }
  if (state.version) {
    return <StrategyVersionInspector version={state.version} onOpenObject={onOpenObject} />;
  }
  return <ErrorState message="对象类型暂不支持" />;
}

function BacktestInspector({
  detail,
  onOpenObject,
}: {
  detail: StrategyBacktestDetail;
  onOpenObject: (object: InspectorObject) => void;
}) {
  const metrics = detail.result?.metrics;
  const equityCurve = detail.result?.curves?.find((curve) => curve.curve_type === "equity");
  const drawdownCurve = detail.result?.curves?.find((curve) => curve.curve_type === "drawdown");
  const symbols = detail.backtest.config.symbols.join("、");

  return (
    <div className="grid gap-3">
      <ObjectTitle
        icon={<BarChart3 className="h-4 w-4" />}
        eyebrow="回测结果"
        title={symbols || detail.backtest.id}
        subtitle={`${detail.backtest.config.start_date} 至 ${detail.backtest.config.end_date}`}
      />
      <div className="grid grid-cols-2 gap-2">
        <Metric label="总收益" value={formatPercent(metrics?.total_return_pct)} tone="gain" />
        <Metric label="最大回撤" value={formatPercent(metrics?.max_drawdown_pct)} tone="risk" />
        <Metric label="年化收益" value={formatPercent(metrics?.annual_return_pct)} />
        <Metric label="交易次数" value={String(metrics?.total_trades ?? 0)} />
      </div>
      {equityCurve ? (
        <CurveCard title="收益曲线" points={equityCurve.points} valueKey="normalized_value" tone="gain" />
      ) : null}
      {drawdownCurve ? (
        <CurveCard title="回撤曲线" points={drawdownCurve.points} valueKey="value" tone="risk" />
      ) : null}
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 text-xs font-semibold text-muted">关联对象</div>
        <div className="grid gap-2">
          <InlineOpenButton
            label="打开策略"
            onClick={() => onOpenObject({ type: "strategy", id: detail.backtest.strategy_id })}
          />
          <InlineOpenButton
            label="查看策略版本"
            onClick={() =>
              onOpenObject({ type: "strategy-version", id: detail.backtest.strategy_version_id })
            }
          />
        </div>
      </section>
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 flex items-center justify-between">
          <div className="text-xs font-semibold text-muted">交易明细</div>
          <div className="font-mono text-[10px] text-muted">{detail.result?.trades?.length ?? 0}</div>
        </div>
        <div className="grid gap-1 text-xs">
          {(detail.result?.trades ?? []).slice(0, 6).map((trade) => (
            <div className="grid grid-cols-[1fr_auto_auto] gap-2 border-t border-line py-2 first:border-t-0" key={trade.id}>
              <span className="truncate font-medium">{trade.symbol}</span>
              <span className={trade.side === "buy" ? "text-brand" : "text-risk"}>
                {trade.side === "buy" ? "买入" : "卖出"}
              </span>
              <span className="font-mono">{formatNumber(trade.price)}</span>
            </div>
          ))}
          {(detail.result?.trades ?? []).length === 0 ? <span className="text-muted">暂无交易</span> : null}
        </div>
      </section>
    </div>
  );
}

function StrategyInspector({
  detail,
  versions,
  onOpenObject,
}: {
  detail: StrategyDetail;
  versions: StrategyVersion[];
  onOpenObject: (object: InspectorObject) => void;
}) {
  const strategy = detail.strategy;
  const currentVersion = versions.find((version) => version.id === strategy.current_version_id);
  return (
    <div className="grid gap-3">
      <ObjectTitle
        icon={<FileCode2 className="h-4 w-4" />}
        eyebrow="策略"
        title={strategy.name}
        subtitle={strategy.description ?? strategy.id}
      />
      <div className="grid grid-cols-2 gap-2">
        <Metric label="状态" value={strategy.status} />
        <Metric label="版本数" value={String(versions.length)} />
      </div>
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 text-xs font-semibold text-muted">标签</div>
        <div className="flex flex-wrap gap-1.5">
          {strategy.tags.length > 0 ? (
            strategy.tags.map((tag) => (
              <span className="rounded border border-line bg-soft px-2 py-1 text-xs" key={tag}>
                {tag}
              </span>
            ))
          ) : (
            <span className="text-xs text-muted">暂无标签</span>
          )}
        </div>
      </section>
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 text-xs font-semibold text-muted">策略版本</div>
        <div className="grid gap-2">
          {versions.map((version) => (
            <button
              className="flex items-center justify-between rounded border border-line bg-soft px-3 py-2 text-left text-xs transition-colors hover:border-signal hover:bg-panel"
              key={version.id}
              type="button"
              onClick={() => onOpenObject({ type: "strategy-version", id: version.id })}
            >
              <span className="font-semibold">V{version.version}</span>
              <span className="truncate font-mono text-[10px] text-muted">
                {version.id === currentVersion?.id ? "当前版本" : version.id}
              </span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function StrategyVersionInspector({
  version,
  onOpenObject,
}: {
  version: StrategyVersion;
  onOpenObject: (object: InspectorObject) => void;
}) {
  return (
    <div className="grid gap-3">
      <ObjectTitle
        icon={<GitBranch className="h-4 w-4" />}
        eyebrow="策略版本"
        title={`V${version.version}`}
        subtitle={version.id}
      />
      <div className="grid grid-cols-2 gap-2">
        <Metric label="模式" value={version.strategy_mode} />
        <Metric label="参数数" value={String(version.custom_params.length)} />
      </div>
      <InlineOpenButton
        label="打开所属策略"
        onClick={() => onOpenObject({ type: "strategy", id: version.strategy_id })}
      />
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 text-xs font-semibold text-muted">参数</div>
        <div className="grid gap-1 text-xs">
          {version.custom_params.length > 0 ? (
            version.custom_params.map((param) => (
              <div className="grid grid-cols-[1fr_auto] gap-2 border-t border-line py-2 first:border-t-0" key={param.name_en}>
                <span className="truncate font-medium">{param.name_cn || param.name_en}</span>
                <span className="font-mono text-muted">{String(param.default)}</span>
              </div>
            ))
          ) : (
            <span className="text-muted">无自定义参数</span>
          )}
        </div>
      </section>
      <section className="rounded-md border border-line bg-panel p-3">
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-muted">
          <Code2 className="h-3.5 w-3.5" />
          源码
        </div>
        <pre className="max-h-80 overflow-auto rounded border border-line bg-soft p-3 text-[11px] leading-5 text-graphite">
          {version.source_code}
        </pre>
      </section>
    </div>
  );
}

function SessionAssets({
  session,
  assets,
  onOpenObject,
}: {
  session: ChatSession | null;
  assets: AssetLink[];
  onOpenObject: (object: InspectorObject) => void;
}) {
  return (
    <div className="grid gap-3">
      <section className="rounded-md border border-line bg-panel p-4">
        <div className="text-xs font-semibold text-muted">当前会话</div>
        <div className="mt-2 truncate text-sm font-semibold text-ink">
          {session?.title ?? "未选择会话"}
        </div>
        <div className="mt-2 grid gap-1 text-xs text-muted">
          <div>策略版本: {session?.current_strategy_version_id ?? "无"}</div>
          <div>回测结果: {session?.current_backtest_run_id ?? "无"}</div>
        </div>
      </section>
      <section className="rounded-md border border-line bg-panel p-4">
        <div className="text-xs font-semibold text-muted">关联对象</div>
        <div className="mt-3 grid gap-2">
          {assets.length === 0 ? (
            <div className="text-sm text-muted">暂无对象</div>
          ) : (
            assets.map((asset) => {
              const object = objectFromAsset(asset);
              return (
                <button
                  className="rounded-md border border-l-[3px] border-line border-l-brandBlue bg-compareSoft p-3 text-left transition-colors hover:border-signal hover:bg-panel"
                  disabled={!object}
                  key={asset.id}
                  type="button"
                  onClick={() => object && onOpenObject(object)}
                >
                  <div className="truncate text-sm font-medium text-ink">
                    {snapshotTitle(asset.display_snapshot) ?? asset.asset_id}
                  </div>
                  <div className="mt-1 text-xs text-muted">
                    {asset.asset_type} · {asset.relation_type}
                  </div>
                </button>
              );
            })
          )}
        </div>
      </section>
    </div>
  );
}

function ObjectTitle({
  icon,
  eyebrow,
  title,
  subtitle,
}: {
  icon: ReactNode;
  eyebrow: string;
  title: string;
  subtitle: string;
}) {
  return (
    <section className="rounded-md border border-line bg-panel p-4">
      <div className="mb-3 inline-flex items-center text-brandBlue">{icon}</div>
      <div className="text-xs font-semibold text-muted">{eyebrow}</div>
      <h2 className="mt-1 break-words text-base font-semibold text-ink">{title}</h2>
      <div className="mt-1 break-all font-mono text-[11px] text-muted">{subtitle}</div>
    </section>
  );
}

function Metric({
  label,
  value,
  tone = "neutral",
}: {
  label: string;
  value: string;
  tone?: "gain" | "risk" | "neutral";
}) {
  const toneClass =
    tone === "gain" ? "text-brand" : tone === "risk" ? "text-risk" : "text-ink";
  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className={`mt-1 truncate font-mono text-sm font-semibold ${toneClass}`}>{value}</div>
    </div>
  );
}

function CurveCard({
  title,
  points,
  valueKey,
  tone,
}: {
  title: string;
  points: StrategyCurvePoint[];
  valueKey: "value" | "normalized_value";
  tone: "gain" | "risk";
}) {
  return (
    <section className="rounded-md border border-line bg-panel p-3">
      <div className="mb-3 flex items-center gap-2 text-xs font-semibold text-muted">
        <LineChart className="h-3.5 w-3.5" />
        {title}
      </div>
      <svg className="h-32 w-full overflow-visible" viewBox="0 0 280 104" role="img" aria-label={title}>
        <path d="M0 88H280" className="stroke-line" strokeWidth="1" />
        <path d="M0 52H280" className="stroke-line" strokeWidth="1" />
        <path d="M0 16H280" className="stroke-line" strokeWidth="1" />
        <polyline
          fill="none"
          points={toPolyline(points, valueKey)}
          className={tone === "gain" ? "stroke-brand" : "stroke-risk"}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2.5"
        />
      </svg>
    </section>
  );
}

function InlineOpenButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      className="inline-flex items-center justify-between rounded-md border border-line bg-panel px-3 py-2 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink"
      type="button"
      onClick={onClick}
    >
      {label}
      <ExternalLink className="h-3.5 w-3.5" />
    </button>
  );
}

function LoadingState() {
  return (
    <div className="flex items-center gap-2 rounded-md border border-line bg-panel p-4 text-sm text-muted">
      <Loader2 className="h-4 w-4 animate-spin" />
      加载对象
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-risk/30 bg-riskSoft p-4 text-sm text-risk">
      {message}
    </div>
  );
}

function objectFromAsset(asset: AssetLink): InspectorObject | null {
  if (asset.asset_type === "backtest_run") {
    return { type: "backtest", id: asset.asset_id };
  }
  if (asset.asset_type === "strategy") {
    return { type: "strategy", id: asset.asset_id };
  }
  if (asset.asset_type === "strategy_version") {
    return { type: "strategy-version", id: asset.asset_id };
  }
  return null;
}

function snapshotTitle(snapshot: JsonValue | null): string | null {
  if (snapshot && typeof snapshot === "object" && !Array.isArray(snapshot)) {
    const title = snapshot.title;
    return typeof title === "string" ? title : null;
  }
  return null;
}

function toPolyline(points: StrategyCurvePoint[], valueKey: "value" | "normalized_value") {
  const values = points
    .map((point) => Number(point[valueKey] ?? point.value))
    .filter((value) => Number.isFinite(value));
  if (values.length === 0) {
    return "";
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(1, max - min);
  const lastIndex = Math.max(1, values.length - 1);
  return values
    .map((value, index) => {
      const x = (index / lastIndex) * 280;
      const y = 92 - ((value - min) / span) * 80;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

function formatPercent(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return `${Number(value).toFixed(2)}%`;
}

function formatNumber(value: string | null | undefined) {
  if (value == null) {
    return "--";
  }
  return Number(value).toLocaleString("zh-CN", { maximumFractionDigits: 2 });
}

function storedPanelWidth() {
  const stored = Number(window.localStorage.getItem("chatq.insight.width"));
  return clampPanelWidth(Number.isFinite(stored) && stored > 0 ? stored : defaultPanelWidth);
}

function clampPanelWidth(value: number) {
  return Math.min(maxPanelWidth, Math.max(minPanelWidth, value));
}
