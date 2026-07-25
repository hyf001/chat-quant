import { useEffect, useState } from "react";

import { Composer } from "../modules/composer";
import { ConversationShell } from "../modules/conversation";
import { HistoryPanel } from "../modules/history";
import { InsightPanel } from "../modules/insight";
import { RuntimeResultPanel } from "../modules/result";
import { WorkspaceHeader, WorkspaceLayout } from "../modules/workspace";
import {
  executePythonArtifact,
  getRuntimeHealth,
  type ExecutionResult,
  type RuntimeHealth,
} from "../shared/api";

const sampleCode = `
import csv
import json
import os
from pathlib import Path

payload = json.loads(Path(os.environ["CHATQ_STDIN_JSON"]).read_text(encoding="utf-8"))
output_dir = Path(os.environ["CHATQ_OUTPUT_DIR"])
tables_dir = output_dir / "tables"
tables_dir.mkdir(parents=True, exist_ok=True)

rows = [
    {"symbol": symbol, "score": 88 - index * 3, "signal": "watch"}
    for index, symbol in enumerate(payload["symbols"])
]

with (tables_dir / "screening.csv").open("w", newline="", encoding="utf-8") as file_obj:
    writer = csv.DictWriter(file_obj, fieldnames=["symbol", "score", "signal"])
    writer.writeheader()
    writer.writerows(rows)

result = {
    "status": "succeeded",
    "summary": "sample screening completed",
    "rows": rows,
    "warnings": [],
}
(output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
print(f"screened {len(rows)} symbols")
`.trim();

export function WorkbenchPage() {
  const [health, setHealth] = useState<RuntimeHealth | null>(null);
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getRuntimeHealth()
      .then(setHealth)
      .catch((runtimeError: unknown) => {
        setError(runtimeError instanceof Error ? runtimeError.message : "Runtime health failed");
      });
  }, []);

  const handleRunSample = async () => {
    setIsRunning(true);
    setError(null);
    try {
      const executionResult = await executePythonArtifact({
        chat_session_id: "conv_demo_m4",
        code_artifact_id: "code_demo_inline",
        entrypoint: "analysis.py",
        stdin_json: {
          symbols: ["沪深300", "中证500", "创业板指"],
          start_date: "2026-04-24",
          end_date: "2026-07-24",
        },
        timeout_seconds: 30,
        expected_outputs: ["result.json", "tables/screening.csv"],
        purpose: "stock_screening",
        code_files: [{ path: "analysis.py", content: sampleCode }],
      });
      setResult(executionResult);
    } catch (runtimeError: unknown) {
      setError(runtimeError instanceof Error ? runtimeError.message : "Runtime execute failed");
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <WorkspaceLayout
      history={<HistoryPanel />}
      header={<WorkspaceHeader health={health} />}
      conversation={<ConversationShell />}
      result={
        <RuntimeResultPanel
          health={health}
          result={result}
          isRunning={isRunning}
          error={error}
          onRunSample={handleRunSample}
        />
      }
      composer={<Composer />}
      insight={<InsightPanel health={health} result={result} />}
    />
  );
}
