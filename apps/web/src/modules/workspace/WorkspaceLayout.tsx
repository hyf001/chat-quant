import type { ReactNode } from "react";

type WorkspaceLayoutProps = {
  history: ReactNode;
  header: ReactNode;
  conversation: ReactNode;
  composer: ReactNode;
  insight: ReactNode;
};

export function WorkspaceLayout({
  history,
  header,
  conversation,
  composer,
  insight,
}: WorkspaceLayoutProps) {
  return (
    <main className="min-h-screen bg-app text-ink">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] xl:grid-cols-[292px_minmax(0,1fr)_360px]">
        {history}
        <section className="flex min-h-screen min-w-0 flex-col">
          {header}
          {conversation}
          {composer}
        </section>
        {insight}
      </div>
    </main>
  );
}
