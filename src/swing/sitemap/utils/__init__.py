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

from .cached_sitemap_view import cached_sitemap_view
from .compress_content import compress_content
from .decompress_content import decompress_content
from .get_cache import get_cache
from .get_cached_sitemap import get_cached_sitemap
from .invalidate_cache import invalidate_cache
from .make_cache_key import make_cache_key
from .set_cached_sitemap import set_cached_sitemap
from .util_submit_sitemap import PING_ENDPOINTS, submit_sitemap


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
