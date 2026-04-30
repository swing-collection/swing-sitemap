# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Get Cached Sitemap
==================

Retrieve a cached sitemap.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from swing.sitemap.conf import get_setting

from .get_cache import get_cache


# =============================================================================
# Functions
# =============================================================================

def get_cached_sitemap(key: str) -> bytes | None:
    """
    Retrieve a cached sitemap.

    Args:
        key: Cache key for the sitemap.

    Returns:
        Cached sitemap content as bytes, or None if not cached.
    """
    cache_config = get_setting("cache", default={}) or {}
    if not cache_config.get("enabled", False):
        return None

    cache = get_cache()
    return cache.get(key)


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_cached_sitemap"]
