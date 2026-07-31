import {
  Activity,
  AlertCircle,
  BarChart3,
  Brain,
  ChevronDown,
  FileCode2,
  FileText,
  Loader2,
  Search,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { AssetLink, ChatSession, SDKStreamEnvelope, SdkMessage } from "../../shared/api";
import type { Components } from "react-markdown";
import type { ReactNode } from "react";

type ConversationShellProps = {
  session: ChatSession | null;
  messages: SdkMessage[];
  envelopes: SDKStreamEnvelope[];
  assets: AssetLink[];
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
  onPromptSelect?: (content: string) => void | Promise<void>;
};

type UnknownRecord = Record<string, unknown>;

type ToolCallView = {
  id: string;
  groupId: string;
  name: string;
  command: string;
  status: "running" | "completed" | "failed";
  turnId: string | null;
  startedAt: string;
  completedAt: string | null;
  detail: string | null;
  sequence: number;
};

type ToolGroupView = {
  id: string;
  turnId: string | null;
  calls: ToolCallView[];
  status: "running" | "completed" | "failed";
  startedAt: string;
  completedAt: string | null;
  sequence: number;
};

type ThinkingProcessView = {
  id: string;
  text: string;
  segmentCount: number;
  startedAt: string;
  completedAt: string;
  sequence: number;
};

type TimelineItem =
  | {
      type: "message";
      id: string;
      timestamp: string;
      sequence: number;
      message: SdkMessage;
    }
  | {
      type: "thinking";
      id: string;
      timestamp: string;
      sequence: number;
      thinking: ThinkingProcessView;
    }
  | {
      type: "tool";
      id: string;
      timestamp: string;
      sequence: number;
      toolGroup: ToolGroupView;
    };

type TimelineStageTone = "thinking" | "tool" | "answer" | "error";

type TimelineGroup =
  | {
      type: "user";
      id: string;
      item: Extract<TimelineItem, { type: "message" }>;
    }
  | {
      type: "turn";
      id: string;
      items: TimelineItem[];
    };

const markdownComponents: Components = {
  table({ children }) {
    return (
      <div className="markdown-table-scroll">
        <table>{children}</table>
      </div>
    );
  },
};

function blockText(message: SdkMessage): string {
  const text = message.content
    .filter((block) => block.type === "text")
    .map((block) => block.text)
    .filter((value): value is string => Boolean(value))
    .join("\n");
  return text || "工具调用结果已记录";
}

function hasTextContent(message: SdkMessage): boolean {
  return message.content.some((block) => block.type === "text" && Boolean(block.text));
}

export function ConversationShell({
  session,
  messages,
  envelopes,
  assets,
  isLoading,
  isStreaming,
  error,
  onPromptSelect,
}: ConversationShellProps) {
  const [now, setNow] = useState(() => Date.now());
  const textMessages = useMemo(() => messages.filter(hasTextContent), [messages]);
  const toolCalls = useMemo(() => buildToolCalls(envelopes), [envelopes]);
  const toolGroups = useMemo(() => buildToolGroups(toolCalls), [toolCalls]);
  const thinkingProcesses = useMemo(() => buildThinkingProcesses(envelopes), [envelopes]);
  const timelineItems = useMemo(
    () => buildTimelineItems(textMessages, thinkingProcesses, toolGroups),
    [textMessages, thinkingProcesses, toolGroups],
  );
  const timelineGroups = useMemo(() => buildTimelineGroups(timelineItems), [timelineItems]);
  const activityLabel = useMemo(
    () => currentActivityLabel(isStreaming, timelineItems),
    [isStreaming, timelineItems],
  );
  const elapsedLabel = useMemo(
    () =>
      formatElapsed(
        getRunStartedAt(textMessages, envelopes),
        isStreaming ? new Date(now).toISOString() : getRunEndedAt(envelopes),
      ),
    [envelopes, isStreaming, textMessages, now],
  );
  const latestAssistantId = useMemo(() => {
    for (let index = textMessages.length - 1; index >= 0; index -= 1) {
      if (textMessages[index].role === "assistant") {
        return textMessages[index].uuid;
      }
    }
    return null;
  }, [textMessages]);
  const latestUserId = useMemo(() => {
    for (let index = textMessages.length - 1; index >= 0; index -= 1) {
      if (textMessages[index].role === "user") {
        return textMessages[index].uuid;
      }
    }
    return null;
  }, [textMessages]);

  useEffect(() => {
    if (!isStreaming) {
      return undefined;
    }
    const intervalId = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(intervalId);
  }, [isStreaming]);

  return (
    <section aria-label="对话线程">
      <div className="mx-auto w-full max-w-3xl space-y-6">
        {error ? (
          <div className="flex items-start gap-3 rounded-md border-2 border-red-500 bg-red-50/20 p-4 text-xs font-medium text-red-950 shadow-md">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-600" />
            <span className="min-w-0 break-words">{error}</span>
          </div>
        ) : null}

        {isLoading ? (
          <div className="rounded-md border border-zinc-300 bg-zinc-50/50 p-4 text-xs text-zinc-600">
            加载中
          </div>
        ) : null}

        {!isLoading && !session ? (
          <NewTaskHome isDisabled={isStreaming} onPromptSelect={onPromptSelect} />
        ) : null}

        {session && timelineItems.length === 0 && !isStreaming ? (
          <div className="rounded-md border border-dashed border-zinc-300 bg-zinc-50/50 p-5 text-xs leading-6 text-zinc-500">
            当前会话还没有消息。
          </div>
        ) : null}

        {timelineGroups.length > 0 || (isStreaming && session) || activityLabel ? (
          <div className="space-y-6">
            {timelineGroups.map((group) => {
              if (group.type === "user") {
                const item = group.item;
                return (
                  <div className="space-y-1 pt-5 first:pt-0" key={group.id}>
                    <MessageEntry
                      isStreaming={isStreaming}
                      latestAssistantId={latestAssistantId}
                      message={item.message}
                    />
                    {item.message.uuid === latestUserId && elapsedLabel ? (
                      <TurnStatusEntry elapsedLabel={elapsedLabel} isStreaming={isStreaming} />
                    ) : null}
                  </div>
                );
              }
              return (
                <TimelineRail key={group.id}>
                  {group.items.map((item) => {
                    if (item.type === "message") {
                      const isActive = isStreaming && item.id === lastTimelineItemId(timelineItems);
                      return (
                        <TimelineStage isActive={isActive} key={item.id} tone="answer">
                          <MessageEntry
                            isStreaming={isStreaming}
                            latestAssistantId={latestAssistantId}
                            message={item.message}
                          />
                        </TimelineStage>
                      );
                    }
                    if (item.type === "thinking") {
                      const isActive = isStreaming && item.id === lastTimelineItemId(timelineItems);
                      return (
                        <TimelineStage isActive={isActive} key={item.id} tone="thinking">
                          <ThinkingEntry isActive={isActive} thinking={item.thinking} />
                        </TimelineStage>
                      );
                    }
                    const isActive = isStreaming && item.id === lastTimelineItemId(timelineItems);
                    return (
                      <TimelineStage
                        isActive={isActive}
                        key={item.id}
                        tone={item.toolGroup.status === "failed" ? "error" : "tool"}
                      >
                        <ToolGroupEntry isActive={isActive} toolGroup={item.toolGroup} />
                      </TimelineStage>
                    );
                  })}
                </TimelineRail>
              );
            })}

            {isStreaming && session && thinkingProcesses.length === 0 ? (
              <TimelineRail>
                <TimelineStage isActive tone="thinking">
                  <ThinkingEntry isActive thinking={null} />
                </TimelineStage>
              </TimelineRail>
            ) : null}

            {activityLabel ? <ActivityHint label={activityLabel} /> : null}
          </div>
        ) : null}

        {assets.length > 0 ? (
          <div className="rounded-md border border-zinc-300 bg-white p-4">
            <div className="font-mono text-[10px] font-bold uppercase tracking-wider text-zinc-400">
              会话资产
            </div>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {assets.slice(0, 4).map((asset) => (
                <div className="rounded border border-zinc-200 bg-zinc-50 p-3" key={asset.id}>
                  <div className="truncate text-xs font-bold text-zinc-900">{asset.asset_id}</div>
                  <div className="mt-1 text-xs text-zinc-500">
                    {asset.asset_type} · {asset.relation_type}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null}

      </div>
    </section>
  );
}

const starterPrompts = [
  {
    label: "选股",
    description: "按条件筛候选，比如强势、低估、低回撤。",
    prompt: "帮我筛选近期强势、估值合理且风险可控的股票候选，并说明筛选逻辑。",
    icon: Search,
    iconClass: "text-sky-500",
  },
  {
    label: "诊股",
    description: "拆解个股表现，看看机会、压力位和风险。",
    prompt: "帮我诊断一只股票的基本面、技术面和风险点，并给出后续关注指标。",
    icon: Activity,
    iconClass: "text-emerald-600",
  },
  {
    label: "策略",
    description: "把交易想法变成规则、参数和风控条件。",
    prompt: "帮我设计一个可回测的量化交易策略，包含交易逻辑、参数和风险控制。",
    icon: FileCode2,
    iconClass: "text-violet-500",
  },
  {
    label: "回测",
    description: "验证策略收益、回撤、胜率和基准对比。",
    prompt: "帮我对当前策略做回测，分析收益、回撤、胜率和相对基准表现。",
    icon: BarChart3,
    iconClass: "text-orange-600",
  },
];

function NewTaskHome({
  isDisabled,
  onPromptSelect,
}: {
  isDisabled: boolean;
  onPromptSelect?: (content: string) => void | Promise<void>;
}) {
  return (
    <div className="flex min-h-[calc(100vh-15rem)] items-center justify-center py-12">
      <div className="w-full">
        <div className="mx-auto grid h-12 w-12 place-items-center rounded-full border border-zinc-200 bg-zinc-50 text-zinc-400">
          <Brain className="h-6 w-6" />
        </div>
        <h1 className="mt-5 text-center text-2xl font-semibold text-zinc-900">
          我能帮助你什么
        </h1>
        <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {starterPrompts.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className="flex min-h-32 flex-col items-start justify-between rounded-lg border border-zinc-200 bg-white p-4 text-left shadow-sm transition-colors hover:border-zinc-300 hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-zinc-900/20 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={isDisabled || !onPromptSelect}
                key={item.label}
                type="button"
                onClick={() => void onPromptSelect?.(item.prompt)}
              >
                <Icon className={`h-4 w-4 ${item.iconClass}`} />
                <span className="grid gap-1.5">
                  <span className="text-sm font-semibold leading-5 text-zinc-900">
                    {item.label}
                  </span>
                  <span className="text-xs leading-5 text-zinc-500">{item.description}</span>
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function TimelineRail({ children }: { children: ReactNode }) {
  return (
    <div className="relative space-y-6 before:absolute before:bottom-0 before:left-0 before:top-0 before:w-px before:bg-zinc-200 before:content-['']">
      {children}
    </div>
  );
}

function TimelineStage({
  children,
  isActive = false,
  tone,
}: {
  children: ReactNode;
  isActive?: boolean;
  tone: TimelineStageTone;
}) {
  const toneClass =
    tone === "error"
      ? "bg-red-600 shadow-[0_0_0_1px_rgba(220,38,38,0.35)]"
      : tone === "answer"
        ? "bg-zinc-900 shadow-[0_0_0_1px_rgba(24,24,27,0.22)]"
        : tone === "tool"
          ? "bg-zinc-500 shadow-[0_0_0_1px_rgba(113,113,122,0.28)]"
          : "bg-white shadow-[0_0_0_1px_rgba(113,113,122,0.32)]";
  const activeClass = isActive ? "ring-4 ring-zinc-200/80" : "";

  return (
    <div className="relative pl-6">
      <span
        aria-hidden="true"
        className={`absolute left-0 top-3 z-10 h-3 w-3 -translate-x-1/2 rounded-full border-2 border-white ${toneClass} ${activeClass}`}
      />
      {children}
    </div>
  );
}

function ActivityHint({ label }: { label: string }) {
  return (
    <div className="pl-6 text-xs text-zinc-500">
      <span className="inline-flex items-center gap-2">
        <span className="activity-dot" aria-hidden="true" />
        {label}
      </span>
    </div>
  );
}

function TurnStatusEntry({
  elapsedLabel,
  isStreaming,
}: {
  elapsedLabel: string;
  isStreaming: boolean;
}) {
  return (
    <div className="flex justify-end text-xs text-zinc-500">
      <span className="inline-flex items-center gap-1">
        {isStreaming ? "处理中" : "已处理"} {elapsedLabel}
        <ChevronDown className="h-3.5 w-3.5" />
      </span>
    </div>
  );
}

function MessageEntry({
  message,
  latestAssistantId,
  isStreaming,
}: {
  message: SdkMessage;
  latestAssistantId: string | null;
  isStreaming: boolean;
}) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const isLatestAssistant = message.uuid === latestAssistantId;
  if (isUser) {
    return (
      <article className="flex justify-end">
        <div className="max-w-[min(78%,42rem)] rounded-md border border-zinc-900 bg-zinc-900 px-4 py-3 text-left shadow-sm">
          <p className="whitespace-pre-wrap break-words text-sm font-semibold leading-relaxed text-white">
            {blockText(message)}
          </p>
        </div>
      </article>
    );
  }

  return (
    <article>
      <div className="min-w-0 text-sm leading-relaxed text-zinc-800">
        {isAssistant ? (
          <div>
            <MarkdownContent text={blockText(message)} />
            {isStreaming && isLatestAssistant ? <span className="streaming-caret" /> : null}
          </div>
        ) : (
          <p className="whitespace-pre-wrap break-words">{blockText(message)}</p>
        )}
      </div>
    </article>
  );
}

function MarkdownContent({ text }: { text: string }) {
  return (
    <div className="markdown-content">
      <ReactMarkdown components={markdownComponents} remarkPlugins={[remarkGfm]}>
        {text}
      </ReactMarkdown>
    </div>
  );
}

function ThinkingEntry({
  thinking,
  isActive,
}: {
  thinking: ThinkingProcessView | null;
  isActive: boolean;
}) {
  return (
    <div>
      <details className="group overflow-hidden rounded-md border border-zinc-300 bg-zinc-50/50" open={isActive}>
        <summary className="flex cursor-pointer list-none items-center justify-between px-3.5 py-2 text-xs font-semibold text-zinc-700 transition-colors hover:bg-zinc-100">
          <span className="inline-flex min-w-0 items-center gap-2">
            {isActive ? (
              <span className="thinking-rings text-zinc-500" aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            ) : (
              <Brain className="h-4 w-4 text-zinc-500" />
            )}
            {thinkingSummary(thinking)}
          </span>
          <span className="flex shrink-0 items-center gap-2 text-xs text-zinc-400">
            {thinking ? formatElapsed(thinking.startedAt, thinking.completedAt) : "进行中"}
            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
          </span>
        </summary>
        <p className="whitespace-pre-wrap break-words border-t border-zinc-200 bg-white p-3.5 font-mono text-xs leading-relaxed text-zinc-600">
          {thinking?.text || "正在组织思路"}
          {isActive ? <span className="streaming-caret" /> : null}
        </p>
      </details>
    </div>
  );
}

function ToolGroupEntry({
  toolGroup,
}: {
  toolGroup: ToolGroupView;
  isActive: boolean;
}) {
  const firstToolCall = toolGroup.calls[0];
  if (!firstToolCall) {
    return null;
  }

  return (
    <div aria-label="工具调用">
      <details
        className={`group/tool-group overflow-hidden rounded-md bg-white ${
          toolGroup.status === "failed"
            ? "border-2 border-red-500 bg-red-50/20"
            : "border border-zinc-300"
        }`}
      >
        <summary
          className={`flex cursor-pointer list-none items-center gap-2.5 px-3.5 py-2 font-mono text-xs transition-colors ${
            toolGroup.status === "failed"
              ? "bg-red-50 hover:bg-red-100/60"
              : "bg-zinc-50 hover:bg-zinc-100"
          }`}
        >
          <span className="flex min-w-0 items-center gap-2.5">
            {toolGroup.status === "running" ? (
              <Loader2 className="h-4 w-4 shrink-0 animate-spin text-zinc-700" />
            ) : toolGroup.status === "failed" ? (
              <AlertCircle className="h-4 w-4 shrink-0 text-red-600" />
            ) : (
              <FileText className="h-4 w-4 shrink-0 text-zinc-700" />
            )}
            <span
              className={`truncate font-bold ${
                toolGroup.status === "failed" ? "text-red-950" : "text-zinc-900"
              }`}
            >
              {toolSummary(toolGroup)}
            </span>
            {toolGroup.calls.length === 1 ? (
              <span
                className={`truncate ${
                  toolGroup.status === "failed" ? "text-red-900/80" : "text-zinc-500"
                }`}
              >
                {firstToolCall.command}
              </span>
            ) : null}
          </span>
          <span className="ml-auto flex shrink-0 items-center gap-2">
            <span
              className={`rounded px-2 py-0.5 font-sans text-[10px] font-bold ${toolStatusBadgeClass(
                toolGroup.status,
              )}`}
            >
              {toolStatusLabel(toolGroup.status)}
            </span>
            <ChevronDown
              className={`h-4 w-4 transition-transform group-open/tool-group:rotate-180 ${
                toolGroup.status === "failed" ? "text-red-400" : "text-zinc-400"
              }`}
            />
          </span>
        </summary>
        {toolGroup.calls.length > 1 ? (
          <div className="grid gap-2 border-t border-zinc-300 bg-zinc-50 p-2">
            {toolGroup.calls.map((toolCall) => (
              <ToolCallDisclosure key={toolCall.id} toolCall={toolCall} />
            ))}
          </div>
        ) : (
          <ToolCallDetail toolCall={firstToolCall} />
        )}
      </details>
    </div>
  );
}

function ToolCallDisclosure({ toolCall }: { toolCall: ToolCallView }) {
  return (
    <details className="group/tool-call overflow-hidden rounded border border-zinc-300 bg-white">
      <summary className="flex cursor-pointer list-none items-center gap-2 px-3 py-2 font-mono text-xs transition-colors hover:bg-zinc-100">
        <span className="min-w-0 truncate font-bold text-zinc-900">{toolCall.name}</span>
        <span className="min-w-0 truncate text-zinc-500">{toolCall.command}</span>
        <span className="ml-auto flex shrink-0 items-center gap-2">
          <span
            className={`rounded px-2 py-0.5 font-sans text-[10px] font-bold ${toolStatusBadgeClass(
              toolCall.status,
            )}`}
          >
            {toolStatusLabel(toolCall.status)}
          </span>
          <ChevronDown className="h-4 w-4 text-zinc-400 transition-transform group-open/tool-call:rotate-180" />
        </span>
      </summary>
      <ToolCallDetail toolCall={toolCall} />
    </details>
  );
}

function ToolCallDetail({ toolCall }: { toolCall: ToolCallView }) {
  return (
    <div className="grid gap-3 border-t border-zinc-300 bg-zinc-950 p-3 font-mono text-xs text-zinc-200">
      <div>
        <span className="text-[10px] font-bold uppercase text-zinc-500">Input</span>
        <pre className="mt-0.5 whitespace-pre-wrap break-words text-zinc-300">
          {toolCall.command}
        </pre>
      </div>
      <div>
        <span
          className={`text-[10px] font-bold uppercase ${
            toolCall.status === "failed" ? "text-red-400" : "text-zinc-500"
          }`}
        >
          {toolCall.status === "failed" ? "Stderr Output" : "Output"}
        </span>
        {toolCall.detail ? (
          <pre
            className={`mt-0.5 max-h-64 overflow-auto whitespace-pre-wrap break-words ${
              toolCall.status === "failed" ? "text-red-400" : "text-emerald-400"
            }`}
          >
            {toolCall.detail}
          </pre>
        ) : (
          <pre className="mt-0.5 text-zinc-500">
            {toolCall.status === "running" ? "Running..." : "No output"}
          </pre>
        )}
      </div>
    </div>
  );
}

function toolStatusLabel(status: ToolCallView["status"]): string {
  if (status === "failed") {
    return "FAILED";
  }
  if (status === "running") {
    return "RUNNING";
  }
  return "SUCCESS";
}

function toolStatusBadgeClass(status: ToolCallView["status"]): string {
  if (status === "failed") {
    return "bg-red-600 text-white";
  }
  if (status === "running") {
    return "bg-zinc-900 text-white";
  }
  return "bg-zinc-200 text-zinc-800";
}

function buildTimelineItems(
  messages: SdkMessage[],
  thinkingProcesses: ThinkingProcessView[],
  toolGroups: ToolGroupView[],
): TimelineItem[] {
  const messageItems: TimelineItem[] = messages.map((message) => ({
    type: "message",
    id: `message_${message.uuid}`,
    timestamp: message.created_at,
    sequence: message.source_sequence ?? 0,
    message,
  }));
  const thinkingItems: TimelineItem[] = thinkingProcesses.map((thinking) => ({
    type: "thinking",
    id: `thinking_${thinking.id}`,
    timestamp: thinking.startedAt,
    sequence: thinking.sequence,
    thinking,
  }));
  const toolItems: TimelineItem[] = toolGroups.map((toolGroup) => ({
    type: "tool",
    id: `tool_${toolGroup.id}`,
    timestamp: toolGroup.startedAt,
    sequence: toolGroup.sequence,
    toolGroup,
  }));

  const sortedItems = [...messageItems, ...thinkingItems, ...toolItems].sort((left, right) => {
    if (left.sequence > 0 && right.sequence > 0 && left.sequence !== right.sequence) {
      return left.sequence - right.sequence;
    }
    const timeDelta = timestampMs(left.timestamp) - timestampMs(right.timestamp);
    if (timeDelta !== 0) {
      return timeDelta;
    }
    return left.sequence - right.sequence;
  });

  return mergeConsecutiveTimelineItems(sortedItems);
}

function mergeConsecutiveTimelineItems(items: TimelineItem[]): TimelineItem[] {
  const mergedItems: TimelineItem[] = [];

  items.forEach((item) => {
    const previousItem = mergedItems[mergedItems.length - 1];
    if (previousItem?.type === "tool" && item.type === "tool") {
      mergedItems[mergedItems.length - 1] = mergeToolTimelineItems(previousItem, item);
      return;
    }
    if (previousItem?.type === "thinking" && item.type === "thinking") {
      mergedItems[mergedItems.length - 1] = mergeThinkingTimelineItems(previousItem, item);
      return;
    }
    mergedItems.push(item);
  });

  return mergedItems;
}

function mergeToolTimelineItems(
  left: Extract<TimelineItem, { type: "tool" }>,
  right: Extract<TimelineItem, { type: "tool" }>,
): Extract<TimelineItem, { type: "tool" }> {
  const calls = [...left.toolGroup.calls, ...right.toolGroup.calls].sort(
    (leftCall, rightCall) => leftCall.sequence - rightCall.sequence,
  );
  const firstCall = calls[0];
  return {
    type: "tool",
    id: `${left.id}_${right.id}`,
    timestamp: left.timestamp,
    sequence: left.sequence,
    toolGroup: {
      id: `${left.toolGroup.id}_${right.toolGroup.id}`,
      turnId: left.toolGroup.turnId ?? right.toolGroup.turnId,
      calls,
      status: toolGroupStatus(calls),
      startedAt: firstCall?.startedAt ?? left.toolGroup.startedAt,
      completedAt: latestCompletedAt(calls),
      sequence: firstCall?.sequence ?? left.toolGroup.sequence,
    },
  };
}

function mergeThinkingTimelineItems(
  left: Extract<TimelineItem, { type: "thinking" }>,
  right: Extract<TimelineItem, { type: "thinking" }>,
): Extract<TimelineItem, { type: "thinking" }> {
  return {
    type: "thinking",
    id: `${left.id}_${right.id}`,
    timestamp: left.timestamp,
    sequence: left.sequence,
    thinking: {
      id: `${left.thinking.id}_${right.thinking.id}`,
      text: appendThinkingText(`${left.thinking.text}\n\n`, right.thinking.text),
      segmentCount: left.thinking.segmentCount + right.thinking.segmentCount,
      startedAt: left.thinking.startedAt,
      completedAt: right.thinking.completedAt,
      sequence: left.thinking.sequence,
    },
  };
}

function buildTimelineGroups(items: TimelineItem[]): TimelineGroup[] {
  const groups: TimelineGroup[] = [];
  let activeTurnItems: TimelineItem[] = [];

  const flushTurn = () => {
    if (activeTurnItems.length === 0) {
      return;
    }
    const firstItem = activeTurnItems[0];
    const lastItem = activeTurnItems[activeTurnItems.length - 1];
    groups.push({
      type: "turn",
      id: `turn_${firstItem.id}_${lastItem.id}`,
      items: activeTurnItems,
    });
    activeTurnItems = [];
  };

  items.forEach((item) => {
    if (item.type === "message" && item.message.role === "user") {
      flushTurn();
      groups.push({
        type: "user",
        id: `user_${item.id}`,
        item,
      });
      return;
    }
    activeTurnItems.push(item);
  });

  flushTurn();
  return groups;
}

function currentActivityLabel(isStreaming: boolean, items: TimelineItem[]): string | null {
  if (!isStreaming) {
    return null;
  }
  const latestItem = items[items.length - 1];
  if (!latestItem) {
    return "正在思考";
  }
  if (latestItem.type === "tool") {
    return latestItem.toolGroup.calls.length > 1
      ? "正在运行多个命令"
      : `正在运行 ${truncateText(latestItem.toolGroup.calls[0]?.command ?? "命令", 56)}`;
  }
  if (latestItem.type === "thinking") {
    return "正在思考";
  }
  if (latestItem.type === "message" && latestItem.message.role === "assistant") {
    return "正在输出回复";
  }
  return "正在处理";
}

function lastTimelineItemId(items: TimelineItem[]): string | null {
  return items.length > 0 ? items[items.length - 1].id : null;
}

function buildThinkingProcesses(envelopes: SDKStreamEnvelope[]): ThinkingProcessView[] {
  const processes: ThinkingProcessView[] = [];
  let activeProcess: ThinkingProcessView | null = null;
  const sortedEnvelopes = [...envelopes].sort((left, right) => left.sequence - right.sequence);

  sortedEnvelopes.forEach((envelope) => {
    const event = unwrapEvent(envelope.sdk_event);
    const thinkingText = extractThinkingText(event).join("");
    if (thinkingText) {
      if (!activeProcess) {
        activeProcess = {
          id: `thinking_${envelope.sequence}`,
          text: "",
          segmentCount: 1,
          startedAt: envelope.received_at,
          completedAt: envelope.received_at,
          sequence: envelope.sequence,
        };
      }
      activeProcess = {
        ...activeProcess,
        text: appendThinkingText(activeProcess.text, thinkingText),
        completedAt: envelope.received_at,
      };
      if (isThinkingBoundaryEvent(event)) {
        processes.push(activeProcess);
        activeProcess = null;
      }
      return;
    }

    if (activeProcess && isThinkingBoundaryEvent(event)) {
      processes.push(activeProcess);
      activeProcess = null;
    }
  });

  if (activeProcess) {
    processes.push(activeProcess);
  }

  return processes;
}

function appendThinkingText(current: string, next: string): string {
  if (!current) {
    return next.trimStart();
  }
  if (!next) {
    return current;
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

function isThinkingBoundaryEvent(event: UnknownRecord): boolean {
  const type = asString(event.type);
  if (type === "result_message" || type === "runtime_error" || type === "cancelled") {
    return true;
  }
  if (type === "text_delta") {
    return true;
  }
  if (type === "content_block_delta") {
    const delta = asRecord(event.delta);
    return Boolean(asString(delta?.text) ?? asString(event.text));
  }
  if (extractToolUses(event).length > 0 || extractToolResults(event).length > 0) {
    return true;
  }
  return textFromEventContent(event).length > 0;
}

function promptIdFromEvent(event: UnknownRecord): string | null {
  return asString(event.promptId) ?? asString(event.prompt_id);
}

function isHumanUserBoundaryEvent(event: UnknownRecord): boolean {
  if (asString(event.type) !== "user_message") {
    return false;
  }
  const content = event.content;
  if (typeof content === "string") {
    return true;
  }
  const message = asRecord(event.message);
  return typeof message?.content === "string";
}

function buildToolCalls(envelopes: SDKStreamEnvelope[]): ToolCallView[] {
  const toolCalls = new Map<string, ToolCallView>();
  const sortedEnvelopes = [...envelopes].sort((left, right) => left.sequence - right.sequence);
  let currentFallbackTurnId: string | null = null;
  let currentToolGroupId: string | null = null;
  let previousToolUseSequence: number | null = null;

  sortedEnvelopes.forEach((envelope) => {
    const event = unwrapEvent(envelope.sdk_event);
    const eventTurnId = envelope.turn_id ?? promptIdFromEvent(event);
    if (eventTurnId) {
      currentFallbackTurnId = eventTurnId;
    } else if (isHumanUserBoundaryEvent(event)) {
      currentFallbackTurnId = `fallback_turn_${envelope.sequence}`;
    }
    const turnId = eventTurnId ?? currentFallbackTurnId;
    const toolUses = extractToolUses(event);
    const toolResults = extractToolResults(event);

    if (toolUses.length > 0) {
      if (previousToolUseSequence === null || envelope.sequence > previousToolUseSequence + 1) {
        currentToolGroupId = `tool_group_${envelope.sequence}`;
      }
      previousToolUseSequence = envelope.sequence;
    }

    toolUses.forEach((toolUse) => {
      toolCalls.set(toolUse.id, {
        id: toolUse.id,
        groupId: currentToolGroupId ?? `tool_group_${envelope.sequence}`,
        name: toolUse.name,
        command: toolUse.command,
        status: "running",
        turnId,
        startedAt: envelope.received_at,
        completedAt: null,
        detail: formatDetail(toolUse.input),
        sequence: envelope.sequence,
      });
    });

    toolResults.forEach((toolResult) => {
      const existing = toolCalls.get(toolResult.id);
      toolCalls.set(toolResult.id, {
        id: toolResult.id,
        groupId: existing?.groupId ?? `tool_group_${envelope.sequence}`,
        name: existing?.name ?? "工具",
        command: existing?.command ?? "工具调用",
        status: toolResult.isError ? "failed" : "completed",
        turnId: existing?.turnId ?? turnId,
        startedAt: existing?.startedAt ?? envelope.received_at,
        completedAt: envelope.received_at,
        detail: mergeDetail(existing?.detail ?? null, toolResult.content),
        sequence: existing?.sequence ?? envelope.sequence,
      });
    });
  });

  return [...toolCalls.values()];
}

function buildToolGroups(toolCalls: ToolCallView[]): ToolGroupView[] {
  const sortedToolCalls = [...toolCalls].sort((left, right) => left.sequence - right.sequence);
  if (sortedToolCalls.length === 0) {
    return [];
  }

  const groups = new Map<string, ToolCallView[]>();
  sortedToolCalls.forEach((toolCall) => {
    const key = toolCall.groupId;
    groups.set(key, [...(groups.get(key) ?? []), toolCall]);
  });

  return [...groups.entries()].map(([key, calls]) => ({
    id: `${key}_${calls.map((toolCall) => toolCall.id).join("_")}`,
    turnId: calls[0]?.turnId ?? null,
    calls,
    status: toolGroupStatus(calls),
    startedAt: calls[0].startedAt,
    completedAt: latestCompletedAt(calls),
    sequence: calls[0].sequence,
  }));
}

function toolGroupStatus(toolCalls: ToolCallView[]): ToolGroupView["status"] {
  if (toolCalls.some((toolCall) => toolCall.status === "failed")) {
    return "failed";
  }
  if (toolCalls.some((toolCall) => toolCall.status === "running")) {
    return "running";
  }
  return "completed";
}

function latestCompletedAt(toolCalls: ToolCallView[]): string | null {
  const completedTimes = toolCalls
    .map((toolCall) => toolCall.completedAt)
    .filter((value): value is string => Boolean(value))
    .sort((left, right) => timestampMs(right) - timestampMs(left));
  return completedTimes[0] ?? null;
}

function thinkingSummary(thinking: ThinkingProcessView | null): string {
  if (thinking && thinking.segmentCount > 1) {
    return `多次思考 · ${thinking.segmentCount} 次`;
  }
  return "思考逻辑 (Task Decomposition)";
}

function toolSummary(toolGroup: ToolGroupView): string {
  if (toolGroup.calls.length > 1) {
    return `多个命令 · ${toolGroup.calls.length} 个`;
  }
  const name = toolGroup.calls[0]?.name ?? "command";
  return `tool:${name}`;
}

function truncateText(value: string, maxLength: number): string {
  if (value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, maxLength - 1)}…`;
}

function extractToolUses(event: UnknownRecord): Array<{
  id: string;
  name: string;
  command: string;
  input: unknown;
}> {
  return collectEventAndBlocks(event)
    .filter((block) => asString(block.type) === "tool_use")
    .map((block) => {
      const input = asRecord(block.input);
      const command = asString(input?.command) ?? formatDetail(input) ?? "工具调用";
      return {
        id: asString(block.id) ?? `tool_${command}`,
        name: asString(block.name) ?? "工具",
        command,
        input: block.input,
      };
    });
}

function extractToolResults(event: UnknownRecord): Array<{
  id: string;
  content: string | null;
  isError: boolean;
}> {
  return collectEventAndBlocks(event)
    .filter((block) => asString(block.type) === "tool_result")
    .map((block) => ({
      id: asString(block.tool_use_id) ?? "tool_result",
      content: stringifyToolResult(block.content),
      isError: block.is_error === true,
    }));
}

function extractThinkingText(event: UnknownRecord): string[] {
  return collectEventAndBlocks(event)
    .map((block) => {
      const thinking = asString(block.thinking);
      if (thinking) return thinking;
      const delta = asRecord(block.delta);
      const deltaThinking = asString(delta?.thinking);
      if (deltaThinking) return deltaThinking;
      if (asString(block.type) === "thinking") {
        return asString(block.text) ?? asString(block.content);
      }
      return null;
    })
    .filter((value): value is string => Boolean(value?.trim()));
}

function textFromEventContent(event: UnknownRecord): string[] {
  return collectEventAndBlocks(event)
    .map((block) => {
      if (asString(block.type) === "text") {
        return asString(block.text);
      }
      const delta = asRecord(block.delta);
      return asString(delta?.text) ?? asString(block.text);
    })
    .filter((value): value is string => Boolean(value?.trim()));
}

function collectEventAndBlocks(event: UnknownRecord): UnknownRecord[] {
  const blocks: UnknownRecord[] = [event];
  const content = event.content;
  if (Array.isArray(content)) {
    content.forEach((block) => {
      const record = asRecord(block);
      if (record) {
        blocks.push(record);
      }
    });
  }
  return blocks;
}

function unwrapEvent(event: UnknownRecord): UnknownRecord {
  const innerEvent = asRecord(event.event);
  if (asString(event.type) === "stream_event" && innerEvent) {
    return { ...innerEvent, uuid: event.uuid, session_id: event.session_id };
  }
  if (asString(event.type) === "stream_event") {
    return normalizeFlattenedStreamEvent(event);
  }
  return event;
}

function normalizeFlattenedStreamEvent(event: UnknownRecord): UnknownRecord {
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

function stringifyToolResult(content: unknown): string | null {
  if (typeof content === "string") {
    return content;
  }
  return formatDetail(content);
}

function mergeDetail(existing: string | null, result: string | null): string | null {
  if (!existing) {
    return result;
  }
  if (!result) {
    return existing;
  }
  return `${existing}\n\n返回：\n${result}`;
}

function formatDetail(value: unknown): string | null {
  if (value === null || value === undefined) {
    return null;
  }
  if (typeof value === "string") {
    return value;
  }
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

function getRunStartedAt(messages: SdkMessage[], envelopes: SDKStreamEnvelope[]): string | null {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    if (messages[index].role === "user") {
      return messages[index].created_at;
    }
  }
  return envelopes[0]?.received_at ?? null;
}

function getRunEndedAt(envelopes: SDKStreamEnvelope[]): string | null {
  return envelopes.length > 0 ? envelopes[envelopes.length - 1].received_at : null;
}

function timestampMs(value: string): number {
  const parsed = new Date(value).getTime();
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatElapsed(startAt: string | null, endAt: string | null): string | null {
  if (!startAt || !endAt) {
    return null;
  }
  const start = new Date(startAt).getTime();
  const end = new Date(endAt).getTime();
  if (!Number.isFinite(start) || !Number.isFinite(end) || end < start) {
    return null;
  }
  const totalSeconds = Math.max(1, Math.round((end - start) / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  if (minutes > 0) {
    return `${minutes}m ${seconds}s`;
  }
  return `${seconds}s`;
}

function asRecord(value: unknown): UnknownRecord | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as UnknownRecord)
    : null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}
