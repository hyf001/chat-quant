import { FormEvent, useState } from "react";

type ComposerProps = {
  disabled: boolean;
  placeholder?: string;
  onSendMessage: (content: string) => Promise<void>;
};

export function Composer({ disabled, placeholder = "向 Agent 追加指令...", onSendMessage }: ComposerProps) {
  const [content, setContent] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = content.trim();
    if (!trimmed || disabled) {
      return;
    }
    setContent("");
    await onSendMessage(trimmed);
  };

  return (
    <footer className="shrink-0 border-t border-zinc-200 bg-white p-4">
      <form
        className="mx-auto flex max-w-3xl items-center gap-2 rounded-lg border border-zinc-300 bg-zinc-50 px-3 py-2.5 transition-all focus-within:border-zinc-900 focus-within:bg-white"
        onSubmit={handleSubmit}
      >
        <span className="select-none font-mono text-xs font-bold text-zinc-500">&gt;</span>
        <input
          className="min-w-0 flex-1 bg-transparent text-xs text-zinc-900 outline-none placeholder:text-zinc-400"
          disabled={disabled}
          id="agent-message-input"
          name="message"
          onChange={(event) => setContent(event.target.value)}
          placeholder={placeholder}
          value={content}
        />
        <button
          className="shrink-0 rounded bg-zinc-900 px-3.5 py-1 text-xs font-semibold text-white transition-colors hover:bg-black focus:outline-none focus:ring-2 focus:ring-zinc-900/25 disabled:cursor-not-allowed disabled:bg-zinc-300 disabled:text-zinc-500"
          disabled={disabled || content.trim().length === 0}
          type="submit"
        >
          发送
        </button>
      </form>
    </footer>
  );
}
