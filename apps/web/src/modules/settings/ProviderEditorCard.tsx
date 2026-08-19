import { Check, Loader2, PlugZap, Save, Trash2 } from "lucide-react";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import type { ModelProvider } from "../../shared/api";
import { ApiKeyField, TextField, ToggleField } from "./SettingsFields";
import { emptyToNull } from "./settingsUtils";
import type { ProviderDraft, ProviderTestResult } from "./types";

type ProviderEditorCardProps = {
  provider: ModelProvider | null;
  providerDraft: ProviderDraft;
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
    <Card
      className={`grid gap-3 rounded-md border px-3 py-2.5 ${
        isActive ? "border-accent bg-muted" : ""
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
            <span className="block truncate font-mono text-[10px] text-mutedText">
              {displayBaseUrl}
            </span>
          </button>
        ) : (
          <div className="min-w-0">
            <span className="block truncate text-xs font-semibold text-ink">{displayName}</span>
            <span className="block truncate font-mono text-[10px] text-mutedText">
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
          <div className="flex flex-wrap items-center justify-end gap-2 sm:col-span-2">
            {provider && !isActive ? (
              <Button
                size="sm"
                variant="outline"
                type="button"
                disabled={!provider.enabled}
                onClick={() => onUseProvider(provider)}
              >
                <Check className="h-3.5 w-3.5" />
                使用
              </Button>
            ) : null}
            <Button
              size="sm"
              variant="outline"
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
            </Button>
            <Button
              size="sm"
              type="button"
              disabled={isProviderSaving || !providerDraft.name.trim() || !isProviderTested}
              onClick={onSaveProvider}
            >
              <Save className="h-3.5 w-3.5" />
              保存 Provider
            </Button>
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
            <Button
              className="h-7 text-[11px]"
              size="sm"
              variant="outline"
              type="button"
              disabled={!provider.enabled}
              onClick={() => onUseProvider(provider)}
            >
              <Check className="h-3 w-3" />
              使用
            </Button>
          ) : null}
          <Button
            className="h-7 text-[11px]"
            size="sm"
            variant="outline"
            type="button"
            onClick={() => provider && onSelectProviderDraft(provider)}
          >
            编辑
          </Button>
          {provider ? (
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button
                  className="h-7 text-[11px]"
                  size="sm"
                  variant="outline"
                  type="button"
                  disabled={isActive}
                >
                  <Trash2 className="h-3 w-3" />
                  删除
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>删除 Provider {provider.name}？</AlertDialogTitle>
                  <AlertDialogDescription>
                    删除后该 Provider 会从模型供应商列表中移除，已保存的 API Key 也将不可用。
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>取消</AlertDialogCancel>
                  <AlertDialogAction
                    className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                    onClick={() => onDeleteProvider(provider)}
                  >
                    删除
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          ) : null}
          {provider?.has_api_key ? (
            <span className="ml-auto font-mono text-[10px] text-mutedText">已保存密钥</span>
          ) : null}
        </div>
      )}
    </Card>
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

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <Badge
            className="mb-2 w-fit"
            variant={result.ok ? "default" : "destructive"}
          >
            {result.ok ? "连接正常" : "连接失败"}
          </Badge>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>
            {result.ok
              ? `已获取 ${result.modelCount} 个可用模型。`
              : "未能从该 Provider 获取模型列表。"}
          </DialogDescription>
        </DialogHeader>
        <div className="rounded-md border bg-muted px-3 py-2 text-xs leading-5">
          {toChineseProviderMessage(result)}
        </div>
        <DialogFooter>
          <Button size="sm" type="button" onClick={onClose}>
            知道了
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function toChineseProviderMessage(result: ProviderTestResult): string {
  if (result.ok) {
    return `测试成功，接口可访问，模型数量：${result.modelCount}。`;
  }
  return result.message || "测试失败，请检查 Base URL、API Key 或网络连接。";
}
