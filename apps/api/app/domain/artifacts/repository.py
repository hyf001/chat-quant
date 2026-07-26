from __future__ import annotations

from typing import Protocol

from app.domain.artifacts.models import ArtifactFile, ArtifactVersion, CodeArtifact


class ArtifactRepository(Protocol):
    async def save_artifact(self, artifact: CodeArtifact, version: ArtifactVersion) -> None: ...

    async def add_files(self, artifact_id: str, files: list[ArtifactFile]) -> CodeArtifact: ...

    async def get_artifact(self, artifact_id: str) -> CodeArtifact | None: ...

    async def list_artifacts(self, chat_session_id: str | None = None) -> list[CodeArtifact]: ...

    async def find_idempotent(
        self,
        source_sdk_tool_use_id: str,
        artifact_type: str,
        checksum: str,
        entrypoint: str | None,
    ) -> CodeArtifact | None: ...


class InMemoryArtifactRepository:
    def __init__(self) -> None:
        self._artifacts: dict[str, CodeArtifact] = {}
        self._versions: dict[str, list[ArtifactVersion]] = {}

    async def save_artifact(self, artifact: CodeArtifact, version: ArtifactVersion) -> None:
        self._artifacts[artifact.id] = artifact
        self._versions.setdefault(artifact.id, []).append(version)

    async def add_files(self, artifact_id: str, files: list[ArtifactFile]) -> CodeArtifact:
        artifact = self._artifacts.get(artifact_id)
        if artifact is None:
            raise KeyError(artifact_id)
        artifact.files.extend(files)
        return artifact

    async def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        return self._artifacts.get(artifact_id)

    async def list_artifacts(self, chat_session_id: str | None = None) -> list[CodeArtifact]:
        artifacts = list(self._artifacts.values())
        if chat_session_id is not None:
            artifacts = [
                artifact for artifact in artifacts if artifact.chat_session_id == chat_session_id
            ]
        return sorted(artifacts, key=lambda item: item.created_at, reverse=True)

    async def find_idempotent(
        self,
        source_sdk_tool_use_id: str,
        artifact_type: str,
        checksum: str,
        entrypoint: str | None,
    ) -> CodeArtifact | None:
        for artifact in self._artifacts.values():
            if (
                artifact.source_sdk_tool_use_id == source_sdk_tool_use_id
                and artifact.artifact_type.value == artifact_type
                and artifact.checksum == checksum
                and artifact.entrypoint == entrypoint
            ):
                return artifact
        return None
