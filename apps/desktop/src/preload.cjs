const { contextBridge, ipcRenderer } = require("electron");

const prefix = "--chatq-api-base-url=";
const apiBaseUrl =
  process.argv.find((argument) => argument.startsWith(prefix))?.slice(prefix.length) ??
  "http://127.0.0.1:12345";

contextBridge.exposeInMainWorld("chatqDesktop", {
  apiBaseUrl,
  selectProjectDirectory: () => ipcRenderer.invoke("chatq:select-project-directory"),
  createProjectDirectory: () => ipcRenderer.invoke("chatq:create-project-directory"),
});
