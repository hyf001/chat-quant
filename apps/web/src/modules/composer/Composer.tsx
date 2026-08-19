import { FormEvent, useState } from "react";
import { RefreshCw, Send, Square } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

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
        className="mx-auto flex max-w-5xl items-center gap-3 rounded-lg border bg-card px-4 py-3 shadow-sm transition-all focus-within:ring-2 focus-within:ring-ring/20"
        onFocusCapture={onModelRefresh}
        onSubmit={handleSubmit}
      >
        <span className="select-none font-mono text-lg font-black text-accent">&gt;</span>
        <Input
          className="h-10 min-w-0 flex-1 border-0 bg-transparent px-0 shadow-none focus-visible:ring-0"
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
        <Select
          disabled={!canSelectModel}
          value={hasModels ? selectedModel : ""}
          onValueChange={onModelChange}
        >
          <SelectTrigger
            className="h-9 max-w-52 shrink-0 font-mono text-[11px]"
            id="agent-model-select"
          >
            <SelectValue placeholder={isModelLoading ? "loading model" : "no model"} />
          </SelectTrigger>
          <SelectContent>
            {hasModels && currentModel && !models.some((model) => model.id === currentModel) ? (
              <SelectItem value={currentModel}>{currentModel}</SelectItem>
            ) : null}
            {models.map((model) => (
              <SelectItem key={model.id} value={model.id}>
                {model.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {onModelRefresh ? (
          <Button
            aria-label="刷新模型列表"
            disabled={disabled || isModelLoading || isModelSaving || isStreaming}
            size="icon"
            title="刷新模型列表"
            type="button"
            variant="outline"
            onClick={onModelRefresh}
          >
            <RefreshCw className={isModelLoading ? "animate-spin" : ""} />
          </Button>
        ) : null}
        <Button
          size="sm"
          variant={isStreaming ? "destructive" : "default"}
          disabled={isSubmitDisabled}
          onClick={isStreaming ? handleStopClick : undefined}
          type={isStreaming ? "button" : "submit"}
        >
          {isStreaming ? <Square /> : <Send />}
          {isStreaming ? "停止" : "发送"}
        </Button>
      </form>
    </footer>
  );
}
