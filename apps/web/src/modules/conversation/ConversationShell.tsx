export function ConversationShell() {
  return (
    <section className="min-h-0 flex-1 overflow-auto px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-4">
        <div className="rounded-lg border border-line bg-panel p-4">
          <div className="text-sm font-semibold">对话线程</div>
          <p className="mt-2 text-sm leading-6 text-muted">
            这里后续承载用户消息、Agent 回复、澄清卡、工具调用进度和结果对象。
          </p>
        </div>
      </div>
    </section>
  );
}
