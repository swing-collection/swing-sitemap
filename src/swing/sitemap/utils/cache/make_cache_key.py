# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Make Cache Key
==============

Build a cache key from prefix and parts.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import hashlib

from swing.sitemap.conf import get_setting


# =============================================================================
# Functions
# =============================================================================

def make_cache_key(prefix: str, *parts: str) -> str:
    """
    Build a cache key from prefix and parts.

    Args:
        prefix: Cache key prefix (usually from settings).
        *parts: Additional parts to include in the key.

    Returns:
        A sanitized cache key string.
    """
    cache_config = get_setting("cache", default={}) or {}
    key_prefix = cache_config.get("key_prefix", "swing_sitemap")

    # Build the key
    key_parts = [key_prefix, prefix] + list(parts)
    raw_key = ":".join(str(p) for p in key_parts if p)

    # Ensure key is safe for all cache backends
    if len(raw_key) > 250:
        # Hash long keys
        hash_part = hashlib.md5(raw_key.encode()).hexdigest()[:16]
        raw_key = f"{key_prefix}:{prefix}:{hash_part}"

    return raw_key


# =============================================================================
# Exports
# =============================================================================

__all__ = ["make_cache_key"]
