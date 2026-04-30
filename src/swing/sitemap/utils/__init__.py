# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Utilities Module
=================================

Utility helpers for sitemap generation and caching.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from swing.sitemap.utils.util_cache import (
    cached_sitemap_view,
    compress_content,
    decompress_content,
    get_cache,
    get_cached_sitemap,
    invalidate_cache,
    make_cache_key,
    set_cached_sitemap,
)
from swing.sitemap.utils.util_submit_sitemap import PING_ENDPOINTS, submit_sitemap


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "PING_ENDPOINTS",
    "cached_sitemap_view",
    "compress_content",
    "decompress_content",
    "get_cache",
    "get_cached_sitemap",
    "invalidate_cache",
    "make_cache_key",
    "set_cached_sitemap",
    "submit_sitemap",
]
