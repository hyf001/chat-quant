import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import http from "node:http";
import { createRequire } from "node:module";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const electron = require("electron");
const { app, BrowserWindow, dialog, ipcMain } = electron;
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_RUNTIME_CONFIG = {
  database_path: "data/chat-quant.db",
  api_host: "127.0.0.1",
  api_port: 12345,
  web_host: "127.0.0.1",
  web_port: 12346,
};
const API_RUNTIME_FILE_NAME = "api-runtime.json";

let apiProcess = null;
let mainWindow = null;

async function main() {
  await app.whenReady();
  registerDesktopIpc();

  const configFilePath = desktopConfigFilePath();
  const runtimeConfig = loadRuntimeConfig(configFilePath);
  const apiBaseUrl = `http://${runtimeConfig.api_host}:${runtimeConfig.api_port}`;

  apiProcess = startApiSidecar(runtimeConfig);
  app.on("before-quit", stopApiSidecar);

  mainWindow = createWindow(apiBaseUrl);
  attachWindowDiagnostics(mainWindow);

  try {
    await waitForHealth(`${apiBaseUrl}/api/health`, 120_000);
    writeApiRuntimeFile(apiBaseUrl, runtimeConfig, configFilePath);
    console.log(`Chat Quant API ready at ${apiBaseUrl}`);
    await mainWindow.loadFile(webIndexPath());
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await dialog.showMessageBox(mainWindow, {
      type: "error",
      title: "Chat Quant API failed to start",
      message: "The embedded FastAPI sidecar did not become ready.",
      detail: message,
    });
    await mainWindow.loadURL(
      `data:text/html;charset=utf-8,${encodeURIComponent(errorHtml(message))}`,
    );
  }
}

function registerDesktopIpc() {
  ipcMain.handle("chatq:select-project-directory", async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ["openDirectory", "createDirectory"],
    });
    if (result.canceled || result.filePaths.length === 0) {
      return null;
    }
    return result.filePaths[0];
  });

  ipcMain.handle("chatq:create-project-directory", async () => {
    const result = await dialog.showSaveDialog(mainWindow, {
      title: "Create Chat Quant Project",
      buttonLabel: "Create",
      properties: ["createDirectory"],
    });
    if (result.canceled || !result.filePath) {
      return null;
    }
    mkdirSync(result.filePath, { recursive: true });
    return result.filePath;
  });
}

function createWindow(apiBaseUrl) {
  return new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1180,
    minHeight: 720,
    title: "Chat Quant",
    backgroundColor: "#f6f7f3",
    webPreferences: {
      additionalArguments: [`--chatq-api-base-url=${apiBaseUrl}`],
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, "preload.cjs"),
      sandbox: false,
    },
  });
}

function attachWindowDiagnostics(window) {
  window.webContents.on("did-fail-load", (_event, errorCode, errorDescription, validatedUrl) => {
    console.error(
      `Renderer failed to load ${validatedUrl}: ${errorCode} ${errorDescription}`,
    );
  });
  window.webContents.on("render-process-gone", (_event, details) => {
    console.error(`Renderer process gone: ${details.reason} (${details.exitCode})`);
  });
  window.webContents.on("console-message", (_event, level, message, line, sourceId) => {
    if (level >= 2) {
      console.error(`[renderer] ${sourceId}:${line} ${message}`);
    }
  });
  window.webContents.on("preload-error", (_event, preloadPath, error) => {
    console.error(`Preload failed ${preloadPath}: ${error.message}`);
  });

  if (process.env.CHATQ_DESKTOP_OPEN_DEVTOOLS === "1") {
    window.webContents.openDevTools({ mode: "detach" });
  }
}

function startApiSidecar(runtimeConfig) {
  const command = sidecarCommand(runtimeConfig);
  const child = spawn(command.executable, command.args, {
    cwd: command.cwd,
    env: sidecarEnv(),
    stdio: ["ignore", "pipe", "pipe"],
  });

  child.stdout?.on("data", (chunk) => {
    console.log(`[api] ${chunk.toString().trimEnd()}`);
  });
  child.stderr?.on("data", (chunk) => {
    console.error(`[api] ${chunk.toString().trimEnd()}`);
  });
  child.on("exit", (code, signal) => {
    if (code !== 0 && signal !== "SIGTERM") {
      console.error(`API sidecar exited with code ${code ?? "null"} signal ${signal ?? "null"}`);
    }
  });

  return child;
}

function sidecarEnv() {
  return {
    ...process.env,
    PATH: desktopCliPath(),
  };
}

function desktopCliPath() {
  const existingPath = process.env.PATH ?? "";
  const home = os.homedir();
  const candidateDirs = [
    ...nvmNodeBinDirs(home),
    path.join(home, ".local", "bin"),
    path.join(home, ".npm-global", "bin"),
    path.join(home, "node_modules", ".bin"),
    path.join(home, ".yarn", "bin"),
    path.join(home, ".claude", "local"),
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
    "/bin",
    "/usr/sbin",
    "/sbin",
  ];
  const pathParts = [...candidateDirs, ...existingPath.split(path.delimiter)]
    .filter(Boolean)
    .filter((dir, index, dirs) => dirs.indexOf(dir) === index);
  return pathParts.join(path.delimiter);
}

function nvmNodeBinDirs(home) {
  const versionsDir = path.join(home, ".nvm", "versions", "node");
  if (!existsSync(versionsDir)) {
    return [];
  }
  try {
    return readdirSync(versionsDir)
      .map((version) => path.join(versionsDir, version, "bin"))
      .filter((binDir) => existsSync(binDir));
  } catch {
    return [];
  }
}

function sidecarCommand(runtimeConfig) {
  const packagedBinary = packagedSidecarPath();
  if (app.isPackaged && packagedBinary) {
    return {
      executable: packagedBinary,
      args: [
        "--host",
        runtimeConfig.api_host,
        "--port",
        String(runtimeConfig.api_port),
      ],
      cwd: process.resourcesPath,
    };
  }

  const repoRoot = path.resolve(__dirname, "../../..");
  return {
    executable: process.env.CHATQ_DESKTOP_UV_BIN ?? "uv",
    args: [
      "run",
      "--project",
      "apps/api",
      "python",
      "-m",
      "app.desktop_entry",
      "--host",
      runtimeConfig.api_host,
      "--port",
      String(runtimeConfig.api_port),
    ],
    cwd: repoRoot,
  };
}

function packagedSidecarPath() {
  const sidecarName = process.platform === "win32" ? "chat-quant-api.exe" : "chat-quant-api";
  const onedirCandidate = path.join(
    process.resourcesPath,
    "sidecars",
    "chat-quant-api",
    sidecarName,
  );
  if (existsSync(onedirCandidate)) {
    return onedirCandidate;
  }

  const onefileCandidate = path.join(process.resourcesPath, "sidecars", sidecarName);
  return existsSync(onefileCandidate) ? onefileCandidate : null;
}

function stopApiSidecar() {
  removeApiRuntimeFile();
  if (!apiProcess || apiProcess.killed) {
    return;
  }
  apiProcess.kill();
  apiProcess = null;
}

function webIndexPath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, "web", "dist", "index.html");
  }
  return path.resolve(__dirname, "../../web/dist/index.html");
}

function waitForHealth(url, timeoutMs) {
  const startedAt = Date.now();
  return new Promise((resolve, reject) => {
    const poll = () => {
      http
        .get(url, (response) => {
          response.resume();
          if (response.statusCode && response.statusCode >= 200 && response.statusCode < 300) {
            resolve();
            return;
          }
          retry();
        })
        .on("error", retry);
    };

    const retry = () => {
      if (Date.now() - startedAt > timeoutMs) {
        reject(new Error(`Timed out waiting for ${url}`));
        return;
      }
      setTimeout(poll, 350);
    };

    poll();
  });
}

function desktopConfigFilePath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, "config.json");
  }
  return path.resolve(__dirname, "../../..", "config.json");
}

function loadRuntimeConfig(configFilePath) {
  let payload = {};
  try {
    payload = JSON.parse(readFileSync(configFilePath, "utf8"));
  } catch {
    payload = {};
  }
  const apiHost = coerceString(payload.api_host, DEFAULT_RUNTIME_CONFIG.api_host);
  const apiPort = coercePort(payload.api_port, DEFAULT_RUNTIME_CONFIG.api_port);
  return {
    config_file_path: configFilePath,
    database_path: coerceString(payload.database_path, DEFAULT_RUNTIME_CONFIG.database_path),
    api_host: apiHost,
    api_port: apiPort,
    web_host: coerceString(payload.web_host, DEFAULT_RUNTIME_CONFIG.web_host),
    web_port: coercePort(payload.web_port, DEFAULT_RUNTIME_CONFIG.web_port),
  };
}

function coerceString(value, fallback) {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

function coercePort(value, fallback) {
  const port = Number.parseInt(String(value ?? ""), 10);
  return Number.isInteger(port) && port > 0 && port <= 65535 ? port : fallback;
}

function apiRuntimeFilePath() {
  return path.join(app.getPath("userData"), API_RUNTIME_FILE_NAME);
}

function writeApiRuntimeFile(apiBaseUrl, runtimeConfig, configFilePath) {
  const userDataPath = app.getPath("userData");
  mkdirSync(userDataPath, { recursive: true });
  writeFileSync(
    apiRuntimeFilePath(),
    `${JSON.stringify(
      {
        host: runtimeConfig.api_host,
        port: runtimeConfig.api_port,
        base_url: apiBaseUrl,
        api_base_url: `${apiBaseUrl}/api`,
        database_path: runtimeConfig.database_path,
        pid: apiProcess?.pid ?? null,
        config_file_path: configFilePath,
        updated_at: new Date().toISOString(),
      },
      null,
      2,
    )}\n`,
    "utf8",
  );
}

function removeApiRuntimeFile() {
  const runtimeFilePath = apiRuntimeFilePath();
  if (existsSync(runtimeFilePath)) {
    rmSync(runtimeFilePath, { force: true });
  }
}

function errorHtml(message) {
  return `<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>Chat Quant</title>
    <style>
      body {
        margin: 0;
        display: grid;
        min-height: 100vh;
        place-items: center;
        background: #f6f7f3;
        color: #171a16;
        font-family: Inter, system-ui, sans-serif;
      }
      main {
        max-width: 560px;
        border: 1px solid #d9ded6;
        background: #fffdf8;
        padding: 28px;
      }
      h1 { margin: 0 0 10px; font-size: 18px; }
      pre {
        overflow: auto;
        background: #171a16;
        color: #dbe7df;
        padding: 14px;
        white-space: pre-wrap;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>内置 API 未能启动</h1>
      <p>请检查 Python/uv 环境，或确认已打包 FastAPI sidecar。</p>
      <pre>${escapeHtml(message)}</pre>
    </main>
  </body>
</html>`;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

main().catch((error) => {
  console.error(error);
  app.quit();
});
