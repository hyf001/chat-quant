import { BacktestResultPanel } from "../result";
import type { BacktestDetail } from "../../shared/types/backtests";

type ConversationShellProps = {
  backtestDetail: BacktestDetail;
  backtestError: string | null;
  isRunningBacktest: boolean;
  onRunDemoBacktest: () => void;
};

export function ConversationShell({
  backtestDetail,
  backtestError,
  isRunningBacktest,
  onRunDemoBacktest,
}: ConversationShellProps) {
  return (
    <section className="min-h-0 flex-1 overflow-auto px-5 py-6" aria-label="对话线程">
      <div className="mx-auto grid w-full max-w-4xl gap-4">
        <div className="rounded-lg border border-line bg-panel p-4">
          <div className="text-xs font-semibold text-muted">用户</div>
          <p className="mt-2 text-sm leading-6">
            用沪深300做一个 20/60 日均线突破策略回测，并给出收益、回撤和交易胜率。
          </p>
        </div>
        <div className="rounded-lg border border-line bg-panel p-4">
          <div className="text-xs font-semibold text-muted">Agent</div>
          <p className="mt-2 text-sm leading-6">
            已固化回测参数，策略版本为 {backtestDetail.run.strategy_version_id}，
            结果已保存为 {backtestDetail.result?.id ?? backtestDetail.run.id}。
          </p>
        </div>
        <BacktestResultPanel
          detail={backtestDetail}
          error={backtestError}
          isRunning={isRunningBacktest}
          onRunDemo={onRunDemoBacktest}
        />
      </div>
    </section>
  );
}
