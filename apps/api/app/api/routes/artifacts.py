from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.dependencies import ProjectId, UserId
from app.application.artifact_service import CodeArtifactService
from app.application.dependencies import get_artifact_service
from app.domain.artifacts.errors import (
    ArtifactChecksumMismatchError,
    ArtifactError,
    ArtifactFileTooLargeError,
    ArtifactNotFoundError,
)
from app.domain.artifacts.models import ArtifactFile, CodeArtifact
from app.schemas.artifacts import (
    ArtifactEntrypointResponse,
    ArtifactFileResponse,
    ArtifactListResponse,
    CodeArtifactResponse,
    SaveCodeArtifactRequest,
    SaveGeneratedFilesRequest,
)

router = APIRouter(prefix="/artifacts", tags=["artifacts"])
ArtifactServiceDep = Annotated[CodeArtifactService, Depends(get_artifact_service)]


@router.post("/code", response_model=CodeArtifactResponse, status_code=201)
async def save_code_artifact(
    request: SaveCodeArtifactRequest,
    service: ArtifactServiceDep,
    user_id: UserId,
    project_id: ProjectId,
) -> CodeArtifactResponse:
    try:
        artifact = await service.save_code_artifact(
            request.model_copy(
                update={
                    "user_id": request.user_id
                    if "user_id" in request.model_fields_set
                    else user_id,
                    "project_id": request.project_id
                    if "project_id" in request.model_fields_set
                    else project_id,
                }
            )
        )
    except ArtifactError as exc:
        raise _http_error(exc) from exc
    return to_artifact_response(artifact)


@router.post("/files", response_model=list[ArtifactFileResponse], status_code=201)
async def save_generated_files(
    request: SaveGeneratedFilesRequest,
    service: ArtifactServiceDep,
    user_id: UserId,
    project_id: ProjectId,
) -> list[ArtifactFileResponse]:
    try:
        files = await service.save_generated_files(
            request.model_copy(
                update={
                    "user_id": request.user_id
                    if "user_id" in request.model_fields_set
                    else user_id,
                    "project_id": request.project_id
                    if "project_id" in request.model_fields_set
                    else project_id,
                }
            )
        )
    except ArtifactError as exc:
        raise _http_error(exc) from exc
    return [to_file_response(file) for file in files]


@router.get("", response_model=ArtifactListResponse)
async def list_artifacts(
    service: ArtifactServiceDep,
    chat_session_id: str | None = None,
) -> ArtifactListResponse:
    artifacts = await service.list_artifacts(chat_session_id)
    return ArtifactListResponse(
        items=[to_artifact_response(item) for item in artifacts]
    )


@router.get("/{artifact_id}", response_model=CodeArtifactResponse)
async def get_artifact(
    artifact_id: str,
    service: ArtifactServiceDep,
) -> CodeArtifactResponse:
    try:
        artifact = await service.get_artifact(artifact_id)
    except ArtifactError as exc:
        raise _http_error(exc) from exc
    return to_artifact_response(artifact)


@router.get("/{artifact_id}/entrypoint", response_model=ArtifactEntrypointResponse)
async def get_artifact_entrypoint(
    artifact_id: str,
    service: ArtifactServiceDep,
) -> ArtifactEntrypointResponse:
    try:
        artifact, main_file, absolute_root_path = await service.get_entrypoint(artifact_id)
    except ArtifactError as exc:
        raise _http_error(exc) from exc
    return ArtifactEntrypointResponse(
        artifact_id=artifact.id,
        artifact_type=artifact.artifact_type,
        entrypoint=artifact.entrypoint or main_file.relative_path,
        absolute_root_path=str(absolute_root_path),
        main_file=main_file.relative_path,
        checksum=artifact.checksum,
    )


@router.get("/{artifact_id}/files/{file_id}")
async def download_artifact_file(
    artifact_id: str,
    file_id: str,
    service: ArtifactServiceDep,
) -> FileResponse:
    artifact_file, path = await _get_download_path(service, artifact_id, file_id)
    return FileResponse(
        path=path,
        media_type=artifact_file.mime_type,
        filename=Path(artifact_file.relative_path).name,
    )


@router.get("/{artifact_id}/files/{file_id}/preview")
async def preview_artifact_file(
    artifact_id: str,
    file_id: str,
    service: ArtifactServiceDep,
) -> FileResponse:
    artifact_file, path = await _get_download_path(service, artifact_id, file_id)
    if artifact_file.mime_type == "text/html":
        raise HTTPException(status_code=400, detail={"code": "ARTIFACT_PREVIEW_DISABLED"})
    return FileResponse(path=path, media_type=artifact_file.mime_type)


async def _get_download_path(
    service: CodeArtifactService,
    artifact_id: str,
    file_id: str,
) -> tuple[ArtifactFile, Path]:
    try:
        artifact_file, path = await service.get_file(artifact_id, file_id)
    except ArtifactError as exc:
        raise _http_error(exc) from exc
    if not path.is_file():
        raise HTTPException(status_code=404, detail={"code": "ARTIFACT_FILE_MISSING"})
    return artifact_file, path


def to_artifact_response(artifact: CodeArtifact) -> CodeArtifactResponse:
    return CodeArtifactResponse(
        artifact_id=artifact.id,
        user_id=artifact.user_id,
        project_id=artifact.project_id,
        chat_session_id=artifact.chat_session_id,
        source_sdk_session_id=artifact.source_sdk_session_id,
        source_sdk_message_uuid=artifact.source_sdk_message_uuid,
        source_sdk_tool_use_id=artifact.source_sdk_tool_use_id,
        artifact_type=artifact.artifact_type,
        title=artifact.title,
        description=artifact.description,
        version=artifact.version,
        entrypoint=artifact.entrypoint,
        root_path=artifact.root_path,
        main_file_id=artifact.main_file_id,
        checksum=artifact.checksum,
        metadata=artifact.metadata_json,
        status=artifact.status,
        files=[to_file_response(item) for item in artifact.files],
        created_at=artifact.created_at.isoformat(),
        updated_at=artifact.updated_at.isoformat(),
    )


def to_file_response(file: ArtifactFile) -> ArtifactFileResponse:
    preview_url = f"/api/artifacts/{file.artifact_id}/files/{file.id}/preview"
    if file.mime_type == "text/html":
        preview_url = None
    return ArtifactFileResponse(
        file_id=file.id,
        artifact_id=file.artifact_id,
        relative_path=file.relative_path,
        file_role=file.file_role,
        storage_uri=file.storage_uri,
        mime_type=file.mime_type,
        size_bytes=file.size_bytes,
        checksum=file.checksum,
        is_entrypoint=file.is_entrypoint,
        render_metadata=file.render_metadata_json,
        download_url=f"/api/artifacts/{file.artifact_id}/files/{file.id}",
        preview_url=preview_url,
        created_at=file.created_at.isoformat(),
    )


def _http_error(exc: ArtifactError) -> HTTPException:
    status_code = 400
    if isinstance(exc, ArtifactNotFoundError):
        status_code = 404
    if isinstance(exc, ArtifactFileTooLargeError):
        status_code = 413
    if isinstance(exc, ArtifactChecksumMismatchError):
        status_code = 409
    return HTTPException(status_code=status_code, detail={"code": exc.code, "message": exc.message})
