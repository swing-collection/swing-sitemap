# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Caching Utilities
=================

Provides caching support for sitemap generation.

The caching layer helps reduce database load and response times for
frequently requested sitemaps.

Configuration via Django settings::

    SWING_SITEMAP = {
        "cache": {
            "enabled": True,
            "timeout": 3600,  # 1 hour
            "backend": "default",
            "key_prefix": "swing_sitemap",
        },
    }
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import gzip
import hashlib
import logging
from functools import wraps
from typing import Any, Callable

from django.core.cache import caches
from django.http import HttpRequest, HttpResponse

from swing.sitemap.conf import get_setting

logger = logging.getLogger(__name__)


# =============================================================================
# Cache Helpers
# =============================================================================


def get_cache():
    """Get the cache backend configured for sitemaps."""
    cache_config = get_setting("cache", default={}) or {}
    backend = cache_config.get("backend", "default")
    return caches[backend]


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
# Compression
# =============================================================================


def compress_content(content: bytes) -> bytes:
    """
    Compress content using gzip.

    Args:
        content: Raw content bytes.

    Returns:
        Gzip-compressed content.
    """
    return gzip.compress(content, compresslevel=9)


def decompress_content(content: bytes) -> bytes:
    """
    Decompress gzip content.

    Args:
        content: Gzip-compressed content.

    Returns:
        Decompressed content bytes.
    """
    return gzip.decompress(content)


# =============================================================================
# View Decorator
# =============================================================================


def cached_sitemap_view(
    cache_key_func: Callable[[HttpRequest], str] | None = None,
    timeout: int | None = None,
):
    """
    Decorator for caching sitemap views.

    Args:
        cache_key_func: Function that takes request and returns cache key.
            If None, uses request.path.
        timeout: Cache timeout override.

    Usage::

        @cached_sitemap_view(timeout=7200)
        def my_sitemap_view(request):
            ...
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            cache_config = get_setting("cache", default={}) or {}
            if not cache_config.get("enabled", False):
                return view_func(request, *args, **kwargs)

            # Build cache key
            if cache_key_func:
                key = make_cache_key("view", cache_key_func(request))
            else:
                key = make_cache_key("view", request.path)

            # Try cache
            cached = get_cached_sitemap(key)
            if cached is not None:
                logger.debug("Cache hit: %s", key)
                response = HttpResponse(
                    cached,
                    content_type="application/xml",
                )
                response["X-Sitemap-Cache"] = "HIT"
                return response

            # Generate response
            response = view_func(request, *args, **kwargs)

            # Cache successful responses
            if response.status_code == 200:
                content = response.content
                set_cached_sitemap(key, content, timeout)
                response["X-Sitemap-Cache"] = "MISS"

            return response

        return wrapped

    return decorator


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cached_sitemap_view",
    "compress_content",
    "decompress_content",
    "get_cache",
    "get_cached_sitemap",
    "invalidate_cache",
    "make_cache_key",
    "set_cached_sitemap",
]
