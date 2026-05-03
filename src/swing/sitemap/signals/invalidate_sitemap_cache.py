# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Invalidate Sitemap Cache
========================

Invalidate sitemap cache entries.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging

from django.core.cache import cache

from swing.sitemap.conf import get_setting

logger = logging.getLogger(__name__)


# =============================================================================
# Functions
# =============================================================================


def invalidate_sitemap_cache(model_label: str | None = None) -> None:
    """
    Invalidate sitemap cache entries.

    Args:
        model_label: Optional model label (e.g. 'myapp.Article') to
            invalidate only that model's cache entries. If None,
            invalidates all sitemap caches.
    """
    cache_config = get_setting("cache", default={}) or {}
    prefix = cache_config.get("key_prefix", "swing_sitemap")

    if model_label:
        cache_key = f"{prefix}:{model_label.replace('.', '_')}"
        cache.delete(cache_key)
        logger.debug("Invalidated sitemap cache for %s", model_label)
    else:  # pragma: no cover
        # Try to clear all sitemap cache keys
        try:
            cache.delete_pattern(f"{prefix}:*")  # type: ignore[attr-defined]
            logger.debug("Invalidated all sitemap cache entries")
        except AttributeError:
            # Fallback: clear known cache keys
            logger.debug("Cache backend doesn't support delete_pattern")

    # Also invalidate the main sitemap cache
    cache.delete(f"{prefix}:sitemap")
    cache.delete(f"{prefix}:sitemap_index")


# =============================================================================
# Exports
# =============================================================================

__all__ = ["invalidate_sitemap_cache"]
