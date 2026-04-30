# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cached Sitemap View
===================

Decorator for caching sitemap views.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from functools import wraps
import logging
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse

from swing.sitemap.conf import get_setting
from swing.sitemap.utils.cache.get_cached_sitemap import get_cached_sitemap
from swing.sitemap.utils.cache.make_cache_key import make_cache_key
from swing.sitemap.utils.cache.set_cached_sitemap import set_cached_sitemap

logger = logging.getLogger(__name__)


# =============================================================================
# Functions
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
# Exports
# =============================================================================

__all__ = ["cached_sitemap_view"]
