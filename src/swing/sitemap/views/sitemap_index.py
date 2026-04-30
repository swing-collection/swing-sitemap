# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index Function-Based View
==================================

Renders the sitemap index XML.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.contrib.sitemaps.views import index as _index
from django.http import HttpRequest, HttpResponse

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps


# =============================================================================
# Functions
# =============================================================================

def sitemap_index(
    request: HttpRequest,
    sitemaps: dict | None = None,
    *,
    sitemap_url_name: str = "swing-sitemap-section",
    **kwargs,
) -> HttpResponse:
    """
    Render the sitemap index XML.

    Args:
        request: Incoming HTTP request.
        sitemaps: Optional sitemap mapping. Defaults to
            :func:`swing.sitemap.default_sitemaps`.
        sitemap_url_name: Name of the per-section URL pattern that
            Django will reverse to populate the index.
        **kwargs: Forwarded to ``django.contrib.sitemaps.views.index``.
    """
    return _index(
        request,
        sitemaps if sitemaps is not None else default_sitemaps(),
        sitemap_url_name=sitemap_url_name,
        **kwargs,
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_index"]
