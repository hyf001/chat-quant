/// <reference types="vite/client" />

interface Window {
  chatqDesktop?: {
    apiBaseUrl: string;
    selectProjectDirectory?: () => Promise<string | null>;
    createProjectDirectory?: () => Promise<string | null>;
  };
}
