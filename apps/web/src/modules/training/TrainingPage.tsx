import { Plus } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  listTrainingSessions,
  type Project,
  type TrainingSessionSummary,
  type TrainingStatus,
} from "@/shared/api";
import { EmptyState, LoadingState } from "@/shared/components";

import { TrainingChart } from "./TrainingChart";
import { TrainingCreateDialog, type TrainingCreateForm } from "./TrainingCreateDialog";
import { TrainingIntradayDialog } from "./TrainingIntradayDialog";
import { TrainingOrderPanel } from "./TrainingOrderPanel";
import { TrainingReportDialog } from "./TrainingReportDialog";
import { TrainingStatsBar, formatDuration, formatMoney } from "./TrainingStatsBar";
import { ratioSize, type TrainingPositionRatio } from "./types";
import { useTrainingSession } from "./useTrainingSession";

const LIST_PAGE_SIZE = 20;
const LIST_STATUS_ALL = "all";
type ListStatusFilter = TrainingStatus | typeof LIST_STATUS_ALL;

type TrainingPageProps = {
  project: Project | null;
};

export function TrainingPage({ project }: TrainingPageProps) {
  const { state, start, reveal, finish, reset, resume, openReport, clearError } =
    useTrainingSession(project?.id ?? null);
  const [buyRatio, setBuyRatio] = useState<TrainingPositionRatio>("half");
  const [sellRatio, setSellRatio] = useState<TrainingPositionRatio>("half");
  const [initialCash, setInitialCash] = useState("100000");
  const [commission, setCommission] = useState("0.0005");
  const [slippage, setSlippage] = useState("0.001");
  const [excludeSt, setExcludeSt] = useState(true);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isReportOpen, setIsReportOpen] = useState(false);
  // 双击的那一根日线（分时弹窗）；null 表示没在看分时
  const [intradaySeq, setIntradaySeq] = useState<number | null>(null);
  const [sessions, setSessions] = useState<TrainingSessionSummary[]>([]);
  const [listTotal, setListTotal] = useState(0);
  const [listStatus, setListStatus] = useState<ListStatusFilter>(LIST_STATUS_ALL);
  const [listKeyword, setListKeyword] = useState("");
  const [keywordDraft, setKeywordDraft] = useState("");
  const [listPage, setListPage] = useState(1);
  const [isListLoading, setIsListLoading] = useState(false);
  const [listError, setListError] = useState<string | null>(null);
  const [listVersion, setListVersion] = useState(0);

  const session = state.session;
  const isActive = state.phase === "active" && session !== null;
  const inSession = session !== null;

  // 弹窗的开局默认值：上一局的输入留着，但只有内容真的变了才换引用（否则会打断输入）
  const createDefaults = useMemo<TrainingCreateForm>(
    () => ({
      initialCash,
      commission,
      slippage,
      excludeSt,
    }),
    [commission, excludeSt, initialCash, slippage],
  );

  useEffect(() => {
    if (state.phase === "finished" && state.report) {
      setIsReportOpen(true);
    }
  }, [state.phase, state.report]);

  // 关键字防抖：停止输入 300ms 后再去查，并把页码拉回第一页
  useEffect(() => {
    const trimmed = keywordDraft.trim();
    const timer = window.setTimeout(() => {
      setListKeyword(trimmed);
      setListPage(1);
    }, 300);
    return () => window.clearTimeout(timer);
  }, [keywordDraft]);

  // 回到列表（开局前 / 收局后）都重新拉一次，保证刚结束的那局状态是最新的
  useEffect(() => {
    if (!project || inSession) {
      return undefined;
    }
    let cancelled = false;
    setIsListLoading(true);
    setListError(null);
    listTrainingSessions(project.id, {
      limit: LIST_PAGE_SIZE,
      offset: (listPage - 1) * LIST_PAGE_SIZE,
      status: listStatus === LIST_STATUS_ALL ? undefined : listStatus,
      keyword: listKeyword || undefined,
    })
      .then((payload) => {
        if (cancelled) {
          return;
        }
        setSessions(payload.items);
        setListTotal(payload.total);
        // 筛选后总量可能变小，把越界的页码收回到最后一页
        const lastPage = Math.max(1, Math.ceil(payload.total / LIST_PAGE_SIZE));
        if (listPage > lastPage) {
          setListPage(lastPage);
        }
      })
      .catch((caught: unknown) => {
        if (!cancelled) {
          setListError(caught instanceof Error ? caught.message : "训练列表加载失败");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsListLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [inSession, listKeyword, listPage, listStatus, listVersion, project]);

  // 键盘：空格下一根、B 买入、S 卖出
  useEffect(() => {
    if (!isActive) {
      return undefined;
    }
    const handler = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      if (target && ["INPUT", "TEXTAREA"].includes(target.tagName)) {
        return;
      }
      // 有弹窗时把键盘让给弹窗（二次确认的空格 / 回车不能被当成下单）
      if (document.querySelector('[role="dialog"], [role="alertdialog"]')) {
        return;
      }
      const key = event.key.toLowerCase();
      if (event.code === "Space") {
        event.preventDefault();
        void reveal("hold");
      } else if (key === "b") {
        void reveal("buy", ratioSize(buyRatio));
      } else if (key === "s") {
        void reveal("sell", ratioSize(sellRatio));
      } else if (key === "escape") {
        setIsReportOpen(false);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [buyRatio, isActive, reveal, sellRatio]);

  const handleAction = (action: "buy" | "sell" | "hold") => {
    if (action === "hold") {
      void reveal("hold");
      return;
    }
    void reveal(action, ratioSize(action === "buy" ? buyRatio : sellRatio));
  };

  const openCreate = () => {
    clearError();
    setIsCreateOpen(true);
  };

  const handleCreate = async (form: TrainingCreateForm) => {
    const created = await start({
      initial_cash: form.initialCash,
      commission: form.commission,
      slippage: form.slippage,
      exclude_st: form.excludeSt,
    });
    if (created) {
      setInitialCash(form.initialCash);
      setCommission(form.commission);
      setSlippage(form.slippage);
      setExcludeSt(form.excludeSt);
      setIsCreateOpen(false);
    }
  };

  const handleBackToList = () => {
    setIsReportOpen(false);
    setIntradaySeq(null);
    reset();
    setListVersion((version) => version + 1);
  };

  if (!project) {
    return (
      <EmptyState
        title="先创建或选择项目"
        description="训练会话挂在项目下；项目建立后即可开局。"
      />
    );
  }

  return (
    <div className="h-full overflow-y-auto p-5 lg:p-7">
      <header className="mb-4 flex flex-wrap items-center gap-3">
        <h1 className="text-lg font-semibold text-ink">双盲 K 线训练</h1>
        {inSession ? (
          <div className="ml-auto flex items-center gap-2">
            <Badge variant={isActive ? "secondary" : "outline"}>
              {session.instrument_alias} · {isActive ? "进行中" : "已结束"}
            </Badge>
            <Button variant="outline" size="sm" onClick={handleBackToList}>
              返回列表
            </Button>
          </div>
        ) : null}
      </header>

      {inSession ? (
        <div className="space-y-3">
          <TrainingStatsBar session={session} elapsedSeconds={state.elapsedSeconds} />
          <TrainingChart
            bars={state.bars}
            markers={state.markers}
            height={460}
            ariaLabel={`${session.instrument_alias} 训练 K 线`}
            onBarDoubleClick={setIntradaySeq}
          />
          <p className="text-xs text-mutedText">
            双击 K 线上任意一根已揭示的日线，可以看那一根的当日分时。
          </p>
          {isActive ? (
            <TrainingOrderPanel
              cash={session.account.cash}
              positionSize={session.account.position_size}
              positionValue={session.account.position_value}
              positionPrice={session.account.position_price}
              positionPct={session.account.position_pct}
              buyRatio={buyRatio}
              sellRatio={sellRatio}
              disabled={state.busy}
              remaining={session.remaining}
              onBuyRatioChange={setBuyRatio}
              onSellRatioChange={setSellRatio}
              onAction={handleAction}
              onFinish={() => void finish()}
            />
          ) : (
            <div className="flex gap-2">
              <Button onClick={() => void openReport(session.id)}>查看复盘报告</Button>
              <Button variant="outline" onClick={handleBackToList}>
                返回列表
              </Button>
            </div>
          )}
        </div>
      ) : (
        <TrainingList
          sessions={sessions}
          total={listTotal}
          page={listPage}
          pageSize={LIST_PAGE_SIZE}
          status={listStatus}
          keyword={keywordDraft}
          isLoading={isListLoading || (!isCreateOpen && state.phase === "loading")}
          error={listError}
          onStatusChange={(next) => {
            setListStatus(next);
            setListPage(1);
          }}
          onKeywordChange={setKeywordDraft}
          onPageChange={setListPage}
          onResume={(sessionId) => void resume(sessionId)}
          onOpenReport={(sessionId) => void openReport(sessionId)}
          onCreate={openCreate}
        />
      )}

      <TrainingCreateDialog
        open={isCreateOpen}
        busy={state.busy}
        error={state.error}
        defaultForm={createDefaults}
        onClose={() => setIsCreateOpen(false)}
        onSubmit={(form) => void handleCreate(form)}
      />

      <TrainingReportDialog
        open={isReportOpen}
        report={state.report}
        onClose={() => setIsReportOpen(false)}
        onRestart={() => {
          setIsReportOpen(false);
          handleBackToList();
          openCreate();
        }}
      />

      <TrainingIntradayDialog
        open={intradaySeq !== null}
        sessionId={session?.id ?? ""}
        seq={intradaySeq}
        onClose={() => setIntradaySeq(null)}
      />
    </div>
  );
}

type TrainingListProps = {
  sessions: TrainingSessionSummary[];
  total: number;
  page: number;
  pageSize: number;
  status: ListStatusFilter;
  keyword: string;
  isLoading: boolean;
  error: string | null;
  onStatusChange: (status: ListStatusFilter) => void;
  onKeywordChange: (keyword: string) => void;
  onPageChange: (page: number) => void;
  onResume: (sessionId: string) => void;
  onOpenReport: (sessionId: string) => void;
  onCreate: () => void;
};

function TrainingList({
  sessions,
  total,
  page,
  pageSize,
  status,
  keyword,
  isLoading,
  error,
  onStatusChange,
  onKeywordChange,
  onPageChange,
  onResume,
  onOpenReport,
  onCreate,
}: TrainingListProps) {
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  const isFiltered = status !== LIST_STATUS_ALL || keyword.trim() !== "";

  return (
    <div className="w-full space-y-3">
      <section className="overflow-hidden rounded-lg border border-line bg-panel">
        <header className="flex flex-wrap items-center gap-3 border-b border-line px-4 py-3">
          <h2 className="text-sm font-semibold text-ink">训练记录</h2>
          <div className="ml-auto flex flex-wrap items-center gap-2">
            <Input
              className="h-9 w-52 text-xs"
              placeholder="按会话 ID 搜索"
              value={keyword}
              onChange={(event) => onKeywordChange(event.target.value)}
            />
            <Select
              value={status}
              onValueChange={(value) => onStatusChange(value as ListStatusFilter)}
            >
              <SelectTrigger className="h-9 w-28 text-xs">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={LIST_STATUS_ALL}>全部状态</SelectItem>
                <SelectItem value="active">进行中</SelectItem>
                <SelectItem value="finished">已结束</SelectItem>
              </SelectContent>
            </Select>
            <Button size="sm" onClick={onCreate}>
              <Plus className="h-4 w-4" />
              新建训练
            </Button>
          </div>
        </header>

        {error ? (
          <div className="p-4">
            <EmptyState title="训练列表加载失败" description={error} />
          </div>
        ) : isLoading && sessions.length === 0 ? (
          <div className="p-4">
            <LoadingState title="正在加载训练列表" />
          </div>
        ) : sessions.length === 0 ? (
          <div className="p-4">
            <EmptyState
              title={isFiltered ? "没有符合条件的训练" : "还没有训练记录"}
              description={isFiltered ? "换个状态或会话 ID 再试试。" : undefined}
            />
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>会话 ID</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>进度</TableHead>
                <TableHead>初始资金</TableHead>
                <TableHead>用时</TableHead>
                <TableHead>开始时间</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sessions.map((item) => {
                const active = item.status === "active";
                return (
                  <TableRow key={item.id}>
                    <TableCell className="font-mono text-xs text-mutedText">{item.id}</TableCell>
                    <TableCell>
                      <Badge variant={active ? "secondary" : "outline"}>
                        {active ? "进行中" : "已结束"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-ink">
                      {progressLabel(item)}
                    </TableCell>
                    <TableCell className="text-sm text-ink">
                      {formatMoney(item.initial_cash)}
                    </TableCell>
                    <TableCell className="text-sm text-ink">
                      {formatDuration(item.elapsed_seconds)}
                    </TableCell>
                    <TableCell className="text-sm text-mutedText">
                      {formatDateTime(item.started_at)}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        variant={active ? "default" : "outline"}
                        onClick={() => (active ? onResume(item.id) : onOpenReport(item.id))}
                      >
                        {active ? "继续训练" : "查看复盘"}
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        )}

        <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-line px-4 py-2">
          <p className="text-xs text-mutedText">
            共 {total} 条 · 第 {page} / {pageCount} 页
          </p>
          <Pagination className="mx-0 w-auto">
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  disabled={page <= 1 || isLoading}
                  onClick={() => onPageChange(Math.max(1, page - 1))}
                />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext
                  disabled={page >= pageCount || isLoading}
                  onClick={() => onPageChange(page + 1)}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </footer>
      </section>
    </div>
  );
}

function progressLabel(item: TrainingSessionSummary): string {
  if (item.training_bars === null) {
    return `已推进 ${item.cursor_index} 根`;
  }
  return `${item.cursor_index} / ${item.training_bars}`;
}

function formatDateTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
}
