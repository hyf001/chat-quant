import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

import type { AppSettings, ModelProvider, ProviderModel } from "../../shared/api";
import {
  ChipListField,
  FormSection,
  NumberField,
  SelectField,
  ToggleField,
} from "./SettingsFields";
import { ProviderEditorCard } from "./ProviderEditorCard";
import { providerSignature } from "./settingsUtils";
import type { ProviderDraft, ProviderTestResult } from "./types";

type AgentFieldPatch = Partial<Omit<AppSettings["agent"], "thinking">> & {
  thinking?: Partial<AppSettings["agent"]["thinking"]>;
};

type AgentSettingsFormProps = {
  draft: AppSettings;
  providers: ModelProvider[];
  models: ProviderModel[];
  providerDraft: ProviderDraft;
  availableToolOptions: string[];
  isProviderSaving: boolean;
  testedProviderSignature: string | null;
  providerTestResult: ProviderTestResult | null;
  onChange: (settings: AppSettings) => void;
  onSaveAgentField: (patch: AgentFieldPatch, message: string) => void;
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
  providerDraft,
  availableToolOptions,
  isProviderSaving,
  testedProviderSignature,
  providerTestResult,
  onChange,
  onSaveAgentField,
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

  const updateAgent = (patch: AgentFieldPatch) =>
    onChange({
      ...draft,
      agent: {
        ...agent,
        ...patch,
        thinking: patch.thinking ? { ...agent.thinking, ...patch.thinking } : agent.thinking,
      },
    });

  const updateAndSaveAgent = (patch: AgentFieldPatch, message: string) => {
    updateAgent(patch);
    onSaveAgentField(patch, message);
  };

  return (
    <div className="grid gap-5">
      <FormSection title="Agent 模型">
        <SelectField
          label="Provider"
          value={agent.provider_id}
          options={enabledProviders.map((provider) => ({ label: provider.name, value: provider.id }))}
          onChange={(provider_id) => updateAndSaveAgent({ provider_id }, "Provider 选择已保存")}
        />
        <SelectField
          label="模型"
          value={agent.model}
          disabled={models.length === 0}
          options={models.map((model) => ({ label: model.name, value: model.id }))}
          placeholder={models.length === 0 ? agent.model || "先测试 Provider 获取模型" : undefined}
          onChange={(model) => updateAndSaveAgent({ model }, "模型已保存")}
        />
      </FormSection>

      <div className="grid gap-3 border-t border-line pt-4">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">模型供应商</h2>
          <Button
            size="sm"
            variant="outline"
            type="button"
            onClick={onCreateProvider}
          >
            <Plus className="h-3.5 w-3.5" />
            新增
          </Button>
        </div>

        <div className="grid gap-2">
          {providerDraft.id === null ? (
            <ProviderEditorCard
              provider={null}
              providerDraft={providerDraft}
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
                updateAndSaveAgent({ provider_id: provider.id }, "Provider 选择已保存")
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
              onDeleteProvider={onDeleteProvider}
              onProviderDraftChange={onProviderDraftChange}
              onSaveProvider={onSaveProvider}
              onSelectProviderDraft={onSelectProviderDraft}
              onTestProviderDraft={onTestProviderDraft}
              onCopyProviderApiKey={onCopyProviderApiKey}
              onCloseProviderTestResult={onCloseProviderTestResult}
              testResult={providerDraft.id === provider.id ? providerTestResult : null}
              onUseProvider={(provider) =>
                updateAndSaveAgent({ provider_id: provider.id }, "Provider 选择已保存")
              }
            />
          ))}
        </div>
      </div>

      <FormSection title="Agent 参数">
        <NumberField
          label="最大轮数"
          value={agent.max_turns}
          onChange={(max_turns) => updateAgent({ max_turns })}
          onCommit={() => onSaveAgentField({ max_turns: agent.max_turns }, "最大轮数已保存")}
        />
        <NumberField
          label="执行超时 秒"
          value={agent.turn_timeout_seconds}
          onChange={(turn_timeout_seconds) => updateAgent({ turn_timeout_seconds })}
          onCommit={() =>
            onSaveAgentField(
              { turn_timeout_seconds: agent.turn_timeout_seconds },
              "执行超时已保存",
            )
          }
        />
        <NumberField
          label="首包超时 秒"
          value={agent.first_token_timeout_seconds}
          onChange={(first_token_timeout_seconds) => updateAgent({ first_token_timeout_seconds })}
          onCommit={() =>
            onSaveAgentField(
              { first_token_timeout_seconds: agent.first_token_timeout_seconds },
              "首包超时已保存",
            )
          }
        />
        <SelectField
          label="思考模式"
          value={agent.thinking.type}
          options={["disabled", "adaptive", "enabled"]}
          onChange={(type) =>
            updateAndSaveAgent(
              {
                thinking: {
                  type: type as AppSettings["agent"]["thinking"]["type"],
                },
              },
              "思考模式已保存",
            )
          }
        />
        <NumberField
          label="思考预算"
          value={agent.thinking.budget_tokens}
          onChange={(budget_tokens) => updateAgent({ thinking: { budget_tokens } })}
          onCommit={() =>
            onSaveAgentField(
              { thinking: { budget_tokens: agent.thinking.budget_tokens } },
              "思考预算已保存",
            )
          }
        />
        <ToggleField
          label="保留增量消息"
          description="保存模型流式输出中的中间片段，便于排查运行过程。"
          checked={agent.include_partial_messages}
          onChange={(include_partial_messages) =>
            updateAndSaveAgent({ include_partial_messages }, "保留增量消息已保存")
          }
        />
        <ChipListField
          label="可用工具"
          value={agent.available_tools}
          options={availableToolOptions}
          onChange={(available_tools) =>
            updateAndSaveAgent({ available_tools }, "可用工具已保存")
          }
        />
      </FormSection>
    </div>
  );
}
