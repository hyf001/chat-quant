import { AlertCircle, FileCode2, RefreshCw, Tag } from "lucide-react";
import { useEffect, useState } from "react";

import { listStrategies, type Project, type StrategyParamValue, type StrategySummary } from "../../shared/api";

type StrategyListProps = {
  project: Project | null;
};

export function StrategyList({ project }: StrategyListProps) {
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadStrategies = async () => {
    if (!project) {
      setStrategies([]);
      setError(null);
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const data = await listStrategies(project.id);
      setStrategies(data);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "策略列表加载失败");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadStrategies();
  }, [project?.id]);

  return (
    <section className="mx-auto w-full max-w-5xl" aria-label="策略列表">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="font-mono text-[10px] font-bold uppercase tracking-wider text-zinc-400">
            Strategies
          </div>
          <h1 className="mt-1 truncate text-xl font-semibold text-zinc-900">策略</h1>
          <p className="mt-1 truncate text-xs text-zinc-500">
            当前项目：{project?.name ?? "未选择项目"}
          </p>
        </div>
        <button
          className="grid h-9 w-9 shrink-0 place-items-center rounded-md border border-zinc-300 bg-white text-zinc-600 transition-colors hover:border-zinc-400 hover:bg-zinc-50 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20 disabled:cursor-not-allowed disabled:border-zinc-200 disabled:text-zinc-300"
          type="button"
          aria-label="刷新策略列表"
          title="刷新"
          disabled={!project || isLoading}
          onClick={() => void loadStrategies()}
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {!project ? <Notice text="请先创建或选择项目" /> : null}
      {project && error ? <ErrorNotice message={error} /> : null}
      {project && isLoading ? <Notice text="策略加载中" /> : null}
      {project && !isLoading && !error && strategies.length === 0 ? (
        <Notice text="当前项目暂无策略" />
      ) : null}

      {strategies.length > 0 ? (
        <div className="overflow-hidden rounded-md border border-zinc-200 bg-white">
          <div className="grid grid-cols-[minmax(0,1.4fr)_120px_120px_minmax(0,1fr)_140px] gap-3 border-b border-zinc-200 bg-zinc-50 px-4 py-2.5 text-[10px] font-bold uppercase tracking-wider text-zinc-500">
            <span>策略</span>
            <span>版本</span>
            <span>状态</span>
            <span>参数</span>
            <span>更新</span>
          </div>
          <div className="divide-y divide-zinc-100">
            {strategies.map((strategy) => (
              <article
                className="grid grid-cols-[minmax(0,1.4fr)_120px_120px_minmax(0,1fr)_140px] gap-3 px-4 py-3 text-xs transition-colors hover:bg-zinc-50"
                key={strategy.strategy_version_id}
              >
                <div className="min-w-0">
                  <div className="flex min-w-0 items-center gap-2">
                    <FileCode2 className="h-4 w-4 shrink-0 text-zinc-500" />
                    <span className="truncate font-semibold text-zinc-900">{strategy.name}</span>
                  </div>
                  <div className="mt-1 flex min-w-0 flex-wrap items-center gap-1.5">
                    {strategy.tags.slice(0, 3).map((tag) => (
                      <span
                        className="inline-flex max-w-28 items-center gap-1 rounded bg-zinc-100 px-1.5 py-0.5 text-[10px] text-zinc-600"
                        key={tag}
                      >
                        <Tag className="h-2.5 w-2.5 shrink-0" />
                        <span className="truncate">{tag}</span>
                      </span>
                    ))}
                  </div>
                </div>
                <span className="font-mono text-xs text-zinc-600">V{strategy.version}</span>
                <div>
                  <StatusBadge status={strategy.status} />
                </div>
                <span className="min-w-0 truncate font-mono text-[11px] text-zinc-500">
                  {formatParams(strategy.default_params)}
                </span>
                <span className="font-mono text-[11px] text-zinc-500">
                  {formatDate(strategy.updated_at)}
                </span>
              </article>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}

function StatusBadge({ status }: { status: StrategySummary["status"] }) {
  const className =
    status === "active"
      ? "border-emerald-200 bg-emerald-50 text-emerald-700"
      : status === "deleted"
        ? "border-red-200 bg-red-50 text-red-700"
        : "border-zinc-200 bg-zinc-50 text-zinc-600";

  return (
    <span className={`inline-flex rounded border px-2 py-0.5 font-mono text-[10px] ${className}`}>
      {status}
    </span>
  );
}

function ErrorNotice({ message }: { message: string }) {
  return (
    <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-800">
      <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-600" />
      <span className="min-w-0 break-words">{message}</span>
    </div>
  );
}

function Notice({ text }: { text: string }) {
  return (
    <div className="rounded-md border border-dashed border-zinc-300 bg-zinc-50 px-3 py-3 text-xs text-zinc-500">
      {text}
    </div>
  );
}

function formatParams(params: Record<string, StrategyParamValue>): string {
  const entries = Object.entries(params);
  if (entries.length === 0) {
    return "-";
  }
  return entries
    .slice(0, 3)
    .map(([key, value]) => `${key}=${String(value)}`)
    .join(", ");
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
