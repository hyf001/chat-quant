import type { ModelProvider } from "../../shared/api";
import type { ProviderDraft } from "./types";

export const blankProviderDraft: ProviderDraft = {
  id: null,
  name: "",
  base_url: null,
  api_key: null,
  enabled: true,
};

export function providerToDraft(provider: ModelProvider): ProviderDraft {
  return {
    id: provider.id,
    name: provider.name,
    base_url: provider.base_url,
    api_key: null,
    enabled: provider.enabled,
  };
}

export function emptyToNull(value: string): string | null {
  return value.trim() ? value : null;
}

export function providerSignature(provider: ProviderDraft): string {
  return JSON.stringify({
    id: provider.id,
    name: provider.name.trim(),
    base_url: provider.base_url ?? null,
    api_key: provider.api_key ?? null,
    enabled: provider.enabled,
  });
}

export function linesToList(value: string): string[] {
  return value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}

