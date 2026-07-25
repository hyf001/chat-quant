from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoredArtifactFile:
    storage_uri: str
    size_bytes: int


class FilesystemArtifactStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write_package(
        self,
        root_path: str,
        files: list[tuple[str, bytes]],
    ) -> list[StoredArtifactFile]:
        stored: list[StoredArtifactFile] = []
        package_root = self.absolute_root_path(root_path)
        package_root.mkdir(parents=True, exist_ok=True)
        for relative_path, content in files:
            destination = self._safe_destination(package_root, relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            stored.append(
                StoredArtifactFile(
                    storage_uri=self._storage_uri(root_path, relative_path),
                    size_bytes=len(content),
                )
            )
        return stored

    def copy_files(
        self,
        root_path: str,
        source_base_dir: Path,
        files: list[tuple[str, str]],
    ) -> list[StoredArtifactFile]:
        stored: list[StoredArtifactFile] = []
        package_root = self.absolute_root_path(root_path)
        source_root = source_base_dir.resolve()
        package_root.mkdir(parents=True, exist_ok=True)
        for source_path, relative_path in files:
            source = (source_root / source_path).resolve()
            destination = self._safe_destination(package_root, relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            stored.append(
                StoredArtifactFile(
                    storage_uri=self._storage_uri(root_path, relative_path),
                    size_bytes=destination.stat().st_size,
                )
            )
        return stored

    def absolute_root_path(self, root_path: str) -> Path:
        return self._safe_destination(self.root, root_path)

    def absolute_path(self, storage_uri: str) -> Path:
        prefix = "file://"
        path = storage_uri[len(prefix) :] if storage_uri.startswith(prefix) else storage_uri
        return self._safe_destination(self.root, path)

    def _storage_uri(self, root_path: str, relative_path: str) -> str:
        return f"file://{root_path.rstrip('/')}/{relative_path.lstrip('/')}"

    @staticmethod
    def _safe_destination(root: Path, relative_path: str) -> Path:
        resolved_root = root.resolve()
        destination = (resolved_root / relative_path).resolve()
        if not destination.is_relative_to(resolved_root):
            raise ValueError("artifact path escapes storage root")
        return destination
