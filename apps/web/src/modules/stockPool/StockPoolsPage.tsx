import {
  CheckSquare,
  Database,
  Pencil,
  Plus,
  RefreshCw,
  Search,
  Square,
  Trash2,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
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
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { EmptyState, LoadingState } from "@/shared/components";
import { StockKlineDialog } from "@/shared/components/stockPreview";
import {
  addPoolStock,
  createStockPool,
  deletePoolStock,
  deleteStockPool,
  getStockPool,
  importSnapshotInfoStocks,
  listPoolStocks,
  listStockPools,
  searchStockPoolCandidates,
  updatePoolStock,
  updateStockPool,
  type Project,
  type StockPool,
  type StockPoolCandidate,
  type StockPoolDetail,
  type StockPoolStock,
} from "@/shared/api";
import { notify } from "@/shared/notify";

type StockPoolsPageProps = {
  project: Project | null;
};

type PoolForm = {
  name: string;
  description: string;
};

type StockForm = {
  symbol: string;
  name: string;
  tags: string;
  note: string;
};

const emptyPoolForm: PoolForm = {
  name: "",
  description: "",
};

const emptyStockForm: StockForm = {
  symbol: "",
  name: "",
  tags: "",
  note: "",
};

const candidatePageSize = 20;
const stockPageSize = 100;

export function StockPoolsPage({ project }: StockPoolsPageProps) {
  const [pools, setPools] = useState<StockPool[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<StockPoolDetail | null>(null);
  const [stockRows, setStockRows] = useState<StockPoolStock[]>([]);
  const [stockTotal, setStockTotal] = useState(0);
  const [stockPage, setStockPage] = useState(1);
  const [query, setQuery] = useState("");
  const [stockQuery, setStockQuery] = useState("");
  const [poolForm, setPoolForm] = useState<PoolForm>(emptyPoolForm);
  const [stockForm, setStockForm] = useState<StockForm>(emptyStockForm);
  const [candidateQuery, setCandidateQuery] = useState("");
  const [candidates, setCandidates] = useState<StockPoolCandidate[]>([]);
  const [candidateTotal, setCandidateTotal] = useState(0);
  const [candidatePage, setCandidatePage] = useState(1);
  const [selectedCandidates, setSelectedCandidates] = useState<string[]>([]);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editingPool, setEditingPool] = useState<StockPool | null>(null);
  const [deletingPool, setDeletingPool] = useState<StockPool | null>(null);
  const [isAddStockOpen, setIsAddStockOpen] = useState(false);
  const [editingStock, setEditingStock] = useState<StockPoolStock | null>(null);
  const [deletingStock, setDeletingStock] = useState<StockPoolStock | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [isStocksLoading, setIsStocksLoading] = useState(false);
  const [isCandidateLoading, setIsCandidateLoading] = useState(false);
  const [pendingAction, setPendingAction] = useState<string | null>(null);

  const filteredPools = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    if (!keyword) {
      return pools;
    }
    return pools.filter((pool) =>
      [pool.name, pool.description, pool.id].join(" ").toLowerCase().includes(keyword),
    );
  }, [pools, query]);

  const stockPageCount = Math.max(1, Math.ceil(stockTotal / stockPageSize));

  const loadPools = useCallback(
    async (preferredId?: string | null) => {
      if (!project) {
        setPools([]);
        setSelectedId(null);
        setDetail(null);
        setStockRows([]);
        setStockTotal(0);
        return;
      }
      setIsLoading(true);
      try {
        const response = await listStockPools(project.id);
        setPools(response.items);
        setSelectedId((current) => {
          return (
            response.items.find((pool) => pool.id === preferredId)?.id ??
            response.items.find((pool) => pool.id === current)?.id ??
            response.items[0]?.id ??
            null
          );
        });
      } catch (caught) {
        notify(caught instanceof Error ? caught.message : "股票池加载失败", "error");
      } finally {
        setIsLoading(false);
      }
    },
    [project],
  );

  const loadDetail = useCallback(async (poolId: string) => {
    setIsDetailLoading(true);
    try {
      setDetail(await getStockPool(poolId, { includeStocks: false }));
    } catch (caught) {
      setDetail(null);
      notify(caught instanceof Error ? caught.message : "股票池详情加载失败", "error");
    } finally {
      setIsDetailLoading(false);
    }
  }, []);

  const loadStocks = useCallback(
    async (poolId = selectedId) => {
      if (!poolId) {
        setStockRows([]);
        setStockTotal(0);
        return;
      }
      setIsStocksLoading(true);
      try {
        const response = await listPoolStocks(poolId, {
          query: stockQuery,
          limit: stockPageSize,
          offset: (stockPage - 1) * stockPageSize,
        });
        const nextPageCount = Math.max(1, Math.ceil(response.total / stockPageSize));
        if (stockPage > nextPageCount) {
          setStockPage(nextPageCount);
          return;
        }
        setStockRows(response.items);
        setStockTotal(response.total);
      } catch (caught) {
        setStockRows([]);
        setStockTotal(0);
        notify(caught instanceof Error ? caught.message : "股票列表加载失败", "error");
      } finally {
        setIsStocksLoading(false);
      }
    },
    [selectedId, stockPage, stockQuery],
  );

  const loadCandidates = useCallback(async () => {
    if (!detail) {
      setCandidates([]);
      setCandidateTotal(0);
      return;
    }
    setIsCandidateLoading(true);
    try {
      const response = await searchStockPoolCandidates(
        detail.id,
        candidateQuery,
        candidatePageSize,
        (candidatePage - 1) * candidatePageSize,
      );
      setCandidates(response.items);
      setCandidateTotal(response.total);
      setSelectedCandidates((current) =>
        current.filter(
          (symbol) =>
            !response.items.some(
              (candidate) => candidate.symbol === symbol && candidate.in_pool,
            ),
        ),
      );
    } catch (caught) {
      setCandidates([]);
      setCandidateTotal(0);
      notify(caught instanceof Error ? caught.message : "候选股票加载失败", "error");
    } finally {
      setIsCandidateLoading(false);
    }
  }, [candidatePage, candidateQuery, detail]);

  useEffect(() => {
    void loadPools();
  }, [loadPools]);

  useEffect(() => {
    setStockQuery("");
    setStockPage(1);
    setStockRows([]);
    setStockTotal(0);
    if (selectedId) {
      void loadDetail(selectedId);
    } else {
      setDetail(null);
    }
  }, [loadDetail, selectedId]);

  useEffect(() => {
    void loadStocks();
  }, [loadStocks]);

  useEffect(() => {
    if (isAddStockOpen) {
      void loadCandidates();
    }
  }, [isAddStockOpen, loadCandidates]);

  const refreshCurrent = async (preferredId = selectedId) => {
    await loadPools(preferredId);
    if (preferredId) {
      await loadDetail(preferredId);
      await loadStocks(preferredId);
    }
  };

  const handleCreatePool = async () => {
    if (!project || !poolForm.name.trim()) {
      return;
    }
    setPendingAction("create-pool");
    try {
      const pool = await createStockPool({
        project_id: project.id,
        name: poolForm.name.trim(),
        description: poolForm.description.trim() || null,
      });
      setIsCreateOpen(false);
      setPoolForm(emptyPoolForm);
      await refreshCurrent(pool.id);
      notify("股票池已创建", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "创建股票池失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleUpdatePool = async () => {
    if (!editingPool || !poolForm.name.trim()) {
      return;
    }
    setPendingAction(`pool-${editingPool.id}`);
    try {
      await updateStockPool(editingPool.id, {
        name: poolForm.name.trim(),
        description: poolForm.description.trim() || null,
      });
      setEditingPool(null);
      setPoolForm(emptyPoolForm);
      await refreshCurrent(editingPool.id);
      notify("股票池已更新", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "更新股票池失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleDeletePool = async () => {
    if (!deletingPool) {
      return;
    }
    setPendingAction(`pool-${deletingPool.id}`);
    try {
      await deleteStockPool(deletingPool.id);
      setDeletingPool(null);
      await loadPools(null);
      notify("股票池已删除", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "删除股票池失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleAddStock = async (candidate: StockPoolCandidate) => {
    if (!detail || candidate.in_pool) {
      return;
    }
    setPendingAction(`candidate-${candidate.symbol}`);
    try {
      await addPoolStock(detail.id, {
        symbol: candidate.symbol,
        name: candidate.name ?? null,
        tags: [],
        note: null,
      });
      await refreshCurrent(detail.id);
      await loadCandidates();
      notify("股票已加入股票池", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "加入股票失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleAddSelectedStocks = async () => {
    if (!detail || selectedCandidates.length === 0) {
      return;
    }
    setPendingAction("selected-candidates");
    try {
      const result = await importSnapshotInfoStocks(detail.id, { symbols: selectedCandidates });
      setSelectedCandidates([]);
      await refreshCurrent(detail.id);
      await loadCandidates();
      notify(`已新增 ${result.created} 只，跳过 ${result.skipped} 只`, "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "加入股票失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleUpdateStock = async () => {
    if (!editingStock || !stockForm.symbol.trim()) {
      return;
    }
    setPendingAction(`stock-${editingStock.id}`);
    try {
      await updatePoolStock(editingStock.id, stockPayload(stockForm));
      setEditingStock(null);
      setStockForm(emptyStockForm);
      await refreshCurrent(detail?.id ?? editingStock.pool_id);
      notify("股票信息已更新", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "更新股票失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  const handleDeleteStock = async () => {
    if (!deletingStock) {
      return;
    }
    setPendingAction(`stock-${deletingStock.id}`);
    try {
      await deletePoolStock(deletingStock.id);
      setDeletingStock(null);
      await refreshCurrent(detail?.id ?? deletingStock.pool_id);
      notify("股票已移出股票池", "success");
    } catch (caught) {
      notify(caught instanceof Error ? caught.message : "移出股票失败", "error");
    } finally {
      setPendingAction(null);
    }
  };

  if (!project) {
    return <EmptyState title="暂无项目" description="先创建或选择一个项目后再管理股票池。" />;
  }

  return (
    <section className="mx-auto flex w-full max-w-none flex-col gap-4" aria-label="股票池">
      <header className="flex flex-wrap items-end justify-between gap-3 border-b border-line pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase text-mutedText">
            <Database className="h-4 w-4" />
            Stock Pools
          </div>
          <h1 className="mt-1 text-xl font-black text-ink">股票池</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" type="button" onClick={() => void refreshCurrent()}>
            <RefreshCw className="h-4 w-4" />
            刷新
          </Button>
          <Button
            type="button"
            onClick={() => {
              setPoolForm(emptyPoolForm);
              setIsCreateOpen(true);
            }}
          >
            <Plus className="h-4 w-4" />
            新建股票池
          </Button>
        </div>
      </header>

      <div className="grid min-h-0 gap-4 lg:grid-cols-[300px_minmax(0,1fr)] 2xl:grid-cols-[340px_minmax(0,1fr)]">
        <section className="min-w-0 rounded-lg border bg-panel">
          <div className="border-b border-line p-3">
            <div className="flex items-center gap-2">
              <Search className="h-4 w-4 text-mutedText" />
              <Input
                className="h-8 text-xs"
                placeholder="搜索股票池"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
          </div>
          <div className="max-h-[calc(100vh-220px)] overflow-y-auto p-2">
            {isLoading ? <LoadingState title="股票池加载中" rows={2} /> : null}
            {!isLoading && filteredPools.length === 0 ? (
              <div className="p-2">
                <EmptyState title="暂无股票池" description="暂无记录。" />
              </div>
            ) : null}
            <div className="grid gap-1">
              {filteredPools.map((pool) => {
                const isSelected = pool.id === selectedId;
                return (
                  <button
                    key={pool.id}
                    className={[
                      "rounded-md border px-3 py-2 text-left transition",
                      isSelected
                        ? "border-primary bg-primary/10"
                        : "border-transparent hover:border-line hover:bg-muted",
                    ].join(" ")}
                    type="button"
                    onClick={() => setSelectedId(pool.id)}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="truncate text-sm font-bold text-ink">{pool.name}</span>
                      <Badge variant="outline">{pool.stock_count}</Badge>
                    </div>
                    <div className="mt-1 truncate text-xs text-mutedText">
                      {pool.description || pool.id}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        <section className="min-w-0 overflow-hidden rounded-lg border bg-panel">
          {!detail && !isDetailLoading ? (
            <div className="p-4">
              <EmptyState title="未选择股票池" description="暂无详情。" />
            </div>
          ) : null}
          {isDetailLoading ? (
            <div className="p-4">
              <LoadingState title="股票池详情加载中" />
            </div>
          ) : null}
          {detail && !isDetailLoading ? (
            <>
              <div className="flex flex-wrap items-start justify-between gap-3 border-b border-line px-4 py-3">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="truncate text-base font-black text-ink">{detail.name}</h2>
                    <Badge variant="outline">{detail.stock_count} 只股票</Badge>
                  </div>
                  <p className="mt-1 max-w-2xl text-xs text-mutedText">
                    {detail.description || "无描述"}
                  </p>
                  <div className="mt-1 font-mono text-[11px] text-mutedText">
                    {detail.id} · {formatDateTime(detail.updated_at)}
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    type="button"
                    onClick={() => {
                      setPoolForm({
                        name: detail.name,
                        description: detail.description ?? "",
                      });
                      setEditingPool(detail);
                    }}
                  >
                    <Pencil className="h-4 w-4" />
                    编辑
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    type="button"
                    onClick={() => setDeletingPool(detail)}
                  >
                    <Trash2 className="h-4 w-4" />
                    删除
                  </Button>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-4 py-3">
                <div className="flex items-center gap-2">
                  <Input
                    className="h-8 w-64 text-xs"
                    placeholder="搜索代码 / 名称 / 标签 / 备注"
                    value={stockQuery}
                    onChange={(event) => {
                      setStockQuery(event.target.value);
                      setStockPage(1);
                    }}
                  />
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    type="button"
                    onClick={() => {
                      setCandidateQuery("");
                      setCandidates([]);
                      setCandidateTotal(0);
                      setCandidatePage(1);
                      setSelectedCandidates([]);
                      setIsAddStockOpen(true);
                    }}
                  >
                    <Plus className="h-4 w-4" />
                    添加股票
                  </Button>
                </div>
              </div>

              <Table className="min-w-[680px]">
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-28">代码</TableHead>
                    <TableHead className="w-32">名称</TableHead>
                    <TableHead className="w-40">标签</TableHead>
                    <TableHead>备注</TableHead>
                    <TableHead className="w-36">更新时间</TableHead>
                    <TableHead className="w-24 text-right">操作</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {isStocksLoading ? (
                    <TableRow>
                      <TableCell colSpan={6} className="h-32 text-center text-sm text-mutedText">
                        股票加载中
                      </TableCell>
                    </TableRow>
                  ) : null}
                  {!isStocksLoading && stockRows.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="h-32 text-center">
                        <div className="text-sm font-semibold text-ink">暂无股票</div>
                        <div className="mt-1 text-xs text-mutedText">暂无记录。</div>
                      </TableCell>
                    </TableRow>
                  ) : null}
                  {!isStocksLoading
                    ? stockRows.map((stock) => (
                        <TableRow key={stock.id}>
                          <TableCell className="font-mono text-xs font-bold text-ink">
                            <StockKlineDialog symbol={stock.symbol}>
                              <span className="text-brandBlue underline-offset-2 hover:underline">
                                {stock.symbol}
                              </span>
                            </StockKlineDialog>
                          </TableCell>
                          <TableCell className="text-sm text-graphite">
                            {stock.name ? (
                              <StockKlineDialog symbol={stock.symbol}>
                                <span className="underline-offset-2 hover:text-brandBlue hover:underline">
                                  {stock.name}
                                </span>
                              </StockKlineDialog>
                            ) : (
                              "-"
                            )}
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {stock.tags.length ? (
                                stock.tags.map((tag) => (
                                  <Badge key={tag} variant="outline">
                                    {tag}
                                  </Badge>
                                ))
                              ) : (
                                <span className="text-xs text-mutedText">-</span>
                              )}
                            </div>
                          </TableCell>
                          <TableCell className="max-w-64 truncate text-sm text-mutedText">
                            {stock.note || "-"}
                          </TableCell>
                          <TableCell className="whitespace-nowrap text-xs text-mutedText">
                            {formatDateTime(stock.updated_at)}
                          </TableCell>
                          <TableCell className="w-24 text-right">
                            <div className="flex shrink-0 justify-end gap-2">
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    aria-label="编辑"
                                    className="h-8 w-8"
                                    size="iconSm"
                                    variant="outline"
                                    type="button"
                                    onClick={() => {
                                      setStockForm(stockFormFromRecord(stock));
                                      setEditingStock(stock);
                                    }}
                                  >
                                    <Pencil className="h-4 w-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>编辑</TooltipContent>
                              </Tooltip>
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    aria-label="移出"
                                    className="h-8 w-8"
                                    size="iconSm"
                                    variant="outline"
                                    type="button"
                                    onClick={() => setDeletingStock(stock)}
                                  >
                                    <Trash2 className="h-4 w-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>移出</TooltipContent>
                              </Tooltip>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    : null}
                </TableBody>
              </Table>
              <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-3">
                <div className="text-xs text-mutedText">
                  {stockTotal
                    ? `${(stockPage - 1) * stockPageSize + 1}-${Math.min(
                        stockPage * stockPageSize,
                        stockTotal,
                      )} / ${stockTotal}`
                    : "0 / 0"}
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    type="button"
                    disabled={stockPage <= 1 || isStocksLoading}
                    onClick={() => setStockPage((current) => Math.max(1, current - 1))}
                  >
                    上一页
                  </Button>
                  <Badge variant="outline">
                    {stockPage}/{stockPageCount}
                  </Badge>
                  <Button
                    size="sm"
                    variant="outline"
                    type="button"
                    disabled={stockPage >= stockPageCount || isStocksLoading}
                    onClick={() =>
                      setStockPage((current) => Math.min(stockPageCount, current + 1))
                    }
                  >
                    下一页
                  </Button>
                </div>
              </div>
            </>
          ) : null}
        </section>
      </div>

      <PoolDialog
        form={poolForm}
        isOpen={isCreateOpen}
        isSaving={pendingAction === "create-pool"}
        title="新建股票池"
        onChange={setPoolForm}
        onClose={() => setIsCreateOpen(false)}
        onSubmit={() => void handleCreatePool()}
      />
      <PoolDialog
        form={poolForm}
        isOpen={Boolean(editingPool)}
        isSaving={editingPool ? pendingAction === `pool-${editingPool.id}` : false}
        title="编辑股票池"
        onChange={setPoolForm}
        onClose={() => setEditingPool(null)}
        onSubmit={() => void handleUpdatePool()}
      />
      <CandidateStockDialog
        isOpen={isAddStockOpen}
        candidates={candidates}
        isLoading={isCandidateLoading}
        page={candidatePage}
        pageSize={candidatePageSize}
        pendingAction={pendingAction}
        query={candidateQuery}
        selectedSymbols={selectedCandidates}
        total={candidateTotal}
        onChangeQuery={(value) => {
          setCandidateQuery(value);
          setCandidatePage(1);
        }}
        onClose={() => setIsAddStockOpen(false)}
        onPageChange={setCandidatePage}
        onRefresh={() => void loadCandidates()}
        onSelectMany={() => void handleAddSelectedStocks()}
        onSelect={(candidate) => void handleAddStock(candidate)}
        onSelectedSymbolsChange={setSelectedCandidates}
      />
      <EditStockDialog
        form={stockForm}
        isOpen={Boolean(editingStock)}
        isSaving={editingStock ? pendingAction === `stock-${editingStock.id}` : false}
        title="编辑股票"
        onChange={setStockForm}
        onClose={() => setEditingStock(null)}
        onSubmit={() => void handleUpdateStock()}
      />
      <AlertDialog
        open={Boolean(deletingPool)}
        onOpenChange={(open) => (open ? undefined : setDeletingPool(null))}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>删除股票池“{deletingPool?.name ?? ""}”？</AlertDialogTitle>
            <AlertDialogDescription>
              删除后会同时移除该股票池中的全部股票记录。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={() => void handleDeletePool()}>删除</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog
        open={Boolean(deletingStock)}
        onOpenChange={(open) => (open ? undefined : setDeletingStock(null))}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>移出 {deletingStock?.symbol ?? ""}？</AlertDialogTitle>
            <AlertDialogDescription>该股票的标签和备注也会从当前股票池移除。</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={() => void handleDeleteStock()}>移出</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  );
}

type PoolDialogProps = {
  form: PoolForm;
  isOpen: boolean;
  isSaving: boolean;
  title: string;
  onChange: (form: PoolForm) => void;
  onClose: () => void;
  onSubmit: () => void;
};

function PoolDialog({
  form,
  isOpen,
  isSaving,
  title,
  onChange,
  onClose,
  onSubmit,
}: PoolDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <div className="grid gap-3">
          <Field label="名称" required>
            <Input
              value={form.name}
              onChange={(event) => onChange({ ...form, name: event.target.value })}
            />
          </Field>
          <Field label="描述">
            <Textarea
              value={form.description}
              onChange={(event) => onChange({ ...form, description: event.target.value })}
            />
          </Field>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={isSaving || !form.name.trim()} onClick={onSubmit}>
            保存
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type CandidateStockDialogProps = {
  isOpen: boolean;
  candidates: StockPoolCandidate[];
  isLoading: boolean;
  page: number;
  pageSize: number;
  pendingAction: string | null;
  query: string;
  selectedSymbols: string[];
  total: number;
  onChangeQuery: (query: string) => void;
  onClose: () => void;
  onPageChange: (page: number) => void;
  onRefresh: () => void;
  onSelectMany: () => void;
  onSelect: (candidate: StockPoolCandidate) => void;
  onSelectedSymbolsChange: (symbols: string[]) => void;
};

function CandidateStockDialog({
  isOpen,
  candidates,
  isLoading,
  page,
  pageSize,
  pendingAction,
  query,
  selectedSymbols,
  total,
  onChangeQuery,
  onClose,
  onPageChange,
  onRefresh,
  onSelectMany,
  onSelect,
  onSelectedSymbolsChange,
}: CandidateStockDialogProps) {
  const selectableSymbols = candidates
    .filter((candidate) => !candidate.in_pool)
    .map((candidate) => candidate.symbol);
  const selectedSet = new Set(selectedSymbols);
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  const isPageSelected =
    selectableSymbols.length > 0 && selectableSymbols.every((symbol) => selectedSet.has(symbol));

  const toggleSymbol = (symbol: string) => {
    if (selectedSet.has(symbol)) {
      onSelectedSymbolsChange(selectedSymbols.filter((item) => item !== symbol));
      return;
    }
    onSelectedSymbolsChange([...selectedSymbols, symbol]);
  };

  const selectCurrentPage = () => {
    if (isPageSelected) {
      onSelectedSymbolsChange(
        selectedSymbols.filter((symbol) => !selectableSymbols.includes(symbol)),
      );
      return;
    }
    onSelectedSymbolsChange([...new Set([...selectedSymbols, ...selectableSymbols])]);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>添加股票</DialogTitle>
        </DialogHeader>
        <div className="flex flex-wrap items-center gap-2">
          <Input
            className="h-8 flex-1 text-xs"
            value={query}
            onChange={(event) => onChangeQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                onRefresh();
              }
            }}
            placeholder="搜索代码或名称"
          />
          <Button size="sm" variant="outline" type="button" onClick={onRefresh}>
            <RefreshCw className="h-4 w-4" />
            搜索
          </Button>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={selectableSymbols.length === 0}
              onClick={selectCurrentPage}
            >
              {isPageSelected ? (
                <CheckSquare className="h-4 w-4" />
              ) : (
                <Square className="h-4 w-4" />
              )}
              {isPageSelected ? "取消本页" : "全选本页"}
            </Button>
            <Badge variant="outline">已选 {selectedSymbols.length}</Badge>
          </div>
          <div className="text-xs text-mutedText">
            {total ? `${(page - 1) * pageSize + 1}-${Math.min(page * pageSize, total)} / ${total}` : "0 / 0"}
          </div>
        </div>
        <div className="max-h-96 overflow-y-auto rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">选择</TableHead>
                <TableHead>代码</TableHead>
                <TableHead>名称</TableHead>
                <TableHead>状态</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={5} className="h-24 text-center text-sm text-mutedText">
                    候选股票加载中
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading && candidates.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="h-24 text-center text-sm text-mutedText">
                    暂无候选股票
                  </TableCell>
                </TableRow>
              ) : null}
              {!isLoading
                ? candidates.map((candidate) => {
                    const isSelected = selectedSet.has(candidate.symbol);
                    return (
                      <TableRow
                        key={candidate.symbol}
                        className={candidate.in_pool ? "bg-muted/60 opacity-60" : undefined}
                      >
                        <TableCell>
                          <Button
                            aria-label={isSelected ? "取消选择" : "选择"}
                            className="h-7 w-7"
                            size="iconSm"
                            variant="ghost"
                            type="button"
                            disabled={candidate.in_pool}
                            onClick={() => toggleSymbol(candidate.symbol)}
                          >
                            {isSelected ? (
                              <CheckSquare className="h-4 w-4" />
                            ) : (
                              <Square className="h-4 w-4" />
                            )}
                          </Button>
                        </TableCell>
                        <TableCell className="font-mono text-xs font-bold text-ink">
                          {candidate.symbol}
                        </TableCell>
                        <TableCell>{candidate.name || "-"}</TableCell>
                        <TableCell>
                          <Badge variant={candidate.in_pool ? "default" : "outline"}>
                            {candidate.in_pool ? "已在池中" : "可加入"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            size="sm"
                            type="button"
                            disabled={
                              candidate.in_pool ||
                              pendingAction === `candidate-${candidate.symbol}`
                            }
                            onClick={() => onSelect(candidate)}
                          >
                            <Plus className="h-4 w-4" />
                            加入
                          </Button>
                        </TableCell>
                      </TableRow>
                    );
                  })
                : null}
            </TableBody>
          </Table>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={page <= 1}
              onClick={() => onPageChange(page - 1)}
            >
              上一页
            </Button>
            <span className="text-xs text-mutedText">
              {page}/{pageCount}
            </span>
            <Button
              size="sm"
              variant="outline"
              type="button"
              disabled={page >= pageCount}
              onClick={() => onPageChange(page + 1)}
            >
              下一页
            </Button>
          </div>
          <Button
            size="sm"
            type="button"
            disabled={
              selectedSymbols.length === 0 || pendingAction === "selected-candidates"
            }
            onClick={onSelectMany}
          >
            <Plus className="h-4 w-4" />
            加入已选
          </Button>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            关闭
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

type EditStockDialogProps = {
  form: StockForm;
  isOpen: boolean;
  isSaving: boolean;
  title: string;
  onChange: (form: StockForm) => void;
  onClose: () => void;
  onSubmit: () => void;
};

function EditStockDialog({
  form,
  isOpen,
  isSaving,
  title,
  onChange,
  onClose,
  onSubmit,
}: EditStockDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => (open ? undefined : onClose())}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="股票代码" required>
            <Input
              className="font-mono"
              value={form.symbol}
              readOnly
            />
          </Field>
          <Field label="股票名称">
            <Input
              value={form.name}
              readOnly
            />
          </Field>
          <Field label="标签">
            <Input
              value={form.tags}
              onChange={(event) => onChange({ ...form, tags: event.target.value })}
              placeholder="白酒, 消费, 核心"
            />
          </Field>
          <Field label="备注">
            <Input
              value={form.note}
              onChange={(event) => onChange({ ...form, note: event.target.value })}
            />
          </Field>
        </div>
        <DialogFooter>
          <Button variant="outline" type="button" onClick={onClose}>
            取消
          </Button>
          <Button type="button" disabled={isSaving || !form.symbol.trim()} onClick={onSubmit}>
            保存
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: ReactNode;
}) {
  return (
    <div className="grid gap-1.5">
      <Label className="text-xs font-bold text-mutedText">
        {label}
        {required ? <span className="ml-1 text-destructive">*</span> : null}
      </Label>
      {children}
    </div>
  );
}

function stockPayload(form: StockForm) {
  return {
    symbol: form.symbol.trim(),
    name: form.name.trim() || null,
    tags: splitTags(form.tags),
    note: form.note.trim() || null,
  };
}

function stockFormFromRecord(stock: StockPoolStock): StockForm {
  return {
    symbol: stock.symbol,
    name: stock.name ?? "",
    tags: stock.tags.join(", "),
    note: stock.note ?? "",
  };
}

function splitTags(value: string): string[] {
  const normalized = value.replace("，", ",").replace("；", ",").replace(";", ",");
  const tags: string[] = [];
  for (const part of normalized.split(/[\s,]+/)) {
    const tag = part.trim();
    if (tag && !tags.includes(tag)) {
      tags.push(tag);
    }
  }
  return tags;
}

function formatDateTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
}
