import type { ModelProviderPayload } from "../../shared/api";

export type SettingsTab = "agent" | "system" | "logging" | "data" | "datasets";

export type ProviderDraft = ModelProviderPayload & {
  id: string | null;
};

export type ProviderTestResult = {
  ok: boolean;
  message: string;
  modelCount: number;
};
