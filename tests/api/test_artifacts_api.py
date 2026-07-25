from pathlib import Path

from app.application.artifact_service import CodeArtifactService
from app.application.dependencies import get_artifact_service
from app.domain.artifacts.repository import InMemoryArtifactRepository
from app.infrastructure.storage import FilesystemArtifactStore
from app.main import create_app
from fastapi.testclient import TestClient


def test_artifact_api_saves_reads_entrypoint_and_downloads_file(tmp_path: Path) -> None:
    service = CodeArtifactService(
        repository=InMemoryArtifactRepository(),
        store=FilesystemArtifactStore(tmp_path / "artifacts"),
    )
    app = create_app()
    app.dependency_overrides[get_artifact_service] = lambda: service

    with TestClient(app) as client:
        response = client.post(
            "/api/artifacts/code",
            json={
                "chat_session_id": "conv_api",
                "source_sdk_tool_use_id": "toolu_api",
                "artifact_type": "strategy_script",
                "title": "API 策略",
                "entrypoint": "src/strategy.py:GeneratedStrategy",
                "files": [
                    {
                        "relative_path": "src/strategy.py",
                        "content": "class GeneratedStrategy:\n    pass\n",
                        "file_role": "strategy_script",
                    }
                ],
            },
        )
        assert response.status_code == 201
        artifact = response.json()
        artifact_id = artifact["artifact_id"]
        file_id = artifact["files"][0]["file_id"]

        detail = client.get(f"/api/artifacts/{artifact_id}")
        assert detail.status_code == 200
        assert detail.json()["entrypoint"] == "src/strategy.py:GeneratedStrategy"

        entrypoint = client.get(f"/api/artifacts/{artifact_id}/entrypoint")
        assert entrypoint.status_code == 200
        assert entrypoint.json()["main_file"] == "src/strategy.py"

        download = client.get(f"/api/artifacts/{artifact_id}/files/{file_id}")
        assert download.status_code == 200
        assert "GeneratedStrategy" in download.text
