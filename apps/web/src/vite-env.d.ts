/// <reference types="vite/client" />

declare const __CHATQ_API_BASE_URL__: string;

interface Window {
  chatqDesktop?: {
    apiBaseUrl: string;
    selectProjectDirectory?: () => Promise<string | null>;
    selectDirectory?: (options?: {
      title?: string;
      buttonLabel?: string;
      defaultPath?: string;
    }) => Promise<string | null>;
    createProjectDirectory?: () => Promise<string | null>;
  };
}
