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

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { EmptyState, LoadingState } from "@/shared/components";

import type { ChatSession, Project } from "../../shared/api";
import type { PrimaryRoute } from "../../shared/routes";

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
              <div className="mt-1 font-mono text-[10px] font-bold uppercase text-mutedText">
                AI Quant Cockpit
              </div>
            </div>
          </div>
        </div>

        <div className="border-b border-line p-2">
          <Button
            className="w-full justify-start"
            size="sm"
            variant={activeRoute === "new-task" ? "default" : "ghost"}
            type="button"
            onClick={() => onNavigateRoute("new-task")}
          >
            <Plus className="h-4 w-4" />
            <span>新建任务</span>
          </Button>
          <Button
            className="mt-1 w-full justify-start"
            size="sm"
            variant={activeRoute === "strategies" ? "default" : "ghost"}
            type="button"
            onClick={() => onNavigateRoute("strategies")}
          >
            <FileText className="h-4 w-4" />
            <span>策略</span>
          </Button>
        </div>

        <ScrollArea className="min-h-0 flex-1">
          <div className="space-y-4 p-2">
            <div className="flex items-center justify-between px-2 py-1">
              <span className="font-mono text-[10px] font-bold uppercase text-mutedText">
                Recent runs
              </span>
              <span className="ml-auto mr-1 font-mono text-[10px] font-bold text-mutedText">
                {sessions.length}
              </span>
              <Button
                className="h-6 w-6"
                size="iconSm"
                variant="ghost"
                type="button"
                aria-label="搜索历史执行记录"
                aria-expanded={isSearchOpen}
                title="搜索"
                onClick={() => setIsSearchOpen(true)}
              >
                <Search className="h-3.5 w-3.5" />
              </Button>
            </div>
            {isSearchOpen ? (
              <div className="px-2 pb-2">
                <Input
                  className="h-8 text-xs"
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
                      <span className="mt-0.5 block truncate font-mono text-[10px] leading-3 text-mutedText">
                        {sessionCode(session.id)} · {statusLabel}
                      </span>
                    </span>
                    <span className="font-mono text-[10px] leading-none text-mutedText">
                      {sessionTimeLabel(session.updated_at)}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </ScrollArea>

        <div className="relative flex items-center gap-2 border-t border-line p-2 text-xs text-mutedText">
          <Popover open={isProjectSwitcherOpen} onOpenChange={setIsProjectSwitcherOpen}>
            <PopoverTrigger asChild>
              <Button
                className="min-w-0 flex-1 justify-start px-2"
                type="button"
                aria-label="切换项目"
              >
                <ChevronsUpDown className="h-3.5 w-3.5 shrink-0 opacity-70" />
                <span className="block min-w-0 flex-1 truncate font-mono text-[11px] font-semibold">
                  {activeProject?.name ?? "none"}
                </span>
              </Button>
            </PopoverTrigger>
            <PopoverContent align="start" className="w-64 p-1">
              <div className="px-2 py-1.5 text-[11px] font-semibold text-foreground">
                切换项目
              </div>
              <ScrollArea className="max-h-72">
                {projects.length === 0 ? <Notice text="暂无项目" /> : null}
                {projects.map((project) => {
                  const isActive = project.id === activeProjectId;
                  return (
                    <Button
                      className="w-full justify-start px-2.5 text-xs"
                      variant="ghost"
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
                    </Button>
                  );
                })}
              </ScrollArea>
              <div className="border-t border-line pt-1">
                <Button
                  className="w-full justify-start text-xs"
                  size="sm"
                  type="button"
                  onClick={() => {
                    setIsProjectSwitcherOpen(false);
                    setIsProjectManagementOpen(true);
                  }}
                >
                  管理项目...
                </Button>
              </div>
            </PopoverContent>
          </Popover>
          <Button
            size="iconSm"
            variant="ghost"
            type="button"
            aria-label="帮助文档"
            title="帮助文档"
          >
            <CircleHelp className="h-4 w-4" />
          </Button>
          <Button
            size="iconSm"
            variant={activeRoute === "settings" ? "default" : "ghost"}
            type="button"
            aria-label="设置"
            title="设置"
            onClick={() => onNavigateRoute("settings")}
          >
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </aside>

      <Dialog open={isProjectManagementOpen} onOpenChange={setIsProjectManagementOpen}>
        <DialogContent className="h-[min(680px,calc(100vh-48px))] max-w-4xl overflow-hidden p-0">
          <div className="flex min-h-0 flex-1 overflow-hidden">
            <nav className="hidden w-48 shrink-0 border-r bg-muted p-3 sm:block">
              <DialogHeader className="mb-3">
                <DialogTitle className="text-sm">项目管理</DialogTitle>
                <DialogDescription className="sr-only">管理本地项目目录</DialogDescription>
              </DialogHeader>
              <Button className="w-full justify-start" size="sm" type="button">
                <FolderOpen className="h-4 w-4" />
                项目管理
              </Button>
            </nav>

            <section className="min-w-0 flex-1 overflow-y-auto p-5">
              <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-base font-semibold text-ink">项目管理</h2>
                  <p className="mt-1 max-w-xl truncate text-xs text-mutedText">
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
                  <Input
                    className="min-w-0 flex-1 text-xs"
                    onChange={(event) => setNewProjectName(event.target.value)}
                    placeholder="项目名称（可选）"
                    value={newProjectName}
                  />
                  <Button
                    size="sm"
                    variant="outline"
                    type="button"
                    onClick={() => void onOpenProject()}
                  >
                    <FolderOpen className="h-4 w-4" />
                    打开
                  </Button>
                  <Button
                    size="sm"
                    type="submit"
                  >
                    <Plus className="h-4 w-4" />
                    新建
                  </Button>
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
                              <Folder className="h-4 w-4 shrink-0 text-mutedText" />
                            )}
                            {isEditing ? (
                              <Input
                                className="h-8 min-w-0 flex-1 text-sm"
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
                          <p className="truncate font-mono text-[10px] text-mutedText">
                            {project.local_path}
                          </p>
                        </div>
                        {isActive ? (
                          <Badge
                            className="h-5 shrink-0 px-1.5"
                            title="当前项目"
                            aria-label="当前项目"
                          >
                            <Check className="h-3 w-3" />
                          </Badge>
                        ) : null}
                      </div>

                      <div className="mt-4 flex items-center justify-between gap-2">
                        <span className="text-xs text-mutedText">
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
                                onClick={() => undefined}
                                confirm={{
                                  title: `移除项目“${project.name}”？`,
                                  description: "只会从项目列表移除，不会删除本地目录。",
                                  onConfirm: () => void onDeleteProject(project.id),
                                }}
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
        </DialogContent>
      </Dialog>
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
  confirm,
}: {
  label: string;
  onClick: () => void;
  children: ReactNode;
  tone?: "default" | "danger";
  confirm?: {
    title: string;
    description: string;
    onConfirm: () => void;
  };
}) {
  const actionButton = (
    <Button
      className={tone === "danger" ? "text-destructive hover:text-destructive" : undefined}
      size="iconSm"
      variant="ghost"
      type="button"
      aria-label={label}
      onClick={confirm ? undefined : onClick}
    >
      {children}
    </Button>
  );

  if (!confirm) {
    return (
      <Tooltip>
        <TooltipTrigger asChild>{actionButton}</TooltipTrigger>
        <TooltipContent>{label}</TooltipContent>
      </Tooltip>
    );
  }

  return (
    <AlertDialog>
      <Tooltip>
        <TooltipTrigger asChild>
          <AlertDialogTrigger asChild>{actionButton}</AlertDialogTrigger>
        </TooltipTrigger>
        <TooltipContent>{label}</TooltipContent>
      </Tooltip>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{confirm.title}</AlertDialogTitle>
          <AlertDialogDescription>{confirm.description}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>取消</AlertDialogCancel>
          <AlertDialogAction
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            onClick={confirm.onConfirm}
          >
            移除
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

function Notice({ text }: { text: string }) {
  const isLoading = text.includes("加载");
  return isLoading ? (
    <LoadingState rows={2} title={text} />
  ) : (
    <EmptyState title={text} />
  );
}
