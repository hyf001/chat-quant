import { CheckCircle2, Loader2, Terminal, XCircle } from "lucide-react";

import type { ChatMessageView, ToolCallView } from "../../shared/types/agentRuntime";

type ConversationShellProps = {
  messages: ChatMessageView[];
  tools: ToolCallView[];
  error: string | null;
};

export function ConversationShell({ messages, tools, error }: ConversationShellProps) {
  return (
    <section className="min-h-0 flex-1 overflow-auto px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-4">
        {messages.map((message) => (
          <article
            className={
              message.role === "user"
                ? "ml-auto max-w-[82%] rounded-lg bg-ink px-4 py-3 text-sm leading-6 text-white"
                : "max-w-[88%] rounded-lg border border-line bg-panel px-4 py-3 text-sm leading-6 shadow-panel"
            }
            key={message.id}
          >
            <div className="whitespace-pre-wrap break-words">{message.content}</div>
          </article>
        ))}

        {tools.length > 0 && (
          <div className="rounded-lg border border-line bg-panel p-3">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold">
              <Terminal size={16} />
              平台命令
            </div>
            <div className="grid gap-2">
              {tools.map((tool) => (
                <div
                  className="grid grid-cols-[20px_minmax(0,1fr)] items-start gap-2 rounded-md bg-soft px-3 py-2"
                  key={tool.id}
                >
                  {tool.status === "running" && (
                    <Loader2 className="mt-0.5 animate-spin text-brandBlue" size={15} />
                  )}
                  {tool.status === "completed" && (
                    <CheckCircle2 className="mt-0.5 text-brand" size={15} />
                  )}
                  {(tool.status === "failed" || tool.status === "blocked") && (
                    <XCircle className="mt-0.5 text-risk" size={15} />
                  )}
                  <div className="min-w-0">
                    <div className="truncate font-mono text-xs text-ink">{tool.command}</div>
                    {tool.output && (
                      <pre className="mt-2 max-h-28 overflow-auto whitespace-pre-wrap break-words rounded-md border border-line bg-panel p-2 text-xs text-muted">
                        {tool.output}
                      </pre>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-risk/40 bg-panel px-4 py-3 text-sm text-risk">
            {error}
          </div>
        )}
      </div>
    </section>
  );
}
