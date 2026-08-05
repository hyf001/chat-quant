import { Check, Loader2, Save, X } from "lucide-react";
import { useEffect, useState } from "react";

import {
  getAppConfig,
  updateAppConfig,
  type AppConfig,
  type AppSettings,
} from "../../shared/api";

type AppSettingsDialogProps = {
  isOpen: boolean;
  onClose: () => void;
};

type SettingsTab = "agent" | "paths" | "identity" | "system" | "logging";

const tabs: Array<{ id: SettingsTab; label: string }> = [
  { id: "agent", label: "Agent" },
  { id: "paths", label: "路径" },
  { id: "identity", label: "身份" },
  { id: "system", label: "系统" },
  { id: "logging", label: "日志" },
];

export function AppSettingsDialog({ isOpen, onClose }: AppSettingsDialogProps) {
  const [activeTab, setActiveTab] = useState<SettingsTab>("agent");
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [draft, setDraft] = useState<AppSettings | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!isOpen) {
      return;
    }
    setIsLoading(true);
    setMessage(null);
    getAppConfig()
      .then((nextConfig) => {
        setConfig(nextConfig);
        setDraft(nextConfig.settings);
      })
      .catch((caught) => {
        setMessage(caught instanceof Error ? caught.message : "设置加载失败");
      })
      .finally(() => setIsLoading(false));
  }, [isOpen]);

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
      setConfig(nextConfig);
      setDraft(nextConfig.settings);
      setMessage("已保存");
    } catch (caught) {
      setMessage(caught instanceof Error ? caught.message : "保存失败");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
      role="dialog"
      aria-modal="true"
      aria-label="应用设置"
    >
      <div className="flex h-[min(760px,calc(100vh-40px))] w-full max-w-5xl overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
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
              {activeTab === "agent" ? <AgentForm draft={draft} onChange={setDraft} /> : null}
              {activeTab === "paths" ? <PathForm draft={draft} onChange={setDraft} /> : null}
              {activeTab === "identity" ? <IdentityForm draft={draft} onChange={setDraft} /> : null}
              {activeTab === "system" ? <SystemForm draft={draft} onChange={setDraft} /> : null}
              {activeTab === "logging" ? <LoggingForm draft={draft} onChange={setDraft} /> : null}
            </div>
          ) : null}
        </section>

        <div className="flex w-44 shrink-0 flex-col justify-between border-l border-line bg-soft p-3">
          <div className="text-xs leading-5 text-muted">
            配置保存在 SQLite 的结构化设置表中；配置文件只负责定位数据库。
          </div>
          <div className="grid gap-2">
            {message ? (
              <div className="rounded-md border border-line bg-panel px-2.5 py-2 text-xs text-muted">
                {message === "已保存" ? (
                  <span className="inline-flex items-center gap-1 text-brand">
                    <Check className="h-3.5 w-3.5" />
                    已保存
                  </span>
                ) : (
                  message
                )}
              </div>
            ) : null}
            <button
              className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25 disabled:cursor-not-allowed disabled:opacity-60"
              type="button"
              disabled={!draft || isSaving}
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
  onChange,
}: {
  draft: AppSettings;
  onChange: (settings: AppSettings) => void;
}) {
  const agent = draft.agent;
  return (
    <FormSection title="Agent">
      <TextField label="模型" value={agent.model} onChange={(model) => onChange({ ...draft, agent: { ...agent, model } })} />
      <TextField label="Base URL" value={agent.base_url ?? ""} onChange={(base_url) => onChange({ ...draft, agent: { ...agent, base_url: emptyToNull(base_url) } })} />
      <TextField label="Token" type="password" value={agent.api_token ?? ""} onChange={(api_token) => onChange({ ...draft, agent: { ...agent, api_token: emptyToNull(api_token) } })} />
      <NumberField label="最大轮数" value={agent.max_turns} onChange={(max_turns) => onChange({ ...draft, agent: { ...agent, max_turns } })} />
      <NumberField label="执行超时 秒" value={agent.turn_timeout_seconds} onChange={(turn_timeout_seconds) => onChange({ ...draft, agent: { ...agent, turn_timeout_seconds } })} />
      <NumberField label="首包超时 秒" value={agent.first_token_timeout_seconds} onChange={(first_token_timeout_seconds) => onChange({ ...draft, agent: { ...agent, first_token_timeout_seconds } })} />
      <TextField label="插件目录" value={agent.skill_plugin_dir} onChange={(skill_plugin_dir) => onChange({ ...draft, agent: { ...agent, skill_plugin_dir } })} />
      <TextField label="插件名" value={agent.skill_plugin_name} onChange={(skill_plugin_name) => onChange({ ...draft, agent: { ...agent, skill_plugin_name } })} />
      <SelectField label="思考模式" value={agent.thinking.type} options={["disabled", "adaptive", "enabled"]} onChange={(type) => onChange({ ...draft, agent: { ...agent, thinking: { ...agent.thinking, type: type as AppSettings["agent"]["thinking"]["type"] } } })} />
      <NumberField label="思考预算" value={agent.thinking.budget_tokens} onChange={(budget_tokens) => onChange({ ...draft, agent: { ...agent, thinking: { ...agent.thinking, budget_tokens } } })} />
      <ToggleField label="保留增量消息" checked={agent.include_partial_messages} onChange={(include_partial_messages) => onChange({ ...draft, agent: { ...agent, include_partial_messages } })} />
      <ListField label="默认工具" value={agent.allowed_tools_default} onChange={(allowed_tools_default) => onChange({ ...draft, agent: { ...agent, allowed_tools_default } })} />
      <ListField label="环境变量白名单" value={agent.env_allowlist} onChange={(env_allowlist) => onChange({ ...draft, agent: { ...agent, env_allowlist } })} />
    </FormSection>
  );
}

function PathForm({ draft, onChange }: { draft: AppSettings; onChange: (settings: AppSettings) => void }) {
  const paths = draft.paths;
  return (
    <FormSection title="路径">
      <TextField label="项目目录" value={paths.project_home ?? ""} onChange={(project_home) => onChange({ ...draft, paths: { ...paths, project_home: emptyToNull(project_home) } })} />
      <TextField label="Agent 工作目录" value={paths.claude_agent_cwd ?? ""} onChange={(claude_agent_cwd) => onChange({ ...draft, paths: { ...paths, claude_agent_cwd: emptyToNull(claude_agent_cwd) } })} />
    </FormSection>
  );
}

function IdentityForm({ draft, onChange }: { draft: AppSettings; onChange: (settings: AppSettings) => void }) {
  const identity = draft.identity;
  return (
    <FormSection title="身份">
      <TextField label="默认用户" value={identity.default_user_id} onChange={(default_user_id) => onChange({ ...draft, identity: { ...identity, default_user_id } })} />
      <TextField label="默认项目" value={identity.default_project_id} onChange={(default_project_id) => onChange({ ...draft, identity: { ...identity, default_project_id } })} />
    </FormSection>
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

function FormSection({ title, children }: { title: string; children: React.ReactNode }) {
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

function NumberField({ label, value, onChange }: { label: string; value: number; onChange: (value: number) => void }) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <input className="h-9 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal" min={0} type="number" value={value} onChange={(event) => onChange(Number(event.target.value))} />
    </label>
  );
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-graphite">{label}</span>
      <select className="h-9 rounded-md border border-line bg-panel px-2.5 text-xs text-ink outline-none focus:border-signal" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>{option}</option>
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

function emptyToNull(value: string): string | null {
  return value.trim() ? value : null;
}

function linesToList(value: string): string[] {
  return value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}
