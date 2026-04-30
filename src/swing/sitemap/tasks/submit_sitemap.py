# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Celery Tasks for Sitemap Submission
===================================

Provides Celery tasks for automated sitemap submission to search engines.

Tasks:
- :func:`submit_sitemap_task` - Submit sitemap to search engines
- :func:`submit_sitemap_periodic` - Periodic submission task

Configuration via Django settings::

    SWING_SITEMAP = {
        "submit": {
            "sitemap_url": "https://example.com/sitemap.xml",
            "endpoints": {
                "google": "https://www.google.com/ping?sitemap={url}",
                "bing": "https://www.bing.com/ping?sitemap={url}",
            },
            "timeout": 10.0,
            "retry_delay": 60,
            "max_retries": 3,
        },
    }

Usage::

    from swing.sitemap.tasks import submit_sitemap_task

    # Submit immediately
    submit_sitemap_task.delay("https://example.com/sitemap.xml")

    # Or schedule periodic submission via Celery Beat
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import logging
from typing import Any

try:
    from celery import shared_task
except ImportError:  # pragma: no cover
    shared_task = None  # type: ignore[misc,assignment]

from swing.sitemap.conf import get_setting
from swing.sitemap.utils.util_submit_sitemap import PING_ENDPOINTS, submit_sitemap

logger = logging.getLogger(__name__)


# =============================================================================
# Tasks
# =============================================================================


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
    default_retry_delay=60,
)
def submit_sitemap_task(
    self,
    sitemap_url: str | None = None,
    endpoints: dict[str, str] | None = None,
    timeout: float | None = None,
) -> dict[str, int | None]:
    """
    Submit a sitemap to search engine ping endpoints.

    Args:
        sitemap_url: Absolute URL of the sitemap. Falls back to
            ``SWING_SITEMAP['submit']['sitemap_url']`` if not provided.
        endpoints: Mapping of endpoint names to URL templates. Falls back
            to ``SWING_SITEMAP['submit']['endpoints']`` or built-in defaults.
        timeout: Request timeout in seconds. Falls back to
            ``SWING_SITEMAP['submit']['timeout']`` or 10.0.

    Returns:
        Mapping of endpoint name to HTTP status code (or None on failure).

    Raises:
        ValueError: If no sitemap_url is provided or configured.
    """
    # Get configuration
    submit_config = get_setting("submit", default={}) or {}

    url = sitemap_url or submit_config.get("sitemap_url")
    if not url:
        raise ValueError(
            "sitemap_url must be provided or configured in "
            "SWING_SITEMAP['submit']['sitemap_url']"
        )

    eps = endpoints or submit_config.get("endpoints") or dict(PING_ENDPOINTS)
    to = timeout or submit_config.get("timeout", 10.0)

    logger.info("Submitting sitemap %s to %d endpoints", url, len(eps))

    results = submit_sitemap(url, endpoints=eps, timeout=to)

    # Log results
    for name, status in results.items():
        if status is None:
            logger.warning("Sitemap submission to %s failed", name)
        elif status >= 400:
            logger.warning(
                "Sitemap submission to %s returned HTTP %d", name, status
            )
        else:
            logger.info("Sitemap submitted to %s: HTTP %d", name, status)

    # Check for failures that should trigger retry
    failures = [n for n, s in results.items() if s is None or (s and s >= 500)]
    if failures and self.request.retries < self.max_retries:
        logger.info(
            "Retrying failed endpoints: %s (attempt %d/%d)",
            failures,
            self.request.retries + 1,
            self.max_retries,
        )
        # Let Celery's autoretry handle it
        # Only raise if all endpoints failed
        if len(failures) == len(results):
            raise RuntimeError(f"All sitemap submissions failed: {failures}")

    return results


@shared_task(bind=True)
def submit_sitemap_periodic(self) -> dict[str, Any]:
    """
    Periodic task for sitemap submission.

    Designed to be called by Celery Beat. Uses configuration from
    ``SWING_SITEMAP['submit']``.

    Returns:
        Dict with 'sitemap_url' and 'results' keys.

    Example Celery Beat config::

        CELERY_BEAT_SCHEDULE = {
            'submit-sitemap-daily': {
                'task': 'swing.sitemap.tasks.submit_sitemap.submit_sitemap_periodic',
                'schedule': crontab(hour=6, minute=0),
            },
        }
    """
    submit_config = get_setting("submit", default={}) or {}
    url = submit_config.get("sitemap_url")

    if not url:
        logger.warning(
            "Periodic sitemap submission skipped: no sitemap_url configured"
        )
        return {"sitemap_url": None, "results": {}, "skipped": True}

    results = submit_sitemap_task(url)
    return {"sitemap_url": url, "results": results, "skipped": False}


@shared_task(bind=True)
def invalidate_sitemap_cache(self, cache_key: str | None = None) -> bool:
    """
    Invalidate cached sitemap data.

    Args:
        cache_key: Specific cache key to invalidate. If None, clears all
            sitemap-related cache entries.

    Returns:
        True if cache was invalidated successfully.
    """
    from django.core.cache import cache

    cache_config = get_setting("cache", default={}) or {}
    prefix = cache_config.get("key_prefix", "swing_sitemap")

    if cache_key:
        full_key = f"{prefix}:{cache_key}"
        cache.delete(full_key)
        logger.info("Invalidated sitemap cache key: %s", full_key)
    else:
        # Clear all sitemap cache keys
        # Note: This requires cache backend that supports delete_pattern
        # For other backends, we track keys separately
        try:
            cache.delete_pattern(f"{prefix}:*")
            logger.info("Invalidated all sitemap cache entries")
        except AttributeError:
            # Fallback for backends without delete_pattern
            logger.warning(
                "Cache backend doesn't support delete_pattern. "
                "Consider using Redis or Memcached."
            )
            return False

    return True


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "invalidate_sitemap_cache",
    "submit_sitemap_periodic",
    "submit_sitemap_task",
]
