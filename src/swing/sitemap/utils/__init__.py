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

# Import | Future
from __future__ import annotations

# Import | Local
from .cache import (
    get_cache,
    get_cached_sitemap,
    invalidate_cache,
    make_cache_key,
    set_cached_sitemap,
)
from .compression import compress_content, decompress_content
from .submission import PING_ENDPOINTS, submit_sitemap

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "PING_ENDPOINTS",
    "compress_content",
    "decompress_content",
    "get_cache",
    "get_cached_sitemap",
    "invalidate_cache",
    "make_cache_key",
    "set_cached_sitemap",
    "submit_sitemap",
]
