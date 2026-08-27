import type { ReactNode } from "react";

type WorkspaceLayoutProps = {
  history: ReactNode;
  conversation: ReactNode;
  result?: ReactNode;
  composer?: ReactNode;
  insight?: ReactNode;
  contentClassName?: string;
};

export function WorkspaceLayout({
  history,
  conversation,
  result,
  composer,
  insight,
  contentClassName = "p-5 lg:p-7",
}: WorkspaceLayoutProps) {
  return (
    <main className="workbench-surface flex h-screen overflow-hidden font-sans text-ink">
      <div className="flex h-full min-w-0 flex-1">
        {history}
        <section className="flex h-full min-w-0 flex-1 flex-col bg-app/70">
          <div className={`min-h-0 flex-1 overflow-y-auto ${contentClassName}`}>
            {conversation}
            {result ? (
              <div className="mx-auto mt-6 w-full max-w-5xl">
                <div>{result}</div>
              </div>
            ) : null}
          </div>
          {composer ?? null}
        </section>
        {insight ?? null}
      </div>
    </main>
  );
}
