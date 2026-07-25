import type { ReactNode } from "react";

type ConversationShellProps = {
  artifactList: ReactNode;
};

export function ConversationShell({ artifactList }: ConversationShellProps) {
  return (
    <section className="min-h-0 flex-1 overflow-auto px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-4">
        <div className="rounded-lg border border-line bg-panel p-4">
          <div className="text-sm font-semibold">对话线程</div>
          <p className="mt-2 text-sm leading-6 text-muted">
            工具调用完成后，代码、图表和 JSON 产物会沉淀为可追溯对象。
          </p>
        </div>
        {artifactList}
      </div>
    </section>
  );
}
