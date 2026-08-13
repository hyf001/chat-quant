import type { AppSettings } from "../../shared/api";
import { FormSection, NumberField, SelectField, ToggleField } from "./SettingsFields";

type SystemSettingsFormProps = {
  draft: AppSettings;
  onChange: (settings: AppSettings) => void;
};

export function SystemSettingsForm({ draft, onChange }: SystemSettingsFormProps) {
  const system = draft.system;

  return (
    <FormSection title="系统">
      <SelectField
        label="运行环境"
        value={system.environment}
        options={["development", "desktop", "production"]}
        onChange={(environment) =>
          onChange({
            ...draft,
            system: {
              ...system,
              environment: environment as AppSettings["system"]["environment"],
            },
          })
        }
      />
      <ToggleField
        label="访问日志"
        checked={system.access_log_enabled}
        onChange={(access_log_enabled) =>
          onChange({ ...draft, system: { ...system, access_log_enabled } })
        }
      />
      <NumberField
        label="慢请求阈值 ms"
        value={system.access_log_slow_threshold_ms}
        onChange={(access_log_slow_threshold_ms) =>
          onChange({ ...draft, system: { ...system, access_log_slow_threshold_ms } })
        }
      />
    </FormSection>
  );
}

