# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Invalidate Sitemap Cache Task
=============================

Celery task for invalidating sitemap cache.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import logging

from celery import shared_task

from swing.sitemap.conf import get_setting

logger = logging.getLogger(__name__)


# =============================================================================
# Tasks
# =============================================================================

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
# Exports
# =============================================================================

__all__ = ["invalidate_sitemap_cache"]
