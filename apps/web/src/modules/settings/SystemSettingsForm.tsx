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
  );
}
