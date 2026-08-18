import { FormEvent, useState } from "react";

import type { ProviderModel } from "../../shared/api";

type ComposerProps = {
  disabled: boolean;
  placeholder?: string;
  currentModel: string | null;
  models: ProviderModel[];
  isModelLoading?: boolean;
  isModelSaving?: boolean;
  isStreaming?: boolean;
  isStopping?: boolean;
  onModelChange: (model: string) => void;
  onModelRefresh?: () => void;
  onSendMessage: (content: string) => Promise<void>;
  onStopStreaming?: () => Promise<void> | void;
};

export function Composer({
  disabled,
  placeholder = "向 Agent 追加指令...",
  currentModel,
  models,
  isModelLoading = false,
  isModelSaving = false,
  isStreaming = false,
  isStopping = false,
  onModelChange,
  onModelRefresh,
  onSendMessage,
  onStopStreaming,
}: ComposerProps) {
  const [content, setContent] = useState("");
  const hasModels = models.length > 0;
  const canEdit = !disabled && !isStreaming;
  const canSelectModel = hasModels && canEdit && !isModelSaving;
  const isSubmitDisabled = isStreaming
    ? isStopping || !onStopStreaming
    : disabled || content.trim().length === 0;
  const selectedModel = currentModel ?? models[0]?.id ?? "";

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isStreaming) {
      await onStopStreaming?.();
      return;
    }
    const trimmed = content.trim();
    if (!trimmed || !canEdit) {
      return;
    }
    setContent("");
    await onSendMessage(trimmed);
  };

  const handleStopClick = () => {
    void onStopStreaming?.();
  };

  return (
    <footer className="glass-panel shrink-0 border-t border-line p-4">
      <form
        className="mx-auto flex max-w-5xl items-center gap-3 rounded-lg border border-strong bg-panel px-4 py-3 shadow-lift transition-all focus-within:border-signal focus-within:bg-panel"
        onFocusCapture={onModelRefresh}
        onSubmit={handleSubmit}
      >
        <span className="select-none font-mono text-lg font-black text-signal">&gt;</span>
        <input
          className="min-w-0 flex-1 bg-transparent text-sm text-ink outline-none placeholder:text-muted/70"
          disabled={!canEdit}
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
          value={hasModels ? selectedModel : ""}
          onChange={(event) => onModelChange(event.target.value)}
        >
          {hasModels ? null : (
            <option value="">{isModelLoading ? "loading model" : "no model"}</option>
          )}
          {hasModels && currentModel && !models.some((model) => model.id === currentModel) ? (
            <option value={currentModel}>{currentModel}</option>
          ) : null}
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </select>
        <button
          className={
            isStreaming
              ? "h-9 shrink-0 rounded-md bg-rose-600 px-4 text-xs font-bold text-white transition-colors hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500/25 disabled:cursor-not-allowed disabled:bg-strong disabled:text-muted"
              : "h-9 shrink-0 rounded-md bg-ink px-4 text-xs font-bold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:bg-strong disabled:text-muted"
          }
          disabled={isSubmitDisabled}
          onClick={isStreaming ? handleStopClick : undefined}
          type={isStreaming ? "button" : "submit"}
        >
          {isStreaming ? "停止" : "发送"}
        </button>
      </form>
    </footer>
  );
}
