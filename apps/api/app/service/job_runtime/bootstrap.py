"""Job runtime bootstrap helpers."""
from __future__ import annotations

from .registry import JobRuntimeRegistry, job_runtime_registry


def register_default_job_runtime_events(
    registry: JobRuntimeRegistry | None = None,
) -> JobRuntimeRegistry:
    """Return the registry after job runtime defaults are available."""
    registry = registry or job_runtime_registry
    from app.service.mindgo.stock_a_adjust_factor.job import (
        register_stock_a_adjust_factor_job_runtime_handlers,
    )
    from app.service.mindgo.stock_a_daily_price.job import (
        register_stock_a_daily_price_job_runtime_handlers,
    )

    register_stock_a_adjust_factor_job_runtime_handlers(registry)
    register_stock_a_daily_price_job_runtime_handlers(registry)
    return registry


def register_default_job_runtime_adapters(
    registry: JobRuntimeRegistry | None = None,
) -> JobRuntimeRegistry:
    """Compatibility alias kept while callers migrate to event registration."""
    return register_default_job_runtime_events(registry)
