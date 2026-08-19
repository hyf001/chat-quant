import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

function runtimeConfig() {
  const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
  const configPath = resolve(repoRoot, "config.json");
  if (!existsSync(configPath)) {
    return {};
  }
  try {
    return JSON.parse(readFileSync(configPath, "utf8")) as Record<string, unknown>;
  } catch {
    return {};
  }
}

const config = runtimeConfig();
const apiHost = typeof config.api_host === "string" ? config.api_host : "127.0.0.1";
const apiPort = typeof config.api_port === "number" ? config.api_port : 12345;
const apiBaseUrl = process.env.NODE_ENV === "production" ? "" : `http://${apiHost}:${apiPort}`;

export default defineConfig({
  base: "./",
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve(dirname(fileURLToPath(import.meta.url)), "src"),
    },
  },
  define: {
    __CHATQ_API_BASE_URL__: JSON.stringify(apiBaseUrl),
  },
  server: {
    host: typeof config.web_host === "string" ? config.web_host : "127.0.0.1",
    port: typeof config.web_port === "number" ? config.web_port : 12346,
  },
});
