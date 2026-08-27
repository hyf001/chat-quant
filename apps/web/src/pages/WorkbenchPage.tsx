import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { FolderOpen, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

import { AppSettingsPage } from "./AppSettingsPage";
import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { ProjectFilesPanel } from "../modules/files";
import { HistoryPanel } from "../modules/history";
import { NotebookPage } from "../modules/notebook";
import { StrategiesPage, StrategyDeploymentsPage } from "../modules/strategy";
import { WorkspaceLayout } from "../modules/workspace";
import {
  createProject,
  deleteProject,
  getAgentChatSessionDetail,
  getAppConfig,
  getChatSessionDetail,
  listChatSessions,
  listProviderModels,
  listProjects,
  openProject,
  readChatStream,
  sendAgentChatMessage,
  stopAgentChatSession,
  updateAppConfig,
  updateProject,
  type AgentChatSessionDetail,
  type AppSettings,
  type ChatSession,
  type ChatSessionDetail,
  type Project,
  type ProviderModel,
  type SDKStreamEnvelope,
  type SdkMessage,
} from "../shared/api";
import { notify } from "../shared/notify";
import type { PrimaryRoute } from "../shared/routes";

const routePaths: Record<PrimaryRoute, string> = {
  "new-task": "/tasks/new",
  notebooks: "/notebooks",
  strategies: "/strategies",
  "strategy-deployments": "/strategy-deployments",
  settings: "/settings",
};

type ComposerModelState = {
  currentModel: string | null;
  models: ProviderModel[];
};

export function WorkbenchPage() {
  const [activeRoute, setActiveRoute] = useState<PrimaryRoute>(() =>
    routeFromPath(window.location.pathname),
  );
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [detail, setDetail] = useState<ChatSessionDetail | null>(null);
  const [conversationEnvelopes, setConversationEnvelopes] = useState<SDKStreamEnvelope[]>([]);
  const [historyQuery, setHistoryQuery] = useState("");
  const [isProjectLoading, setIsProjectLoading] = useState(true);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isStopping, setIsStopping] = useState(false);
  const [composerModelState, setComposerModelState] = useState<ComposerModelState>({
    currentModel: null,
    models: [],
  });
  const [isModelLoading, setIsModelLoading] = useState(false);
  const [isModelSaving, setIsModelSaving] = useState(false);
  const streamingSessionIdRef = useRef<string | null>(null);
  const loadDetailRequestIdRef = useRef(0);
  const modelStateRequestIdRef = useRef(0);

  const activeSession = useMemo(
    () => detail?.session ?? sessions.find((session) => session.id === activeSessionId) ?? null,
    [activeSessionId, detail?.session, sessions],
  );
  const activeProject = useMemo(
    () => projects.find((project) => project.id === activeProjectId) ?? null,
    [activeProjectId, projects],
  );
  const envelopeMessages = useMemo(
    () => messagesFromEnvelopes(conversationEnvelopes),
    [conversationEnvelopes],
  );
  const conversationMessages = useMemo(() => {
    if (envelopeMessages.length > 0) {
      return envelopeMessages;
    }
    if (detail?.messages.length) {
      return detail.messages;
    }
    return activeSession ? fallbackMessagesFromSession(activeSession) : [];
  }, [activeSession, detail?.messages, envelopeMessages]);
  const conversationRuntimeEnvelopes = conversationEnvelopes;
  const hasNoProjects = !isProjectLoading && projects.length === 0;
  const showError = useCallback((message: string) => {
    notify(message, "error");
  }, []);

  const refreshProjects = useCallback(async (preferredProjectId?: string | null) => {
    setIsProjectLoading(true);
    try {
      const data = await listProjects();
      setProjects(data.items);
      setActiveProjectId((currentProjectId) => {
        return (
          data.items.find((project) => project.id === preferredProjectId)?.id ??
          data.items.find((project) => project.id === currentProjectId)?.id ??
          data.items[0]?.id ??
          null
        );
      });
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "项目列表加载失败");
    } finally {
      setIsProjectLoading(false);
    }
  }, [showError]);

  const refreshSessions = useCallback(
    async (query: string, projectId: string | null) => {
      if (!projectId) {
        setSessions([]);
        setActiveSessionId(null);
        setIsHistoryLoading(false);
        return;
      }
      setIsHistoryLoading(true);
      try {
        const data = await listChatSessions(query.trim() || undefined, projectId);
        setSessions(data.items);
        setActiveSessionId((currentSessionId) =>
          data.items.some((session) => session.id === currentSessionId) ? currentSessionId : null,
        );
      } catch (caught) {
        showError(caught instanceof Error ? caught.message : "会话列表加载失败");
      } finally {
        setIsHistoryLoading(false);
      }
    },
    [showError],
  );

  const loadComposerModelState = useCallback(async () => {
    const requestId = modelStateRequestIdRef.current + 1;
    modelStateRequestIdRef.current = requestId;
    setIsModelLoading(true);
    try {
      const config = await getAppConfig();
      const providerId = config.settings.agent.provider_id;
      if (!providerId) {
        if (requestId === modelStateRequestIdRef.current) {
          setComposerModelState({ currentModel: config.settings.agent.model || null, models: [] });
        }
        return config.settings;
      }
      const response = await listProviderModels(providerId);
      if (requestId === modelStateRequestIdRef.current) {
        setComposerModelState({
          currentModel: config.settings.agent.model || null,
          models: response.models,
        });
      }
      return config.settings;
    } catch {
      if (requestId === modelStateRequestIdRef.current) {
        setComposerModelState({ currentModel: null, models: [] });
      }
      return null;
    } finally {
      if (requestId === modelStateRequestIdRef.current) {
        setIsModelLoading(false);
      }
    }
  }, []);

  const loadDetail = useCallback(async (chatSessionId: string) => {
    const requestId = loadDetailRequestIdRef.current + 1;
    loadDetailRequestIdRef.current = requestId;
    setIsDetailLoading(true);
    try {
      const sessionDetail = await getChatSessionDetail(chatSessionId);
      if (requestId !== loadDetailRequestIdRef.current) {
        return;
      }
      setDetail(sessionDetail);
      const agentDetail = await getAgentDetailOrNull(chatSessionId);
      if (requestId !== loadDetailRequestIdRef.current) {
        return;
      }
      setConversationEnvelopes((current) =>
        streamingSessionIdRef.current === chatSessionId
          ? current
          : agentDetail
            ? agentDetailEnvelopes(agentDetail)
            : [],
      );
    } catch (caught) {
      if (requestId === loadDetailRequestIdRef.current) {
        showError(caught instanceof Error ? caught.message : "会话详情加载失败");
      }
    } finally {
      if (requestId === loadDetailRequestIdRef.current) {
        setIsDetailLoading(false);
      }
    }
  }, [showError]);

  useEffect(() => {
    void refreshProjects();
  }, [refreshProjects]);

  useEffect(() => {
    const handlePopState = () => {
      setActiveRoute(routeFromPath(window.location.pathname));
    };
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  useEffect(() => {
    void loadComposerModelState();
  }, [loadComposerModelState]);

  useEffect(() => {
    setHistoryQuery("");
    setActiveSessionId(null);
    setDetail(null);
    setConversationEnvelopes([]);
    void refreshSessions("", activeProjectId);
  }, [activeProjectId, refreshSessions]);

  useEffect(() => {
    if (activeSessionId) {
      void loadDetail(activeSessionId);
    } else {
      loadDetailRequestIdRef.current += 1;
      setDetail(null);
      setConversationEnvelopes([]);
    }
  }, [activeSessionId, loadDetail]);

  const handleSearchChange = (query: string) => {
    setHistoryQuery(query);
    void refreshSessions(query, activeProjectId);
  };

  const handleSelectProject = (projectId: string) => {
    setActiveProjectId(projectId);
  };

  const handleNavigateRoute = (route: PrimaryRoute) => {
    setActiveRoute(route);
    if (window.location.pathname !== routePaths[route]) {
      window.history.pushState({}, "", routePaths[route]);
    }
    if (route === "new-task") {
      setActiveSessionId(null);
      setDetail(null);
      setConversationEnvelopes([]);
    }
  };

  const handleBackFromSettings = () => {
    const nextRoute: PrimaryRoute = "new-task";
    setActiveRoute(nextRoute);
    if (window.location.pathname !== routePaths[nextRoute]) {
      window.history.pushState({}, "", routePaths[nextRoute]);
    }
  };

  const handleSelectSession = (chatSessionId: string) => {
    setActiveRoute("new-task");
    if (window.location.pathname !== routePaths["new-task"]) {
      window.history.pushState({}, "", routePaths["new-task"]);
    }
    setActiveSessionId(chatSessionId);
  };

  const handleCreateProject = async (name: string) => {
    try {
      const localPath = await selectCreateProjectPath();
      if (!localPath) {
        return;
      }
      const project = await createProject({
        local_path: localPath,
        name: name || undefined,
      });
      await refreshProjects(project.id);
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "新建项目失败");
    }
  };

  const handleOpenProject = async () => {
    try {
      const localPath = await selectOpenProjectPath();
      if (!localPath) {
        return;
      }
      const project = await openProject({ local_path: localPath });
      await refreshProjects(project.id);
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "打开项目失败");
    }
  };

  const handleRenameProject = async (projectId: string, name: string) => {
    try {
      await updateProject(projectId, { name });
      await refreshProjects(activeProjectId);
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "编辑项目失败");
    }
  };

  const handleDeleteProject = async (projectId: string) => {
    try {
      await deleteProject(projectId);
      await refreshProjects(projectId === activeProjectId ? null : activeProjectId);
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "删除项目失败");
    }
  };

  const handleSendMessage = async (content: string) => {
    if (isSending) {
      return;
    }
    if (!activeProjectId) {
      showError("请先创建或选择项目");
      return;
    }
    setIsSending(true);
    try {
      const currentSessionId = activeSessionId;

      const accepted = await sendAgentChatMessage({
        chatSessionId: currentSessionId,
        projectId: activeProjectId,
        message: content,
      });
      const sessionId = accepted.chat_session_id;
      streamingSessionIdRef.current = sessionId;
      if (!currentSessionId) {
        setActiveSessionId(sessionId);
        void refreshSessions(historyQuery, activeProjectId);
      }
      setConversationEnvelopes((current) =>
        appendOptimisticUserMessage({
          envelopes: current,
          chatSessionId: sessionId,
          sdkSessionId: accepted.sdk_session_id,
          userMessageId: accepted.user_message_id,
          content,
        }),
      );
      let receivedStreamEnvelope = false;
      await readChatStream(accepted.stream_url, (envelope) => {
        receivedStreamEnvelope = true;
        setConversationEnvelopes((current) => appendStreamEnvelope(current, envelope));
      });
      if (!receivedStreamEnvelope) {
        showError("本轮没有收到任何模型返回事件。可能是流连接提前结束、模型调用超时或被中断，请稍后重试，或切换模型/Provider。");
      }
      await loadDetail(sessionId);
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "消息发送失败");
    } finally {
      streamingSessionIdRef.current = null;
      setIsSending(false);
      setIsStopping(false);
      void refreshSessions(historyQuery, activeProjectId);
    }
  };

  const handleStopStreaming = async () => {
    const chatSessionId = streamingSessionIdRef.current;
    if (!chatSessionId || isStopping) {
      return;
    }
    setIsStopping(true);
    try {
      await stopAgentChatSession(chatSessionId);
    } catch (caught) {
      setIsStopping(false);
      showError(caught instanceof Error ? caught.message : "停止会话失败");
    }
  };

  const handleModelChange = async (model: string) => {
    if (!model) {
      return;
    }
    setIsModelSaving(true);
    try {
      const settings = await loadComposerModelState();
      if (!settings || model === settings.agent.model) {
        return;
      }
      const nextSettings: AppSettings = {
        ...settings,
        agent: {
          ...settings.agent,
          model,
        },
      };
      await updateAppConfig(nextSettings);
      await loadComposerModelState();
    } catch (caught) {
      showError(caught instanceof Error ? caught.message : "模型切换失败");
    } finally {
      setIsModelSaving(false);
    }
  };

  const handleModelRefresh = () => {
    if (isSending || isModelLoading || isModelSaving) {
      return;
    }
    void loadComposerModelState();
  };

  if (activeRoute === "settings") {
    return (
      <main className="workbench-surface h-screen overflow-y-auto p-5 font-sans text-ink lg:p-7">
        <AppSettingsPage onBack={handleBackFromSettings} />
      </main>
    );
  }

  return (
    <WorkspaceLayout
      history={
        <HistoryPanel
          projects={projects}
          activeProjectId={activeProjectId}
          sessions={sessions}
          activeSessionId={activeSessionId}
          activeRoute={activeRoute}
          query={historyQuery}
          isProjectLoading={isProjectLoading}
          isLoading={isHistoryLoading}
          isStreaming={isSending}
          onCreateProject={handleCreateProject}
          onOpenProject={handleOpenProject}
          onRenameProject={handleRenameProject}
          onDeleteProject={handleDeleteProject}
          onSelectProject={handleSelectProject}
          onNavigateRoute={handleNavigateRoute}
          onQueryChange={handleSearchChange}
          onSelectSession={handleSelectSession}
        />
      }
      conversation={
        hasNoProjects ? (
          <ProjectOnboarding
            onCreateProject={() => void handleCreateProject("")}
            onOpenProject={() => void handleOpenProject()}
          />
        ) : activeRoute === "new-task" ? (
          <ConversationShell
            session={activeSession}
            messages={conversationMessages}
            envelopes={conversationRuntimeEnvelopes}
            assets={detail?.assets ?? []}
            isLoading={isDetailLoading}
            isStreaming={isSending}
            onPromptSelect={handleSendMessage}
          />
        ) : activeRoute === "notebooks" ? (
          <NotebookPage project={activeProject} />
        ) : activeRoute === "strategies" ? (
          <StrategiesPage project={activeProject} />
        ) : activeRoute === "strategy-deployments" ? (
          <StrategyDeploymentsPage project={activeProject} />
        ) : null
      }
      composer={
        activeRoute === "new-task" && !hasNoProjects ? (
          <Composer
            disabled={!activeProjectId}
            currentModel={composerModelState.currentModel}
            models={composerModelState.models}
            isModelLoading={isModelLoading}
            isModelSaving={isModelSaving}
            isStreaming={isSending}
            isStopping={isStopping}
            placeholder={activeProjectId ? "随心输入" : "先创建或选择项目"}
            onModelChange={(model) => void handleModelChange(model)}
            onModelRefresh={handleModelRefresh}
            onSendMessage={handleSendMessage}
            onStopStreaming={handleStopStreaming}
          />
        ) : null
      }
      insight={
        activeRoute === "notebooks" ? null : <ProjectFilesPanel project={activeProject} />
      }
      contentClassName={activeRoute === "notebooks" ? "p-0" : undefined}
    />
  );
}

type ProjectOnboardingProps = {
  onCreateProject: () => void;
  onOpenProject: () => void;
};

function ProjectOnboarding({
  onCreateProject,
  onOpenProject,
}: ProjectOnboardingProps) {
  return (
    <section className="grid min-h-[calc(100vh-160px)] place-items-center">
      <Card className="w-full max-w-xl border-dashed text-center">
        <CardHeader>
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg border bg-muted text-accent">
            <FolderOpen className="h-6 w-6" />
          </div>
          <CardTitle className="mt-3 text-xl">创建或打开项目</CardTitle>
          <CardDescription className="mx-auto max-w-md leading-6">
            Chat Quant 需要先绑定一个本地项目目录，策略、会话和运行产物都会归属到这个项目。
          </CardDescription>
        </CardHeader>
        <CardContent>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Button
            type="button"
            onClick={onCreateProject}
          >
            <Plus className="h-4 w-4" />
            新建项目
          </Button>
          <Button
            variant="outline"
            type="button"
            onClick={onOpenProject}
          >
            <FolderOpen className="h-4 w-4" />
            打开已有目录
          </Button>
        </div>
        </CardContent>
      </Card>
    </section>
  );
}

async function selectCreateProjectPath(): Promise<string | null> {
  if (window.chatqDesktop?.createProjectDirectory) {
    return window.chatqDesktop.createProjectDirectory();
  }
  return window.prompt("输入要创建或注册的本地项目目录")?.trim() || null;
}

async function selectOpenProjectPath(): Promise<string | null> {
  if (window.chatqDesktop?.selectProjectDirectory) {
    return window.chatqDesktop.selectProjectDirectory();
  }
  return window.prompt("输入要打开的本地项目目录")?.trim() || null;
}

function routeFromPath(pathname: string): PrimaryRoute {
  if (pathname === routePaths.settings || pathname.startsWith(`${routePaths.settings}/`)) {
    return "settings";
  }
  if (
    pathname === routePaths["strategy-deployments"] ||
    pathname.startsWith(`${routePaths["strategy-deployments"]}/`)
  ) {
    return "strategy-deployments";
  }
  if (pathname === routePaths.notebooks || pathname.startsWith(`${routePaths.notebooks}/`)) {
    return "notebooks";
  }
  return pathname.endsWith(routePaths.strategies) ? "strategies" : "new-task";
}

async function getAgentDetailOrNull(chatSessionId: string): Promise<AgentChatSessionDetail | null> {
  try {
    return await getAgentChatSessionDetail(chatSessionId);
  } catch {
    return null;
  }
}

function agentDetailEnvelopes(agentDetail: AgentChatSessionDetail): SDKStreamEnvelope[] {
  return agentDetail.envelopes.length > 0 ? agentDetail.envelopes : agentDetail.sdk_messages;
}

function messagesFromEnvelopes(envelopes: SDKStreamEnvelope[]): SdkMessage[] {
  const messages: SdkMessage[] = [];
  const seenUserMessageIds = new Set<string>();
  let activeAssistant: {
    id: string;
    text: string;
    createdAt: string;
    sourceSequence: number;
  } | null = null;

  const flushAssistant = () => {
    if (!activeAssistant?.text.trim()) {
      activeAssistant = null;
      return;
    }
    messages.push(
      makeTextMessage({
        id: activeAssistant.id,
        role: "assistant",
        text: activeAssistant.text,
        createdAt: activeAssistant.createdAt,
        sourceSequence: activeAssistant.sourceSequence,
      }),
    );
    activeAssistant = null;
  };

  [...envelopes]
    .sort((left, right) => left.sequence - right.sequence)
    .forEach((envelope) => {
      const event = unwrapEvent(envelope.sdk_event);
      const type = asString(event.type);

      if (type === "user_message") {
        flushAssistant();
        const text = textFromUserEvent(event);
        const id = userEventId(event) ?? `sdk_user_${envelope.sequence}`;
        if (text && isDisplayableUserMessage(event) && !seenUserMessageIds.has(id)) {
          seenUserMessageIds.add(id);
          messages.push(
            makeTextMessage({
              id,
              role: "user",
              text,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            }),
          );
        }
        return;
      }

      if (type === "assistant_message") {
        const text = assistantTextFromEvent(event);
        if (text) {
          activeAssistant = {
            id: asString(event.id) ?? asString(event.uuid) ?? `sdk_assistant_${envelope.sequence}`,
            text,
            createdAt: activeAssistant?.createdAt ?? envelope.received_at,
            sourceSequence: activeAssistant?.sourceSequence ?? envelope.sequence,
          };
          flushAssistant();
        }
        return;
      }

      const deltaText = assistantDeltaTextFromEvent(event);
      if (deltaText) {
        activeAssistant = {
          id: activeAssistant?.id ?? `sdk_assistant_stream_${envelope.sequence}`,
          text: appendStreamText(activeAssistant?.text ?? "", deltaText, true),
          createdAt: activeAssistant?.createdAt ?? envelope.received_at,
          sourceSequence: activeAssistant?.sourceSequence ?? envelope.sequence,
        };
        return;
      }

      if (type === "result_message") {
        if (!activeAssistant && messages.every((message) => message.role !== "assistant")) {
          const resultText = asString(event.result);
          if (resultText) {
            activeAssistant = {
              id: asString(event.uuid) ?? `sdk_result_${envelope.sequence}`,
              text: resultText,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            };
          }
        }
        flushAssistant();
        return;
      }

      if (type === "runtime_error") {
        flushAssistant();
        const message = asString(event.message);
        if (message) {
          messages.push(
            makeTextMessage({
              id: asString(event.uuid) ?? `sdk_error_${envelope.sequence}`,
              role: "assistant",
              text: `运行失败：${message}`,
              createdAt: envelope.received_at,
              sourceSequence: envelope.sequence,
            }),
          );
        }
      }
    });

  flushAssistant();
  return messages;
}

function makeTextMessage({
  id,
  role,
  text,
  createdAt,
  sourceSequence,
}: {
  id: string;
  role: SdkMessage["role"];
  text: string;
  createdAt: string;
  sourceSequence?: number;
}): SdkMessage {
  return {
    uuid: id,
    role,
    content: [{ type: "text", text, tool_use_id: null, name: null }],
    created_at: createdAt,
    source_sequence: sourceSequence,
  };
}

function assistantTextFromEvent(event: Record<string, unknown>): string | null {
  const text = textFromContentBlocks(event.content);
  if (text) {
    return text;
  }
  const message = asRecord(event.message);
  return message ? textFromContentBlocks(message.content) : null;
}

function assistantDeltaTextFromEvent(event: Record<string, unknown>): string | null {
  const type = asString(event.type);
  if (type === "content_block_delta") {
    const delta = asRecord(event.delta);
    return asString(delta?.text) ?? asString(event.text) ?? null;
  }
  if (type === "text_delta") {
    return asString(event.text) ?? asString(asRecord(event.delta)?.text);
  }
  return null;
}

function appendStreamText(current: string, next: string, isDelta: boolean): string {
  if (!current) {
    return next;
  }
  if (!next) {
    return current;
  }
  if (!isDelta) {
    return `${current}\n\n${next}`;
  }
  if (current.endsWith("\n") || next.startsWith("\n") || next.startsWith(" ")) {
    return `${current}${next}`;
  }
  if (shouldInsertSpace(current, next)) {
    return `${current} ${next}`;
  }
  return `${current}${next}`;
}

function shouldInsertSpace(current: string, next: string): boolean {
  const last = current[current.length - 1];
  const first = next[0];
  return /[A-Za-z0-9]/.test(last) && /[A-Za-z0-9]/.test(first);
}

function textFromContentBlocks(content: unknown): string | null {
  if (!Array.isArray(content)) {
    return null;
  }
  const text = content
    .map((block) =>
      block &&
      typeof block === "object" &&
      "type" in block &&
      block.type === "text" &&
      "text" in block &&
      typeof block.text === "string"
        ? block.text
        : null,
    )
    .filter((value): value is string => Boolean(value))
    .join("\n");
  return text || null;
}

function textFromUserEvent(event: Record<string, unknown>): string | null {
  const content = event.content;
  if (typeof content === "string") {
    return content;
  }
  const text = textFromContentBlocks(content);
  if (text) {
    return text;
  }
  const message = asRecord(event.message);
  const messageContent = message?.content;
  return typeof messageContent === "string" ? messageContent : textFromContentBlocks(messageContent);
}

function isDisplayableUserMessage(event: Record<string, unknown>): boolean {
  if (isInternalSkillContext(textFromUserEvent(event))) {
    return false;
  }
  if (typeof event.content === "string") {
    return true;
  }
  if (textFromContentBlocks(event.content)) {
    return true;
  }
  const message = asRecord(event.message);
  return typeof message?.content === "string" || Boolean(textFromContentBlocks(message?.content));
}

function isInternalSkillContext(text: string | null): boolean {
  return Boolean(text?.trimStart().startsWith("Base directory for this skill:"));
}

function fallbackMessagesFromSession(session: ChatSession): SdkMessage[] {
  const text = fallbackUserTextFromSession(session);
  if (!text) {
    return [];
  }
  return [
    {
      uuid: `session_fallback_${session.id}`,
      role: "user",
      content: [{ type: "text", text, tool_use_id: null, name: null }],
      created_at: session.last_saved_at ?? session.updated_at ?? session.created_at,
    },
  ];
}

function fallbackUserTextFromSession(session: ChatSession): string | null {
  const summaryPrefix = "最近请求：";
  if (session.snippet?.trim()) {
    return session.snippet.trim();
  }
  if (session.summary?.startsWith(summaryPrefix)) {
    return session.summary.slice(summaryPrefix.length).trim() || null;
  }
  if (session.title && session.title !== "Chat-Quant 分析会话" && session.title !== "新的分析会话") {
    return session.title;
  }
  return null;
}

function appendStreamEnvelope(
  envelopes: SDKStreamEnvelope[],
  nextEnvelope: SDKStreamEnvelope,
): SDKStreamEnvelope[] {
  const lastSequence = envelopes.at(-1)?.sequence ?? 0;
  const sequence =
    nextEnvelope.sequence > lastSequence ? nextEnvelope.sequence : lastSequence + 1;
  return [...envelopes, { ...nextEnvelope, sequence }];
}

function appendOptimisticUserMessage({
  envelopes,
  chatSessionId,
  sdkSessionId,
  userMessageId,
  content,
}: {
  envelopes: SDKStreamEnvelope[];
  chatSessionId: string;
  sdkSessionId: string | null;
  userMessageId: string;
  content: string;
}): SDKStreamEnvelope[] {
  if (envelopes.some((envelope) => userEventId(unwrapEvent(envelope.sdk_event)) === userMessageId)) {
    return envelopes;
  }
  const lastSequence = envelopes.at(-1)?.sequence ?? 0;
  return [
    ...envelopes,
    {
      sequence: lastSequence + 1,
      chat_session_id: chatSessionId,
      sdk_session_id: sdkSessionId,
      turn_id: null,
      received_at: formatLocalDateTime(new Date()),
      sdk_event: {
        type: "user_message",
        id: userMessageId,
        content,
      },
    },
  ];
}

function userEventId(event: Record<string, unknown>): string | null {
  const message = asRecord(event.message);
  return asString(event.id) ?? asString(event.uuid) ?? asString(message?.id) ?? asString(message?.uuid);
}

function formatLocalDateTime(value: Date): string {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  const hour = String(value.getHours()).padStart(2, "0");
  const minute = String(value.getMinutes()).padStart(2, "0");
  const second = String(value.getSeconds()).padStart(2, "0");
  const millisecond = String(value.getMilliseconds()).padStart(3, "0");
  return `${year}-${month}-${day}T${hour}:${minute}:${second}.${millisecond}`;
}

function unwrapEvent(event: Record<string, unknown>): Record<string, unknown> {
  const innerEvent = asRecord(event.event);
  if (event.type === "stream_event" && innerEvent) {
    return { ...innerEvent, uuid: event.uuid, session_id: event.session_id };
  }
  if (event.type === "stream_event") {
    return normalizeFlattenedStreamEvent(event);
  }
  return event;
}

function normalizeFlattenedStreamEvent(event: Record<string, unknown>): Record<string, unknown> {
  const delta = asRecord(event.delta);
  const deltaType = asString(delta?.type);
  if (deltaType === "text_delta") {
    return { ...event, type: "text_delta", text: delta?.text };
  }
  if (deltaType === "thinking_delta") {
    return { ...event, type: "content_block_delta" };
  }
  if (delta && ("text" in delta || "thinking" in delta)) {
    return { ...event, type: "content_block_delta" };
  }

  const contentBlock = asRecord(event.content_block);
  const contentBlockType = asString(contentBlock?.type);
  if (contentBlockType) {
    return { ...event, ...contentBlock, type: contentBlockType };
  }

  if (typeof event.result === "string") {
    return { ...event, type: "result_message" };
  }
  return event;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" && value.trim().length > 0 ? value : null;
}
