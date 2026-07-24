import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";

export function WorkbenchPage() {
  return (
    <WorkspaceLayout
      history={<HistoryPanel />}
      header={<WorkspaceHeader />}
      conversation={<ConversationShell />}
      composer={<Composer />}
      insight={<InsightPanel />}
    />
  );
}
