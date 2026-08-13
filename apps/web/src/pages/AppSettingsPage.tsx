import {
  ArrowLeft,
  Loader2,
} from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { AgentSettingsForm } from "../modules/settings/AgentSettingsForm";
import { LoggingSettingsForm } from "../modules/settings/LoggingSettingsForm";
import { StatusMessage } from "../modules/settings/SettingsFields";
import { SystemSettingsForm } from "../modules/settings/SystemSettingsForm";
import {
  blankProviderDraft,
  providerSignature,
  providerToDraft,
} from "../modules/settings/settingsUtils";
import type { ProviderDraft, ProviderTestResult, SettingsTab } from "../modules/settings/types";
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
} from "../shared/api";

type AppSettingsPageProps = {
  onBack: () => void;
};

const tabs: Array<{ id: SettingsTab; label: string }> = [
  { id: "agent", label: "Agent" },
  { id: "system", label: "系统" },
  { id: "logging", label: "日志" },
];

export function AppSettingsPage({ onBack }: AppSettingsPageProps) {
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
  const [providerTestResult, setProviderTestResult] = useState<ProviderTestResult | null>(null);

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
    void loadSettings();
  }, [loadSettings]);

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

  const handleSaveLogging = async (logging: AppSettings["logging"]) => {
    setIsSaving(true);
    setMessage(null);
    try {
      const currentConfig = await getAppConfig();
      const nextConfig = await updateAppConfig({
        ...currentConfig.settings,
        logging,
      });
      await loadSettings(nextConfig.settings.agent.provider_id);
      setMessage("日志级别切换成功");
    } catch (caught) {
      setMessage(caught instanceof Error ? caught.message : "日志设置保存失败");
    } finally {
      setIsSaving(false);
    }
  };

  const updateProviderDraft = (nextDraft: ProviderDraft) => {
    setProviderDraft(nextDraft);
    setProviderMessage(null);
    setProviderTestResult(null);
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
      setProviderTestResult({
        ok: response.ok,
        message: response.message,
        modelCount: response.models.length,
      });
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
      const message = caught instanceof Error ? caught.message : "Provider 测试失败";
      setProviderTestResult({
        ok: false,
        message,
        modelCount: 0,
      });
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

  const availableToolOptions =
    config?.fields.find((field) => field.key === "agent_available_tools")?.options ?? [];

  return (
    <section className="mx-auto grid w-full max-w-7xl gap-5">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-line pb-4">
        <div className="flex min-w-0 items-center gap-3">
          <button
            className="inline-flex h-9 items-center gap-2 rounded-md border border-line bg-panel px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            onClick={onBack}
          >
            <ArrowLeft className="h-4 w-4" />
            返回
          </button>
          <div className="min-w-0">
            <h1 className="text-xl font-semibold leading-tight text-ink">设置</h1>
            <p className="mt-1 text-xs text-muted">
              管理模型供应商、Agent 参数和运行日志。
            </p>
          </div>
        </div>
        {message ? <StatusMessage message={message} /> : null}
      </header>

      <div className="grid gap-4 xl:grid-cols-[220px_minmax(0,1fr)]">
        <nav className="grid gap-3 rounded-lg border border-line bg-soft p-3 xl:sticky xl:top-0 xl:self-start">
          <div className="grid grid-cols-3 gap-1 xl:grid-cols-1">
            {tabs.map((tab) => (
              <button
                className={`rounded-md px-2.5 py-2 text-center text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 xl:text-left ${
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
            <div className="grid gap-1 border-t border-line pt-3 font-mono text-[10px] text-muted">
              <span className="truncate">config: {config.bootstrap.config_file_path}</span>
              <span className="truncate">sqlite: {config.bootstrap.database_path}</span>
            </div>
          ) : null}
        </nav>

        <div className="grid min-w-0 gap-4 pb-8">
          {isLoading ? (
            <div className="flex min-h-28 items-center gap-2 rounded-lg border border-line bg-panel px-4 text-xs text-muted">
              <Loader2 className="h-4 w-4 animate-spin" />
              加载中
            </div>
          ) : null}

          {draft ? (
            <div className="grid gap-4">
              {activeTab === "agent" ? (
                <AgentSettingsForm
                  draft={draft}
                  models={models}
                  modelMessage={modelMessage}
                  providerDraft={providerDraft}
                  providerMessage={providerMessage}
                  providers={providers}
                  availableToolOptions={availableToolOptions}
                  isProviderSaving={isProviderSaving}
                  onChange={setDraft}
                  onCreateProvider={() => updateProviderDraft(blankProviderDraft)}
                  onDeleteProvider={handleDeleteProvider}
                  onProviderDraftChange={updateProviderDraft}
                  onSaveProvider={() => void handleSaveProvider()}
                  onSelectProviderDraft={(provider) => updateProviderDraft(providerToDraft(provider))}
                  onTestProviderDraft={() => void handleTestProviderDraft()}
                  onCopyProviderApiKey={(provider) => void handleCopyProviderApiKey(provider)}
                  onCloseProviderTestResult={() => setProviderTestResult(null)}
                  testedProviderSignature={testedProviderSignature}
                  providerTestResult={providerTestResult}
                />
              ) : null}
              {activeTab === "system" ? (
                <SystemSettingsForm draft={draft} onChange={setDraft} />
              ) : null}
              {activeTab === "logging" ? (
                <LoggingSettingsForm
                  draft={draft}
                  onChange={setDraft}
                  onLoggingChange={(logging) => void handleSaveLogging(logging)}
                />
              ) : null}
            </div>
          ) : null}

          {!isLoading && !draft && message ? (
            <StatusMessage message={message} />
          ) : null}

          <div className="pb-4 text-xs leading-5 text-muted">
            配置保存在 SQLite；配置文件只负责定位数据库。
          </div>
        </div>
      </div>
    </section>
  );
}
