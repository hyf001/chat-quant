from functools import lru_cache

from app.application.artifact_service import CodeArtifactService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.infrastructure.db import SQLiteArtifactRepository
from app.infrastructure.storage import FilesystemArtifactStore

logger = get_logger(__name__)


@lru_cache
def get_artifact_service() -> CodeArtifactService:
    settings = get_settings()
    logger.info(
        "artifact service initialized",
        extra={
            "artifact_root": str(settings.artifact_root),
            "artifact_index_path": str(settings.artifact_index_path),
        },
    )
    return CodeArtifactService(
        repository=SQLiteArtifactRepository(settings.artifact_index_path),
        store=FilesystemArtifactStore(settings.artifact_root),
    )
