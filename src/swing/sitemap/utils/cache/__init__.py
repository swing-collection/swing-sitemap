# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Cache Utilities
================================

Utilities for caching sitemap content.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Local
from .get_cache import get_cache
from .get_cached_sitemap import get_cached_sitemap
from .invalidate_cache import invalidate_cache
from .make_cache_key import make_cache_key
from .set_cached_sitemap import set_cached_sitemap

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "get_cache",
    "get_cached_sitemap",
    "invalidate_cache",
    "make_cache_key",
    "set_cached_sitemap",
]
