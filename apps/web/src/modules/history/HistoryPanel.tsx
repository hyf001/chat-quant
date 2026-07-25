import { Plus, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

import { listStrategies, type StrategySummary } from "../../shared/api";
import { IconButton } from "../../shared/components";

const statusLabel: Record<StrategySummary["version_status"], string> = {
  draft: "草稿",
  validating: "校验中",
  validated: "已校验",
  invalid: "未通过",
  archived: "已归档",
};

export function HistoryPanel() {
  const [strategies, setStrategies] = useState<StrategySummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void refreshStrategies();
  }, []);

  async function refreshStrategies() {
    try {
      setIsLoading(true);
      setError(null);
      const items = await listStrategies();
      setStrategies(items);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "历史策略加载失败");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <aside className="hidden border-r border-line bg-panel/85 px-4 py-5 lg:block" aria-label="历史会话">
      <div className="mb-5 flex items-center gap-3">
        <div className="grid size-9 place-items-center rounded-lg bg-brand text-sm font-bold text-white">
          CQ
        </div>
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold">Chat-Quant</div>
          <div className="truncate text-xs text-muted">股票分析智能体</div>
        </div>
      </div>

      <button className="mb-5 flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white">
        <Plus size={16} />
        新建会话
      </button>

      <div className="mb-3 flex items-center justify-between gap-2">
        <div className="text-xs font-semibold text-muted">策略型历史会话</div>
        <button
          className="grid size-8 place-items-center rounded-lg border border-line bg-soft text-ink transition hover:border-strong hover:bg-panel disabled:cursor-not-allowed disabled:opacity-50"
          type="button"
          aria-label="刷新策略型历史会话"
          onClick={refreshStrategies}
          disabled={isLoading}
        >
          <RefreshCw size={14} />
        </button>
      </div>

      {isLoading ? <HistoryNotice text="正在读取策略资产" /> : null}
      {!isLoading && error ? <HistoryNotice text={error} tone="risk" /> : null}
      {!isLoading && !error && strategies.length === 0 ? (
        <HistoryNotice text="暂无策略型会话，右侧对象详情可生成示例策略。" />
      ) : null}

      {!isLoading && !error && strategies.length > 0 ? (
        <div className="grid gap-2">
          {strategies.map((strategy) => (
            <button
              className="w-full rounded-lg border border-line bg-soft p-3 text-left transition hover:border-strong hover:bg-panel"
              key={strategy.strategy_id}
              type="button"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="min-w-0 truncate text-sm font-semibold">{strategy.name}</div>
                <span className="shrink-0 rounded-full border border-line bg-panel px-2 py-0.5 text-xs text-muted">
                  V{strategy.version}
                </span>
              </div>
              <div className="mt-2 line-clamp-2 text-xs leading-5 text-muted">
                {strategy.logic_summary ?? "策略逻辑摘要待补充"}
              </div>
              <div className="mt-3 flex flex-wrap gap-1.5">
                <Tag text={statusLabel[strategy.version_status]} />
                <Tag text={strategy.strategy_type} />
                <Tag text={summarizeParams(strategy.default_params)} />
              </div>
            </button>
          ))}
        </div>
      ) : null}

      <div className="mt-4 lg:hidden">
        <IconButton label="关闭历史" icon={<Plus size={16} />} />
      </div>
    </aside>
  );
}

function Tag({ text }: { text: string }) {
  return (
    <span className="max-w-full truncate rounded-full border border-line bg-panel px-2 py-0.5 text-xs text-muted">
      {text}
    </span>
  );
}

function HistoryNotice({ text, tone = "muted" }: { text: string; tone?: "muted" | "risk" }) {
  const toneClass = tone === "risk" ? "border-risk/40 text-risk" : "border-dashed text-muted";
  return <div className={`rounded-lg border bg-soft p-4 text-sm ${toneClass}`}>{text}</div>;
}

function summarizeParams(params: Record<string, number | string | boolean>): string {
  const entries = Object.entries(params).slice(0, 2);
  if (entries.length === 0) {
    return "无默认参数";
  }
  return entries.map(([key, value]) => `${key}=${String(value)}`).join(" / ");
}
