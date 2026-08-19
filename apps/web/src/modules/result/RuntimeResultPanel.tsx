import { CheckCircle2, FileJson, XCircle } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState, InlineAlert } from "@/shared/components";

import type { ExecutionResult, RuntimeHealth } from "../../shared/api/client";

type RuntimeResultPanelProps = {
  health: RuntimeHealth | null;
  result: ExecutionResult | null;
  error: string | null;
};

export function RuntimeResultPanel({
  health,
  result,
  error,
}: RuntimeResultPanelProps) {
  const statusTone = result?.status === "succeeded" ? "text-emerald-700" : "text-risk";

  return (
    <Card aria-label="M4 运行结果">
      <CardHeader className="border-b">
        <div className="min-w-0">
          <CardTitle className="text-sm">M4 Python 运行时</CardTitle>
          <div className="mt-1 text-xs text-mutedText">
            Python {health?.python_version ?? "-"}
          </div>
        </div>
      </CardHeader>

      <div className="grid gap-3 p-4 sm:grid-cols-3">
        <Metric label="状态" value={result?.status ?? "idle"} />
        <Metric label="耗时" value={result ? `${result.duration_ms} ms` : "-"} />
        <Metric label="产物" value={String(result?.artifacts.length ?? 0)} />
      </div>

      {error ? (
        <InlineAlert className="mx-4 mb-4" title="运行失败" description={error} />
      ) : null}

      {result ? (
        <CardContent className="grid gap-3 border-t p-4 lg:grid-cols-[minmax(0,1fr)_240px]">
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
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-mutedText">
              <FileJson size={14} />
              产物
            </div>
            <div className="grid gap-2">
              {result.artifacts.map((artifact) => (
                <Card key={artifact.path} className="min-w-0 rounded-md p-2 shadow-none">
                  <div className="truncate text-xs font-semibold">{artifact.name ?? artifact.path}</div>
                  <div className="mt-1 text-[11px] text-mutedText">{artifact.type}</div>
                </Card>
              ))}
              {result.artifacts.length === 0 ? (
                <EmptyState title="暂无产物" />
              ) : null}
            </div>
          </div>
        </CardContent>
      ) : (
        <CardContent className="border-t p-4">
          <EmptyState title="等待运行" />
        </CardContent>
      )}
    </Card>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <Card className="bg-muted p-3 shadow-none">
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="mt-1 truncate text-sm font-semibold">{value}</div>
    </Card>
  );
}
