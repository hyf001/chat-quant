/**
 * CLI Type Definitions
 */

export interface CLIOption {
  id: string;
  name: string;
  description: string;
  icon?: string;
  available: boolean;
  configured: boolean;
  models?: CLIModel[];
  enabled?: boolean;
}

export interface CLIModel {
  id: string;
  name: string;
  description?: string;
}

export interface CLIStatus {
  cli_type: string;
  available: boolean;
  configured: boolean;
  error?: string;
  models?: string[];
}

export interface CLIPreference {
  preferred_cli: string;
  fallback_enabled: boolean;
  selected_model?: string;
}

export const CLI_OPTIONS: CLIOption[] = [
  {
    id: 'agent',
    name: 'Claude Agent',
    description: 'Claude Agent Python SDK with advanced AI capabilities',
    available: true,
    configured: false,
    enabled: true,
    models: [
      { id: 'claude-sonnet-4-5', name: 'Claude Sonnet 4.5' },
      { id: 'claude-opus-4.1', name: 'Claude Opus 4.1' },
      { id: 'claude-sonnet-4', name: 'Claude Sonnet 4' },
      { id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet' },
      { id: 'claude-3-opus', name: 'Claude 3 Opus' },
      { id: 'claude-3-haiku', name: 'Claude 3 Haiku' }
    ]
  }
];
