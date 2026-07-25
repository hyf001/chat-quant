import { Send } from "lucide-react";
import { FormEvent, useState } from "react";

type ComposerProps = {
  disabled: boolean;
  onSendMessage: (content: string) => Promise<void>;
};

export function Composer({ disabled, onSendMessage }: ComposerProps) {
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
    <footer className="border-t border-line bg-app/95 px-5 py-4">
      <form
        className="mx-auto flex max-w-4xl items-end gap-2 rounded-lg border border-line bg-panel p-2 shadow-panel"
        onSubmit={handleSubmit}
      >
        <textarea
          className="min-h-12 flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-muted"
          disabled={disabled}
          onChange={(event) => setContent(event.target.value)}
          placeholder="输入股票问题、选股条件或策略想法..."
          rows={2}
          value={content}
        />
        <button
          className="grid size-10 place-items-center rounded-lg bg-brand text-white transition hover:bg-brand/90 focus:outline-none focus:ring-2 focus:ring-brand/40 disabled:cursor-not-allowed disabled:bg-muted"
          aria-label="发送"
          disabled={disabled || content.trim().length === 0}
          type="submit"
        >
          <Send size={17} />
        </button>
      </form>
    </footer>
  );
}
