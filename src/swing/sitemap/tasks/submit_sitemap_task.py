# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Submit Sitemap Task
===================

Celery task for submitting sitemap to search engines.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging

from swing.sitemap.conf import get_setting
from swing.sitemap.utils.submission import PING_ENDPOINTS, submit_sitemap

try:
    # Import | Libraries
    from celery import shared_task
except ImportError:  # pragma: no cover
    shared_task = None  # type: ignore[misc,assignment]


logger = logging.getLogger(__name__)


# =============================================================================
# Tasks
# =============================================================================


@shared_task(  # pragma: no cover
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
    default_retry_delay=60,
)
def submit_sitemap_task(  # pragma: no cover
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
            logger.warning("Sitemap submission to %s returned HTTP %d", name, status)
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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["submit_sitemap_task"]
