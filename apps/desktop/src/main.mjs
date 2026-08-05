import { app, BrowserWindow, dialog, ipcMain } from "electron";
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const API_HOST = "127.0.0.1";
const DEFAULT_API_PORT = 12345;
const API_RUNTIME_FILE_NAME = "api-runtime.json";

let apiProcess = null;
let mainWindow = null;

async function main() {
  await app.whenReady();
  registerDesktopIpc();

  const port = await resolveApiPort();
  const apiBaseUrl = `http://${API_HOST}:${port}`;
  const configFilePath = ensureDesktopConfigFile();

  apiProcess = startApiSidecar(port, configFilePath);
  app.on("before-quit", stopApiSidecar);

  mainWindow = createWindow(apiBaseUrl);

  try {
    await waitForHealth(`${apiBaseUrl}/api/health`, 120_000);
    writeApiRuntimeFile(apiBaseUrl, port, configFilePath);
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

function startApiSidecar(port, configFilePath) {
  const command = sidecarCommand(port);
  const child = spawn(command.executable, command.args, {
    cwd: command.cwd,
    env: {
      ...process.env,
      CHATQ_CONFIG_FILE: configFilePath,
    },
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

function sidecarCommand(port) {
  const packagedBinary = packagedSidecarPath();
  if (app.isPackaged && packagedBinary) {
    return {
      executable: packagedBinary,
      args: ["--host", API_HOST, "--port", String(port)],
      cwd: path.dirname(packagedBinary),
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
      API_HOST,
      "--port",
      String(port),
    ],
    cwd: repoRoot,
  };
}

function packagedSidecarPath() {
  const sidecarName = process.platform === "win32" ? "chat-quant-api.exe" : "chat-quant-api";
  const candidate = path.join(process.resourcesPath, "sidecars", sidecarName);
  return existsSync(candidate) ? candidate : null;
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

async function resolveApiPort() {
  const configuredPort = Number.parseInt(process.env.CHATQ_DESKTOP_API_PORT ?? "", 10);
  if (Number.isInteger(configuredPort) && configuredPort > 0) {
    return configuredPort;
  }
  return DEFAULT_API_PORT;
}

function ensureDesktopConfigFile() {
  const userDataPath = app.getPath("userData");
  const configFilePath = path.join(userDataPath, "chat-quant.env");
  if (!existsSync(configFilePath)) {
    mkdirSync(userDataPath, { recursive: true });
    const databasePath = path.join(userDataPath, "chat-quant.db");
    writeFileSync(configFilePath, `CHATQ_DATABASE_PATH=${databasePath}\n`, "utf8");
  }
  return configFilePath;
}

function apiRuntimeFilePath() {
  return path.join(app.getPath("userData"), API_RUNTIME_FILE_NAME);
}

function writeApiRuntimeFile(apiBaseUrl, port, configFilePath) {
  const userDataPath = app.getPath("userData");
  mkdirSync(userDataPath, { recursive: true });
  writeFileSync(
    apiRuntimeFilePath(),
    `${JSON.stringify(
      {
        host: API_HOST,
        port,
        base_url: apiBaseUrl,
        api_base_url: `${apiBaseUrl}/api`,
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
