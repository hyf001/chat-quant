from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MINDGO_STORAGE_ROOT = Path("data") / "mindgo" / "parquet"
DEFAULT_MINDGO_PARTITION_FILENAME = "data.parquet"


@dataclass(frozen=True)
class MindgoDatasetStorage:
    storage_root: Path

    def __init__(self, storage_root: Path | str = DEFAULT_MINDGO_STORAGE_ROOT) -> None:
        object.__setattr__(self, "storage_root", Path(storage_root).expanduser())

    def dataset_root(self, dataset_id: str) -> Path:
        return self.storage_root / _safe_path_segment(dataset_id)

    def partition_path(
        self,
        dataset_id: str,
        partition_values: Mapping[str, str],
        *,
        filename: str = DEFAULT_MINDGO_PARTITION_FILENAME,
    ) -> Path:
        path = self.dataset_root(dataset_id)
        for key, value in partition_values.items():
            path /= f"{_safe_path_segment(key)}={_safe_path_segment(value)}"
        return path / _safe_path_segment(filename)

def mindgo_dataset_partition_path(
    storage_root: Path | str,
    dataset_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    return MindgoDatasetStorage(storage_root).partition_path(dataset_id, partition_values)


def _safe_path_segment(value: str) -> str:
    text = str(value)
    if not text or "/" in text or "\\" in text or text in {".", ".."}:
        raise ValueError(f"invalid MindGo storage path segment: {text!r}")
    return text
