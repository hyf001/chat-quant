import {
  Check,
  ChevronsUpDown,
  CircleHelp,
  FileText,
  Folder,
  FolderOpen,
  Pencil,
  Plus,
  Search,
  Settings,
  Trash2,
  X,
} from "lucide-react";
import { useState } from "react";
import type { ReactNode } from "react";

import type { ChatSession, Project } from "../../shared/api";
import { AppSettingsDialog } from "./AppSettingsDialog";

export type PrimaryRoute = "new-task" | "strategies";

type HistoryPanelProps = {
  projects: Project[];
  activeProjectId: string | null;
  sessions: ChatSession[];
  activeSessionId: string | null;
  activeRoute: PrimaryRoute;
  query: string;
  isProjectLoading: boolean;
  isLoading: boolean;
  isStreaming: boolean;
  onCreateProject: (name: string) => Promise<void>;
  onOpenProject: () => Promise<void>;
  onRenameProject: (projectId: string, name: string) => Promise<void>;
  onDeleteProject: (projectId: string) => Promise<void>;
  onSelectProject: (projectId: string) => void;
  onNavigateRoute: (route: PrimaryRoute) => void;
  onQueryChange: (query: string) => void;
  onSelectSession: (chatSessionId: string) => void;
};

export function HistoryPanel({
  projects,
  activeProjectId,
  sessions,
  activeSessionId,
  activeRoute,
  query,
  isProjectLoading,
  isLoading,
  isStreaming,
  onCreateProject,
  onOpenProject,
  onRenameProject,
  onDeleteProject,
  onSelectProject,
  onNavigateRoute,
  onQueryChange,
  onSelectSession,
}: HistoryPanelProps) {
  const [newProjectName, setNewProjectName] = useState("");
  const [editingProjectId, setEditingProjectId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState("");
  const [isProjectManagementOpen, setIsProjectManagementOpen] = useState(false);
  const [isProjectSwitcherOpen, setIsProjectSwitcherOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const hasActiveProject = activeProjectId !== null;
  const activeProject = projects.find((project) => project.id === activeProjectId) ?? null;

  const handleCreateProject = async () => {
    const trimmed = newProjectName.trim();
    setNewProjectName("");
    await onCreateProject(trimmed);
  };

  const handleStartRename = (project: Project) => {
    setEditingProjectId(project.id);
    setEditingName(project.name);
  };

  const handleRenameProject = async (projectId: string) => {
    const trimmed = editingName.trim();
    if (!trimmed) {
      return;
    }
    setEditingProjectId(null);
    await onRenameProject(projectId, trimmed);
  };

  const handleDeleteProject = async (project: Project) => {
    const confirmed = window.confirm(`从列表移除项目“${project.name}”？不会删除本地目录。`);
    if (!confirmed) {
      return;
    }
    await onDeleteProject(project.id);
  };

  return (
    <>
      <aside
        className="glass-panel flex h-full w-72 shrink-0 flex-col border-r border-line text-ink"
        aria-label="历史会话"
      >
        <div className="border-b border-line px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="cq-brand-mark" aria-hidden="true">
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>
            <div className="min-w-0">
              <div className="text-sm font-bold leading-none text-ink">Chat Quant</div>
              <div className="mt-1 font-mono text-[10px] font-bold uppercase text-muted">
                AI Quant Cockpit
              </div>
            </div>
          </div>
        </div>

        <div className="border-b border-line p-2">
          <button
            className={`flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-900/20 ${
              activeRoute === "new-task"
                ? "bg-ink text-panel shadow-[inset_3px_0_0_#c9851a]"
                : "text-graphite hover:bg-soft hover:text-ink"
            }`}
            type="button"
            onClick={() => onNavigateRoute("new-task")}
          >
            <Plus className="h-4 w-4" />
            <span>新建任务</span>
          </button>
          <button
            className={`mt-1 flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-900/20 ${
              activeRoute === "strategies"
                ? "bg-ink text-panel shadow-[inset_3px_0_0_#c9851a]"
                : "text-graphite hover:bg-soft hover:text-ink"
            }`}
            type="button"
            onClick={() => onNavigateRoute("strategies")}
          >
            <FileText className="h-4 w-4" />
            <span>策略</span>
          </button>
        </div>

        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-2">
          <div>
            <div className="flex items-center justify-between px-2 py-1">
              <span className="font-mono text-[10px] font-bold uppercase text-muted">
                Recent runs
              </span>
              <span className="ml-auto mr-1 font-mono text-[10px] font-bold text-muted">
                {sessions.length}
              </span>
              <button
                className="grid h-6 w-6 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                type="button"
                aria-label="搜索历史执行记录"
                aria-expanded={isSearchOpen}
                title="搜索"
                onClick={() => setIsSearchOpen(true)}
              >
                <Search className="h-3.5 w-3.5" />
              </button>
            </div>
            {isSearchOpen ? (
              <div className="px-2 pb-2">
                <input
                  className="w-full rounded-md border border-line bg-panel px-2 py-1.5 text-xs text-ink outline-none placeholder:text-muted/70 focus:border-signal disabled:cursor-not-allowed disabled:bg-soft disabled:text-muted"
                  autoFocus
                  disabled={!hasActiveProject}
                  onChange={(event) => onQueryChange(event.target.value)}
                  placeholder="搜索当前项目会话"
                  value={query}
                />
              </div>
            ) : null}
            <div className="mt-1 space-y-1">
              {!hasActiveProject ? <Notice text="请先创建或选择项目" /> : null}
              {hasActiveProject && isLoading ? <Notice text="加载中" /> : null}
              {hasActiveProject && !isLoading && sessions.length === 0 ? (
                <Notice text="暂无会话" />
              ) : null}
              {sessions.map((session) => {
                const isActive = session.id === activeSessionId;
                const statusLabel = sessionStatusLabel(session, isActive, isStreaming);
                return (
                  <button
                    className={`grid min-h-12 w-full grid-cols-[26px_minmax(0,1fr)_auto] items-center gap-2 rounded-lg border px-2 py-2 text-left transition-all focus:outline-none focus:ring-2 focus:ring-signal/20 ${
                      isActive
                        ? "border-strong bg-panel text-ink shadow-lift"
                        : "border-transparent text-graphite hover:bg-soft/80 hover:text-ink"
                    }`}
                    key={session.id}
                    type="button"
                    onClick={() => onSelectSession(session.id)}
                  >
                    <span
                      className={`mx-auto h-2.5 w-2.5 rounded-full ${
                        isActive
                          ? "bg-signal shadow-[0_0_0_5px_#f8efd9]"
                          : "bg-brandBlue shadow-[0_0_0_5px_#e3eef7]"
                      }`}
                      aria-hidden="true"
                    />
                    <span className="min-w-0">
                      <span className="block truncate text-xs font-bold leading-4 text-ink">
                        {session.title}
                      </span>
                      <span className="mt-0.5 block truncate font-mono text-[10px] leading-3 text-muted">
                        {sessionCode(session.id)} · {statusLabel}
                      </span>
                    </span>
                    <span className="font-mono text-[10px] leading-none text-muted">
                      {sessionTimeLabel(session.updated_at)}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <div className="relative flex items-center gap-2 border-t border-line p-2 text-xs text-muted">
          <button
            className="flex h-9 min-w-0 flex-1 items-center gap-2 rounded-md bg-ink px-2 text-left text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="切换项目"
            aria-expanded={isProjectSwitcherOpen}
            onClick={() => setIsProjectSwitcherOpen((isOpen) => !isOpen)}
          >
            <ChevronsUpDown className="h-3.5 w-3.5 shrink-0 text-panel/70" />
            <span className="block min-w-0 flex-1 truncate font-mono text-[11px] font-semibold text-panel">
              {activeProject?.name ?? "none"}
            </span>
          </button>
          {isProjectSwitcherOpen ? (
            <div className="absolute bottom-11 left-2 z-40 w-64 overflow-hidden rounded-lg border border-line bg-panel shadow-panel">
              <div className="border-b border-line px-3 py-2 text-[11px] font-semibold text-ink">
                切换项目
              </div>
              <div className="max-h-72 overflow-y-auto p-1">
                {projects.length === 0 ? <Notice text="暂无项目" /> : null}
                {projects.map((project) => {
                  const isActive = project.id === activeProjectId;
                  return (
                    <button
                      className="flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                      key={project.id}
                      type="button"
                      onClick={() => {
                        onSelectProject(project.id);
                        setIsProjectSwitcherOpen(false);
                      }}
                    >
                      {isActive ? (
                        <Check className="h-3.5 w-3.5 shrink-0 text-signal" />
                      ) : (
                        <span className="h-3.5 w-3.5 shrink-0" />
                      )}
                      <span className="min-w-0 flex-1 truncate">{project.name}</span>
                    </button>
                  );
                })}
              </div>
              <div className="border-t border-line p-1">
                <button
                  className="flex w-full items-center rounded-md bg-ink px-2.5 py-2 text-left text-xs font-medium text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25"
                  type="button"
                  onClick={() => {
                    setIsProjectSwitcherOpen(false);
                    setIsProjectManagementOpen(true);
                  }}
                >
                  管理项目...
                </button>
              </div>
            </div>
          ) : null}
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="帮助文档"
            title="帮助文档"
          >
            <CircleHelp className="h-4 w-4" />
          </button>
          <button
            className="grid h-8 w-8 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-soft hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
            type="button"
            aria-label="设置"
            title="设置"
            onClick={() => setIsSettingsOpen(true)}
          >
            <Settings className="h-4 w-4" />
          </button>
        </div>
      </aside>

      {isProjectManagementOpen ? (
        <div
          className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
          role="dialog"
          aria-modal="true"
          aria-label="项目管理"
        >
          <div className="flex h-[min(680px,calc(100vh-48px))] w-full max-w-4xl overflow-hidden rounded-lg border border-line bg-panel shadow-2xl">
            <nav className="w-48 shrink-0 border-r border-line bg-soft p-3">
              <div className="mb-3 flex items-center justify-between">
                <span className="text-sm font-semibold text-ink">项目管理</span>
                <button
                  className="grid h-7 w-7 place-items-center rounded-md text-muted transition-colors hover:bg-panel hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                  type="button"
                  aria-label="关闭项目管理"
                  onClick={() => setIsProjectManagementOpen(false)}
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <button
                className="flex w-full items-center gap-2 rounded-md bg-ink px-2.5 py-2 text-left text-xs font-medium text-panel"
                type="button"
              >
                <FolderOpen className="h-4 w-4" />
                项目管理
              </button>
            </nav>

            <section className="min-w-0 flex-1 overflow-y-auto p-5">
              <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-base font-semibold text-ink">项目管理</h2>
                  <p className="mt-1 max-w-xl truncate text-xs text-muted">
                    {activeProject ? `${activeProject.name} · ${activeProject.local_path}` : "未选择项目"}
                  </p>
                </div>
                <form
                  className="flex min-w-80 flex-wrap items-center justify-end gap-2"
                  onSubmit={(event) => {
                    event.preventDefault();
                    void handleCreateProject();
                  }}
                >
                  <input
                    className="min-w-0 flex-1 rounded-md border border-line bg-panel px-3 py-2 text-xs text-ink outline-none placeholder:text-muted/70 focus:border-signal"
                    onChange={(event) => setNewProjectName(event.target.value)}
                    placeholder="项目名称（可选）"
                    value={newProjectName}
                  />
                  <button
                    className="inline-flex h-9 items-center gap-1.5 rounded-md border border-line px-3 text-xs font-semibold text-graphite transition-colors hover:border-signal hover:text-ink focus:outline-none focus:ring-2 focus:ring-signal/20"
                    type="button"
                    onClick={() => void onOpenProject()}
                  >
                    <FolderOpen className="h-4 w-4" />
                    打开
                  </button>
                  <button
                    className="inline-flex h-9 items-center gap-1.5 rounded-md bg-ink px-3 text-xs font-semibold text-panel transition-colors hover:bg-graphite focus:outline-none focus:ring-2 focus:ring-signal/25"
                    type="submit"
                  >
                    <Plus className="h-4 w-4" />
                    新建
                  </button>
                </form>
              </div>

              {isProjectLoading ? <Notice text="项目加载中" /> : null}
              {!isProjectLoading && projects.length === 0 ? <Notice text="暂无项目" /> : null}
              <div className="grid gap-3 sm:grid-cols-2">
                {projects.map((project) => {
                  const isActive = project.id === activeProjectId;
                  const isEditing = project.id === editingProjectId;
                  return (
                    <article
                      className={`rounded-lg border p-4 transition-colors ${
                        isActive
                          ? "border-strong bg-soft shadow-lift"
                          : "border-line bg-panel hover:border-strong"
                      }`}
                      key={project.id}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="mb-2 flex items-center gap-2">
                            {isActive ? (
                              <FolderOpen className="h-4 w-4 shrink-0 text-signal" />
                            ) : (
                              <Folder className="h-4 w-4 shrink-0 text-muted" />
                            )}
                            {isEditing ? (
                              <input
                                className="min-w-0 flex-1 rounded-md border border-line bg-panel px-2 py-1 text-sm text-ink outline-none focus:border-signal"
                                onChange={(event) => setEditingName(event.target.value)}
                                onKeyDown={(event) => {
                                  if (event.key === "Enter") {
                                    void handleRenameProject(project.id);
                                  }
                                  if (event.key === "Escape") {
                                    setEditingProjectId(null);
                                  }
                                }}
                                value={editingName}
                              />
                            ) : (
                              <h3 className="truncate text-sm font-semibold text-ink">
                                {project.name}
                              </h3>
                            )}
                          </div>
                          <p className="truncate font-mono text-[10px] text-muted">
                            {project.local_path}
                          </p>
                        </div>
                        {isActive ? (
                          <span
                            className="grid h-5 w-5 shrink-0 place-items-center rounded-full bg-gainSoft text-brand ring-1 ring-brand/20"
                            title="当前项目"
                            aria-label="当前项目"
                          >
                            <Check className="h-3 w-3" />
                          </span>
                        ) : null}
                      </div>

                      <div className="mt-4 flex items-center justify-between gap-2">
                        <span className="text-xs text-muted">
                          {isActive ? "当前项目" : "项目"}
                        </span>
                        <div className="flex items-center gap-1">
                          {isEditing ? (
                            <>
                              <IconAction
                                label="保存项目名"
                                onClick={() => void handleRenameProject(project.id)}
                              >
                                <Check className="h-3.5 w-3.5" />
                              </IconAction>
                              <IconAction
                                label="取消编辑项目"
                                onClick={() => setEditingProjectId(null)}
                              >
                                <X className="h-3.5 w-3.5" />
                              </IconAction>
                            </>
                          ) : (
                            <>
                              <IconAction label="编辑项目" onClick={() => handleStartRename(project)}>
                                <Pencil className="h-3.5 w-3.5" />
                              </IconAction>
                              <IconAction
                                label="删除项目"
                                tone="danger"
                                onClick={() => void handleDeleteProject(project)}
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </IconAction>
                            </>
                          )}
                        </div>
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          </div>
        </div>
      ) : null}
      <AppSettingsDialog isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
    </>
  );
}

function sessionCode(id: string): string {
  const compactId = id.replace(/[^a-zA-Z0-9]/g, "").slice(-4).toUpperCase() || "0000";
  return `TASK-${compactId}`;
}

function sessionStatusLabel(
  session: ChatSession,
  isActive: boolean,
  isStreaming: boolean,
): string {
  if (isActive && isStreaming) {
    return "running";
  }
  if (session.current_backtest_run_id || session.current_strategy_version_id) {
    return "asset";
  }
  return "saved";
}

function sessionTimeLabel(timestamp: string): string {
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return "--:--";
  }
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  }
  return date.toLocaleDateString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
  });
}

function IconAction({
  label,
  onClick,
  children,
  tone = "default",
}: {
  label: string;
  onClick: () => void;
  children: ReactNode;
  tone?: "default" | "danger";
}) {
  const toneClass =
    tone === "danger"
      ? "text-muted hover:bg-riskSoft hover:text-risk focus:ring-risk/20"
      : "text-muted hover:bg-soft hover:text-ink focus:ring-signal/20";

  return (
    <button
      className={`grid h-7 w-7 shrink-0 place-items-center rounded-md transition-colors focus:outline-none focus:ring-2 ${toneClass}`}
      type="button"
      aria-label={label}
      title={label}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

function Notice({ text }: { text: string }) {
  return (
    <div className="rounded-md border border-dashed border-line bg-panel px-2.5 py-2 text-xs text-muted">
      {text}
    </div>
  );
}
