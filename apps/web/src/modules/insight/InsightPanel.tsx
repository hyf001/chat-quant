import type { ExecutionResult, RuntimeHealth } from "../../shared/api";

type InsightPanelProps = {
  health: RuntimeHealth | null;
  result: ExecutionResult | null;
};

export function InsightPanel({ health, result }: InsightPanelProps) {
  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      <div className="grid gap-3">
        <Detail label="运行 ID" value={result?.run_id ?? "-"} />
        <Detail label="Python" value={health?.python_version ?? "-"} />
        <Detail label="exit code" value={result?.exit_code === null ? "-" : String(result?.exit_code ?? "-")} />
        <Detail label="输出目录" value={result?.output_dir ?? "-"} />
        <div className="rounded-lg border border-line bg-soft p-3">
          <div className="mb-2 text-xs font-semibold text-muted">核心包</div>
          <div className="grid gap-2 text-xs">
            {Object.entries(health?.packages ?? {}).map(([name, status]) => (
              <div key={name} className="flex items-center justify-between gap-2">
                <span>{name}</span>
                <span className={status === "installed" ? "text-emerald-700" : "text-muted"}>
                  {status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-line bg-soft p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 truncate text-xs font-semibold">{value}</div>
    </div>
  );
}
