# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Invalidate Cache
================

Invalidate cached sitemaps.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging

from swing.sitemap.conf import get_setting

# Import | Local
from .get_cache import get_cache

logger = logging.getLogger(__name__)


# =============================================================================
# Functions
# =============================================================================


def invalidate_cache(pattern: str | None = None) -> int:
    """
    Invalidate cached sitemaps.

    Args:
        pattern: Optional pattern to match cache keys. If None, clears
            all sitemap cache entries.

    Returns:
        Number of keys invalidated (if supported by backend).
    """
    cache_config = get_setting("cache", default={}) or {}
    if not cache_config.get("enabled", False):
        return 0

    cache = get_cache()
    key_prefix = cache_config.get("key_prefix", "swing_sitemap")

    if pattern:
        full_pattern = f"{key_prefix}:{pattern}"
    else:
        full_pattern = f"{key_prefix}:*"

    try:
        # Redis-style pattern delete
        count = cache.delete_pattern(full_pattern)
        logger.info("Invalidated %d cached sitemap entries", count or 0)
        return count or 0
    except AttributeError:
        # Fallback: just log a warning
        logger.warning(
            "Cache backend doesn't support delete_pattern. "
            "Consider using Redis for better cache management."
        )
        return 0


# =============================================================================
# Exports
# =============================================================================

__all__ = ["invalidate_cache"]
