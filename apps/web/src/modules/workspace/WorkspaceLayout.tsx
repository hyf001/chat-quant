import type { ReactNode } from "react";

type WorkspaceLayoutProps = {
  history: ReactNode;
  header: ReactNode;
  conversation: ReactNode;
  result?: ReactNode;
  composer?: ReactNode;
  insight?: ReactNode;
};

export function WorkspaceLayout({
  history,
  header,
  conversation,
  result,
  composer,
  insight: _insight,
}: WorkspaceLayoutProps) {
  return (
    <main className="flex h-screen overflow-hidden bg-white font-sans text-zinc-900">
      <div className="flex h-full min-w-0 flex-1">
        {history}
        <section className="flex h-full min-w-0 flex-1 flex-col bg-white">
          {header}
          <div className="min-h-0 flex-1 overflow-y-auto p-8">
            {conversation}
            {result ? (
              <div className="mx-auto mt-6 w-full max-w-3xl">
                <div>{result}</div>
              </div>
            ) : null}
          </div>
          {composer ?? null}
        </section>
      </div>
    </main>
  );
}
