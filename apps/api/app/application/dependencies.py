from functools import lru_cache

from app.application.artifact_service import CodeArtifactService
from app.core.config import get_settings
from app.infrastructure.db import SQLiteArtifactRepository
from app.infrastructure.storage import FilesystemArtifactStore


@lru_cache
def get_artifact_service() -> CodeArtifactService:
    settings = get_settings()
    return CodeArtifactService(
        repository=SQLiteArtifactRepository(settings.artifact_index_path),
        store=FilesystemArtifactStore(settings.artifact_root),
    )
