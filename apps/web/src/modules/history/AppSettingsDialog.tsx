import {
  Check,
  Copy,
  Loader2,
  PlugZap,
  Plus,
  Save,
  Trash2,
  X,
} from "lucide-react";
import { useCallback, useEffect, useState, type ReactNode } from "react";

import {
  createModelProvider,
  deleteModelProvider,
  getModelProviderApiKey,
  getAppConfig,
  listModelProviders,
  listProviderModels,
  testModelProviderPayload,
  updateAppConfig,
  updateModelProvider,
  type AppConfig,
  type AppSettings,
  type ModelProvider,
  type ModelProviderPayload,
  type ProviderModel,
} from "../../shared/api";

type AppSettingsDialogProps = {
  isOpen: boolean;
  onClose: () => void;
};

type SettingsTab = "agent" | "system" | "logging";

type ProviderDraft = ModelProviderPayload & {
  id: string | null;
};

const tabs: Array<{ id: SettingsTab; label: string }> = [
  { id: "agent", label: "Agent" },
  { id: "system", label: "系统" },
  { id: "logging", label: "日志" },
];

const blankProviderDraft: ProviderDraft = {
  id: null,
  name: "",
  base_url: null,
  api_key: null,
  enabled: true,
};

export function AppSettingsDialog({ isOpen, onClose }: AppSettingsDialogProps) {
  const [activeTab, setActiveTab] = useState<SettingsTab>("agent");
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [draft, setDraft] = useState<AppSettings | null>(null);
  const [providers, setProviders] = useState<ModelProvider[]>([]);
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [providerDraft, setProviderDraft] = useState<ProviderDraft>(blankProviderDraft);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isProviderSaving, setIsProviderSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [modelMessage, setModelMessage] = useState<string | null>(null);
  const [providerMessage, setProviderMessage] = useState<string | null>(null);
  const [testedProviderSignature, setTestedProviderSignature] = useState<string | null>(null);

  const loadProviderModels = useCallback(async (providerId: string) => {
    try {
      const response = await listProviderModels(providerId);
      setModels(response.models);
      setModelMessage(null);
      return response.models;
    } catch (caught) {
      setModels([]);
      setModelMessage(
        `模型列表加载失败：${caught instanceof Error ? caught.message : "Provider 不可用"}`,
      );
      return [];
    }
  }, []);

  const loadSettings = useCallback(async (selectedProviderId?: string | null) => {
    setIsLoading(true);
    setMessage(null);
    setProviderMessage(null);
    setModelMessage(null);
    try {
      const [nextConfig, providerResponse] = await Promise.all([
        getAppConfig(),
        listModelProviders(),
      ]);
      const providerId = nextConfig.settings.agent.provider_id;
      const nextModels = providerId ? await loadProviderModels(providerId) : [];
      const nextSettings =
        nextModels.length > 0 &&
        !nextModels.some((model) => model.id === nextConfig.settings.agent.model)
          ? {
              ...nextConfig.settings,
              agent: {
                ...nextConfig.settings.agent,
                model: nextModels[0].id,
              },
            }
          : nextConfig.settings;
      const selectedProvider =
        providerResponse.providers.find((provider) => provider.id === selectedProviderId) ??
        providerResponse.providers.find((provider) => provider.id === providerId) ??
        null;
      setConfig(nextConfig);
      setDraft(nextSettings);
      setProviders(providerResponse.providers);
      setModels(nextModels);
      setProviderDraft(selectedProvider ? providerToDraft(selectedProvider) : blankProviderDraft);
      setTestedProviderSignature(null);
      return { config: nextConfig, providers: providerResponse.providers, models: nextModels };
    } catch (caught) {
      setMessage(caught instanceof Error ? caught.message : "设置加载失败");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [loadProviderModels]);

  useEffect(() => {
    if (!isOpen) {
      return;
    }
    void loadSettings();
  }, [isOpen, loadSettings]);

  useEffect(() => {
    const providerId = draft?.agent.provider_id;
    if (!providerId) {
      setModels([]);
      setModelMessage(null);
      return;
    }
    loadProviderModels(providerId)
      .then((nextModels) => {
        setDraft((current) => {
          if (!current || current.agent.provider_id !== providerId) {
            return current;
          }
          if (nextModels.length === 0 || nextModels.some((model) => model.id === current.agent.model)) {
            return current;
          }
          return {
            ...current,
            agent: {
              ...current.agent,
              model: nextModels[0].id,
            },
          };
        });
      });
  }, [draft?.agent.provider_id, loadProviderModels]);

  if (!isOpen) {
    return null;
  }

  const handleSave = async () => {
    if (!draft) {
      return;
    }
    setIsSaving(true);
    setMessage(null);
    try {
      const nextConfig = await updateAppConfig(draft);
      await loadSettings(nextConfig.settings.agent.provider_id);
      setMessage("已保存");
    } catch (caught) {
      setMessage(caught instanceof Error ? caught.message : "保存失败");
    } finally {
      setIsSaving(false);
    }
  };

  const updateProviderDraft = (nextDraft: ProviderDraft) => {
    setProviderDraft(nextDraft);
    setProviderMessage(null);
    setTestedProviderSignature(null);
  };

  const providerPayload = (): ModelProviderPayload => ({
    name: providerDraft.name,
    base_url: providerDraft.base_url,
    api_key: providerDraft.api_key,
    enabled: providerDraft.enabled,
  });

  const handleCopyProviderApiKey = async (provider: ModelProvider) => {
    if (!provider.has_api_key) {
      return;
    }
    setProviderMessage(null);
    try {
      const response = await getModelProviderApiKey(provider.id);
      if (!response.api_key) {
        setProviderMessage("API Key 为空");
        return;
      }
      await navigator.clipboard.writeText(response.api_key);
      setProviderMessage("API Key 已复制");
    } catch (caught) {
      setProviderMessage(caught instanceof Error ? caught.message : "API Key 复制失败");
    }
  };

  const handleTestProviderDraft = async () => {
    setIsProviderSaving(true);
    setProviderMessage(null);
    try {
      const response = await testModelProviderPayload(providerPayload(), providerDraft.id);
      setProviderMessage(response.message);
      if (response.ok) {
        setTestedProviderSignature(providerSignature(providerDraft));
        if (draft?.agent.provider_id === providerDraft.id) {
          setModels(response.models);
          if (!response.models.some((model) => model.id === draft.agent.model)) {
            setDraft({
              ...draft,
              agent: {
                ...draft.agent,
                model: response.models[0]?.id ?? "",
              },
            });
          }
        }
      }
    } catch (caught) {
      setProviderMessage(caught instanceof Error ? caught.message : "Provider 测试失败");
    } finally {
      setIsProviderSaving(false);
    }
  };

  const handleSaveProvider = async () => {
    if (testedProviderSignature !== providerSignature(providerDraft)) {
      setProviderMessage("请先测试 Provider");
      return;
    }
    setIsProviderSaving(true);
    setProviderMessage(null);
    try {
      const payload = providerPayload();
      const savedProvider = providerDraft.id
        ? await updateModelProvider(providerDraft.id, payload)
        : await createModelProvider(payload);
      const [currentConfig, modelResponse] = await Promise.all([
        getAppConfig(),
        listProviderModels(savedProvider.id),
      ]);
      const shouldUseSavedProvider =
        providerDraft.id === null ||
        !currentConfig.settings.agent.provider_id ||
        currentConfig.settings.agent.provider_id === savedProvider.id;
      if (shouldUseSavedProvider) {
        const nextModel = modelResponse.models.some(
          (model) => model.id === currentConfig.settings.agent.model,
        )
          ? currentConfig.settings.agent.model
          : modelResponse.models[0]?.id ?? "";
        await updateAppConfig({
          ...currentConfig.settings,
          agent: {
            ...currentConfig.settings.agent,
            provider_id: savedProvider.id,
            model: nextModel,
          },
        });
      }
      await loadSettings(savedProvider.id);
      setProviderMessage("Provider 已保存");
    } catch (caught) {
      setProviderMessage(caught instanceof Error ? caught.message : "Provider 保存失败");
    } finally {
      setIsProviderSaving(false);
    }
  };

  const handleDeleteProvider = async (provider: ModelProvider) => {
    if (!window.confirm(`删除 Provider ${provider.name}？`)) {
      return;
    }
    setProviderMessage(null);
    try {
      await deleteModelProvider(provider.id);
      await loadSettings();
      setProviderMessage("Provider 已删除");
    } catch (caught) {
      setProviderMessage(caught instanceof Error ? caught.message : "Provider 删除失败");
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
      role="dialog"
      aria-modal="true"
      aria-label="应用设置"
    >
      <div className="flex h-[min(780px,calc(100vh-40px))] w-full max-w-6xl overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
        <nav className="flex w-52 shrink-0 flex-col border-r border-line bg-soft p-3">
          <div className="mb-3 flex items-center justify-between">
            <span className="text-sm font-semibold text-ink">设置</span>
            <button
              className="grid h-7 w-7 place-items-center rounded-md text-muted transition-colors hover:bg-panel hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
              type="button"
              aria-label="关闭设置"
              onClick={onClose}
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="grid gap-1">
            {tabs.map((tab) => (
              <button
                className={`rounded-md px-2.5 py-2 text-left text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 ${
                  activeTab === tab.id ? "bg-ink text-panel" : "text-muted hover:bg-panel hover:text-ink"
                }`}
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {config ? (
            <div className="mt-auto grid gap-1 border-t border-line pt-3 font-mono text-[10px] text-muted">
              <span className="truncate">config: {config.bootstrap.config_file_path}</span>
              <span className="truncate">sqlite: {config.bootstrap.database_path}</span>
            </div>
          ) : null}
        </nav>

        <section className="min-w-0 flex-1 overflow-y-auto p-5">
          {isLoading ? (
            <div className="flex items-center gap-2 text-xs text-muted">
              <Loader2 className="h-4 w-4 animate-spin" />
              加载中
            </div>
          ) : null}

          {draft ? (
            <div className="grid gap-4">
              {activeTab === "agent" ? (
                <AgentForm
                  draft={draft}
                  models={models}
                  modelMessage={modelMessage}
                  providerDraft={providerDraft}
                  providerMessage={providerMessage}
                  providers={providers}
                  isProviderSaving={isProviderSaving}
                  onChange={setDraft}
                  onCreateProvider={() => updateProviderDraft(blankProviderDraft)}
                  onDeleteProvider={handleDeleteProvider}
                  onProviderDraftChange={updateProviderDraft}
                  onSaveProvider={() => void handleSaveProvider()}
                  onSelectProviderDraft={(provider) => updateProviderDraft(providerToDraft(provider))}
                  onTestProviderDraft={() => void handleTestProviderDraft()}
                  onCopyProviderApiKey={(provider) => void handleCopyProviderApiKey(provider)}
                  testedProviderSignature={testedProviderSignature}
                />
              ) : null}
              {activeTab === "system" ? <SystemForm draft={draft} onChange={setDraft} /> : null}
              {activeTab === "logging" ? <LoggingForm draft={draft} onChange={setDraft} /> : null}
            </div>
          ) : null}

          {!isLoading && !draft && message ? (
            <StatusMessage message={message} />
          ) : null}
        </section>

        <div className="flex w-44 shrink-0 flex-col justify-between border-l border-line bg-soft p-3">
          <div className="text-xs leading-5 text-muted">
            配置保存在 SQLite；配置文件只负责定位数据库。
          </div>
          <div className="grid gap-2">
            {message ? <StatusMessage message={message} /> : null}
            <button
              className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={!draft || !draft.agent.model || isSaving}
              onClick={() => void handleSave()}
            >
              {isSaving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Save className="h-3.5 w-3.5" />}
              保存
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function AgentForm({
  draft,
  providers,
  models,
  modelMessage,
  providerDraft,
  providerMessage,
  isProviderSaving,
  onChange,
  onCreateProvider,
  onDeleteProvider,
  onProviderDraftChange,
  onSaveProvider,
  onSelectProviderDraft,
  onTestProviderDraft,
  onCopyProviderApiKey,
  testedProviderSignature,
}: {
  draft: AppSettings;
  providers: ModelProvider[];
  models: ProviderModel[];
  modelMessage: string | null;
  providerDraft: ProviderDraft;
  providerMessage: string | null;
  isProviderSaving: boolean;
  onChange: (settings: AppSettings) => void;
  onCreateProvider: () => void;
  onDeleteProvider: (provider: ModelProvider) => void;
  onProviderDraftChange: (provider: ProviderDraft) => void;
  onSaveProvider: () => void;
  onSelectProviderDraft: (provider: ModelProvider) => void;
  onTestProviderDraft: () => void;
  onCopyProviderApiKey: (provider: ModelProvider) => void;
  testedProviderSignature: string | null;
}) {
  const agent = draft.agent;
  const enabledProviders = providers.filter((provider) => provider.enabled);
  const isProviderTested = testedProviderSignature === providerSignature(providerDraft);
  return (
    <div className="grid gap-5">
      <FormSection title="Agent 模型">
        <SelectField
          label="Provider"
          value={agent.provider_id}
          options={enabledProviders.map((provider) => ({ label: provider.name, value: provider.id }))}
          onChange={(provider_id) => onChange({ ...draft, agent: { ...agent, provider_id } })}
        />
        <SelectField
          label="模型"
          value={agent.model}
          disabled={models.length === 0}
          options={models.map((model) => ({ label: model.name, value: model.id }))}
          placeholder={models.length === 0 ? agent.model || "先测试 Provider 获取模型" : undefined}
          onChange={(model) => onChange({ ...draft, agent: { ...agent, model } })}
        />
        {modelMessage ? <StatusMessage message={modelMessage} /> : null}
      </FormSection>

      <div className="grid gap-3 border-t border-line pt-4">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">模型供应商</h2>
          <button
            className="inline-flex h-8 items-center justify-center gap-1.5 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink"
            type="button"
            onClick={onCreateProvider}
          >
            <Plus className="h-3.5 w-3.5" />
            新增
          </button>
        </div>

        <div className="grid gap-2">
          {providerDraft.id === null ? (
            <ProviderEditorCard
              provider={null}
              providerDraft={providerDraft}
              providerMessage={providerMessage}
              isActive={false}
              isProviderSaving={isProviderSaving}
              isProviderTested={isProviderTested}
              onDeleteProvider={onDeleteProvider}
              onProviderDraftChange={onProviderDraftChange}
              onSaveProvider={onSaveProvider}
              onSelectProviderDraft={onSelectProviderDraft}
              onTestProviderDraft={onTestProviderDraft}
              onCopyProviderApiKey={onCopyProviderApiKey}
              onUseProvider={(provider) =>
                onChange({ ...draft, agent: { ...agent, provider_id: provider.id } })
              }
            />
          ) : null}
            {providers.map((provider) => (
              <ProviderEditorCard
                isActive={provider.id === agent.provider_id}
                isProviderSaving={isProviderSaving}
                isProviderTested={isProviderTested}
                key={provider.id}
                provider={provider}
                providerDraft={providerDraft}
                providerMessage={providerDraft.id === provider.id ? providerMessage : null}
                onDeleteProvider={onDeleteProvider}
                onProviderDraftChange={onProviderDraftChange}
                onSaveProvider={onSaveProvider}
                onSelectProviderDraft={onSelectProviderDraft}
                onTestProviderDraft={onTestProviderDraft}
                onCopyProviderApiKey={onCopyProviderApiKey}
                onUseProvider={(provider) =>
                  onChange({ ...draft, agent: { ...agent, provider_id: provider.id } })
                }
              />
            ))}
        </div>
      </div>

      <FormSection title="Agent 参数">
        <NumberField label="最大轮数" value={agent.max_turns} onChange={(max_turns) => onChange({ ...draft, agent: { ...agent, max_turns } })} />
        <NumberField label="执行超时 秒" value={agent.turn_timeout_seconds} onChange={(turn_timeout_seconds) => onChange({ ...draft, agent: { ...agent, turn_timeout_seconds } })} />
        <NumberField label="首包超时 秒" value={agent.first_token_timeout_seconds} onChange={(first_token_timeout_seconds) => onChange({ ...draft, agent: { ...agent, first_token_timeout_seconds } })} />
        <SelectField label="思考模式" value={agent.thinking.type} options={["disabled", "adaptive", "enabled"]} onChange={(type) => onChange({ ...draft, agent: { ...agent, thinking: { ...agent.thinking, type: type as AppSettings["agent"]["thinking"]["type"] } } })} />
        <NumberField label="思考预算" value={agent.thinking.budget_tokens} onChange={(budget_tokens) => onChange({ ...draft, agent: { ...agent, thinking: { ...agent.thinking, budget_tokens } } })} />
        <ToggleField label="保留增量消息" checked={agent.include_partial_messages} onChange={(include_partial_messages) => onChange({ ...draft, agent: { ...agent, include_partial_messages } })} />
        <ListField label="可用工具" value={agent.available_tools} onChange={(available_tools) => onChange({ ...draft, agent: { ...agent, available_tools } })} />
        <ListField label="环境变量白名单" value={agent.env_allowlist} onChange={(env_allowlist) => onChange({ ...draft, agent: { ...agent, env_allowlist } })} />
      </FormSection>
    </div>
  );
}

function ProviderEditorCard({
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
  onUseProvider,
}: {
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
  onUseProvider: (provider: ModelProvider) => void;
}) {
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
            selected
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
            onCopy={
              provider?.has_api_key
                ? () => onCopyProviderApiKey(provider)
                : undefined
            }
          />
          <ToggleField
            label="启用"
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
              {isProviderSaving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <PlugZap className="h-3.5 w-3.5" />}
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
            <span className="ml-auto font-mono text-[10px] text-muted">key saved</span>
          ) : null}
        </div>
      )}
    </div>
  );
}

function SystemForm({ draft, onChange }: { draft: AppSettings; onChange: (settings: AppSettings) => void }) {
  const system = draft.system;
  return (
    <FormSection title="系统">
      <SelectField label="运行环境" value={system.environment} options={["development", "desktop", "production"]} onChange={(environment) => onChange({ ...draft, system: { ...system, environment: environment as AppSettings["system"]["environment"] } })} />
      <ToggleField label="访问日志" checked={system.access_log_enabled} onChange={(access_log_enabled) => onChange({ ...draft, system: { ...system, access_log_enabled } })} />
      <NumberField label="慢请求阈值 ms" value={system.access_log_slow_threshold_ms} onChange={(access_log_slow_threshold_ms) => onChange({ ...draft, system: { ...system, access_log_slow_threshold_ms } })} />
      <ListField label="CORS 来源" value={system.cors_origins} onChange={(cors_origins) => onChange({ ...draft, system: { ...system, cors_origins } })} />
    </FormSection>
  );
}

function LoggingForm({ draft, onChange }: { draft: AppSettings; onChange: (settings: AppSettings) => void }) {
  const logging = draft.logging;
  return (
    <FormSection title="日志">
      <SelectField label="级别" value={logging.level} options={["DEBUG", "INFO", "WARNING", "ERROR"]} onChange={(level) => onChange({ ...draft, logging: { ...logging, level: level as AppSettings["logging"]["level"] } })} />
      <SelectField label="格式" value={logging.format} options={["text", "json"]} onChange={(format) => onChange({ ...draft, logging: { ...logging, format: format as AppSettings["logging"]["format"] } })} />
    </FormSection>
  );
}

function FormSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div>
      <h2 className="mb-3 text-sm font-semibold text-ink">{title}</h2>
      <div className="grid gap-3 sm:grid-cols-2">{children}</div>
    </div>
  );
}

function TextField({ label, value, onChange, type = "text" }: { label: string; value: string; onChange: (value: string) => void; type?: "text" | "password" }) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <input className="h-9 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal" type={type} value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function ApiKeyField({
  hasSavedApiKey,
  value,
  onChange,
  onCopy,
}: {
  hasSavedApiKey: boolean;
  value: string | null;
  onChange: (value: string | null) => void;
  onCopy?: () => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const displayValue = value ?? (hasSavedApiKey && !isEditing ? "***" : "");
  const isShowingSavedMask = value === null && hasSavedApiKey && !isEditing;
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">API Key</span>
      <span className="flex h-9 items-center rounded-md border border-line bg-panel focus-within:border-signal">
        <input
          className="min-w-0 flex-1 bg-transparent px-2.5 text-xs text-ink outline-none"
          type={isShowingSavedMask ? "text" : "password"}
          value={displayValue}
          onFocus={() => setIsEditing(true)}
          onBlur={() => {
            if (!value) {
              setIsEditing(false);
            }
          }}
          onChange={(event) => onChange(emptyToNull(event.target.value))}
        />
        {onCopy ? (
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            title="复制 API Key"
            aria-label="复制 API Key"
            onClick={onCopy}
          >
            <Copy className="h-3.5 w-3.5" />
          </button>
        ) : null}
      </span>
    </label>
  );
}

function NumberField({ label, value, onChange }: { label: string; value: number; onChange: (value: number) => void }) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <input className="h-9 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal" min={0} type="number" value={value} onChange={(event) => onChange(Number(event.target.value))} />
    </label>
  );
}

function SelectField({
  label,
  value,
  options,
  onChange,
  disabled = false,
  placeholder,
}: {
  label: string;
  value: string;
  options: string[] | Array<{ label: string; value: string }>;
  onChange: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
}) {
  const normalizedOptions = options.map((option) =>
    typeof option === "string" ? { label: option, value: option } : option,
  );
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <select
        className="h-9 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
        value={disabled && placeholder ? "" : value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
      >
        {placeholder ? <option value="">{placeholder}</option> : null}
        {normalizedOptions.map((option) => (
          <option key={option.value} value={option.value}>{option.label}</option>
        ))}
      </select>
    </label>
  );
}

function ToggleField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex h-9 items-center gap-2 rounded-md border border-line bg-panel px-2.5 text-xs font-semibold text-graphite">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      {label}
    </label>
  );
}

function ListField({ label, value, onChange }: { label: string; value: string[]; onChange: (value: string[]) => void }) {
  return (
    <label className="grid gap-1.5 sm:col-span-2">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <textarea className="min-h-20 rounded-md border border-line bg-panel px-2.5 py-2 text-xs leading-5 text-ink outline-none focus:border-signal" value={value.join("\n")} onChange={(event) => onChange(linesToList(event.target.value))} />
    </label>
  );
}

function StatusMessage({ message }: { message: string }) {
  const isSaved = message.includes("已");
  return (
    <div className="rounded-md border border-line bg-panel px-2.5 py-2 text-xs text-muted">
      {isSaved ? (
        <span className="inline-flex items-center gap-1 text-brand">
          <Check className="h-3.5 w-3.5" />
          {message}
        </span>
      ) : (
        message
      )}
    </div>
  );
}

function providerToDraft(provider: ModelProvider): ProviderDraft {
  return {
    id: provider.id,
    name: provider.name,
    base_url: provider.base_url,
    api_key: null,
    enabled: provider.enabled,
  };
}

function emptyToNull(value: string): string | null {
  return value.trim() ? value : null;
}

function providerSignature(provider: ProviderDraft): string {
  return JSON.stringify({
    id: provider.id,
    name: provider.name.trim(),
    base_url: provider.base_url ?? null,
    api_key: provider.api_key ?? null,
    enabled: provider.enabled,
  });
}

function linesToList(value: string): string[] {
  return value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}
