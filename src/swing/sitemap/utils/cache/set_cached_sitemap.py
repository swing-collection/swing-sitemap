# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Set Cached Sitemap
==================

Cache sitemap content.

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


def set_cached_sitemap(key: str, content: bytes, timeout: int | None = None) -> None:
    """
    Cache sitemap content.

    Args:
        key: Cache key for the sitemap.
        content: Sitemap content as bytes.
        timeout: Cache timeout in seconds. Uses default if not provided.
    """
    cache_config = get_setting("cache", default={}) or {}
    if not cache_config.get("enabled", False):
        return

    cache = get_cache()
    cache_timeout = timeout or cache_config.get("timeout", 3600)
    cache.set(key, content, cache_timeout)
    logger.debug("Cached sitemap: %s (timeout: %ds)", key, cache_timeout)


# =============================================================================
# Exports
# =============================================================================

__all__ = ["set_cached_sitemap"]
