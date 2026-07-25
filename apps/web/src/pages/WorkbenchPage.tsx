import { useCallback, useEffect, useMemo, useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { ArtifactList } from "../modules/result";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import { listArtifacts, type CodeArtifact } from "../shared/api";

export function WorkbenchPage() {
  const [artifacts, setArtifacts] = useState<CodeArtifact[]>([]);
  const [selectedArtifactId, setSelectedArtifactId] = useState<string | null>(null);
  const [isLoadingArtifacts, setIsLoadingArtifacts] = useState(true);
  const [artifactError, setArtifactError] = useState<string | null>(null);

  const loadArtifacts = useCallback(() => {
    setIsLoadingArtifacts(true);
    setArtifactError(null);
    listArtifacts()
      .then((items) => {
        setArtifacts(items);
        setSelectedArtifactId((current) => current ?? items[0]?.artifact_id ?? null);
      })
      .catch((error: unknown) => {
        const message = error instanceof Error ? error.message : "Artifact request failed";
        setArtifactError(message);
      })
      .finally(() => {
        setIsLoadingArtifacts(false);
      });
  }, []);

  useEffect(() => {
    loadArtifacts();
  }, [loadArtifacts]);

  const selectedArtifact = useMemo(
    () => artifacts.find((artifact) => artifact.artifact_id === selectedArtifactId) ?? null,
    [artifacts, selectedArtifactId],
  );

  return (
    <WorkspaceLayout
      history={<HistoryPanel />}
      header={<WorkspaceHeader />}
      conversation={
        <ConversationShell
          artifactList={
            <ArtifactList
              artifacts={artifacts}
              selectedArtifactId={selectedArtifactId}
              isLoading={isLoadingArtifacts}
              error={artifactError}
              onRefresh={loadArtifacts}
              onSelectArtifact={setSelectedArtifactId}
            />
          }
        />
      }
      composer={<Composer />}
      insight={<InsightPanel artifact={selectedArtifact} />}
    />
  );
}
