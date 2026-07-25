import { Download, FileCode2, RefreshCcw } from "lucide-react";

import { API_BASE_URL, type CodeArtifact } from "../../shared/api";

type ArtifactListProps = {
  artifacts: CodeArtifact[];
  selectedArtifactId: string | null;
  isLoading: boolean;
  error: string | null;
  onRefresh: () => void;
  onSelectArtifact: (artifactId: string) => void;
};

const artifactTypeLabel: Record<CodeArtifact["artifact_type"], string> = {
  query_script: "查询脚本",
  analysis_script: "分析脚本",
  strategy_script: "策略代码",
  backtest_script: "回测脚本",
  json_result: "JSON 结果",
  chart_file: "图表文件",
};

export function ArtifactList({
  artifacts,
  selectedArtifactId,
  isLoading,
  error,
  onRefresh,
  onSelectArtifact,
}: ArtifactListProps) {
  return (
    <section className="rounded-lg border border-line bg-panel p-4" aria-label="代码产物">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div>
          <div className="text-sm font-semibold">M3 代码产物</div>
          <div className="mt-1 text-xs text-muted">{artifacts.length} 个可追溯对象</div>
        </div>
        <button
          className="grid size-9 place-items-center rounded-lg border border-line text-muted hover:bg-soft focus:outline-none focus:ring-2 focus:ring-brand/30 disabled:opacity-50"
          type="button"
          aria-label="刷新产物列表"
          onClick={onRefresh}
          disabled={isLoading}
          title="刷新"
        >
          <RefreshCcw size={16} />
        </button>
      </div>

      {error ? (
        <div className="rounded-lg border border-risk/40 bg-risk/5 px-3 py-2 text-sm text-risk">
          {error}
        </div>
      ) : null}

      {!error && isLoading ? (
        <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
          正在加载产物
        </div>
      ) : null}

      {!error && !isLoading && artifacts.length === 0 ? (
        <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
          暂无产物
        </div>
      ) : null}

      <div className="grid gap-2">
        {artifacts.map((artifact) => (
          <button
            key={artifact.artifact_id}
            className={`w-full rounded-lg border px-3 py-3 text-left transition focus:outline-none focus:ring-2 focus:ring-brand/30 ${
              artifact.artifact_id === selectedArtifactId
                ? "border-brand bg-brand/5"
                : "border-line bg-panel hover:bg-soft"
            }`}
            type="button"
            onClick={() => onSelectArtifact(artifact.artifact_id)}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <div className="truncate text-sm font-semibold">{artifact.title}</div>
                <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted">
                  <span>{artifactTypeLabel[artifact.artifact_type]}</span>
                  <span>v{artifact.version}</span>
                  <span>{artifact.status}</span>
                </div>
              </div>
              <FileCode2 className="shrink-0 text-brand" size={17} />
            </div>
            <div className="mt-2 flex items-center gap-2 text-xs text-muted">
              <Download size={13} />
              <span className="truncate">
                {artifact.files.length > 0 ? `${artifact.files.length} 个文件` : "无文件"}
              </span>
            </div>
          </button>
        ))}
      </div>

      <div className="mt-3 text-[11px] text-muted">API: {API_BASE_URL}/api/artifacts</div>
    </section>
  );
}
