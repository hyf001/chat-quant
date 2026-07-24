export function InsightPanel() {
  return (
    <aside
      className="hidden border-l border-line bg-panel/70 px-4 py-5 xl:block"
      aria-label="对象详情"
    >
      <div className="mb-3 text-sm font-semibold">对象详情</div>
      <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
        图表对象、结果对象和参数快照待接入
      </div>
    </aside>
  );
}
