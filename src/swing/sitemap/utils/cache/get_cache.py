# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Get Cache
=========

Get the cache backend configured for sitemaps.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.core.cache import caches

from swing.sitemap.conf import get_setting

# =============================================================================
# Functions
# =============================================================================


def get_cache():
    """Get the cache backend configured for sitemaps."""
    cache_config = get_setting("cache", default={}) or {}
    backend = cache_config.get("backend", "default")
    return caches[backend]


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_cache"]
