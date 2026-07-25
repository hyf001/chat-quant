import { Download, Eye, FileCode2 } from "lucide-react";

import { API_BASE_URL, type CodeArtifact } from "../../shared/api";

type InsightPanelProps = {
  artifact: CodeArtifact | null;
};

const formatter = new Intl.DateTimeFormat("zh-CN", {
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});

export function InsightPanel({ artifact }: InsightPanelProps) {
  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      {artifact ? (
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
      ) : (
        <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
          未选择对象
        </div>
      )}
    </aside>
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
