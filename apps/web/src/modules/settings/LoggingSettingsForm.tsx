import { RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

import { listSystemLogs, type AppSettings, type LogCategory, type LogEntry } from "../../shared/api";
import { FormSection, SelectField } from "./SettingsFields";

type LoggingSettingsFormProps = {
  draft: AppSettings;
  isLoggingSaving: boolean;
  onChange: (settings: AppSettings) => void;
  onLoggingChange: (logging: AppSettings["logging"]) => void;
};

const logCategoryOptions: Array<{ label: string; value: LogCategory }> = [
  { label: "访问日志", value: "access" },
  { label: "业务执行日志", value: "business" },
];

export function LoggingSettingsForm({
  draft,
  isLoggingSaving,
  onChange,
  onLoggingChange,
}: LoggingSettingsFormProps) {
  const logging = draft.logging;
  const [activeLogCategory, setActiveLogCategory] = useState<LogCategory>("access");
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLoadingLogs, setIsLoadingLogs] = useState(false);
  const [logError, setLogError] = useState<string | null>(null);

  const loadLogs = useCallback(async (category: LogCategory) => {
    setIsLoadingLogs(true);
    setLogError(null);
    try {
      const response = await listSystemLogs(120, category);
      setLogs(response.items.slice().reverse());
    } catch (caught) {
      setLogError(caught instanceof Error ? caught.message : "日志加载失败");
    } finally {
      setIsLoadingLogs(false);
    }
  }, []);

  useEffect(() => {
    void loadLogs(activeLogCategory);
  }, [activeLogCategory, loadLogs]);

  return (
    <div className="grid gap-5">
      <FormSection title="日志设置">
        <SelectField
          label="级别"
          value={logging.level}
          disabled={isLoggingSaving}
          options={["DEBUG", "INFO", "WARNING", "ERROR"]}
          onChange={(level) => {
            const nextLogging = {
              ...logging,
              level: level as AppSettings["logging"]["level"],
            };
            onChange({
              ...draft,
              logging: nextLogging,
            });
            onLoggingChange(nextLogging);
          }}
        />
      </FormSection>

      <section className="grid gap-3 border-t border-line pt-4" aria-label="日志查看">
        <div className="grid gap-3 sm:grid-cols-[minmax(220px,320px)_auto] sm:items-end sm:justify-between">
          <SelectField
            label="日志查看"
            value={activeLogCategory}
            options={logCategoryOptions}
            onChange={(category) => setActiveLogCategory(category as LogCategory)}
          />
          <Button
            className="h-10"
            size="sm"
            variant="outline"
            type="button"
            disabled={isLoadingLogs}
            onClick={() => void loadLogs(activeLogCategory)}
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isLoadingLogs ? "animate-spin" : ""}`} />
            刷新
          </Button>
        </div>
        <LogPanel
          logs={logs}
          isLoading={isLoadingLogs}
          error={logError}
        />
      </section>
    </div>
  );
}

function LogPanel({
  logs,
  isLoading,
  error,
}: {
  logs: LogEntry[];
  isLoading: boolean;
  error: string | null;
}) {
  return (
    <div className="grid min-w-0 gap-3">
      {error ? (
        <div className="rounded-md border border-risk/30 bg-riskSoft px-3 py-2 text-xs text-risk">
          {error}
        </div>
      ) : null}

      <div className="max-h-[520px] min-h-60 overflow-auto rounded-md border border-line bg-[#171a16]">
        {logs.length === 0 && !isLoading ? (
          <div className="px-3 py-6 text-center text-xs text-panel/55">暂无日志</div>
        ) : null}
        {logs.map((entry, index) => (
          <LogRow entry={entry} key={`${entry.timestamp}-${entry.logger}-${index}`} />
        ))}
      </div>
    </div>
  );
}

function LogRow({ entry }: { entry: LogEntry }) {
  return (
    <article className="grid gap-1 border-b border-white/10 px-3 py-2 last:border-b-0">
      <div className="flex flex-wrap items-center gap-2 font-mono text-[10px] text-panel/55">
        <span>{formatLogTime(entry.timestamp)}</span>
        <span className={logLevelClass(entry.level)}>{entry.level}</span>
        <span>{entry.logger}</span>
        {entry.method ? <span>{entry.method}</span> : null}
        {entry.path ? <span>{entry.path}</span> : null}
        {entry.status_code ? <span>{entry.status_code}</span> : null}
        {entry.duration_ms ? <span>{entry.duration_ms}ms</span> : null}
        {entry.client_host ? <span>{entry.client_host}</span> : null}
        {entry.request_id && entry.request_id !== "-" ? <span>{entry.request_id}</span> : null}
      </div>
      <p className="whitespace-pre-wrap break-words font-mono text-xs leading-5 text-panel">
        {entry.message}
      </p>
      {entry.error ? (
        <p className="whitespace-pre-wrap break-words font-mono text-[11px] leading-5 text-riskSoft">
          {entry.error}
        </p>
      ) : null}
      {entry.exception ? (
        <pre className="overflow-auto whitespace-pre-wrap rounded bg-black/30 p-2 font-mono text-[11px] leading-5 text-riskSoft">
          {entry.exception}
        </pre>
      ) : null}
      {entry.stack ? (
        <pre className="overflow-auto whitespace-pre-wrap rounded bg-black/30 p-2 font-mono text-[11px] leading-5 text-riskSoft">
          {entry.stack}
        </pre>
      ) : null}
    </article>
  );
}

function formatLogTime(timestamp: string): string {
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return timestamp;
  }
  return date.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

function logLevelClass(level: string): string {
  if (level === "ERROR" || level === "CRITICAL") {
    return "rounded bg-risk/20 px-1.5 py-0.5 text-riskSoft";
  }
  if (level === "WARNING") {
    return "rounded bg-signal/20 px-1.5 py-0.5 text-signal";
  }
  if (level === "DEBUG") {
    return "rounded bg-brandBlue/25 px-1.5 py-0.5 text-[#9cc8ed]";
  }
  return "rounded bg-brand/25 px-1.5 py-0.5 text-[#9ce6c9]";
}
