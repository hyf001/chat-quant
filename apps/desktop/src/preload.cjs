const { contextBridge } = require("electron");

const prefix = "--chatq-api-base-url=";
const apiBaseUrl =
  process.argv.find((argument) => argument.startsWith(prefix))?.slice(prefix.length) ??
  "http://localhost:8000";

contextBridge.exposeInMainWorld("chatqDesktop", {
  apiBaseUrl,
});
