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
    <footer className="glass-panel shrink-0 border-t border-line p-4">
      <form
        className="mx-auto flex max-w-5xl items-center gap-3 rounded-lg border border-strong bg-panel px-4 py-3 shadow-lift transition-all focus-within:border-signal focus-within:bg-panel"
        onSubmit={handleSubmit}
      >
        <span className="select-none font-mono text-lg font-black text-signal">&gt;</span>
        <input
          className="min-w-0 flex-1 bg-transparent text-sm text-ink outline-none placeholder:text-muted/70"
          disabled={disabled}
          id="agent-message-input"
          name="message"
          onChange={(event) => setContent(event.target.value)}
          placeholder={placeholder}
          value={content}
        />
        <button
          className="h-9 shrink-0 rounded-md bg-ink px-4 text-xs font-bold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:bg-strong disabled:text-muted"
          disabled={disabled || content.trim().length === 0}
          type="submit"
        >
          发送
        </button>
      </form>
    </footer>
  );
}
