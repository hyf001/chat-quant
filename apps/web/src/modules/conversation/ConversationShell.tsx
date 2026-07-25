import { AlertCircle, Bot, Database, User } from "lucide-react";
import type { ReactNode } from "react";

import type { AssetLink, ChatSession, SdkMessage } from "../../shared/api";

type ConversationShellProps = {
  session: ChatSession | null;
  messages: SdkMessage[];
  assets: AssetLink[];
  isLoading: boolean;
  error: string | null;
  artifactList?: ReactNode;
};

function blockText(message: SdkMessage): string {
  const text = message.content
    .map((block) => block.text)
    .filter((value): value is string => Boolean(value))
    .join("\n");
  return text || "工具调用结果已记录";
}

function roleLabel(role: SdkMessage["role"]): string {
  if (role === "user") {
    return "你";
  }
  if (role === "assistant") {
    return "Agent";
  }
  if (role === "tool") {
    return "工具";
  }
  return "系统";
}

export function ConversationShell({
  session,
  messages,
  assets,
  isLoading,
  error,
  artifactList,
}: ConversationShellProps) {
  return (
    <section className="min-h-0 flex-1 overflow-auto px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-4">
        {error ? (
          <div className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <AlertCircle className="mt-0.5 shrink-0" size={17} />
            <span className="min-w-0 break-words">{error}</span>
          </div>
        ) : null}

        {isLoading ? (
          <div className="rounded-lg border border-line bg-panel p-4 text-sm text-muted">加载中</div>
        ) : null}

        {!isLoading && !session ? (
          <div className="rounded-lg border border-line bg-panel p-5">
            <div className="text-sm font-semibold">开始新的量化会话</div>
            <p className="mt-2 text-sm leading-6 text-muted">
              输入股票问题、选股条件或策略想法后，系统会创建历史入口并保存会话上下文。
            </p>
          </div>
        ) : null}

        {session && messages.length === 0 ? (
          <div className="rounded-lg border border-dashed border-line bg-panel p-5 text-sm leading-6 text-muted">
            当前会话还没有消息。
          </div>
        ) : null}

        {messages.map((message) => {
          const isUser = message.role === "user";
          return (
            <article
              className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
              key={message.uuid}
            >
              {!isUser ? (
                <div className="grid size-8 shrink-0 place-items-center rounded-lg bg-brand/10 text-brand">
                  {message.role === "assistant" ? <Bot size={17} /> : <Database size={17} />}
                </div>
              ) : null}
              <div
                className={`max-w-[78%] rounded-lg border p-4 ${
                  isUser ? "border-brand bg-brand text-white" : "border-line bg-panel text-ink"
                }`}
              >
                <div className={`mb-2 text-xs font-semibold ${isUser ? "text-white/80" : "text-muted"}`}>
                  {roleLabel(message.role)}
                </div>
                <p className="whitespace-pre-wrap break-words text-sm leading-6">{blockText(message)}</p>
              </div>
              {isUser ? (
                <div className="grid size-8 shrink-0 place-items-center rounded-lg bg-ink text-white">
                  <User size={16} />
                </div>
              ) : null}
            </article>
          );
        })}

        {assets.length > 0 ? (
          <div className="rounded-lg border border-line bg-panel p-4">
            <div className="text-sm font-semibold">会话资产</div>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {assets.slice(0, 4).map((asset) => (
                <div className="rounded-lg border border-line bg-soft p-3" key={asset.id}>
                  <div className="truncate text-sm font-medium">{asset.asset_id}</div>
                  <div className="mt-1 text-xs text-muted">
                    {asset.asset_type} · {asset.relation_type}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null}

        {artifactList}
      </div>
    </section>
  );
}
