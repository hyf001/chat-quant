import {
  ArrowLeft,
  Loader2,
} from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { AgentSettingsForm } from "../modules/settings/AgentSettingsForm";
import { DataSourceSettingsForm } from "../modules/settings/DataSourceSettingsForm";
import { LoggingSettingsForm } from "../modules/settings/LoggingSettingsForm";
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
  type AppSettingsUpdate,
  type ModelProvider,
  type ModelProviderPayload,
  type ProviderModel,
} from "../shared/api";

type AppSettingsPageProps = {
  onBack: () => void;
};

type ToastState = {
  message: string;
  tone: "success" | "error" | "info";
};

const tabs: Array<{ id: SettingsTab; label: string }> = [
  { id: "agent", label: "Agent" },
  { id: "system", label: "系统" },
  { id: "logging", label: "日志" },
  { id: "data", label: "数据源" },
];

export function AppSettingsPage({ onBack }: AppSettingsPageProps) {
  const [activeTab, setActiveTab] = useState<SettingsTab>("agent");
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [draft, setDraft] = useState<AppSettings | null>(null);
  const [providers, setProviders] = useState<ModelProvider[]>([]);
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [providerDraft, setProviderDraft] = useState<ProviderDraft>(blankProviderDraft);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoggingSaving, setIsLoggingSaving] = useState(false);
  const [isProviderSaving, setIsProviderSaving] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);
  const [testedProviderSignature, setTestedProviderSignature] = useState<string | null>(null);
  const [providerTestResult, setProviderTestResult] = useState<ProviderTestResult | null>(null);
  const modelRequestSeqRef = useRef(0);

  const showToast = useCallback((message: string, tone: ToastState["tone"] = "info") => {
    setToast({ message, tone });
  }, []);

  const loadProviderModels = useCallback(async (providerId: string) => {
    const requestSeq = modelRequestSeqRef.current + 1;
    modelRequestSeqRef.current = requestSeq;
    try {
      const response = await listProviderModels(providerId);
      const isCurrent = requestSeq === modelRequestSeqRef.current;
      if (isCurrent) {
        setModels(response.models);
      }
      return { models: response.models, isCurrent };
    } catch (caught) {
      const isCurrent = requestSeq === modelRequestSeqRef.current;
      if (isCurrent) {
        setModels([]);
        showToast(
          `模型列表加载失败：${caught instanceof Error ? caught.message : "Provider 不可用"}`,
          "error",
        );
      }
      return { models: [], isCurrent };
    }
  }, [showToast]);

  const loadSettings = useCallback(async (selectedProviderId?: string | null) => {
    setIsLoading(true);
    setToast(null);
    try {
      const [nextConfig, providerResponse] = await Promise.all([
        getAppConfig(),
        listModelProviders(),
      ]);
      const providerId = nextConfig.settings.agent.provider_id;
      const modelLoadResult = providerId
        ? await loadProviderModels(providerId)
        : { models: [], isCurrent: true };
      const nextModels = modelLoadResult.models;
      const nextSettings =
        modelLoadResult.isCurrent &&
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
      if (!providerId) {
        setModels([]);
      }
      setProviderDraft(selectedProvider ? providerToDraft(selectedProvider) : blankProviderDraft);
      setTestedProviderSignature(null);
      return {
        config: nextConfig,
        providers: providerResponse.providers,
        models: modelLoadResult.isCurrent ? nextModels : [],
      };
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "设置加载失败", "error");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [loadProviderModels]);

  useEffect(() => {
    void loadSettings();
  }, [loadSettings]);

  useEffect(() => {
    if (!toast) {
      return;
    }
    const timeoutId = window.setTimeout(() => setToast(null), 2500);
    return () => window.clearTimeout(timeoutId);
  }, [toast]);

  useEffect(() => {
    const providerId = draft?.agent.provider_id;
    if (!providerId) {
      modelRequestSeqRef.current += 1;
      setModels([]);
      return;
    }
    setModels([]);
    loadProviderModels(providerId)
      .then(({ models: nextModels, isCurrent }) => {
        if (!isCurrent) {
          return;
        }
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

  const saveSettingsPatch = async (patch: AppSettingsUpdate, successMessage: string) => {
    const nextConfig = await updateAppConfig(patch);
    setConfig(nextConfig);
    setDraft((current) => {
      if (!current) {
        return nextConfig.settings;
      }
      return {
        ...current,
        system: patch.system ? nextConfig.settings.system : current.system,
        logging: patch.logging ? nextConfig.settings.logging : current.logging,
        mindgo: patch.mindgo ? nextConfig.settings.mindgo : current.mindgo,
        agent: patch.agent
          ? {
              ...current.agent,
              ...patch.agent,
              thinking: patch.agent.thinking
                ? {
                    ...current.agent.thinking,
                    ...patch.agent.thinking,
                  }
                : current.agent.thinking,
            }
          : current.agent,
      };
    });
    showToast(successMessage, "success");
    return nextConfig;
  };

  const saveSettingsField = async (patch: AppSettingsUpdate, successMessage: string) => {
    try {
      await saveSettingsPatch(patch, successMessage);
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "设置保存失败", "error");
    }
  };

  const handleSaveLogging = async (logging: AppSettings["logging"]) => {
    setIsLoggingSaving(true);
    try {
      await saveSettingsPatch({ logging: { level: logging.level } }, "日志级别已保存");
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "日志设置保存失败", "error");
    } finally {
      setIsLoggingSaving(false);
    }
  };

  const updateProviderDraft = (nextDraft: ProviderDraft) => {
    setProviderDraft(nextDraft);
    setToast(null);
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
    try {
      const response = await getModelProviderApiKey(provider.id);
      if (!response.api_key) {
        showToast("API Key 为空", "info");
        return;
      }
      await navigator.clipboard.writeText(response.api_key);
      showToast("API Key 已复制", "success");
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "API Key 复制失败", "error");
    }
  };

  const handleTestProviderDraft = async () => {
    setIsProviderSaving(true);
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
      showToast("请先测试 Provider", "info");
      return;
    }
    setIsProviderSaving(true);
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
          agent: {
            ...currentConfig.settings.agent,
            provider_id: savedProvider.id,
            model: nextModel,
          },
        });
      }
      await loadSettings(savedProvider.id);
      showToast("Provider 已保存", "success");
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "Provider 保存失败", "error");
    } finally {
      setIsProviderSaving(false);
    }
  };

  const handleDeleteProvider = async (provider: ModelProvider) => {
    if (!window.confirm(`删除 Provider ${provider.name}？`)) {
      return;
    }
    try {
      await deleteModelProvider(provider.id);
      await loadSettings();
      showToast("Provider 已删除", "success");
    } catch (caught) {
      showToast(caught instanceof Error ? caught.message : "Provider 删除失败", "error");
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
              管理模型供应商、Agent 参数、运行日志和数据源。
            </p>
          </div>
        </div>
      </header>

      <div className="grid gap-4 xl:grid-cols-[220px_minmax(0,1fr)]">
        <nav className="grid gap-3 rounded-lg border border-line bg-soft p-3 xl:sticky xl:top-0 xl:self-start">
          <div className="grid grid-cols-2 gap-1 sm:grid-cols-4 xl:grid-cols-1">
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
                  providerDraft={providerDraft}
                  providers={providers}
                  availableToolOptions={availableToolOptions}
                  isProviderSaving={isProviderSaving}
                  onChange={setDraft}
                  onSaveAgentField={(patch, saveMessage) =>
                    void saveSettingsField({ agent: patch }, saveMessage)
                  }
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
                <SystemSettingsForm
                  draft={draft}
                  onChange={setDraft}
                  onSaveSystemField={(patch, saveMessage) =>
                    void saveSettingsField({ system: patch }, saveMessage)
                  }
                />
              ) : null}
              {activeTab === "logging" ? (
                <LoggingSettingsForm
                  draft={draft}
                  isLoggingSaving={isLoggingSaving}
                  onChange={setDraft}
                  onLoggingChange={(logging) => void handleSaveLogging(logging)}
                />
              ) : null}
              {activeTab === "data" ? (
                <DataSourceSettingsForm
                  draft={draft}
                  onChange={setDraft}
                  onSaveMindgoSettings={(mindgo, message) =>
                    void saveSettingsField({ mindgo }, message)
                  }
                  onToast={showToast}
                />
              ) : null}
            </div>
          ) : null}

          <div className="pb-4 text-xs leading-5 text-muted">
            配置保存在 SQLite；配置文件只负责定位数据库。
          </div>
        </div>
      </div>

      {toast ? <SettingsToast toast={toast} /> : null}
    </section>
  );
}

function SettingsToast({ toast }: { toast: ToastState }) {
  const toneClass =
    toast.tone === "success"
      ? "border-brand/25 bg-gainSoft text-brand"
      : toast.tone === "error"
        ? "border-risk/25 bg-riskSoft text-risk"
        : "border-line bg-panel text-muted";

  return (
    <div
      className={`fixed right-4 top-4 z-50 max-w-sm rounded-md border px-3 py-2 text-xs shadow-xl ${toneClass}`}
      role="status"
      aria-live="polite"
    >
      {toast.message}
    </div>
  );
}
