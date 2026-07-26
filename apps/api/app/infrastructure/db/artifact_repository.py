from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.artifacts.models import (
    ArtifactFile,
    ArtifactFileRole,
    ArtifactStatus,
    ArtifactType,
    ArtifactVersion,
    CodeArtifact,
    JsonObject,
)
from app.infrastructure.db.models import ArtifactFileRow, ArtifactVersionRow, CodeArtifactRow


class SQLAlchemyArtifactRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def save_artifact(self, artifact: CodeArtifact, version: ArtifactVersion) -> None:
        async with self._session_factory() as db:
            await db.merge(_artifact_to_row(artifact))
            for file in artifact.files:
                await db.merge(_file_to_row(file))
            await db.merge(_version_to_row(version))
            await db.commit()

    async def add_files(self, artifact_id: str, files: list[ArtifactFile]) -> CodeArtifact:
        async with self._session_factory() as db:
            for file in files:
                await db.merge(_file_to_row(file))
            row = await db.get(CodeArtifactRow, artifact_id)
            if row is None:
                raise KeyError(artifact_id)
            row.updated_at = datetime.now(UTC)
            await db.commit()
        artifact = await self.get_artifact(artifact_id)
        if artifact is None:
            raise KeyError(artifact_id)
        return artifact

    async def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        async with self._session_factory() as db:
            row = await db.get(CodeArtifactRow, artifact_id)
            if row is None:
                return None
            return await self._artifact_from_row(db, row)

    async def list_artifacts(self, chat_session_id: str | None = None) -> list[CodeArtifact]:
        filters = []
        if chat_session_id is not None:
            filters.append(CodeArtifactRow.chat_session_id == chat_session_id)
        async with self._session_factory() as db:
            result = await db.scalars(
                select(CodeArtifactRow)
                .where(*filters)
                .order_by(CodeArtifactRow.created_at.desc())
            )
            return [await self._artifact_from_row(db, row) for row in result.all()]

    async def find_idempotent(
        self,
        source_sdk_tool_use_id: str,
        artifact_type: str,
        checksum: str,
        entrypoint: str | None,
    ) -> CodeArtifact | None:
        async with self._session_factory() as db:
            row = await db.scalar(
                select(CodeArtifactRow).where(
                    CodeArtifactRow.source_sdk_tool_use_id == source_sdk_tool_use_id,
                    CodeArtifactRow.artifact_type == artifact_type,
                    CodeArtifactRow.checksum == checksum,
                    CodeArtifactRow.entrypoint.is_(entrypoint)
                    if entrypoint is None
                    else CodeArtifactRow.entrypoint == entrypoint,
                )
            )
            if row is None:
                return None
            return await self._artifact_from_row(db, row)

    async def _artifact_from_row(
        self,
        db: AsyncSession,
        row: CodeArtifactRow,
    ) -> CodeArtifact:
        file_rows = await db.scalars(
            select(ArtifactFileRow)
            .where(ArtifactFileRow.artifact_id == row.id)
            .order_by(ArtifactFileRow.created_at.asc())
        )
        return CodeArtifact(
            id=row.id,
            user_id=row.user_id,
            project_id=row.project_id,
            chat_session_id=row.chat_session_id,
            source_sdk_session_id=row.source_sdk_session_id,
            source_sdk_message_uuid=row.source_sdk_message_uuid,
            source_sdk_tool_use_id=row.source_sdk_tool_use_id,
            artifact_type=ArtifactType(row.artifact_type),
            title=row.title,
            description=row.description,
            version=row.version,
            entrypoint=row.entrypoint,
            root_path=row.root_path,
            main_file_id=row.main_file_id,
            checksum=row.checksum,
            metadata_json=_json_object(row.metadata_json),
            status=ArtifactStatus(row.status),
            files=[_file_from_row(file_row) for file_row in file_rows.all()],
            created_at=row.created_at,
            updated_at=row.updated_at,
        )


def _artifact_to_row(artifact: CodeArtifact) -> CodeArtifactRow:
    return CodeArtifactRow(
        id=artifact.id,
        user_id=artifact.user_id,
        project_id=artifact.project_id,
        chat_session_id=artifact.chat_session_id,
        source_sdk_session_id=artifact.source_sdk_session_id,
        source_sdk_message_uuid=artifact.source_sdk_message_uuid,
        source_sdk_tool_use_id=artifact.source_sdk_tool_use_id,
        artifact_type=artifact.artifact_type.value,
        title=artifact.title,
        description=artifact.description,
        version=artifact.version,
        entrypoint=artifact.entrypoint,
        root_path=artifact.root_path,
        main_file_id=artifact.main_file_id,
        checksum=artifact.checksum,
        metadata_json=dict(artifact.metadata_json),
        status=artifact.status.value,
        created_at=artifact.created_at,
        updated_at=artifact.updated_at,
    )


def _file_to_row(file: ArtifactFile) -> ArtifactFileRow:
    return ArtifactFileRow(
        id=file.id,
        artifact_id=file.artifact_id,
        file_role=file.file_role.value,
        relative_path=file.relative_path,
        storage_uri=file.storage_uri,
        mime_type=file.mime_type,
        size_bytes=file.size_bytes,
        checksum=file.checksum,
        is_entrypoint=file.is_entrypoint,
        render_metadata_json=dict(file.render_metadata_json),
        created_at=file.created_at,
    )


def _version_to_row(version: ArtifactVersion) -> ArtifactVersionRow:
    return ArtifactVersionRow(
        id=version.id,
        artifact_id=version.artifact_id,
        version=version.version,
        root_path=version.root_path,
        checksum=version.checksum,
        entrypoint=version.entrypoint,
        manifest_json=dict(version.manifest_json),
        created_by_sdk_tool_use_id=version.created_by_sdk_tool_use_id,
        created_at=version.created_at,
    )


def _file_from_row(row: ArtifactFileRow) -> ArtifactFile:
    return ArtifactFile(
        id=row.id,
        artifact_id=row.artifact_id,
        file_role=ArtifactFileRole(row.file_role),
        relative_path=row.relative_path,
        storage_uri=row.storage_uri,
        mime_type=row.mime_type,
        size_bytes=row.size_bytes,
        checksum=row.checksum,
        is_entrypoint=row.is_entrypoint,
        render_metadata_json=_json_object(row.render_metadata_json),
        created_at=row.created_at,
    )


def _json_object(value: object) -> JsonObject:
    return value if isinstance(value, dict) else {}

