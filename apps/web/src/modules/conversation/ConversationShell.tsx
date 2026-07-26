import { AlertCircle, CheckCircle2, ChevronDown, Loader2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { AssetLink, ChatSession, SDKStreamEnvelope, SdkMessage } from "../../shared/api";
import type { Components } from "react-markdown";

type ConversationShellProps = {
  session: ChatSession | null;
  messages: SdkMessage[];
  envelopes: SDKStreamEnvelope[];
  assets: AssetLink[];
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
};

type UnknownRecord = Record<string, unknown>;

type ToolCallView = {
  id: string;
  name: string;
  command: string;
  status: "running" | "completed" | "failed";
  startedAt: string;
  completedAt: string | null;
  detail: string | null;
  sequence: number;
};

type ToolGroupView = {
  id: string;
  calls: ToolCallView[];
  status: "running" | "completed" | "failed";
  startedAt: string;
  completedAt: string | null;
  sequence: number;
};

type ThinkingProcessView = {
  id: string;
  text: string;
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
    <section className="px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-5">
        {error ? (
          <div className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <AlertCircle className="mt-0.5 shrink-0" size={17} />
            <span className="min-w-0 break-words">{error}</span>
          </div>
        ) : null}

        {isLoading ? (
          <div className="rounded-lg border border-line bg-panel p-4 text-sm text-muted">加载中</div>
        ) : null}

        {!isLoading && !session ? (
          <div className="rounded-lg border border-line bg-panel p-5">
            <div className="text-sm font-semibold">开始新的量化会话</div>
            <p className="mt-2 text-sm leading-6 text-muted">
              输入股票问题、选股条件或策略想法后，系统会创建历史入口并保存会话上下文。
            </p>
          </div>
        ) : null}

        {session && timelineItems.length === 0 && !isStreaming ? (
          <div className="rounded-lg border border-dashed border-line bg-panel p-5 text-sm leading-6 text-muted">
            当前会话还没有消息。
          </div>
        ) : null}

        {timelineItems.map((item) => {
          if (item.type === "message") {
            return (
              <div className="contents" key={item.id}>
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
          if (item.type === "thinking") {
            return (
              <ThinkingEntry
                isActive={isStreaming && item.id === lastTimelineItemId(timelineItems)}
                key={item.id}
                thinking={item.thinking}
              />
            );
          }
          return (
            <ToolGroupEntry
              isActive={isStreaming && item.id === lastTimelineItemId(timelineItems)}
              key={item.id}
              toolGroup={item.toolGroup}
            />
          );
        })}

        {isStreaming && session && thinkingProcesses.length === 0 ? (
          <ThinkingEntry isActive thinking={null} />
        ) : null}

        {activityLabel ? <ActivityHint label={activityLabel} /> : null}

        {assets.length > 0 ? (
          <div className="rounded-lg border border-line bg-panel p-4">
            <div className="text-sm font-semibold">会话资产</div>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {assets.slice(0, 4).map((asset) => (
                <div className="rounded-lg border border-line bg-soft p-3" key={asset.id}>
                  <div className="truncate text-sm font-medium">{asset.asset_id}</div>
                  <div className="mt-1 text-xs text-muted">
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

function ActivityHint({ label }: { label: string }) {
  return (
    <div className="px-1 text-sm text-muted">
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
    <div className="border-t border-line/70 pt-4 text-sm text-muted">
      <span className="inline-flex items-center gap-1">
        {isStreaming ? "处理中" : "已处理"} {elapsedLabel}
        <ChevronDown size={14} />
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
  return (
    <article
      className={`flex ${isUser ? "justify-end" : "justify-start border-t border-line/70 pt-5"}`}
    >
      <div
        className={
          isUser
            ? "max-w-[78%] rounded-lg bg-soft px-4 py-3 text-sm leading-6 text-ink shadow-sm"
            : "w-full min-w-0 text-ink"
        }
      >
        {isAssistant ? (
          <div className="text-sm leading-7">
            <MarkdownContent text={blockText(message)} />
            {isStreaming && isLatestAssistant ? <span className="streaming-caret" /> : null}
          </div>
        ) : (
          <p className="whitespace-pre-wrap break-words text-sm leading-6">
            {blockText(message)}
          </p>
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
    <div className="border-t border-line/70 pt-5">
      <details className="group" open={isActive}>
        <summary className="flex cursor-pointer list-none items-center justify-between gap-3 text-sm font-medium text-ink">
          <span className="inline-flex min-w-0 items-center gap-2">
            {isActive ? (
              <span className="thinking-rings text-brand" aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            ) : (
              <Loader2 className="text-muted" size={16} />
            )}
            思考过程
          </span>
          <span className="flex shrink-0 items-center gap-2 text-xs text-muted">
            {thinking ? formatElapsed(thinking.startedAt, thinking.completedAt) : "进行中"}
            <ChevronDown className="transition group-open:rotate-180" size={16} />
          </span>
        </summary>
        <p className="mt-3 whitespace-pre-wrap break-words border-l border-line pl-3 text-sm leading-6 text-muted">
          {thinking?.text || "正在组织思路"}
          {isActive ? <span className="streaming-caret" /> : null}
        </p>
      </details>
    </div>
  );
}

function ToolGroupEntry({
  toolGroup,
  isActive,
}: {
  toolGroup: ToolGroupView;
  isActive: boolean;
}) {
  return (
    <div className="border-t border-line/70 pt-5" aria-label="工具调用">
      <details className="group" open={isActive}>
        <summary className="flex cursor-pointer list-none items-center justify-between gap-3 text-sm text-muted">
          <span className="flex min-w-0 items-center gap-2">
            {toolGroup.status === "running" ? (
              <Loader2 className="shrink-0 animate-spin" size={14} />
            ) : toolGroup.status === "failed" ? (
              <AlertCircle className="shrink-0 text-red-500" size={16} />
            ) : (
              <CheckCircle2 className="shrink-0" size={15} />
            )}
            <span className="truncate font-medium">{toolSummary(toolGroup)}</span>
          </span>
          <span className="flex shrink-0 items-center gap-2 text-xs text-muted">
            {formatElapsed(toolGroup.startedAt, toolGroup.completedAt)}
            <ChevronDown className="transition group-open:rotate-180" size={16} />
          </span>
        </summary>
        <div className="mt-3 grid gap-3">
          {toolGroup.calls.map((toolCall) => (
            <div className="border-l border-line pl-3" key={toolCall.id}>
              <div className="mb-2 px-1 text-xs text-muted">{toolCall.name}</div>
              <div className="rounded-lg border border-line/70 bg-soft/70 p-3 font-mono text-xs leading-6 text-ink">
                <div className="whitespace-pre-wrap break-words text-muted">$ {toolCall.command}</div>
                {toolCall.detail ? (
                  <pre className="mt-3 max-h-64 overflow-auto whitespace-pre-wrap break-words border-t border-line/70 pt-3 text-muted">
                    {toolCall.detail}
                  </pre>
                ) : null}
                <div className="mt-3 flex justify-end text-xs text-muted">
                  {toolCall.status === "failed" ? "失败" : toolCall.status === "running" ? "运行中" : "成功"}
                </div>
              </div>
            </div>
          ))}
        </div>
      </details>
    </div>
  );
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

  return [...messageItems, ...thinkingItems, ...toolItems].sort((left, right) => {
    if (left.sequence > 0 && right.sequence > 0 && left.sequence !== right.sequence) {
      return left.sequence - right.sequence;
    }
    const timeDelta = timestampMs(left.timestamp) - timestampMs(right.timestamp);
    if (timeDelta !== 0) {
      return timeDelta;
    }
    return left.sequence - right.sequence;
  });
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

function buildToolCalls(envelopes: SDKStreamEnvelope[]): ToolCallView[] {
  const toolCalls = new Map<string, ToolCallView>();
  const sortedEnvelopes = [...envelopes].sort((left, right) => left.sequence - right.sequence);

  sortedEnvelopes.forEach((envelope) => {
    const event = unwrapEvent(envelope.sdk_event);
    extractToolUses(event).forEach((toolUse) => {
      toolCalls.set(toolUse.id, {
        id: toolUse.id,
        name: toolUse.name,
        command: toolUse.command,
        status: "running",
        startedAt: envelope.received_at,
        completedAt: null,
        detail: formatDetail(toolUse.input),
        sequence: envelope.sequence,
      });
    });

    extractToolResults(event).forEach((toolResult) => {
      const existing = toolCalls.get(toolResult.id);
      toolCalls.set(toolResult.id, {
        id: toolResult.id,
        name: existing?.name ?? "工具",
        command: existing?.command ?? "工具调用",
        status: toolResult.isError ? "failed" : "completed",
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

  return [
    {
      id: sortedToolCalls.map((toolCall) => toolCall.id).join("_"),
      calls: sortedToolCalls,
      status: toolGroupStatus(sortedToolCalls),
      startedAt: sortedToolCalls[0].startedAt,
      completedAt: latestCompletedAt(sortedToolCalls),
      sequence: sortedToolCalls[0].sequence,
    },
  ];
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

function toolSummary(toolGroup: ToolGroupView): string {
  if (toolGroup.calls.length > 1) {
    return "运行了多个命令";
  }
  const command = toolGroup.calls[0]?.command ?? "";
  if (command.startsWith("cat ") || command.startsWith("sed ") || command.startsWith("rg ")) {
    return "读取文件";
  }
  if (command.startsWith("git ")) {
    return `已运行 ${truncateText(command, 42)}`;
  }
  return "运行了命令";
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
