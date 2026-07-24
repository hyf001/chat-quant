import { Send } from "lucide-react";

export function Composer() {
  return (
    <footer className="border-t border-line bg-app/95 px-5 py-4">
      <div className="mx-auto flex max-w-4xl items-end gap-2 rounded-lg border border-line bg-panel p-2 shadow-panel">
        <textarea
          className="min-h-12 flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-muted"
          placeholder="输入股票问题、选股条件或策略想法..."
          rows={2}
        />
        <button className="grid size-10 place-items-center rounded-lg bg-brand text-white" aria-label="发送">
          <Send size={17} />
        </button>
      </div>
    </footer>
  );
}
