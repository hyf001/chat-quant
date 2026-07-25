import { CheckCircle2, FileJson, Play, Terminal, XCircle } from "lucide-react";

import type { ExecutionResult, RuntimeHealth } from "../../shared/api/client";

type RuntimeResultPanelProps = {
  health: RuntimeHealth | null;
  result: ExecutionResult | null;
  isRunning: boolean;
  error: string | null;
  onRunSample: () => void;
};

export function RuntimeResultPanel({
  health,
  result,
  isRunning,
  error,
  onRunSample,
}: RuntimeResultPanelProps) {
  const statusTone = result?.status === "succeeded" ? "text-emerald-700" : "text-rose-700";

  return (
    <section className="rounded-lg border border-line bg-panel shadow-panel" aria-label="M4 运行结果">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line px-4 py-3">
        <div className="min-w-0">
          <div className="text-sm font-semibold">M4 Python 运行时</div>
          <div className="mt-1 text-xs text-muted">
            Python {health?.python_version ?? "-"} · 输出目录 {health?.runtime_root_writable ? "可写" : "待确认"}
          </div>
        </div>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-lg bg-brand px-3 text-sm font-semibold text-white transition hover:bg-strong disabled:cursor-not-allowed disabled:bg-muted"
          type="button"
          onClick={onRunSample}
          disabled={isRunning}
        >
          <Play size={15} />
          {isRunning ? "运行中" : "运行样例"}
        </button>
      </div>

      <div className="grid gap-3 p-4 sm:grid-cols-3">
        <Metric label="状态" value={result?.status ?? "idle"} />
        <Metric label="耗时" value={result ? `${result.duration_ms} ms` : "-"} />
        <Metric label="产物" value={String(result?.artifacts.length ?? 0)} />
      </div>

      {error ? (
        <div className="mx-4 mb-4 rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      {result ? (
        <div className="grid gap-3 border-t border-line p-4 lg:grid-cols-[minmax(0,1fr)_240px]">
          <div className="min-w-0">
            <div className={`mb-2 flex items-center gap-2 text-sm font-semibold ${statusTone}`}>
              {result.status === "succeeded" ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
              {result.run_id}
            </div>
            <pre className="max-h-56 overflow-auto rounded-lg bg-ink p-3 text-xs leading-5 text-white">
              {result.stdout || result.stderr || "No process output"}
            </pre>
          </div>
          <div className="min-w-0 rounded-lg border border-line bg-soft p-3">
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-muted">
              <FileJson size={14} />
              产物
            </div>
            <div className="grid gap-2">
              {result.artifacts.map((artifact) => (
                <div key={artifact.path} className="min-w-0 rounded border border-line bg-panel p-2">
                  <div className="truncate text-xs font-semibold">{artifact.name ?? artifact.path}</div>
                  <div className="mt-1 text-[11px] text-muted">{artifact.type}</div>
                </div>
              ))}
              {result.artifacts.length === 0 ? (
                <div className="text-xs text-muted">暂无产物</div>
              ) : null}
            </div>
          </div>
        </div>
      ) : (
        <div className="border-t border-line p-4">
          <div className="flex items-center gap-2 rounded-lg border border-dashed border-line bg-soft p-3 text-sm text-muted">
            <Terminal size={16} />
            等待运行
          </div>
        </div>
      )}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-soft p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 truncate text-sm font-semibold">{value}</div>
    </div>
  );
}
