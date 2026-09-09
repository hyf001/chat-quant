import { ExternalLink, FileText, Loader2, Pencil, Plus, RefreshCw, Square, Trash2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { InlineAlert, LoadingState } from "@/shared/components";
import {
  API_BASE_URL,
  createNotebookFile,
  deleteNotebookFile,
  ensureNotebookServer,
  ensureNotebookSession,
  listNotebookFiles,
  renameNotebookFile,
  stopNotebookServer,
  type NotebookFile,
  type NotebookFileListResponse,
  type NotebookServer,
  type Project,
} from "@/shared/api";
import { notify } from "@/shared/notify";

type NotebookPageProps = {
  project: Project | null;
};

type ServerState =
  | { status: "idle" }
  | { status: "loading"; previous?: NotebookServer }
  | { status: "ready"; server: NotebookServer }
  | { status: "error"; message: string; previous?: NotebookServer };

type SessionState =
  | { status: "idle" }
  | { status: "loading"; path: string }
  | { status: "ready"; path: string }
  | { status: "error"; path: string; message: string };

type FileDialogState =
  | { mode: "create" }
  | { mode: "rename"; file: NotebookFile };

export function NotebookPage({ project }: NotebookPageProps) {
  const [state, setState] = useState<ServerState>({ status: "idle" });
  const [sessionState, setSessionState] = useState<SessionState>({ status: "idle" });
  const [fileList, setFileList] = useState<NotebookFileListResponse | null>(null);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [isFileLoading, setIsFileLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isStopping, setIsStopping] = useState(false);
  const [fileDialog, setFileDialog] = useState<FileDialogState | null>(null);
  const [fileDialogName, setFileDialogName] = useState("");
  const [deleteTarget, setDeleteTarget] = useState<NotebookFile | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [sessionRefreshKey, setSessionRefreshKey] = useState(0);
  const server = serverFromState(state);
  const selectedFile = fileList?.files.find((file) => file.relative_path === selectedPath) ?? null;
  const notebookBaseUrl = useMemo(
    () => (server ? browserNotebookBaseUrl(server.proxy_base_url ?? server.base_url) : ""),
    [server],
  );
  const iframeUrl = useMemo(() => {
    if (
      !server ||
      !notebookBaseUrl ||
      !selectedPath ||
      sessionState.status !== "ready" ||
      sessionState.path !== selectedPath
    ) {
      return "";
    }
    return `${notebookBaseUrl}/notebooks/${encodeNotebookPath(selectedPath)}?token=${server.token}`;
  }, [notebookBaseUrl, selectedPath, server, sessionState]);

  const startServer = useCallback(async () => {
    if (!project) {
      setState({ status: "idle" });
      return;
    }
    setState((previous) => ({
      status: "loading",
      previous: serverFromState(previous),
    }));
    try {
      const nextServer = await ensureNotebookServer(project.id);
      setState({ status: "ready", server: nextServer });
    } catch (caught) {
      setState((previous) => ({
        status: "error",
        message: caught instanceof Error ? caught.message : "Notebook 服务启动失败",
        previous: serverFromState(previous),
      }));
    }
  }, [project]);

  const loadFiles = useCallback(async (preferredPath?: string | null) => {
    if (!project) {
      setFileList(null);
      setSelectedPath(null);
      return;
    }
    setIsFileLoading(true);
    try {
      const nextList = await listNotebookFiles(project.id);
      setFileList(nextList);
      setSelectedPath((current) => {
        if (preferredPath && nextList.files.some((file) => file.relative_path === preferredPath)) {
          return preferredPath;
        }
        return current && nextList.files.some((file) => file.relative_path === current)
          ? current
          : nextList.files[0]?.relative_path ?? null;
      });
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "Notebook 列表加载失败", "error");
    } finally {
      setIsFileLoading(false);
    }
  }, [project]);

  useEffect(() => {
    void startServer();
    void loadFiles();
  }, [loadFiles, startServer]);

  useEffect(() => {
    if (!project || !server || !selectedPath) {
      setSessionState({ status: "idle" });
      return;
    }
    let cancelled = false;
    setSessionState({ status: "loading", path: selectedPath });
    ensureNotebookSession(project.id, selectedPath)
      .then(() => {
        if (!cancelled) {
          setSessionState({ status: "ready", path: selectedPath });
        }
      })
      .catch((caught) => {
        if (!cancelled) {
          setSessionState({
            status: "error",
            path: selectedPath,
            message: caught instanceof Error ? caught.message : "Notebook 内核连接失败",
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [project, selectedPath, server?.runtime_id, sessionRefreshKey]);

  const openCreateDialog = () => {
    setFileDialog({ mode: "create" });
    setFileDialogName("Untitled");
  };

  const openRenameDialog = (file: NotebookFile) => {
    setFileDialog({ mode: "rename", file });
    setFileDialogName(file.name);
  };

  const handleFileDialogSubmit = async () => {
    if (!project || isCreating) {
      return;
    }
    const name = fileDialogName.trim();
    if (!fileDialog || !name) {
      return;
    }
    setIsCreating(true);
    try {
      if (fileDialog.mode === "create") {
        const file = await createNotebookFile(project.id, name);
        await loadFiles(file.relative_path);
        notify("Notebook 已创建", "success");
      } else {
        const file = await renameNotebookFile(project.id, fileDialog.file.relative_path, name);
        await loadFiles(file.relative_path);
        notify("Notebook 已重命名", "success");
      }
      setFileDialog(null);
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "Notebook 文件操作失败", "error");
    } finally {
      setIsCreating(false);
    }
  };

  const handleDelete = async () => {
    if (!project || !deleteTarget || isDeleting) {
      return;
    }
    setIsDeleting(true);
    try {
      await deleteNotebookFile(project.id, deleteTarget.relative_path);
      await loadFiles(selectedPath === deleteTarget.relative_path ? null : selectedPath);
      notify("Notebook 已删除", "success");
      setDeleteTarget(null);
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "Notebook 删除失败", "error");
    } finally {
      setIsDeleting(false);
    }
  };

  const handleStop = async () => {
    if (!project || isStopping) {
      return;
    }
    setIsStopping(true);
    try {
      await stopNotebookServer(project.id);
      setState({ status: "idle" });
      setSessionState({ status: "idle" });
      notify("Notebook 服务已停止", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "Notebook 服务停止失败", "error");
    } finally {
      setIsStopping(false);
    }
  };

  const handleRefresh = async () => {
    await startServer();
    setSessionRefreshKey((current) => current + 1);
  };

  const handleOpenWindow = () => {
    if (iframeUrl) {
      window.open(iframeUrl, "_blank", "noopener,noreferrer");
    }
  };

  if (!project) {
    return (
      <section className="mx-auto w-full max-w-4xl">
        <InlineAlert title="请先创建或选择项目" tone="error" />
      </section>
    );
  }

  return (
    <section className="flex h-full min-h-0 overflow-hidden bg-white">
      <aside className="flex w-72 shrink-0 flex-col border-r border-line bg-card/95">
        <div className="flex h-12 shrink-0 items-center gap-2 border-b border-line px-3">
          <div className="min-w-0 flex-1">
            <div className="font-mono text-[10px] font-bold uppercase text-mutedText">
              Notebooks
            </div>
            <div className="truncate text-xs font-semibold text-ink">
              {fileList?.files.length ?? 0} files
            </div>
          </div>
          <Button
            size="iconSm"
            variant="ghost"
            type="button"
            title="新建 Notebook"
            aria-label="新建 Notebook"
            disabled={isCreating}
            onClick={openCreateDialog}
          >
            {isCreating ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Plus className="h-3.5 w-3.5" />}
          </Button>
          <Button
            size="iconSm"
            variant="ghost"
            type="button"
            title="刷新列表"
            aria-label="刷新 Notebook 列表"
            disabled={isFileLoading}
            onClick={() => void loadFiles()}
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isFileLoading ? "animate-spin" : ""}`} />
          </Button>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto p-2">
          {isFileLoading && !fileList ? (
            <LoadingState title="正在加载 Notebook" rows={2} />
          ) : null}
          {fileList && fileList.files.length === 0 ? (
            <div className="p-3 text-xs text-mutedText">
              <Button className="w-full justify-start" size="sm" onClick={openCreateDialog}>
                <Plus className="h-4 w-4" />
                新建 Notebook
              </Button>
            </div>
          ) : null}
          <div className="space-y-1">
            {fileList?.files.map((file) => {
              const isActive = file.relative_path === selectedPath;
              return (
                <div
                  key={file.relative_path}
                  className={`group grid w-full grid-cols-[minmax(0,1fr)_auto] items-center gap-1 rounded-md border transition-colors ${
                    isActive
                      ? "border-signal/30 bg-primary text-primary-foreground"
                      : "border-transparent text-ink hover:bg-soft"
                  }`}
                >
                  <button
                    type="button"
                    className="grid min-w-0 grid-cols-[18px_minmax(0,1fr)] items-center gap-2 px-2 py-2 text-left"
                    onClick={() => setSelectedPath(file.relative_path)}
                  >
                    <FileText className="h-4 w-4" />
                    <span className="min-w-0">
                      <span className="block truncate text-xs font-bold">{file.name}</span>
                      <span
                        className={`block truncate font-mono text-[10px] ${
                          isActive ? "text-primary-foreground/75" : "text-mutedText"
                        }`}
                      >
                        {formatNotebookTime(file.modified_at)}
                      </span>
                    </span>
                  </button>
                  <span className="flex items-center gap-0.5 pr-1 opacity-70 transition-opacity group-hover:opacity-100">
                    <Button
                      size="iconSm"
                      variant="ghost"
                      type="button"
                      title="重命名"
                      aria-label={`重命名 ${file.name}`}
                      className={`h-7 w-7 ${isActive ? "hover:bg-primary-foreground/15 hover:text-primary-foreground" : ""}`}
                      onClick={() => openRenameDialog(file)}
                    >
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      size="iconSm"
                      variant="ghost"
                      type="button"
                      title="删除"
                      aria-label={`删除 ${file.name}`}
                      className={`h-7 w-7 ${
                        isActive
                          ? "hover:bg-primary-foreground/15 hover:text-primary-foreground"
                          : "text-risk hover:bg-riskSoft hover:text-risk"
                      }`}
                      onClick={() => setDeleteTarget(file)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <div className="flex h-10 shrink-0 items-center gap-2 border-b border-line bg-card/95 px-3">
          <div className="min-w-0 flex-1">
            <div className="truncate font-mono text-[10px] font-bold uppercase text-mutedText">
              Data Analysis
            </div>
            <div className="truncate text-[11px] text-mutedText">
              {selectedFile?.relative_path ?? fileList?.root_dir ?? `${project.local_path}/notebook`}
            </div>
          </div>
          {state.status === "loading" ? (
            <span className="inline-flex items-center gap-1.5 rounded-md border px-2 py-1 font-mono text-[10px] text-mutedText">
              <Loader2 className="h-3 w-3 animate-spin" />
              starting
            </span>
          ) : null}
          {isStopping ? (
            <span className="inline-flex items-center gap-1.5 rounded-md border border-risk/30 bg-riskSoft px-2 py-1 font-mono text-[10px] font-semibold text-risk">
              <Loader2 className="h-3 w-3 animate-spin" />
              正在停止 Notebook
            </span>
          ) : null}
          <Button
            size="iconSm"
            variant="ghost"
            type="button"
            title="刷新连接"
            aria-label="刷新 Notebook 连接"
            onClick={() => void handleRefresh()}
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </Button>
          <Button
            size="iconSm"
            variant="ghost"
            type="button"
            title="新窗口打开"
            aria-label="新窗口打开 Notebook"
            disabled={!iframeUrl}
            onClick={handleOpenWindow}
          >
            <ExternalLink className="h-3.5 w-3.5" />
          </Button>
          <Button
            size="iconSm"
            variant="destructive"
            type="button"
            title="停止"
            aria-label="停止 Notebook 服务"
            disabled={!server || isStopping}
            onClick={() => void handleStop()}
          >
            {isStopping ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <Square className="h-3.5 w-3.5 fill-current" />
            )}
          </Button>
        </div>

        <div className="min-h-0 flex-1 bg-white">
          {state.status === "loading" && !server ? (
            <div className="p-4">
              <LoadingState title="正在启动 Notebook" />
            </div>
          ) : null}
          {state.status === "error" && !server ? (
            <div className="p-4">
              <InlineAlert title="Notebook 服务不可用" description={state.message} tone="error" />
            </div>
          ) : null}
          {sessionState.status === "loading" && sessionState.path === selectedPath ? (
            <div className="p-4">
              <LoadingState title="正在连接 Python 内核" rows={2} />
            </div>
          ) : null}
          {sessionState.status === "error" && sessionState.path === selectedPath ? (
            <div className="p-4">
              <InlineAlert title="Notebook 内核不可用" description={sessionState.message} tone="error" />
            </div>
          ) : null}
          {iframeUrl ? (
            <iframe
              className="h-full w-full border-0"
              src={iframeUrl}
              title="Chat Quant Notebook"
            />
          ) : state.status !== "loading" && fileList?.files.length === 0 ? (
            <div className="grid h-full place-items-center p-6">
              <Button type="button" onClick={openCreateDialog}>
                <Plus className="h-4 w-4" />
                新建 Notebook
              </Button>
            </div>
          ) : null}
        </div>
      </div>
      {fileDialog ? (
        <Dialog open onOpenChange={(open) => !open && !isCreating && setFileDialog(null)}>
          <DialogContent className="max-w-sm">
            <DialogHeader>
              <DialogTitle>{fileDialog.mode === "create" ? "新建 Notebook" : "重命名 Notebook"}</DialogTitle>
              <DialogDescription className="sr-only">输入 Notebook 文件名</DialogDescription>
            </DialogHeader>
            <form
              className="grid gap-4"
              onSubmit={(event) => {
                event.preventDefault();
                void handleFileDialogSubmit();
              }}
            >
              <Input
                autoFocus
                value={fileDialogName}
                placeholder="Untitled.ipynb"
                disabled={isCreating}
                onChange={(event) => setFileDialogName(event.target.value)}
              />
              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  disabled={isCreating}
                  onClick={() => setFileDialog(null)}
                >
                  取消
                </Button>
                <Button type="submit" disabled={!fileDialogName.trim() || isCreating}>
                  {isCreating ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                  {fileDialog.mode === "create" ? "创建" : "保存"}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      ) : null}
      <AlertDialog
        open={deleteTarget !== null}
        onOpenChange={(open) => {
          if (!open && !isDeleting) {
            setDeleteTarget(null);
          }
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>删除 Notebook</AlertDialogTitle>
            <AlertDialogDescription>
              确定删除 {deleteTarget?.name}？此操作不能撤销。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeleting}>取消</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              disabled={isDeleting}
              onClick={(event) => {
                event.preventDefault();
                void handleDelete();
              }}
            >
              {isDeleting ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  );
}

function serverFromState(state: ServerState): NotebookServer | undefined {
  if (state.status === "ready") {
    return state.server;
  }
  if (state.status === "loading" || state.status === "error") {
    return state.previous;
  }
  return undefined;
}

function encodeNotebookPath(path: string): string {
  return path
    .split("/")
    .filter(Boolean)
    .map((part) => encodeURIComponent(part))
    .join("/");
}

function browserNotebookBaseUrl(baseUrl: string): string {
  if (!/^https?:\/\//.test(baseUrl)) {
    const apiBaseUrl = browserApiBaseUrl();
    const path = baseUrl.startsWith("/") ? baseUrl : `/${baseUrl}`;
    return `${apiBaseUrl}${path}`.replace(/\/$/, "");
  }
  try {
    const url = new URL(baseUrl);
    if (url.hostname === "127.0.0.1" && window.location.hostname === "localhost") {
      url.hostname = "localhost";
    }
    return url.toString().replace(/\/$/, "");
  } catch {
    return baseUrl.replace(/\/$/, "");
  }
}

function browserApiBaseUrl(): string {
  if (!API_BASE_URL) {
    return "";
  }
  try {
    const url = new URL(API_BASE_URL);
    if (url.hostname === "127.0.0.1" && window.location.hostname === "localhost") {
      url.hostname = "localhost";
    }
    return url.toString().replace(/\/$/, "");
  } catch {
    return API_BASE_URL.replace(/\/$/, "");
  }
}

function formatNotebookTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  return date.toLocaleString([], {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}
