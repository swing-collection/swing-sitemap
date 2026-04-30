# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index View
==================

Thin convenience wrapper around
:func:`django.contrib.sitemaps.views.index` that auto-discovers
sitemaps via :func:`swing_sitemap.default_sitemaps` when none are
explicitly passed.

Most projects do **not** need this view directly; just register the
helper from :mod:`swing_sitemap.urls` (which uses Django's stock view).
This module exists for sites that want to mount the index at a custom
path while keeping auto-discovery.
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.contrib.sitemaps.views import index as _index
from django.http import HttpRequest, HttpResponse

from swing_sitemap.sitemaps.sitemap_defaults import default_sitemaps


# =============================================================================
# Views
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
            :func:`swing_sitemap.default_sitemaps`.
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


__all__ = ["sitemap_index"]
