import {
  ChevronLeft,
  CircleAlert,
  File,
  FileCode2,
  FileText,
  Folder,
  Home,
  Loader2,
  PanelRightClose,
  PanelRightOpen,
  RefreshCw,
  Search,
  X,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import type { PointerEvent as ReactPointerEvent, ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";

import {
  API_BASE_URL,
  getProjectFileContent,
  listProjectFiles,
  type Project,
  type ProjectDirectoryResponse,
  type ProjectFileContentResponse,
  type ProjectFileEntry,
} from "../../shared/api";

type ProjectFilesPanelProps = {
  project: Project | null;
};

type DirectoryState =
  | { status: "idle" }
  | { status: "loading"; previous?: ProjectDirectoryResponse }
  | { status: "error"; message: string; previous?: ProjectDirectoryResponse }
  | { status: "ready"; directory: ProjectDirectoryResponse };

type FileContentState =
  | { status: "idle" }
  | { status: "loading"; file: ProjectFileEntry }
  | { status: "error"; file: ProjectFileEntry; message: string }
  | { status: "ready"; file: ProjectFileEntry; content: ProjectFileContentResponse };

type FileViewMode = "preview" | "text";

const minPanelWidth = 320;
const maxPanelWidth = 1120;
const defaultPanelWidth = 420;
const expandedPanelWidth = 920;

export function ProjectFilesPanel({ project }: ProjectFilesPanelProps) {
  const [panelWidth, setPanelWidth] = useState(() => storedPanelWidth());
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [currentPath, setCurrentPath] = useState("");
  const [query, setQuery] = useState("");
  const [selectedFile, setSelectedFile] = useState<ProjectFileEntry | null>(null);
  const [state, setState] = useState<DirectoryState>({ status: "idle" });
  const [fileState, setFileState] = useState<FileContentState>({ status: "idle" });
  const [isResizing, setIsResizing] = useState(false);

  const loadDirectory = useCallback(
    async (path: string) => {
      if (!project) {
        setState({ status: "idle" });
        return;
      }
      setState((previous) => ({
        status: "loading",
        previous: directoryFromState(previous),
      }));
      try {
        const directory = await listProjectFiles(project.id, path);
        setState({ status: "ready", directory });
        setCurrentPath(directory.current_path);
      } catch (caught) {
        setState((previous) => ({
          status: "error",
          message: caught instanceof Error ? caught.message : "项目文件加载失败",
          previous: directoryFromState(previous),
        }));
      }
    },
    [project],
  );

  useEffect(() => {
    setCurrentPath("");
    setQuery("");
    setSelectedFile(null);
    setFileState({ status: "idle" });
    void loadDirectory("");
  }, [loadDirectory, project?.id]);

  const directory = directoryFromState(state);
  const visibleItems = useMemo(() => {
    if (!directory) {
      return [];
    }
    const normalizedQuery = query.trim().toLowerCase();
    if (!normalizedQuery) {
      return directory.items;
    }
    return directory.items.filter((item) =>
      item.name.toLowerCase().includes(normalizedQuery),
    );
  }, [directory, query]);

  const startResize = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.currentTarget.setPointerCapture(event.pointerId);
      const startX = event.clientX;
      const startWidth = panelWidth;
      const previousCursor = document.body.style.cursor;
      const previousUserSelect = document.body.style.userSelect;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      setIsResizing(true);

      const handleMove = (moveEvent: PointerEvent) => {
        const nextWidth = clampPanelWidth(startWidth + startX - moveEvent.clientX);
        setPanelWidth(nextWidth);
        window.localStorage.setItem("chatq.files.width", String(nextWidth));
      };
      const handleUp = () => {
        document.body.style.cursor = previousCursor;
        document.body.style.userSelect = previousUserSelect;
        setIsResizing(false);
        window.removeEventListener("pointermove", handleMove);
        window.removeEventListener("pointerup", handleUp);
      };

      window.addEventListener("pointermove", handleMove);
      window.addEventListener("pointerup", handleUp);
    },
    [panelWidth],
  );

  const openDirectory = (item: ProjectFileEntry) => {
    setSelectedFile(null);
    setFileState({ status: "idle" });
    void loadDirectory(item.relative_path);
  };

  const expandPanelForFile = () => {
    const nextWidth = Math.min(maxPanelWidth, Math.max(panelWidth, expandedPanelWidth));
    setPanelWidth(nextWidth);
    window.localStorage.setItem("chatq.files.width", String(nextWidth));
  };

  const openFile = async (item: ProjectFileEntry) => {
    if (!project) {
      return;
    }
    setSelectedFile(item);
    expandPanelForFile();
    setFileState({ status: "loading", file: item });
    try {
      const content = await getProjectFileContent(project.id, item.relative_path);
      setFileState({ status: "ready", file: item, content });
    } catch (caught) {
      setFileState({
        status: "error",
        file: item,
        message: caught instanceof Error ? caught.message : "文件内容加载失败",
      });
    }
  };

  const closeFile = () => {
    setSelectedFile(null);
    setFileState({ status: "idle" });
  };

  const refresh = () => {
    void loadDirectory(currentPath);
    if (fileState.status !== "idle" && project) {
      void openFile(fileState.file);
    }
  };

  if (isCollapsed) {
    return (
      <Button
        className="fixed right-3 top-3 z-40 hidden xl:inline-flex"
        size="icon"
        variant="outline"
        type="button"
        title="显示项目文件"
        aria-label="显示项目文件"
        onClick={() => setIsCollapsed(false)}
      >
        <PanelRightOpen className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <>
      <Button
        className="fixed right-3 top-3 z-40 hidden xl:inline-flex"
        size="icon"
        variant="outline"
        type="button"
        title="隐藏项目文件"
        aria-label="隐藏项目文件"
        onClick={() => setIsCollapsed(true)}
      >
        <PanelRightClose className="h-4 w-4" />
      </Button>
      <aside
        className={`glass-panel relative hidden h-full shrink-0 flex-col border-l xl:flex ${
          isResizing ? "border-signal" : "border-line"
        }`}
        style={{ width: panelWidth }}
        aria-label="项目文件"
      >
        <div
          className="group absolute -left-1 top-0 z-30 flex h-full w-3 cursor-col-resize touch-none items-stretch justify-center"
          role="separator"
          aria-orientation="vertical"
          aria-label="调整项目文件区域宽度"
          aria-valuemin={minPanelWidth}
          aria-valuemax={maxPanelWidth}
          aria-valuenow={panelWidth}
          onPointerDown={startResize}
        >
          <span
            className={`h-full w-0.5 rounded-full transition-colors ${
              isResizing ? "bg-signal" : "bg-transparent group-hover:bg-signal"
            }`}
            aria-hidden="true"
          />
        </div>
        <div className="border-b border-line px-4 pb-3 pt-14">
          <PanelHeader project={project} isLoading={state.status === "loading"} onRefresh={refresh} />
          <div className="mt-3 flex items-center gap-2">
            <Button
              className="h-8 w-8"
              size="iconSm"
              variant="outline"
              type="button"
              title="项目根目录"
              aria-label="项目根目录"
              disabled={!project || currentPath === ""}
              onClick={() => {
                setSelectedFile(null);
                void loadDirectory("");
              }}
            >
              <Home className="h-3.5 w-3.5" />
            </Button>
            <Button
              className="h-8 w-8"
              size="iconSm"
              variant="outline"
              type="button"
              title="返回上级"
              aria-label="返回上级"
              disabled={!directory?.parent_path && currentPath === ""}
              onClick={() => {
                setSelectedFile(null);
                void loadDirectory(directory?.parent_path ?? "");
              }}
            >
              <ChevronLeft className="h-3.5 w-3.5" />
            </Button>
            <div className="relative min-w-0 flex-1">
              <Search className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mutedText" />
              <Input
                className="h-8 pl-8 text-xs"
                disabled={!project}
                placeholder="搜索文件..."
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
          </div>
          <PathTrail path={currentPath} />
        </div>

        <div className="min-h-0 flex flex-1">
          <div
            className={`min-h-0 shrink-0 ${
              fileState.status === "idle"
                ? "w-full"
                : "w-[320px] border-r border-line"
            }`}
          >
            <ScrollArea className="h-full">
              <div className="px-3 py-3">
                {!project ? (
                  <EmptyPanel title="未选择项目" description="请先创建或打开一个项目" />
                ) : state.status === "loading" && !directory ? (
                  <LoadingPanel />
                ) : state.status === "error" && !directory ? (
                  <EmptyPanel title="加载失败" description={state.message} />
                ) : directory ? (
                  <FileList
                    items={visibleItems}
                    selectedFile={selectedFile}
                    onOpenDirectory={openDirectory}
                    onOpenFile={(item) => void openFile(item)}
                  />
                ) : null}
              </div>
            </ScrollArea>
          </div>
          {fileState.status !== "idle" ? (
            <FileViewer state={fileState} onClose={closeFile} />
          ) : null}
        </div>

        <FileSummary
          directory={directory}
          error={state.status === "error" ? state.message : null}
          selectedFile={selectedFile}
          visibleCount={visibleItems.length}
        />
      </aside>
    </>
  );
}

function PanelHeader({
  project,
  isLoading,
  onRefresh,
}: {
  project: Project | null;
  isLoading: boolean;
  onRefresh: () => void;
}) {
  return (
    <div className="flex items-start justify-between gap-3">
      <div className="min-w-0">
        <div className="font-mono text-[10px] font-bold uppercase text-mutedText">
          Project Files
        </div>
        <div className="mt-1 truncate text-sm font-semibold text-ink">
          {project?.name ?? "项目文件"}
        </div>
        <div className="mt-1 truncate font-mono text-[10px] text-mutedText">
          {project?.local_path ?? "未绑定目录"}
        </div>
      </div>
      <Button
        className="h-8 w-8"
        size="iconSm"
        variant="outline"
        type="button"
        title="刷新"
        aria-label="刷新"
        disabled={!project || isLoading}
        onClick={onRefresh}
      >
        {isLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="h-3.5 w-3.5" />}
      </Button>
    </div>
  );
}

function PathTrail({ path }: { path: string }) {
  const parts = path ? path.split("/") : [];
  return (
    <div className="mt-3 flex min-h-6 items-center gap-1 overflow-hidden font-mono text-[10px] text-mutedText">
      <span className="shrink-0 text-ink">/</span>
      {parts.length === 0 ? (
        <span className="truncate">project root</span>
      ) : (
        parts.map((part, index) => (
          <span className="min-w-0 truncate" key={`${part}-${index}`}>
            {index > 0 ? " / " : ""}
            {part}
          </span>
        ))
      )}
    </div>
  );
}

function FileList({
  items,
  selectedFile,
  onOpenDirectory,
  onOpenFile,
}: {
  items: ProjectFileEntry[];
  selectedFile: ProjectFileEntry | null;
  onOpenDirectory: (item: ProjectFileEntry) => void;
  onOpenFile: (item: ProjectFileEntry) => void;
}) {
  if (items.length === 0) {
    return <EmptyPanel title="暂无文件" description="当前目录没有匹配项" />;
  }

  return (
    <div className="grid gap-1">
      {items.map((item) => {
        const isDirectory = item.type === "directory";
        const isSelected = selectedFile?.relative_path === item.relative_path;
        return (
          <button
            className={`grid h-11 w-full grid-cols-[24px_minmax(0,1fr)_auto] items-center gap-2 rounded-md border px-2 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-signal/20 ${
              isSelected
                ? "border-strong bg-panel"
                : "border-transparent hover:bg-soft/80"
            }`}
            key={item.relative_path}
            type="button"
            onClick={() => {
              if (isDirectory) {
                onOpenDirectory(item);
              } else {
                onOpenFile(item);
              }
            }}
          >
            <span className="grid h-6 w-6 place-items-center">
              <FileIcon item={item} />
            </span>
            <span className="min-w-0">
              <span className="block truncate text-xs font-semibold text-ink">
                {item.name}
              </span>
              <span className="mt-0.5 block truncate font-mono text-[10px] text-mutedText">
                {formatModifiedAt(item.modified_at)}
              </span>
            </span>
            <span className="max-w-16 truncate font-mono text-[10px] text-mutedText">
              {isDirectory ? "DIR" : formatSize(item.size)}
            </span>
          </button>
        );
      })}
    </div>
  );
}

function FileViewer({
  state,
  onClose,
}: {
  state: Exclude<FileContentState, { status: "idle" }>;
  onClose: () => void;
}) {
  const file = state.file;
  const [viewMode, setViewMode] = useState<FileViewMode>(() => defaultViewModeFor(file));
  const canPreview = isPreviewable(file);

  useEffect(() => {
    setViewMode(defaultViewModeFor(file));
  }, [file.relative_path]);

  return (
    <section className="flex min-w-0 flex-1 flex-col bg-panel/60">
      <div className="flex h-12 shrink-0 items-center justify-between gap-3 border-b border-line px-3">
        <div className="flex min-w-0 items-center gap-2">
          <FileIcon item={file} />
          <div className="min-w-0">
            <div className="truncate text-xs font-semibold text-ink">{file.name}</div>
            <div className="truncate font-mono text-[10px] text-mutedText">
              {file.relative_path}
            </div>
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-1.5">
          {canPreview ? (
            <Button
              size="sm"
              variant="outline"
              type="button"
              onClick={() => setViewMode(viewMode === "preview" ? "text" : "preview")}
            >
              {viewMode === "preview" ? "查看文本" : "预览"}
            </Button>
          ) : null}
          <Button
            className="h-8 w-8"
            size="iconSm"
            variant="ghost"
            type="button"
            title="关闭文件"
            aria-label="关闭文件"
            onClick={onClose}
          >
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
      {state.status === "loading" ? (
        <div className="flex min-h-0 flex-1 items-center justify-center text-sm text-mutedText">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          加载文件内容
        </div>
      ) : state.status === "error" ? (
        <div className="m-3 flex items-start gap-2 rounded-md border border-risk/30 bg-risk/5 p-3 text-sm text-risk">
          <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />
          <span>{state.message}</span>
        </div>
      ) : (
        <FileContent content={state.content} mode={viewMode} />
      )}
    </section>
  );
}

function FileContent({
  content,
  mode,
}: {
  content: ProjectFileContentResponse;
  mode: FileViewMode;
}) {
  const extension = content.extension ?? "";
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      {content.truncated ? (
        <div className="border-b border-line bg-accent/10 px-3 py-2 text-xs text-ink">
          文件较大，仅显示前 {formatSize(content.content.length)} 文本内容
        </div>
      ) : null}
      {mode === "preview" && extension === "md" ? (
        <MarkdownPreview content={content.content} />
      ) : mode === "preview" && extension === "html" ? (
        <HtmlPreview content={content} />
      ) : mode === "preview" && extension === "csv" ? (
        <CsvPreview content={content.content} />
      ) : (
        <SourceView content={content.content} extension={extension} />
      )}
    </div>
  );
}

function MarkdownPreview({ content }: { content: string }) {
  return (
    <ScrollArea className="min-h-0 flex-1">
      <div className="markdown-content p-4 text-sm leading-6">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </ScrollArea>
  );
}

function HtmlPreview({ content }: { content: ProjectFileContentResponse }) {
  return (
    <iframe
      className="min-h-0 flex-1 bg-white"
      sandbox="allow-scripts allow-modals"
      src={projectHtmlPreviewUrl(content)}
      title={content.relative_path}
    />
  );
}

function CsvPreview({ content }: { content: string }) {
  const rows = useMemo(() => parseCsv(content), [content]);
  const [header, ...bodyRows] = rows;
  const visibleRows = bodyRows.slice(0, 300);

  if (!header) {
    return <EmptyPanel title="空 CSV" description="这个文件没有可预览的数据" />;
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      {bodyRows.length > visibleRows.length ? (
        <div className="border-b border-line bg-accent/10 px-3 py-2 text-xs text-ink">
          仅预览前 {visibleRows.length} 行
        </div>
      ) : null}
      <ScrollArea className="min-h-0 flex-1">
        <div className="p-3">
          <table className="min-w-full border-collapse text-xs">
            <thead>
              <tr>
                {header.map((cell, index) => (
                  <th
                    className="sticky top-0 border border-line bg-soft px-2 py-1.5 text-left font-semibold text-ink"
                    key={`${cell}-${index}`}
                  >
                    {cell || `列 ${index + 1}`}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visibleRows.map((row, rowIndex) => (
                <tr className="odd:bg-panel even:bg-soft/40" key={rowIndex}>
                  {header.map((_, cellIndex) => (
                    <td
                      className="max-w-64 border border-line px-2 py-1.5 align-top text-graphite"
                      key={cellIndex}
                    >
                      <span className="block truncate">{row[cellIndex] ?? ""}</span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ScrollArea>
    </div>
  );
}

function SourceView({
  content,
  extension,
}: {
  content: string;
  extension: string;
}) {
  const lines = content.split("\n");
  return (
    <ScrollArea className="min-h-0 flex-1">
      <pre className="min-w-max bg-[#171a16] p-3 font-mono text-[12px] leading-5 text-[#dbe7df]">
        {lines.map((line, index) => (
          <div className="grid grid-cols-[44px_minmax(0,1fr)]" key={index}>
            <span className="select-none pr-3 text-right text-[#7f8a83]">
              {index + 1}
            </span>
            <code className="whitespace-pre">
              {extension === "py" ? highlightPythonLine(line) : line || " "}
            </code>
          </div>
        ))}
      </pre>
    </ScrollArea>
  );
}

function FileIcon({ item }: { item: ProjectFileEntry }) {
  if (item.type === "directory") {
    return <Folder className="h-4 w-4 text-accent" />;
  }
  if (["js", "jsx", "ts", "tsx", "py", "html", "css", "json", "yaml", "yml"].includes(item.extension ?? "")) {
    return <FileCode2 className="h-4 w-4 text-brandBlue" />;
  }
  if (["md", "txt", "csv", "log"].includes(item.extension ?? "")) {
    return <FileText className="h-4 w-4 text-brand" />;
  }
  return <File className="h-4 w-4 text-mutedText" />;
}

function FileSummary({
  directory,
  error,
  selectedFile,
  visibleCount,
}: {
  directory?: ProjectDirectoryResponse;
  error: string | null;
  selectedFile: ProjectFileEntry | null;
  visibleCount: number;
}) {
  const folderCount = directory?.items.filter((item) => item.type === "directory").length ?? 0;
  const fileCount = directory?.items.filter((item) => item.type === "file").length ?? 0;
  return (
    <div className="border-t border-line px-4 py-3 text-xs text-mutedText">
      {error ? <div className="mb-2 text-risk">{error}</div> : null}
      {selectedFile ? (
        <div className="mb-2 rounded-md border border-line bg-panel p-2">
          <div className="truncate font-semibold text-ink">{selectedFile.name}</div>
          <div className="mt-1 break-all font-mono text-[10px]">{selectedFile.relative_path}</div>
          <div className="mt-1 font-mono text-[10px]">
            {formatSize(selectedFile.size)} · {formatModifiedAt(selectedFile.modified_at)}
          </div>
        </div>
      ) : null}
      <div className="flex items-center justify-between font-mono text-[10px]">
        <span>
          {folderCount} folders · {fileCount} files
        </span>
        <span>{visibleCount} shown</span>
      </div>
    </div>
  );
}

function LoadingPanel() {
  return (
    <div className="flex items-center gap-2 rounded-md border border-line bg-panel p-4 text-sm text-mutedText">
      <Loader2 className="h-4 w-4 animate-spin" />
      加载项目文件
    </div>
  );
}

function EmptyPanel({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-md border border-dashed border-line bg-panel/70 p-4 text-sm">
      <div className="font-semibold text-ink">{title}</div>
      <div className="mt-1 text-xs text-mutedText">{description}</div>
    </div>
  );
}

function formatSize(size: number | null) {
  if (size == null) {
    return "--";
  }
  if (size < 1024) {
    return `${size} B`;
  }
  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`;
  }
  return `${(size / 1024 / 1024).toFixed(1)} MB`;
}

function formatModifiedAt(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "--";
  }
  return date.toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function directoryFromState(state: DirectoryState): ProjectDirectoryResponse | undefined {
  if (state.status === "ready") {
    return state.directory;
  }
  if (state.status === "loading" || state.status === "error") {
    return state.previous;
  }
  return undefined;
}

function defaultViewModeFor(file: ProjectFileEntry): FileViewMode {
  return isPreviewable(file) ? "preview" : "text";
}

function isPreviewable(file: ProjectFileEntry) {
  return ["md", "html", "csv"].includes(file.extension ?? "");
}

function parseCsv(content: string) {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let isQuoted = false;

  for (let index = 0; index < content.length; index += 1) {
    const char = content[index];
    const nextChar = content[index + 1];

    if (char === '"') {
      if (isQuoted && nextChar === '"') {
        cell += '"';
        index += 1;
      } else {
        isQuoted = !isQuoted;
      }
      continue;
    }

    if (char === "," && !isQuoted) {
      row.push(cell);
      cell = "";
      continue;
    }

    if ((char === "\n" || char === "\r") && !isQuoted) {
      if (char === "\r" && nextChar === "\n") {
        index += 1;
      }
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
      continue;
    }

    cell += char;
  }

  if (cell || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }

  return rows.filter((cells) => cells.some((value) => value.length > 0));
}

const pythonTokenPattern =
  /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(#.*)|\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b|(\b\d+(?:\.\d+)?\b)/g;

function highlightPythonLine(line: string): ReactNode[] {
  const parts: ReactNode[] = [];
  let cursor = 0;

  for (const match of line.matchAll(pythonTokenPattern)) {
    const index = match.index ?? 0;
    if (index > cursor) {
      parts.push(line.slice(cursor, index));
    }
    const [token, stringToken, commentToken, keywordToken, numberToken] = match;
    const className = stringToken
      ? "text-[#dfb16d]"
      : commentToken
        ? "text-[#7f8a83]"
        : keywordToken
          ? "text-[#7eb6e6]"
          : numberToken
            ? "text-[#9fd18b]"
            : "";
    parts.push(
      <span className={className} key={`${index}-${token}`}>
        {token}
      </span>,
    );
    cursor = index + token.length;
  }

  if (cursor < line.length) {
    parts.push(line.slice(cursor));
  }
  return parts.length > 0 ? parts : [" "];
}

function projectHtmlPreviewUrl(content: ProjectFileContentResponse) {
  const projectId = encodeURIComponent(content.project_id);
  const path = content.relative_path.split("/").map(encodeURIComponent).join("/");
  return `${API_BASE_URL}/api/projects/${projectId}/visualization-html/${path}`;
}

function storedPanelWidth() {
  if (typeof window === "undefined") {
    return defaultPanelWidth;
  }
  const stored = Number(window.localStorage.getItem("chatq.files.width"));
  return clampPanelWidth(Number.isFinite(stored) && stored > 0 ? stored : defaultPanelWidth);
}

function clampPanelWidth(value: number) {
  return Math.min(maxPanelWidth, Math.max(minPanelWidth, value));
}
