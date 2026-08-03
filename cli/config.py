from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api"


@dataclass(frozen=True)
class CliConfig:
    api_base_url: str = DEFAULT_API_BASE_URL


def get_config() -> CliConfig:
    return CliConfig(
        api_base_url=os.environ.get("CHATQ_API_BASE_URL", DEFAULT_API_BASE_URL),
    )
