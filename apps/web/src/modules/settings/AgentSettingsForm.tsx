import { Plus } from "lucide-react";

import type { AppSettings, ModelProvider, ProviderModel } from "../../shared/api";
import {
  ChipListField,
  FormSection,
  NumberField,
  SelectField,
  StatusMessage,
  ToggleField,
} from "./SettingsFields";
import { ProviderEditorCard } from "./ProviderEditorCard";
import { providerSignature } from "./settingsUtils";
import type { ProviderDraft, ProviderTestResult } from "./types";

type AgentSettingsFormProps = {
  draft: AppSettings;
  providers: ModelProvider[];
  models: ProviderModel[];
  modelMessage: string | null;
  providerDraft: ProviderDraft;
  providerMessage: string | null;
  availableToolOptions: string[];
  isProviderSaving: boolean;
  testedProviderSignature: string | null;
  providerTestResult: ProviderTestResult | null;
  onChange: (settings: AppSettings) => void;
  onCreateProvider: () => void;
  onDeleteProvider: (provider: ModelProvider) => void;
  onProviderDraftChange: (provider: ProviderDraft) => void;
  onSaveProvider: () => void;
  onSelectProviderDraft: (provider: ModelProvider) => void;
  onTestProviderDraft: () => void;
  onCopyProviderApiKey: (provider: ModelProvider) => void;
  onCloseProviderTestResult: () => void;
};

export function AgentSettingsForm({
  draft,
  providers,
  models,
  modelMessage,
  providerDraft,
  providerMessage,
  availableToolOptions,
  isProviderSaving,
  testedProviderSignature,
  providerTestResult,
  onChange,
  onCreateProvider,
  onDeleteProvider,
  onProviderDraftChange,
  onSaveProvider,
  onSelectProviderDraft,
  onTestProviderDraft,
  onCopyProviderApiKey,
  onCloseProviderTestResult,
}: AgentSettingsFormProps) {
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
              onCloseProviderTestResult={onCloseProviderTestResult}
              testResult={providerTestResult}
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
              onCloseProviderTestResult={onCloseProviderTestResult}
              testResult={providerDraft.id === provider.id ? providerTestResult : null}
              onUseProvider={(provider) =>
                onChange({ ...draft, agent: { ...agent, provider_id: provider.id } })
              }
            />
          ))}
        </div>
      </div>

      <FormSection title="Agent 参数">
        <NumberField
          label="最大轮数"
          value={agent.max_turns}
          onChange={(max_turns) => onChange({ ...draft, agent: { ...agent, max_turns } })}
        />
        <NumberField
          label="执行超时 秒"
          value={agent.turn_timeout_seconds}
          onChange={(turn_timeout_seconds) =>
            onChange({ ...draft, agent: { ...agent, turn_timeout_seconds } })
          }
        />
        <NumberField
          label="首包超时 秒"
          value={agent.first_token_timeout_seconds}
          onChange={(first_token_timeout_seconds) =>
            onChange({ ...draft, agent: { ...agent, first_token_timeout_seconds } })
          }
        />
        <SelectField
          label="思考模式"
          value={agent.thinking.type}
          options={["disabled", "adaptive", "enabled"]}
          onChange={(type) =>
            onChange({
              ...draft,
              agent: {
                ...agent,
                thinking: {
                  ...agent.thinking,
                  type: type as AppSettings["agent"]["thinking"]["type"],
                },
              },
            })
          }
        />
        <NumberField
          label="思考预算"
          value={agent.thinking.budget_tokens}
          onChange={(budget_tokens) =>
            onChange({
              ...draft,
              agent: {
                ...agent,
                thinking: { ...agent.thinking, budget_tokens },
              },
            })
          }
        />
        <ToggleField
          label="保留增量消息"
          description="保存模型流式输出中的中间片段，便于排查运行过程。"
          checked={agent.include_partial_messages}
          onChange={(include_partial_messages) =>
            onChange({ ...draft, agent: { ...agent, include_partial_messages } })
          }
        />
        <ChipListField
          label="可用工具"
          value={agent.available_tools}
          options={availableToolOptions}
          onChange={(available_tools) =>
            onChange({ ...draft, agent: { ...agent, available_tools } })
          }
        />
      </FormSection>
    </div>
  );
}
