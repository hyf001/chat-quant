import {
  Check,
  Code2,
  Folder,
  FolderOpen,
  Pencil,
  Plus,
  Settings,
  Terminal,
  Trash2,
  X,
} from "lucide-react";
import { useState } from "react";
import type { ReactNode } from "react";

import type { ChatSession, Project } from "../../shared/api";

type HistoryPanelProps = {
  projects: Project[];
  activeProjectId: string | null;
  sessions: ChatSession[];
  activeSessionId: string | null;
  query: string;
  isProjectLoading: boolean;
  isLoading: boolean;
  onCreateProject: (name: string) => Promise<void>;
  onRenameProject: (projectId: string, name: string) => Promise<void>;
  onDeleteProject: (projectId: string) => Promise<void>;
  onSelectProject: (projectId: string) => void;
  onCreateSession: () => void;
  onQueryChange: (query: string) => void;
  onSelectSession: (chatSessionId: string) => void;
};

export function HistoryPanel({
  projects,
  activeProjectId,
  sessions,
  activeSessionId,
  query,
  isProjectLoading,
  isLoading,
  onCreateProject,
  onRenameProject,
  onDeleteProject,
  onSelectProject,
  onCreateSession,
  onQueryChange,
  onSelectSession,
}: HistoryPanelProps) {
  const [newProjectName, setNewProjectName] = useState("");
  const [editingProjectId, setEditingProjectId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState("");
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isProjectSwitcherOpen, setIsProjectSwitcherOpen] = useState(false);
  const hasActiveProject = activeProjectId !== null;
  const activeProject = projects.find((project) => project.id === activeProjectId) ?? null;

  const handleCreateProject = async () => {
    const trimmed = newProjectName.trim() || nextDefaultProjectName(projects);
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
    const confirmed = window.confirm(`删除项目“${project.name}”？`);
    if (!confirmed) {
      return;
    }
    await onDeleteProject(project.id);
  };

  return (
    <>
      <aside
        className="flex h-full w-72 shrink-0 flex-col border-r border-zinc-200 bg-zinc-50 text-zinc-900"
        aria-label="历史会话"
      >
        <div className="border-b border-zinc-200 p-3">
          <button
            className="flex w-full items-center justify-center gap-2 rounded-md bg-zinc-900 px-3 py-2 text-xs font-semibold text-white transition-colors hover:bg-black focus:outline-none focus:ring-2 focus:ring-zinc-900/25 disabled:cursor-not-allowed disabled:bg-zinc-300 disabled:text-zinc-500"
            disabled={!hasActiveProject}
            type="button"
            onClick={onCreateSession}
          >
            <Plus className="h-4 w-4" />
            <span>新建 Agent 任务</span>
          </button>
        </div>

        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-2">
          <div>
            <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-zinc-500">
              历史执行记录
            </div>
            <div className="px-2 pb-2">
              <input
                className="w-full rounded-md border border-zinc-300 bg-white px-2 py-1.5 text-xs text-zinc-900 outline-none placeholder:text-zinc-400 focus:border-zinc-900 disabled:cursor-not-allowed disabled:bg-zinc-100 disabled:text-zinc-400"
                disabled={!hasActiveProject}
                onChange={(event) => onQueryChange(event.target.value)}
                placeholder="搜索当前项目会话"
                value={query}
              />
            </div>
            <div className="mt-1 space-y-1">
              {!hasActiveProject ? <Notice text="请先创建或选择项目" /> : null}
              {hasActiveProject && isLoading ? <Notice text="加载中" /> : null}
              {hasActiveProject && !isLoading && sessions.length === 0 ? (
                <Notice text="暂无会话" />
              ) : null}
              {sessions.map((session) => {
                const isActive = session.id === activeSessionId;
                return (
                  <button
                    className={`flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-900/20 ${
                      isActive
                        ? "bg-zinc-900 font-medium text-white"
                        : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900"
                    }`}
                    key={session.id}
                    type="button"
                    onClick={() => onSelectSession(session.id)}
                  >
                    {isActive ? (
                      <Terminal className="h-3.5 w-3.5 shrink-0 text-zinc-200" />
                    ) : (
                      <Code2 className="h-3.5 w-3.5 shrink-0 text-zinc-500" />
                    )}
                    <span className="truncate">{session.title}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <div className="relative flex items-center justify-between border-t border-zinc-200 p-3 text-xs text-zinc-500">
          <button
            className="min-w-0 truncate rounded px-1 py-0.5 text-left font-mono text-[11px] transition-colors hover:bg-zinc-200 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
            type="button"
            aria-label="切换项目"
            onClick={() => setIsProjectSwitcherOpen((isOpen) => !isOpen)}
          >
            {activeProject?.name ?? "none"}
          </button>
          {isProjectSwitcherOpen ? (
            <div className="absolute bottom-11 left-3 z-40 w-64 overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-xl">
              <div className="border-b border-zinc-100 px-3 py-2 text-[11px] font-semibold text-zinc-900">
                切换项目
              </div>
              <div className="max-h-72 overflow-y-auto p-1">
                {projects.length === 0 ? <Notice text="暂无项目" /> : null}
                {projects.map((project) => {
                  const isActive = project.id === activeProjectId;
                  return (
                    <button
                      className={`flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-xs transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-900/20 ${
                        isActive
                          ? "bg-zinc-900 font-medium text-white"
                          : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900"
                      }`}
                      key={project.id}
                      type="button"
                      onClick={() => {
                        onSelectProject(project.id);
                        setIsProjectSwitcherOpen(false);
                      }}
                    >
                      {isActive ? (
                        <FolderOpen className="h-3.5 w-3.5 shrink-0" />
                      ) : (
                        <Folder className="h-3.5 w-3.5 shrink-0 text-zinc-500" />
                      )}
                      <span className="min-w-0 flex-1 truncate">{project.name}</span>
                      {isActive ? <Check className="h-3.5 w-3.5 shrink-0" /> : null}
                    </button>
                  );
                })}
              </div>
            </div>
          ) : null}
          <button
            className="grid h-6 w-6 shrink-0 place-items-center rounded text-zinc-500 transition-colors hover:bg-zinc-200 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
            type="button"
            aria-label="设置"
            onClick={() => setIsSettingsOpen(true)}
          >
            <Settings className="h-4 w-4" />
          </button>
        </div>
      </aside>

      {isSettingsOpen ? (
        <div
          className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
          role="dialog"
          aria-modal="true"
          aria-label="设置"
        >
          <div className="flex h-[min(680px,calc(100vh-48px))] w-full max-w-4xl overflow-hidden rounded-lg bg-white shadow-2xl">
            <nav className="w-48 shrink-0 border-r border-zinc-200 bg-zinc-50 p-3">
              <div className="mb-3 flex items-center justify-between">
                <span className="text-sm font-semibold text-zinc-900">设置</span>
                <button
                  className="grid h-7 w-7 place-items-center rounded-md text-zinc-500 transition-colors hover:bg-zinc-200 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
                  type="button"
                  aria-label="关闭设置"
                  onClick={() => setIsSettingsOpen(false)}
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <button
                className="flex w-full items-center gap-2 rounded-md bg-zinc-900 px-2.5 py-2 text-left text-xs font-medium text-white"
                type="button"
              >
                <FolderOpen className="h-4 w-4" />
                项目管理
              </button>
            </nav>

            <section className="min-w-0 flex-1 overflow-y-auto p-5">
              <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-base font-semibold text-zinc-900">项目管理</h2>
                  <p className="mt-1 text-xs text-zinc-500">
                    当前项目：{activeProject?.name ?? "未选择"}
                  </p>
                </div>
                <form
                  className="flex min-w-72 items-center gap-2"
                  onSubmit={(event) => {
                    event.preventDefault();
                    void handleCreateProject();
                  }}
                >
                  <input
                    className="min-w-0 flex-1 rounded-md border border-zinc-300 bg-white px-3 py-2 text-xs text-zinc-900 outline-none placeholder:text-zinc-400 focus:border-zinc-900"
                    onChange={(event) => setNewProjectName(event.target.value)}
                    placeholder="新项目名称"
                    value={newProjectName}
                  />
                  <button
                    className="grid h-9 w-9 shrink-0 place-items-center rounded-md bg-zinc-900 text-white transition-colors hover:bg-black focus:outline-none focus:ring-2 focus:ring-zinc-900/25"
                    type="submit"
                    aria-label="创建项目"
                  >
                    <Plus className="h-4 w-4" />
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
                          ? "border-zinc-900 bg-zinc-50"
                          : "border-zinc-200 bg-white hover:border-zinc-400"
                      }`}
                      key={project.id}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="mb-2 flex items-center gap-2">
                            {isActive ? (
                              <FolderOpen className="h-4 w-4 shrink-0 text-zinc-900" />
                            ) : (
                              <Folder className="h-4 w-4 shrink-0 text-zinc-500" />
                            )}
                            {isEditing ? (
                              <input
                                className="min-w-0 flex-1 rounded-md border border-zinc-300 px-2 py-1 text-sm text-zinc-900 outline-none focus:border-zinc-900"
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
                              <h3 className="truncate text-sm font-semibold text-zinc-900">
                                {project.name}
                              </h3>
                            )}
                          </div>
                          <p className="font-mono text-[10px] text-zinc-400">{project.id}</p>
                        </div>
                        {isActive ? (
                          <span
                            className="grid h-5 w-5 shrink-0 place-items-center rounded-full bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200"
                            title="当前项目"
                            aria-label="当前项目"
                          >
                            <Check className="h-3 w-3" />
                          </span>
                        ) : null}
                      </div>

                      <div className="mt-4 flex items-center justify-between gap-2">
                        <span className="text-xs text-zinc-500">
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
    </>
  );
}

function nextDefaultProjectName(projects: Project[]): string {
  const baseName = "新项目";
  const names = new Set(projects.map((project) => project.name));
  if (!names.has(baseName)) {
    return baseName;
  }
  for (let index = 2; index < 1000; index += 1) {
    const candidate = `${baseName} ${index}`;
    if (!names.has(candidate)) {
      return candidate;
    }
  }
  return `${baseName} ${projects.length + 1}`;
}

function IconAction({
  label,
  onClick,
  children,
}: {
  label: string;
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <button
      className="grid h-7 w-7 shrink-0 place-items-center rounded-md text-zinc-500 transition-colors hover:bg-zinc-100 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
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
    <div className="rounded-md border border-dashed border-zinc-300 bg-white px-2.5 py-2 text-xs text-zinc-500">
      {text}
    </div>
  );
}
