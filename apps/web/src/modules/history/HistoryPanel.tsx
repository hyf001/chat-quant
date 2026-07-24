import { Plus } from "lucide-react";

import { IconButton } from "../../shared/components";

export function HistoryPanel() {
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

      <div className="mb-3 text-xs font-semibold text-muted">最近会话</div>
      <div className="rounded-lg border border-dashed border-line bg-soft p-4 text-sm text-muted">
        会话列表待接入
      </div>

      <div className="mt-4 lg:hidden">
        <IconButton label="关闭历史" icon={<Plus size={16} />} />
      </div>
    </aside>
  );
}
