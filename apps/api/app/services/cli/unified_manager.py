"""
Unified CLI facade

This module re-exports the public API for backward compatibility.
Implementations live in:
- Base/Utils: app/services/cli/base.py
- Providers: app/services/cli/adapters/*.py
- Manager: app/services/cli/manager.py
"""

from .base import BaseCLI, MODEL_MAPPING, get_project_root, get_display_path
from .manager import UnifiedSessionManager

__all__ = [
    "BaseCLI",
    "MODEL_MAPPING",
    "get_project_root",
    "get_display_path",
    "UnifiedSessionManager",
]
