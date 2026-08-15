import type { AppSettings } from "../../shared/api";
import { FormSection, NumberField, SelectField, ToggleField } from "./SettingsFields";

type SystemSettingsFormProps = {
  draft: AppSettings;
  onChange: (settings: AppSettings) => void;
  onSaveSystemField: (patch: Partial<AppSettings["system"]>, message: string) => void;
};

export function SystemSettingsForm({
  draft,
  onChange,
  onSaveSystemField,
}: SystemSettingsFormProps) {
  const system = draft.system;
  const updateSystem = (patch: Partial<AppSettings["system"]>) =>
    onChange({
      ...draft,
      system: {
        ...system,
        ...patch,
      },
    });
  const updateAndSaveSystem = (patch: Partial<AppSettings["system"]>, message: string) => {
    updateSystem(patch);
    onSaveSystemField(patch, message);
  };

  return (
    <div className="grid gap-5">
      <FormSection title="系统">
        <SelectField
          label="运行环境"
          value={system.environment}
          options={["development", "desktop", "production"]}
          onChange={(environment) =>
            updateAndSaveSystem(
              { environment: environment as AppSettings["system"]["environment"] },
              "运行环境已保存",
            )
          }
        />
        <ToggleField
          label="访问日志"
          checked={system.access_log_enabled}
          onChange={(access_log_enabled) =>
            updateAndSaveSystem({ access_log_enabled }, "访问日志设置已保存")
          }
        />
        <NumberField
          label="慢请求阈值 ms"
          value={system.access_log_slow_threshold_ms}
          onChange={(access_log_slow_threshold_ms) => updateSystem({ access_log_slow_threshold_ms })}
          onCommit={() =>
            onSaveSystemField(
              { access_log_slow_threshold_ms: system.access_log_slow_threshold_ms },
              "慢请求阈值已保存",
            )
          }
        />
      </FormSection>

      <FormSection title="Worker Runtime">
        <div className="rounded-md border border-line bg-soft px-3 py-2 text-xs leading-5 text-muted sm:col-span-2">
          这些参数保存后需要重启 API 才会生效。
        </div>
        <NumberField
          label="实例创建扫描粒度 min"
          value={system.job_runtime_creation_tick_minutes}
          min={1}
          onChange={(job_runtime_creation_tick_minutes) =>
            updateSystem({ job_runtime_creation_tick_minutes })
          }
          onCommit={() =>
            onSaveSystemField(
              { job_runtime_creation_tick_minutes: system.job_runtime_creation_tick_minutes },
              "Worker Runtime 设置已保存，重启 API 后生效",
            )
          }
        />
        <NumberField
          label="派发扫描间隔 sec"
          value={system.job_runtime_dispatch_interval_seconds}
          min={1}
          onChange={(job_runtime_dispatch_interval_seconds) =>
            updateSystem({ job_runtime_dispatch_interval_seconds })
          }
          onCommit={() =>
            onSaveSystemField(
              {
                job_runtime_dispatch_interval_seconds:
                  system.job_runtime_dispatch_interval_seconds,
              },
              "Worker Runtime 设置已保存，重启 API 后生效",
            )
          }
        />
        <NumberField
          label="每轮派发上限"
          value={system.job_runtime_dispatch_limit}
          min={1}
          onChange={(job_runtime_dispatch_limit) => updateSystem({ job_runtime_dispatch_limit })}
          onCommit={() =>
            onSaveSystemField(
              { job_runtime_dispatch_limit: system.job_runtime_dispatch_limit },
              "Worker Runtime 设置已保存，重启 API 后生效",
            )
          }
        />
        <NumberField
          label="最大并发实例数"
          value={system.job_runtime_max_concurrent_instances}
          min={1}
          onChange={(job_runtime_max_concurrent_instances) =>
            updateSystem({ job_runtime_max_concurrent_instances })
          }
          onCommit={() =>
            onSaveSystemField(
              {
                job_runtime_max_concurrent_instances:
                  system.job_runtime_max_concurrent_instances,
              },
              "Worker Runtime 设置已保存，重启 API 后生效",
            )
          }
        />
      </FormSection>
    </div>
  );
}
