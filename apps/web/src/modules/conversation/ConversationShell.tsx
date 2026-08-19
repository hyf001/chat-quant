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
import { Children, useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

import type { AssetLink, ChatSession, SDKStreamEnvelope, SdkMessage } from "../../shared/api";
import type { Components } from "react-markdown";
import type { ReactNode } from "react";
import type { InspectorObject } from "../../shared/api/types";

type ConversationShellProps = {
  session: ChatSession | null;
  messages: SdkMessage[];
  envelopes: SDKStreamEnvelope[];
  assets: AssetLink[];
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
  onOpenInspectorObject?: (object: InspectorObject) => void;
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

const tradingValidationIllustrationSrc = `${import.meta.env.BASE_URL}trading-validation-illustration.png`;
const inspectorIdPattern = /\b(?:sbt|str|stv)_[A-Za-z0-9]+\b/g;

function markdownComponentsFor(
  onOpenInspectorObject?: (object: InspectorObject) => void,
): Components {
  return {
    ...markdownComponents,
    p({ children }) {
      return <p>{linkifyInspectorIds(children, onOpenInspectorObject)}</p>;
    },
    li({ children }) {
      return <li>{linkifyInspectorIds(children, onOpenInspectorObject)}</li>;
    },
    td({ children }) {
      return <td>{linkifyInspectorIds(children, onOpenInspectorObject)}</td>;
    },
    th({ children }) {
      return <th>{linkifyInspectorIds(children, onOpenInspectorObject)}</th>;
    },
    h1({ children }) {
      return <h1>{linkifyInspectorIds(children, onOpenInspectorObject)}</h1>;
    },
    h2({ children }) {
      return <h2>{linkifyInspectorIds(children, onOpenInspectorObject)}</h2>;
    },
    h3({ children }) {
      return <h3>{linkifyInspectorIds(children, onOpenInspectorObject)}</h3>;
    },
    h4({ children }) {
      return <h4>{linkifyInspectorIds(children, onOpenInspectorObject)}</h4>;
    },
    a({ children, href }) {
      return (
        <a href={href} rel="noreferrer" target={href?.startsWith("http") ? "_blank" : undefined}>
          {children}
        </a>
      );
    },
  };
}

function inspectorObjectFromId(id: string): InspectorObject | null {
  if (id.startsWith("sbt_")) {
    return { type: "backtest", id };
  }
  if (id.startsWith("str_")) {
    return { type: "strategy", id };
  }
  if (id.startsWith("stv_")) {
    return { type: "strategy-version", id };
  }
  return null;
}

function linkifyInspectorIds(
  children: ReactNode,
  onOpenInspectorObject?: (object: InspectorObject) => void,
): ReactNode {
  if (!onOpenInspectorObject) {
    return children;
  }
  return Children.toArray(children).flatMap((child, childIndex) => {
    if (typeof child !== "string") {
      return child;
    }
    return linkifyString(child, childIndex, onOpenInspectorObject);
  });
}

function linkifyString(
  value: string,
  childIndex: number,
  onOpenInspectorObject: (object: InspectorObject) => void,
): ReactNode[] {
  const nodes: ReactNode[] = [];
  let lastIndex = 0;
  for (const match of value.matchAll(inspectorIdPattern)) {
    const id = match[0];
    const index = match.index ?? 0;
    const object = inspectorObjectFromId(id);
    if (!object) {
      continue;
    }
    if (index > lastIndex) {
      nodes.push(value.slice(lastIndex, index));
    }
    nodes.push(
      <button
        className="inline font-mono text-xs font-semibold text-brandBlue underline decoration-brandBlue/40 decoration-dotted underline-offset-2 transition-colors hover:text-signal focus:outline-none focus:ring-2 focus:ring-signal/20"
        key={`${id}-${childIndex}-${index}`}
        type="button"
        onClick={() => onOpenInspectorObject(object)}
      >
        {id}
      </button>,
    );
    lastIndex = index + id.length;
  }
  if (lastIndex === 0) {
    return [value];
  }
  if (lastIndex < value.length) {
    nodes.push(value.slice(lastIndex));
  }
  return nodes;
}

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
  onOpenInspectorObject,
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
        isStreaming ? formatLocalDateTime(new Date(now)) : getRunEndedAt(envelopes),
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
      <div className="mx-auto w-full max-w-5xl space-y-6">
        {error ? (
          <div className="flex items-start gap-3 rounded-md border border-destructive/30 bg-destructive/5 p-4 text-xs font-medium text-destructive shadow-sm">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            <span className="min-w-0 break-words">{error}</span>
          </div>
        ) : null}

        {isLoading ? (
          <Card className="p-4 text-xs text-muted-foreground">
            加载中
          </Card>
        ) : null}

        {!isLoading && !session ? (
          <NewTaskHome isDisabled={isStreaming} onPromptSelect={onPromptSelect} />
        ) : null}

        {session && timelineItems.length === 0 && !isStreaming ? (
          <Card className="border-dashed p-5 text-xs leading-6 text-muted-foreground">
            当前会话还没有消息。
          </Card>
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
                      onOpenInspectorObject={onOpenInspectorObject}
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
                            onOpenInspectorObject={onOpenInspectorObject}
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
          <Card className="p-4">
            <div className="font-mono text-[10px] font-bold uppercase text-mutedText">
              会话资产
            </div>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {assets.slice(0, 4).map((asset) => (
                <Card className="rounded-md bg-muted p-3 shadow-none" key={asset.id}>
                  <div className="truncate text-xs font-bold text-ink">{asset.asset_id}</div>
                  <div className="mt-1 text-xs text-mutedText">
                    {asset.asset_type} · {asset.relation_type}
                  </div>
                </Card>
              ))}
            </div>
          </Card>
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
    iconClass: "text-brandBlue",
  },
  {
    label: "诊股",
    description: "拆解个股表现，看看机会、压力位和风险。",
    prompt: "帮我诊断一只股票的基本面、技术面和风险点，并给出后续关注指标。",
    icon: Activity,
    iconClass: "text-brand",
  },
  {
    label: "策略",
    description: "把交易想法变成规则、参数和风控条件。",
    prompt: "帮我设计一个可回测的量化交易策略，包含交易逻辑、参数和风险控制。",
    icon: FileCode2,
    iconClass: "text-signal",
  },
  {
    label: "回测",
    description: "验证策略收益、回撤、胜率和基准对比。",
    prompt: "帮我对当前策略做回测，分析收益、回撤、胜率和相对基准表现。",
    icon: BarChart3,
    iconClass: "text-risk",
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
    <div className="grid min-h-[calc(100vh-15rem)] items-center py-6">
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.05fr)_minmax(280px,0.95fr)]">
        <section className="research-briefing flex min-h-72 items-center justify-center overflow-hidden rounded-lg border border-strong p-0 shadow-panel lg:min-h-[22rem]">
          <img
            alt="交易策略验证流程插画"
            className="pointer-events-none h-80 w-auto max-w-none select-none object-contain sm:h-[22rem] lg:h-[25rem]"
            src={tradingValidationIllustrationSrc}
          />
        </section>

        <div className="grid gap-3 sm:grid-cols-2">
          {starterPrompts.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                className="flex h-auto min-h-32 flex-col items-start justify-between p-4 text-left"
                disabled={isDisabled || !onPromptSelect}
                key={item.label}
                type="button"
                variant="outline"
                onClick={() => void onPromptSelect?.(item.prompt)}
              >
                <span className="flex w-full items-center justify-between">
                  <span className="grid h-8 w-8 place-items-center rounded-md border bg-muted">
                    <Icon className={`h-4 w-4 ${item.iconClass}`} />
                  </span>
                  <Badge className="font-mono text-[10px] uppercase" variant="secondary">
                    Start
                  </Badge>
                </span>
                <span className="grid gap-1.5">
                  <span className="text-sm font-semibold leading-5 text-ink">{item.label}</span>
                  <span className="text-xs leading-5 text-mutedText">{item.description}</span>
                </span>
              </Button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function TimelineRail({ children }: { children: ReactNode }) {
  return (
    <div className="execution-tape relative rounded-lg border border-line bg-panel/80 shadow-sm">
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
      ? "is-error"
      : tone === "answer"
        ? "is-answer"
        : tone === "tool"
          ? "is-tool"
          : "is-thinking";
  const activeClass = isActive ? "ring-4 ring-signalSoft" : "";

  return (
    <div className="timeline-event relative">
      <span
        aria-hidden="true"
        className={`execution-node ${toneClass} ${activeClass}`}
      >
        {timelineStageLabel(tone)}
      </span>
      {children}
    </div>
  );
}

function timelineStageLabel(tone: TimelineStageTone): string {
  if (tone === "thinking") {
    return "AI";
  }
  if (tone === "tool") {
    return "RUN";
  }
  if (tone === "error") {
    return "ERR";
  }
  return "OUT";
}

function ActivityHint({ label }: { label: string }) {
  return (
    <div className="pl-6 text-xs text-mutedText">
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
    <div className="flex justify-end text-xs text-mutedText">
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
  onOpenInspectorObject,
}: {
  message: SdkMessage;
  latestAssistantId: string | null;
  isStreaming: boolean;
  onOpenInspectorObject?: (object: InspectorObject) => void;
}) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const isLatestAssistant = message.uuid === latestAssistantId;
  if (isUser) {
    return (
      <article className="flex justify-end">
        <div className="max-w-[min(78%,42rem)] rounded-md border border-ink bg-ink px-4 py-3 text-left shadow-sm">
          <p className="whitespace-pre-wrap break-words text-sm font-semibold leading-relaxed text-white">
            {blockText(message)}
          </p>
        </div>
      </article>
    );
  }

  return (
    <article>
      <div className="min-w-0 text-sm leading-relaxed text-graphite">
        {isAssistant ? (
          <div>
            <MarkdownContent text={blockText(message)} onOpenInspectorObject={onOpenInspectorObject} />
            {isStreaming && isLatestAssistant ? <span className="streaming-caret" /> : null}
          </div>
        ) : (
          <p className="whitespace-pre-wrap break-words">{blockText(message)}</p>
        )}
      </div>
    </article>
  );
}

function MarkdownContent({
  text,
  onOpenInspectorObject,
}: {
  text: string;
  onOpenInspectorObject?: (object: InspectorObject) => void;
}) {
  const components = useMemo(
    () => markdownComponentsFor(onOpenInspectorObject),
    [onOpenInspectorObject],
  );
  return (
    <div className="markdown-content">
      <ReactMarkdown
        components={components}
        remarkPlugins={[remarkGfm]}
      >
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
      <details className="group overflow-hidden rounded-md border border-line bg-panel" open={isActive}>
        <summary className="flex cursor-pointer list-none items-center justify-between px-3.5 py-2 text-xs font-semibold text-graphite transition-colors hover:bg-soft">
          <span className="inline-flex min-w-0 items-center gap-2">
            {isActive ? (
              <span className="thinking-rings text-signal" aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            ) : (
              <Brain className="h-4 w-4 text-signal" />
            )}
            {thinkingSummary(thinking)}
          </span>
          <span className="flex shrink-0 items-center gap-2 text-xs text-mutedText">
            {thinking ? formatElapsed(thinking.startedAt, thinking.completedAt) : "进行中"}
            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
          </span>
        </summary>
        <p className="whitespace-pre-wrap break-words border-t border-line bg-soft p-3.5 font-mono text-xs leading-relaxed text-graphite">
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
        className={`group/tool-group overflow-hidden rounded-md bg-panel ${
          toolGroup.status === "failed"
            ? "border-2 border-risk bg-riskSoft"
            : "border border-line"
        }`}
      >
        <summary
          className={`flex cursor-pointer list-none items-center gap-2.5 px-3.5 py-2 font-mono text-xs transition-colors ${
            toolGroup.status === "failed"
              ? "bg-riskSoft hover:bg-riskSoft/70"
              : "bg-soft hover:bg-compareSoft"
          }`}
        >
          <span className="flex min-w-0 items-center gap-2.5">
            {toolGroup.status === "running" ? (
              <Loader2 className="h-4 w-4 shrink-0 animate-spin text-signal" />
            ) : toolGroup.status === "failed" ? (
              <AlertCircle className="h-4 w-4 shrink-0 text-risk" />
            ) : (
              <FileText className="h-4 w-4 shrink-0 text-brandBlue" />
            )}
            <span
              className={`truncate font-bold ${
                toolGroup.status === "failed" ? "text-risk" : "text-ink"
              }`}
            >
              {toolSummary(toolGroup)}
            </span>
            {toolGroup.calls.length === 1 ? (
              <span
                className={`truncate ${
                  toolGroup.status === "failed" ? "text-risk" : "text-mutedText"
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
                toolGroup.status === "failed" ? "text-risk" : "text-mutedText"
              }`}
            />
          </span>
        </summary>
        {toolGroup.calls.length > 1 ? (
          <div className="grid gap-2 border-t border-line bg-soft p-2">
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
    <details className="group/tool-call overflow-hidden rounded border border-line bg-panel">
      <summary className="flex cursor-pointer list-none items-center gap-2 px-3 py-2 font-mono text-xs transition-colors hover:bg-soft">
        <span className="shrink-0 whitespace-nowrap font-bold text-ink" title={toolCall.name}>
          {toolCall.name}
        </span>
        <span className="min-w-0 flex-1 truncate text-mutedText" title={toolCall.command}>
          {toolCall.command}
        </span>
        <span className="ml-auto flex shrink-0 items-center gap-2">
          <span
            className={`rounded px-2 py-0.5 font-sans text-[10px] font-bold ${toolStatusBadgeClass(
              toolCall.status,
            )}`}
          >
            {toolStatusLabel(toolCall.status)}
          </span>
          <ChevronDown className="h-4 w-4 text-mutedText transition-transform group-open/tool-call:rotate-180" />
        </span>
      </summary>
      <ToolCallDetail toolCall={toolCall} />
    </details>
  );
}

function ToolCallDetail({ toolCall }: { toolCall: ToolCallView }) {
  return (
    <div className="grid gap-3 border-t border-line bg-ink p-3 font-mono text-xs text-panel">
      <div>
        <span className="text-[10px] font-bold uppercase text-mutedText">Input</span>
        <pre className="mt-0.5 whitespace-pre-wrap break-words text-panel/80">
          {toolCall.command}
        </pre>
      </div>
      <div>
        <span
          className={`text-[10px] font-bold uppercase ${
            toolCall.status === "failed" ? "text-risk" : "text-mutedText"
          }`}
        >
          {toolCall.status === "failed" ? "Stderr Output" : "Output"}
        </span>
        {toolCall.detail ? (
          <pre
            className={`mt-0.5 max-h-64 overflow-auto whitespace-pre-wrap break-words ${
              toolCall.status === "failed" ? "text-risk" : "text-brand"
            }`}
          >
            {toolCall.detail}
          </pre>
        ) : (
          <pre className="mt-0.5 text-mutedText">
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
    return "bg-risk text-panel";
  }
  if (status === "running") {
    return "bg-signal text-panel";
  }
  return "bg-gainSoft text-brand";
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
        detail: null,
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
        detail: toolResult.content,
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
  if (Array.isArray(content)) {
    const text = content
      .map((item) => {
        const block = asRecord(item);
        return block && asString(block.type) === "text" ? asString(block.text) : null;
      })
      .filter((value): value is string => Boolean(value));
    if (text.length > 0) {
      return text.join("\n");
    }
  }
  return formatDetail(content);
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
