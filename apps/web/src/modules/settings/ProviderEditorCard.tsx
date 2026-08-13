import { Check, Loader2, PlugZap, Save, Trash2, X } from "lucide-react";

import type { ModelProvider } from "../../shared/api";
import { ApiKeyField, StatusMessage, TextField, ToggleField } from "./SettingsFields";
import { emptyToNull } from "./settingsUtils";
import type { ProviderDraft, ProviderTestResult } from "./types";

type ProviderEditorCardProps = {
  provider: ModelProvider | null;
  providerDraft: ProviderDraft;
  providerMessage: string | null;
  isActive: boolean;
  isProviderSaving: boolean;
  isProviderTested: boolean;
  onDeleteProvider: (provider: ModelProvider) => void;
  onProviderDraftChange: (provider: ProviderDraft) => void;
  onSaveProvider: () => void;
  onSelectProviderDraft: (provider: ModelProvider) => void;
  onTestProviderDraft: () => void;
  onCopyProviderApiKey: (provider: ModelProvider) => void;
  onCloseProviderTestResult: () => void;
  onUseProvider: (provider: ModelProvider) => void;
  testResult: ProviderTestResult | null;
};

export function ProviderEditorCard({
  provider,
  providerDraft,
  providerMessage,
  isActive,
  isProviderSaving,
  isProviderTested,
  onDeleteProvider,
  onProviderDraftChange,
  onSaveProvider,
  onSelectProviderDraft,
  onTestProviderDraft,
  onCopyProviderApiKey,
  onCloseProviderTestResult,
  onUseProvider,
  testResult,
}: ProviderEditorCardProps) {
  const isEditing = provider === null || providerDraft.id === provider.id;
  const displayName = provider?.name ?? "新 Provider";
  const displayBaseUrl = provider?.base_url ?? "default Anthropic endpoint";

  return (
    <div
      className={`grid gap-3 rounded-md border px-3 py-2.5 ${
        isActive ? "border-signal bg-soft" : "border-line bg-panel"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        {provider ? (
          <button
            className="min-w-0 text-left"
            type="button"
            onClick={() => onSelectProviderDraft(provider)}
          >
            <span className="block truncate text-xs font-semibold text-ink">{displayName}</span>
            <span className="block truncate font-mono text-[10px] text-muted">
              {displayBaseUrl}
            </span>
          </button>
        ) : (
          <div className="min-w-0">
            <span className="block truncate text-xs font-semibold text-ink">{displayName}</span>
            <span className="block truncate font-mono text-[10px] text-muted">
              Anthropic-compatible endpoint
            </span>
          </div>
        )}
        {isActive ? (
          <span className="shrink-0 rounded-full bg-brand/10 px-2 py-0.5 text-[10px] font-semibold text-brand">
            当前使用
          </span>
        ) : null}
      </div>

      {isEditing ? (
        <div className="grid gap-3 border-t border-line pt-3 sm:grid-cols-2">
          <TextField
            label="名称"
            value={providerDraft.name}
            onChange={(name) => onProviderDraftChange({ ...providerDraft, name })}
          />
          <TextField
            label="Base URL"
            value={providerDraft.base_url ?? ""}
            onChange={(base_url) =>
              onProviderDraftChange({ ...providerDraft, base_url: emptyToNull(base_url) })
            }
          />
          <ApiKeyField
            hasSavedApiKey={provider?.has_api_key ?? false}
            value={providerDraft.api_key}
            onChange={(api_key) => onProviderDraftChange({ ...providerDraft, api_key })}
            onCopy={provider?.has_api_key ? () => onCopyProviderApiKey(provider) : undefined}
          />
          <ToggleField
            label="启用"
            description="关闭后不会出现在 Agent 模型 Provider 选项中。"
            checked={providerDraft.enabled}
            onChange={(enabled) => onProviderDraftChange({ ...providerDraft, enabled })}
          />
          {providerMessage ? <StatusMessage message={providerMessage} /> : null}
          <div className="flex flex-wrap items-center justify-end gap-2 sm:col-span-2">
            {provider && !isActive ? (
              <button
                className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite hover:border-signal disabled:cursor-not-allowed disabled:opacity-60"
                type="button"
                disabled={!provider.enabled}
                onClick={() => onUseProvider(provider)}
              >
                <Check className="h-3.5 w-3.5" />
                使用
              </button>
            ) : null}
            <button
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite hover:border-signal disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={isProviderSaving || !providerDraft.name.trim()}
              onClick={onTestProviderDraft}
            >
              {isProviderSaving ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <PlugZap className="h-3.5 w-3.5" />
              )}
              测试
            </button>
            <button
              className="inline-flex h-8 items-center justify-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={isProviderSaving || !providerDraft.name.trim() || !isProviderTested}
              onClick={onSaveProvider}
            >
              <Save className="h-3.5 w-3.5" />
              保存 Provider
            </button>
          </div>
          {testResult ? (
            <ProviderTestResultDialog
              result={testResult}
              onClose={onCloseProviderTestResult}
            />
          ) : null}
        </div>
      ) : (
        <div className="flex items-center gap-2">
          {provider && !isActive ? (
            <button
              className="inline-flex h-7 items-center gap-1 rounded-md border border-line px-2 text-[11px] font-semibold text-graphite hover:border-signal disabled:cursor-not-allowed disabled:opacity-50"
              type="button"
              disabled={!provider.enabled}
              onClick={() => onUseProvider(provider)}
            >
              <Check className="h-3 w-3" />
              使用
            </button>
          ) : null}
          <button
            className="inline-flex h-7 items-center gap-1 rounded-md border border-line px-2 text-[11px] font-semibold text-graphite hover:border-signal"
            type="button"
            onClick={() => provider && onSelectProviderDraft(provider)}
          >
            编辑
          </button>
          <button
            className="inline-flex h-7 items-center gap-1 rounded-md border border-line px-2 text-[11px] font-semibold text-graphite hover:border-risk hover:text-risk disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            disabled={!provider || isActive}
            onClick={() => provider && onDeleteProvider(provider)}
          >
            <Trash2 className="h-3 w-3" />
            删除
          </button>
          {provider?.has_api_key ? (
            <span className="ml-auto font-mono text-[10px] text-muted">已保存密钥</span>
          ) : null}
        </div>
      )}
    </div>
  );
}

function ProviderTestResultDialog({
  result,
  onClose,
}: {
  result: ProviderTestResult;
  onClose: () => void;
}) {
  const title = result.ok ? "Provider 测试通过" : "Provider 测试失败";
  const toneClass = result.ok
    ? "border-brand/25 bg-gainSoft text-brand"
    : "border-risk/25 bg-riskSoft text-risk";

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-black/35 px-4"
      role="dialog"
      aria-modal="true"
      aria-label={title}
    >
      <div className="grid w-full max-w-md gap-4 rounded-lg border border-line bg-panel p-4 shadow-2xl">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className={`inline-flex rounded-full border px-2 py-0.5 text-[11px] font-semibold ${toneClass}`}>
              {result.ok ? "连接正常" : "连接失败"}
            </div>
            <h3 className="mt-3 text-base font-semibold text-ink">{title}</h3>
            <p className="mt-1 text-xs leading-5 text-muted">
              {result.ok
                ? `已获取 ${result.modelCount} 个可用模型。`
                : "未能从该 Provider 获取模型列表。"}
            </p>
          </div>
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="关闭测试结果"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="rounded-md border border-line bg-soft px-3 py-2 text-xs leading-5 text-graphite">
          {toChineseProviderMessage(result)}
        </div>
        <div className="flex justify-end">
          <button
            className="inline-flex h-9 items-center rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25"
            type="button"
            onClick={onClose}
          >
            知道了
          </button>
        </div>
      </div>
    </div>
  );
}

function toChineseProviderMessage(result: ProviderTestResult): string {
  if (result.ok) {
    return `测试成功，接口可访问，模型数量：${result.modelCount}。`;
  }
  return result.message || "测试失败，请检查 Base URL、API Key 或网络连接。";
}
