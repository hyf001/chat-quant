import { apiGet } from "./client";

export type ArtifactType =
  | "query_script"
  | "analysis_script"
  | "strategy_script"
  | "backtest_script"
  | "json_result"
  | "chart_file";

export type ArtifactStatus = "created" | "validated" | "invalid" | "archived";

export type ArtifactFileRole = ArtifactType | "log_file" | "data_file";

type MetadataValue = string | number | boolean | null | string[];

export type ArtifactFile = {
  file_id: string;
  artifact_id: string;
  relative_path: string;
  file_role: ArtifactFileRole;
  storage_uri: string;
  mime_type: string;
  size_bytes: number;
  checksum: string;
  is_entrypoint: boolean;
  render_metadata: Record<string, MetadataValue>;
  download_url: string;
  preview_url: string | null;
  created_at: string;
};

export type CodeArtifact = {
  artifact_id: string;
  user_id: string;
  project_id: string;
  chat_session_id: string;
  artifact_type: ArtifactType;
  title: string;
  version: number;
  entrypoint: string | null;
  checksum: string;
  root_path: string;
  status: ArtifactStatus;
  files: ArtifactFile[];
  description: string | null;
  source_sdk_session_id: string | null;
  source_sdk_message_uuid: string | null;
  source_sdk_tool_use_id: string | null;
  main_file_id: string | null;
  metadata: Record<string, MetadataValue>;
  created_at: string;
  updated_at: string;
};

type ArtifactListResponse = {
  items: CodeArtifact[];
};

export function listArtifacts(chatSessionId?: string): Promise<CodeArtifact[]> {
  const query = chatSessionId ? `?chat_session_id=${encodeURIComponent(chatSessionId)}` : "";
  return apiGet<ArtifactListResponse>(`/api/artifacts${query}`).then((data) => data.items);
}

export function getArtifact(artifactId: string): Promise<CodeArtifact> {
  return apiGet<CodeArtifact>(`/api/artifacts/${artifactId}`);
}
