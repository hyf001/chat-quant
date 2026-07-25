import { useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { demoBacktestDetail, demoBacktestPayload } from "../modules/result";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import { createBacktestRun, runBacktest } from "../shared/api";
import type { BacktestDetail } from "../shared/types/backtests";

export function WorkbenchPage() {
  const [backtestDetail, setBacktestDetail] = useState<BacktestDetail>(demoBacktestDetail);
  const [isRunningBacktest, setIsRunningBacktest] = useState(false);
  const [backtestError, setBacktestError] = useState<string | null>(null);

  async function handleRunDemoBacktest() {
    setIsRunningBacktest(true);
    setBacktestError(null);

    try {
      const run = await createBacktestRun(demoBacktestPayload);
      const detail = await runBacktest(run.id);
      setBacktestDetail(detail);
    } catch (error) {
      setBacktestError(error instanceof Error ? error.message : "回测请求失败");
    } finally {
      setIsRunningBacktest(false);
    }
  }

  return (
    <WorkspaceLayout
      history={<HistoryPanel />}
      header={<WorkspaceHeader status={backtestDetail.run.status} />}
      conversation={
        <ConversationShell
          backtestDetail={backtestDetail}
          backtestError={backtestError}
          isRunningBacktest={isRunningBacktest}
          onRunDemoBacktest={handleRunDemoBacktest}
        />
      }
      composer={<Composer />}
      insight={<InsightPanel detail={backtestDetail} />}
    />
  );
}
