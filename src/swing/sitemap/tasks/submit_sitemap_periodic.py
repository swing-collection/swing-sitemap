# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Submit Sitemap Periodic Task
============================

Periodic Celery task for sitemap submission.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging
from typing import Any

from swing.sitemap.conf import get_setting

# Import | Local
from .submit_sitemap_task import submit_sitemap_task

try:
    # Import | Libraries
    from celery import shared_task
except ImportError:  # pragma: no cover
    shared_task = None  # type: ignore[misc,assignment]


logger = logging.getLogger(__name__)


# =============================================================================
# Tasks
# =============================================================================


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
                'task': 'swing.sitemap.tasks.submit_sitemap_periodic',
                'schedule': crontab(hour=6, minute=0),
            },
        }
    """
    submit_config = get_setting("submit", default={}) or {}
    url = submit_config.get("sitemap_url")

    if not url:
        logger.warning("Periodic sitemap submission skipped: no sitemap_url configured")
        return {"sitemap_url": None, "results": {}, "skipped": True}

    results = submit_sitemap_task(url)
    return {"sitemap_url": url, "results": results, "skipped": False}


# =============================================================================
# Exports
# =============================================================================

__all__ = ["submit_sitemap_periodic"]
