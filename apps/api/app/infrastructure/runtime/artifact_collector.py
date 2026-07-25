from __future__ import annotations

import hashlib
import mimetypes
from dataclasses import dataclass, field
from pathlib import Path

from app.schemas.contracts.execution_result import RuntimeArtifact


@dataclass(frozen=True)
class ArtifactCollectionResult:
    artifacts: list[RuntimeArtifact]
    warnings: list[str] = field(default_factory=list)


class ArtifactCollector:
    def __init__(self, *, max_files: int, max_file_bytes: int) -> None:
        self.max_files = max_files
        self.max_file_bytes = max_file_bytes

    def collect(self, output_dir: Path) -> ArtifactCollectionResult:
        artifacts: list[RuntimeArtifact] = []
        warnings: list[str] = []
        output_root = output_dir.resolve()

        for path in sorted(output_root.rglob("*")):
            if len(artifacts) >= self.max_files:
                warnings.append(f"Artifact limit reached at {self.max_files} files")
                break
            if not path.is_file():
                continue
            relative_path = path.relative_to(output_root)
            if any(part.startswith(".") for part in relative_path.parts):
                continue
            if path.is_symlink():
                warnings.append(f"Ignored symlink artifact: {relative_path.as_posix()}")
                continue
            if not path.resolve().is_relative_to(output_root):
                warnings.append(f"Ignored out-of-bounds artifact: {relative_path.as_posix()}")
                continue
            size_bytes = path.stat().st_size
            if size_bytes > self.max_file_bytes:
                warnings.append(f"Ignored oversized artifact: {relative_path.as_posix()}")
                continue
            artifact_type = self._classify(relative_path)
            artifacts.append(
                RuntimeArtifact(
                    type=artifact_type,
                    path=relative_path.as_posix(),
                    name=path.name,
                    mime_type=self._mime_type(path),
                    size_bytes=size_bytes,
                    checksum=self._sha256(path),
                    metadata=self._metadata(relative_path),
                )
            )

        return ArtifactCollectionResult(artifacts=artifacts, warnings=warnings)

    def _classify(self, relative_path: Path) -> str:
        path_text = relative_path.as_posix()
        suffix = relative_path.suffix.lower()
        if path_text == "result.json":
            return "json_result"
        if path_text.endswith("_curve.json"):
            return "curve"
        is_chart_json = relative_path.parent.name == "charts" or path_text.endswith(".chart.json")
        if suffix == ".json" and is_chart_json:
            return "chart"
        if suffix == ".csv":
            return "table"
        if suffix == ".png":
            return "image"
        if suffix == ".html":
            return "html"
        if suffix == ".log":
            return "log"
        return "file"

    def _mime_type(self, path: Path) -> str | None:
        if path.suffix.lower() == ".csv":
            return "text/csv"
        mime_type, _encoding = mimetypes.guess_type(path.name)
        return mime_type

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file_obj:
            for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _metadata(self, relative_path: Path) -> dict[str, str]:
        if relative_path.as_posix().endswith("_curve.json"):
            return {"curve_type": relative_path.stem.removesuffix("_curve")}
        return {}
