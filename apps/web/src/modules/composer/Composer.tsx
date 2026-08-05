import { FormEvent, useState } from "react";

import type { ProviderModel } from "../../shared/api";

type ComposerProps = {
  disabled: boolean;
  placeholder?: string;
  currentModel: string | null;
  models: ProviderModel[];
  isModelLoading?: boolean;
  isModelSaving?: boolean;
  onModelChange: (model: string) => void;
  onSendMessage: (content: string) => Promise<void>;
};

export function Composer({
  disabled,
  placeholder = "向 Agent 追加指令...",
  currentModel,
  models,
  isModelLoading = false,
  isModelSaving = false,
  onModelChange,
  onSendMessage,
}: ComposerProps) {
  const [content, setContent] = useState("");
  const canSelectModel = models.length > 0 && !disabled && !isModelLoading && !isModelSaving;

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
        <label className="sr-only" htmlFor="agent-model-select">
          模型
        </label>
        <select
          className="h-9 max-w-52 shrink-0 rounded-md border border-line bg-soft px-2.5 font-mono text-[11px] text-graphite outline-none transition-colors hover:border-signal focus:border-signal disabled:cursor-not-allowed disabled:text-muted"
          disabled={!canSelectModel}
          id="agent-model-select"
          value={canSelectModel ? currentModel ?? "" : ""}
          onChange={(event) => onModelChange(event.target.value)}
        >
          {canSelectModel ? null : (
            <option value="">{isModelLoading ? "loading model" : "no model"}</option>
          )}
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </select>
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
