from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

from app.domain.artifacts.checksums import normalize_text_content, package_checksum, sha256_digest
from app.domain.artifacts.errors import (
    ArtifactChecksumMismatchError,
    ArtifactNotFoundError,
    ArtifactPathEscapeError,
)
from app.domain.artifacts.models import (
    SCRIPT_ARTIFACT_TYPES,
    ArtifactFile,
    ArtifactFileRole,
    ArtifactStatus,
    ArtifactType,
    ArtifactVersion,
    CodeArtifact,
    JsonObject,
)
from app.domain.artifacts.repository import ArtifactRepository
from app.domain.artifacts.validation import (
    inspect_python_status,
    mime_type_for_path,
    normalize_relative_path,
    parse_entrypoint,
    validate_artifact_file_role,
    validate_entrypoint,
    validate_file_size,
    validate_role_extension,
)
from app.infrastructure.storage.artifact_store import FilesystemArtifactStore
from app.schemas.artifacts import (
    CodeArtifactFileCreate,
    GeneratedFileCreate,
    SaveCodeArtifactRequest,
    SaveGeneratedFilesRequest,
)


class CodeArtifactService:
    def __init__(
        self,
        repository: ArtifactRepository,
        store: FilesystemArtifactStore,
    ) -> None:
        self.repository = repository
        self.store = store

    def save_code_artifact(self, command: SaveCodeArtifactRequest) -> CodeArtifact:
        validate_entrypoint(command.artifact_type, command.entrypoint)
        if len(command.files) == 0:
            raise ArtifactPathEscapeError("at least one file is required")

        normalized_files = self._normalize_code_files(command.artifact_type, command.files)
        checksum = package_checksum(
            command.artifact_type,
            command.entrypoint,
            [(item.relative_path, item.checksum) for item in normalized_files],
        )
        if command.source_sdk_tool_use_id:
            existing = self.repository.find_idempotent(
                command.source_sdk_tool_use_id,
                command.artifact_type.value,
                checksum,
                command.entrypoint,
            )
            if existing is not None:
                return existing

        now = datetime.now(UTC)
        artifact_id = command.parent_artifact_id or self._new_id("ca")
        parent = self.repository.get_artifact(artifact_id) if command.parent_artifact_id else None
        if command.parent_artifact_id and parent is None:
            raise ArtifactNotFoundError("parent artifact was not found")

        version = (parent.version + 1) if parent else 1
        root_path = self._root_path(command, artifact_id, version)
        stored_files = self.store.write_package(
            root_path,
            [(item.relative_path, item.content_bytes) for item in normalized_files],
        )

        entrypoint_path, _ = parse_entrypoint(command.entrypoint)
        artifact_files = [
            ArtifactFile(
                id=self._new_id("af"),
                artifact_id=artifact_id,
                file_role=item.file_role,
                relative_path=item.relative_path,
                storage_uri=stored.storage_uri,
                mime_type=mime_type_for_path(item.relative_path),
                size_bytes=stored.size_bytes,
                checksum=item.checksum,
                is_entrypoint=item.relative_path == entrypoint_path,
                render_metadata_json=item.render_metadata,
            )
            for item, stored in zip(normalized_files, stored_files, strict=True)
        ]
        main_file_id = next((item.id for item in artifact_files if item.is_entrypoint), None)
        status = self._overall_status(command.artifact_type, normalized_files)
        artifact = CodeArtifact(
            id=artifact_id,
            user_id=command.user_id,
            project_id=command.project_id,
            chat_session_id=command.chat_session_id,
            source_sdk_session_id=command.source_sdk_session_id,
            source_sdk_message_uuid=command.source_sdk_message_uuid,
            source_sdk_tool_use_id=command.source_sdk_tool_use_id,
            artifact_type=command.artifact_type,
            title=command.title,
            description=command.description,
            version=version,
            entrypoint=command.entrypoint,
            root_path=root_path,
            main_file_id=main_file_id,
            checksum=checksum,
            metadata_json=command.metadata,
            status=status,
            files=artifact_files,
            created_at=parent.created_at if parent else now,
            updated_at=now,
        )
        version_record = ArtifactVersion(
            id=self._new_id("av"),
            artifact_id=artifact.id,
            version=version,
            root_path=root_path,
            checksum=checksum,
            entrypoint=command.entrypoint,
            manifest_json={
                "files": [
                    {
                        "file_id": item.id,
                        "relative_path": item.relative_path,
                        "checksum": item.checksum,
                        "size_bytes": item.size_bytes,
                    }
                    for item in artifact_files
                ]
            },
            created_by_sdk_tool_use_id=command.source_sdk_tool_use_id,
        )
        self.repository.save_artifact(artifact, version_record)
        return artifact

    def save_generated_files(self, command: SaveGeneratedFilesRequest) -> list[ArtifactFile]:
        if len(command.files) == 0:
            raise ArtifactPathEscapeError("at least one file is required")

        parent = self.repository.get_artifact(command.parent_artifact_id or "")
        if command.parent_artifact_id is not None and parent is None:
            raise ArtifactNotFoundError("parent artifact was not found")
        if parent is None:
            parent = self._create_file_collection_artifact(command)

        base_dir = Path(command.source_base_dir)
        normalized_files = self._normalize_generated_files(base_dir, command.files)
        root_path = parent.root_path
        stored_files = self.store.copy_files(
            root_path,
            base_dir,
            [(item.source_path, item.relative_path) for item in normalized_files],
        )
        artifact_files = [
            ArtifactFile(
                id=self._new_id("af"),
                artifact_id=parent.id,
                file_role=item.file_role,
                relative_path=item.relative_path,
                storage_uri=stored.storage_uri,
                mime_type=mime_type_for_path(item.relative_path),
                size_bytes=stored.size_bytes,
                checksum=item.checksum,
                is_entrypoint=False,
                render_metadata_json=item.render_metadata,
            )
            for item, stored in zip(normalized_files, stored_files, strict=True)
        ]
        self.repository.add_files(parent.id, artifact_files)
        return artifact_files

    def get_artifact(self, artifact_id: str) -> CodeArtifact:
        artifact = self.repository.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFoundError("artifact was not found")
        return artifact

    def list_artifacts(self, chat_session_id: str | None = None) -> list[CodeArtifact]:
        return self.repository.list_artifacts(chat_session_id=chat_session_id)

    def get_file(self, artifact_id: str, file_id: str) -> tuple[ArtifactFile, Path]:
        artifact = self.get_artifact(artifact_id)
        for artifact_file in artifact.files:
            if artifact_file.id == file_id:
                return artifact_file, self.store.absolute_path(artifact_file.storage_uri)
        raise ArtifactNotFoundError("artifact file was not found")

    def get_entrypoint(self, artifact_id: str) -> tuple[CodeArtifact, ArtifactFile, Path]:
        artifact = self.get_artifact(artifact_id)
        if artifact.artifact_type not in SCRIPT_ARTIFACT_TYPES or artifact.entrypoint is None:
            raise ArtifactPathEscapeError("artifact does not expose an executable entrypoint")
        entrypoint_path, _ = parse_entrypoint(artifact.entrypoint)
        main_file = next(
            (item for item in artifact.files if item.relative_path == entrypoint_path),
            None,
        )
        if main_file is None:
            raise ArtifactNotFoundError("entrypoint file was not found")
        return artifact, main_file, self.store.absolute_root_path(artifact.root_path)

    def _normalize_code_files(
        self, artifact_type: ArtifactType, files: list[CodeArtifactFileCreate]
    ) -> list[_NormalizedCodeFile]:
        normalized: list[_NormalizedCodeFile] = []
        for item in files:
            relative_path = normalize_relative_path(item.relative_path)
            validate_artifact_file_role(artifact_type, item.file_role)
            validate_role_extension(relative_path, item.file_role)
            content_bytes = normalize_text_content(item.content)
            validate_file_size(relative_path, len(content_bytes))
            checksum = sha256_digest(content_bytes)
            if item.checksum is not None and item.checksum != checksum:
                raise ArtifactChecksumMismatchError("declared checksum does not match content")
            normalized.append(
                _NormalizedCodeFile(
                    relative_path=relative_path,
                    content=item.content,
                    content_bytes=content_bytes,
                    file_role=item.file_role,
                    checksum=checksum,
                    render_metadata=item.render_metadata,
                    status=inspect_python_status(artifact_type, item.content),
                )
            )
        return normalized

    def _normalize_generated_files(
        self, base_dir: Path, files: list[GeneratedFileCreate]
    ) -> list[_NormalizedGeneratedFile]:
        normalized: list[_NormalizedGeneratedFile] = []
        resolved_base = base_dir.resolve()
        for item in files:
            source_path = normalize_relative_path(item.source_path)
            source_file = (resolved_base / source_path).resolve()
            if not source_file.is_relative_to(resolved_base) or source_file.is_symlink():
                raise ArtifactPathEscapeError("source file must stay under source_base_dir")
            if not source_file.is_file():
                raise ArtifactPathEscapeError("source file must exist")
            relative_path = self._generated_destination_path(item.file_role, source_path)
            validate_role_extension(relative_path, item.file_role)
            validate_file_size(relative_path, source_file.stat().st_size)
            checksum = sha256_digest(source_file.read_bytes())
            if item.checksum is not None and item.checksum != checksum:
                raise ArtifactChecksumMismatchError("declared checksum does not match source file")
            normalized.append(
                _NormalizedGeneratedFile(
                    source_path=source_path,
                    relative_path=relative_path,
                    file_role=item.file_role,
                    checksum=checksum,
                    render_metadata=item.render_metadata,
                )
            )
        return normalized

    def _create_file_collection_artifact(self, command: SaveGeneratedFilesRequest) -> CodeArtifact:
        artifact_id = self._new_id("ca")
        root_path = self._root_path_for_parts(
            user_id=command.user_id,
            chat_session_id=command.chat_session_id,
            source_sdk_session_id=command.source_sdk_session_id,
            artifact_id=artifact_id,
            version=1,
        )
        now = datetime.now(UTC)
        artifact = CodeArtifact(
            id=artifact_id,
            user_id=command.user_id,
            project_id=command.project_id,
            chat_session_id=command.chat_session_id,
            source_sdk_session_id=command.source_sdk_session_id,
            source_sdk_message_uuid=command.source_sdk_message_uuid,
            source_sdk_tool_use_id=command.source_sdk_tool_use_id,
            artifact_type=ArtifactType.JSON_RESULT,
            title=command.title or "运行文件产物",
            description=None,
            version=1,
            entrypoint=None,
            root_path=root_path,
            checksum=sha256_digest(artifact_id.encode("utf-8")),
            metadata_json=command.metadata,
            status=ArtifactStatus.CREATED,
            created_at=now,
            updated_at=now,
        )
        version = ArtifactVersion(
            id=self._new_id("av"),
            artifact_id=artifact_id,
            version=1,
            root_path=root_path,
            checksum=artifact.checksum,
            entrypoint=None,
            manifest_json={"files": []},
            created_by_sdk_tool_use_id=command.source_sdk_tool_use_id,
        )
        self.repository.save_artifact(artifact, version)
        return artifact

    @staticmethod
    def _overall_status(
        artifact_type: ArtifactType, files: list[_NormalizedCodeFile]
    ) -> ArtifactStatus:
        if artifact_type not in SCRIPT_ARTIFACT_TYPES:
            return ArtifactStatus.CREATED
        if any(item.status == ArtifactStatus.INVALID for item in files):
            return ArtifactStatus.INVALID
        return ArtifactStatus.VALIDATED

    def _root_path(self, command: SaveCodeArtifactRequest, artifact_id: str, version: int) -> str:
        return self._root_path_for_parts(
            user_id=command.user_id,
            chat_session_id=command.chat_session_id,
            source_sdk_session_id=command.source_sdk_session_id,
            artifact_id=artifact_id,
            version=version,
        )

    @staticmethod
    def _root_path_for_parts(
        user_id: str,
        chat_session_id: str,
        source_sdk_session_id: str | None,
        artifact_id: str,
        version: int,
    ) -> str:
        sdk_session_id = source_sdk_session_id or "manual"
        return (
            f"users/{user_id}/chat_sessions/{chat_session_id}/sdk_sessions/"
            f"{sdk_session_id}/artifacts/{artifact_id}/v{version}"
        )

    @staticmethod
    def _generated_destination_path(file_role: ArtifactFileRole, source_path: str) -> str:
        filename = Path(source_path).name
        if file_role == ArtifactFileRole.LOG_FILE:
            return f"logs/{filename}"
        return f"outputs/{filename}"

    @staticmethod
    def _new_id(prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex}"


class _NormalizedCodeFile:
    def __init__(
        self,
        *,
        relative_path: str,
        content: str,
        content_bytes: bytes,
        file_role: ArtifactFileRole,
        checksum: str,
        render_metadata: JsonObject,
        status: ArtifactStatus,
    ) -> None:
        self.relative_path = relative_path
        self.content = content
        self.content_bytes = content_bytes
        self.file_role = file_role
        self.checksum = checksum
        self.render_metadata = render_metadata
        self.status = status


class _NormalizedGeneratedFile:
    def __init__(
        self,
        *,
        source_path: str,
        relative_path: str,
        file_role: ArtifactFileRole,
        checksum: str,
        render_metadata: JsonObject,
    ) -> None:
        self.source_path = source_path
        self.relative_path = relative_path
        self.file_role = file_role
        self.checksum = checksum
        self.render_metadata = render_metadata
