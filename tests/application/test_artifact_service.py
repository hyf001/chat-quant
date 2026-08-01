from pathlib import Path

import pytest
from app.service.artifact import CodeArtifactService
from app.model.artifact_errors import (
    ArtifactChecksumMismatchError,
    ArtifactNotFoundError,
    ArtifactPathEscapeError,
)
from app.model.artifacts import ArtifactFileRole, ArtifactType
from app.model.artifact_repository import InMemoryArtifactRepository
from app.model.storage import FilesystemArtifactStore
from app.schema.artifacts import (
    CodeArtifactFileCreate,
    GeneratedFileCreate,
    SaveCodeArtifactRequest,
    SaveGeneratedFilesRequest,
)


def make_service(tmp_path: Path) -> CodeArtifactService:
    return CodeArtifactService(
        repository=InMemoryArtifactRepository(),
        store=FilesystemArtifactStore(tmp_path / "artifacts"),
    )


def strategy_request() -> SaveCodeArtifactRequest:
    return SaveCodeArtifactRequest(
        chat_session_id="conv_1",
        source_sdk_session_id="claude_1",
        source_sdk_tool_use_id="toolu_1",
        artifact_type=ArtifactType.STRATEGY_SCRIPT,
        title="均线策略",
        entrypoint="src/strategy.py:GeneratedStrategy",
        files=[
            CodeArtifactFileCreate(
                relative_path="src/strategy.py",
                content=(
                    "class GeneratedStrategy:\n"
                    "    params = ()\n"
                    "    def next(self):\n"
                    "        return None\n"
                ),
                file_role=ArtifactFileRole.STRATEGY_SCRIPT,
            )
        ],
        metadata={"strategy_type": "ma_cross"},
    )


@pytest.mark.asyncio
async def test_save_code_artifact_returns_idempotent_artifact(tmp_path: Path) -> None:
    service = make_service(tmp_path)

    first = await service.save_code_artifact(strategy_request())
    second = await service.save_code_artifact(strategy_request())

    assert first.id == second.id
    assert first.version == 1
    assert first.status == "validated"
    assert first.files[0].is_entrypoint is True
    _, _, root_path = await service.get_entrypoint(first.id)
    assert (root_path / "src/strategy.py").is_file()


@pytest.mark.asyncio
async def test_save_code_artifact_rejects_path_escape(tmp_path: Path) -> None:
    service = make_service(tmp_path)
    request = strategy_request()
    request.files[0].relative_path = "../strategy.py"

    with pytest.raises(ArtifactPathEscapeError):
        await service.save_code_artifact(request)


@pytest.mark.asyncio
async def test_save_code_artifact_rejects_checksum_mismatch(tmp_path: Path) -> None:
    service = make_service(tmp_path)
    request = strategy_request()
    request.files[0].checksum = "sha256:not-real"

    with pytest.raises(ArtifactChecksumMismatchError):
        await service.save_code_artifact(request)


@pytest.mark.asyncio
async def test_save_generated_files_copies_outputs_to_parent_artifact(tmp_path: Path) -> None:
    service = make_service(tmp_path)
    artifact = await service.save_code_artifact(strategy_request())
    output_dir = tmp_path / "runtime-output"
    output_dir.mkdir()
    (output_dir / "result.json").write_text('{"return":0.12}', encoding="utf-8")

    files = await service.save_generated_files(
        SaveGeneratedFilesRequest(
            chat_session_id="conv_1",
            parent_artifact_id=artifact.id,
            source_base_dir=str(output_dir),
            files=[
                GeneratedFileCreate(
                    source_path="result.json",
                    file_role=ArtifactFileRole.JSON_RESULT,
                    render_metadata={"schema": "BacktestResultPayload"},
                )
            ],
        )
    )

    assert files[0].relative_path == "outputs/result.json"
    assert files[0].file_role == ArtifactFileRole.JSON_RESULT
    _, stored_path = await service.get_file(artifact.id, files[0].id)
    assert stored_path.read_text(encoding="utf-8") == '{"return":0.12}'


@pytest.mark.asyncio
async def test_save_generated_files_rejects_missing_parent(tmp_path: Path) -> None:
    service = make_service(tmp_path)
    output_dir = tmp_path / "runtime-output"
    output_dir.mkdir()
    (output_dir / "result.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ArtifactNotFoundError):
        await service.save_generated_files(
            SaveGeneratedFilesRequest(
                chat_session_id="conv_1",
                parent_artifact_id="ca_missing",
                source_base_dir=str(output_dir),
                files=[
                    GeneratedFileCreate(
                        source_path="result.json",
                        file_role=ArtifactFileRole.JSON_RESULT,
                    )
                ],
            )
        )
