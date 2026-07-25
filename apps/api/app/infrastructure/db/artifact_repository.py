from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from app.domain.artifacts.models import (
    ArtifactFile,
    ArtifactFileRole,
    ArtifactStatus,
    ArtifactType,
    ArtifactVersion,
    CodeArtifact,
    JsonObject,
)


class SQLiteArtifactRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def save_artifact(self, artifact: CodeArtifact, version: ArtifactVersion) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                insert or replace into code_artifacts (
                    id, user_id, project_id, chat_session_id, source_sdk_session_id,
                    source_sdk_message_uuid, source_sdk_tool_use_id, artifact_type, title,
                    description, version, entrypoint, root_path, main_file_id, checksum,
                    metadata_json, status, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact.id,
                    artifact.user_id,
                    artifact.project_id,
                    artifact.chat_session_id,
                    artifact.source_sdk_session_id,
                    artifact.source_sdk_message_uuid,
                    artifact.source_sdk_tool_use_id,
                    artifact.artifact_type.value,
                    artifact.title,
                    artifact.description,
                    artifact.version,
                    artifact.entrypoint,
                    artifact.root_path,
                    artifact.main_file_id,
                    artifact.checksum,
                    json.dumps(artifact.metadata_json),
                    artifact.status.value,
                    artifact.created_at.isoformat(),
                    artifact.updated_at.isoformat(),
                ),
            )
            self._insert_files(conn, artifact.files)
            conn.execute(
                """
                insert or replace into artifact_versions (
                    id, artifact_id, version, root_path, checksum, entrypoint, manifest_json,
                    created_by_sdk_tool_use_id, created_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version.id,
                    version.artifact_id,
                    version.version,
                    version.root_path,
                    version.checksum,
                    version.entrypoint,
                    json.dumps(version.manifest_json),
                    version.created_by_sdk_tool_use_id,
                    version.created_at.isoformat(),
                ),
            )

    def add_files(self, artifact_id: str, files: list[ArtifactFile]) -> CodeArtifact:
        with self._connect() as conn:
            self._insert_files(conn, files)
            conn.execute(
                "update code_artifacts set updated_at = ? where id = ?",
                (datetime.now(UTC).isoformat(), artifact_id),
            )
        artifact = self.get_artifact(artifact_id)
        if artifact is None:
            raise KeyError(artifact_id)
        return artifact

    def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        with self._connect() as conn:
            artifact_row = conn.execute(
                "select * from code_artifacts where id = ?",
                (artifact_id,),
            ).fetchone()
            if artifact_row is None:
                return None
            return self._artifact_from_row(conn, artifact_row)

    def list_artifacts(self, chat_session_id: str | None = None) -> list[CodeArtifact]:
        query = "select * from code_artifacts"
        params: tuple[str, ...] = ()
        if chat_session_id is not None:
            query += " where chat_session_id = ?"
            params = (chat_session_id,)
        query += " order by created_at desc"
        with self._connect() as conn:
            return [self._artifact_from_row(conn, row) for row in conn.execute(query, params)]

    def find_idempotent(
        self,
        source_sdk_tool_use_id: str,
        artifact_type: str,
        checksum: str,
        entrypoint: str | None,
    ) -> CodeArtifact | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                select * from code_artifacts
                where source_sdk_tool_use_id = ?
                  and artifact_type = ?
                  and checksum = ?
                  and (entrypoint is ? or entrypoint = ?)
                """,
                (source_sdk_tool_use_id, artifact_type, checksum, entrypoint, entrypoint),
            ).fetchone()
            if row is None:
                return None
            return self._artifact_from_row(conn, row)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                create table if not exists code_artifacts (
                    id text primary key,
                    user_id text not null,
                    project_id text not null,
                    chat_session_id text not null,
                    source_sdk_session_id text,
                    source_sdk_message_uuid text,
                    source_sdk_tool_use_id text,
                    artifact_type text not null,
                    title text not null,
                    description text,
                    version integer not null,
                    entrypoint text,
                    root_path text not null,
                    main_file_id text,
                    checksum text not null,
                    metadata_json text not null default '{}',
                    status text not null default 'created',
                    created_at text not null,
                    updated_at text not null
                );
                create table if not exists artifact_files (
                    id text primary key,
                    artifact_id text not null,
                    file_role text not null,
                    relative_path text not null,
                    storage_uri text not null,
                    mime_type text not null,
                    size_bytes integer not null,
                    checksum text not null,
                    is_entrypoint integer not null default 0,
                    render_metadata_json text not null default '{}',
                    created_at text not null,
                    foreign key (artifact_id) references code_artifacts(id)
                );
                create table if not exists artifact_versions (
                    id text primary key,
                    artifact_id text not null,
                    version integer not null,
                    root_path text not null,
                    checksum text not null,
                    entrypoint text,
                    manifest_json text not null,
                    created_by_sdk_tool_use_id text,
                    created_at text not null,
                    foreign key (artifact_id) references code_artifacts(id)
                );
                create table if not exists artifact_links (
                    id text primary key,
                    artifact_id text not null,
                    file_id text,
                    target_type text not null,
                    target_id text not null,
                    relation text not null,
                    metadata_json text not null default '{}',
                    created_at text not null
                );
                create index if not exists idx_code_artifacts_chat_created
                    on code_artifacts(chat_session_id, created_at);
                create index if not exists idx_code_artifacts_sdk_tool_use
                    on code_artifacts(source_sdk_tool_use_id);
                create index if not exists idx_code_artifacts_type
                    on code_artifacts(artifact_type);
                create unique index if not exists uq_code_artifacts_idempotent
                    on code_artifacts(source_sdk_tool_use_id, artifact_type, checksum, entrypoint);
                create index if not exists idx_artifact_files_artifact
                    on artifact_files(artifact_id);
                create index if not exists idx_artifact_files_role
                    on artifact_files(file_role);
                create unique index if not exists uq_artifact_files_path
                    on artifact_files(artifact_id, relative_path);
                create unique index if not exists uq_artifact_versions_version
                    on artifact_versions(artifact_id, version);
                create unique index if not exists uq_artifact_versions_checksum
                    on artifact_versions(artifact_id, checksum, entrypoint);
                create index if not exists idx_artifact_links_target
                    on artifact_links(target_type, target_id);
                create index if not exists idx_artifact_links_artifact
                    on artifact_links(artifact_id);
                """
            )

    def _insert_files(self, conn: sqlite3.Connection, files: list[ArtifactFile]) -> None:
        conn.executemany(
            """
            insert or replace into artifact_files (
                id, artifact_id, file_role, relative_path, storage_uri, mime_type, size_bytes,
                checksum, is_entrypoint, render_metadata_json, created_at
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item.id,
                    item.artifact_id,
                    item.file_role.value,
                    item.relative_path,
                    item.storage_uri,
                    item.mime_type,
                    item.size_bytes,
                    item.checksum,
                    int(item.is_entrypoint),
                    json.dumps(item.render_metadata_json),
                    item.created_at.isoformat(),
                )
                for item in files
            ],
        )

    def _artifact_from_row(
        self, conn: sqlite3.Connection, row: sqlite3.Row
    ) -> CodeArtifact:
        files = [
            self._file_from_row(file_row)
            for file_row in conn.execute(
                "select * from artifact_files where artifact_id = ? order by created_at asc",
                (row["id"],),
            )
        ]
        return CodeArtifact(
            id=row["id"],
            user_id=row["user_id"],
            project_id=row["project_id"],
            chat_session_id=row["chat_session_id"],
            source_sdk_session_id=row["source_sdk_session_id"],
            source_sdk_message_uuid=row["source_sdk_message_uuid"],
            source_sdk_tool_use_id=row["source_sdk_tool_use_id"],
            artifact_type=ArtifactType(row["artifact_type"]),
            title=row["title"],
            description=row["description"],
            version=row["version"],
            entrypoint=row["entrypoint"],
            root_path=row["root_path"],
            main_file_id=row["main_file_id"],
            checksum=row["checksum"],
            metadata_json=self._json_object(row["metadata_json"]),
            status=ArtifactStatus(row["status"]),
            files=files,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def _file_from_row(row: sqlite3.Row) -> ArtifactFile:
        return ArtifactFile(
            id=row["id"],
            artifact_id=row["artifact_id"],
            file_role=ArtifactFileRole(row["file_role"]),
            relative_path=row["relative_path"],
            storage_uri=row["storage_uri"],
            mime_type=row["mime_type"],
            size_bytes=row["size_bytes"],
            checksum=row["checksum"],
            is_entrypoint=bool(row["is_entrypoint"]),
            render_metadata_json=SQLiteArtifactRepository._json_object(row["render_metadata_json"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    @staticmethod
    def _json_object(value: str) -> JsonObject:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
