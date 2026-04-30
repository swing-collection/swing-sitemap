# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index View
==================

Thin convenience wrapper around
:func:`django.contrib.sitemaps.views.index` that auto-discovers
sitemaps via :func:`swing.sitemap.default_sitemaps` when none are
explicitly passed.

Most projects do **not** need this view directly; just register the
helper from :mod:`swing.sitemap.urls` (which uses Django's stock view).
This module exists for sites that want to mount the index at a custom
path while keeping auto-discovery.

Provides both function-based and class-based views:

- :func:`sitemap_index` - Function-based view
- :class:`SitemapIndexView` - Class-based view

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from typing import Any

from django.contrib.sitemaps.views import index as _index
from django.http import HttpRequest, HttpResponse
from django.views import View

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps


# =============================================================================
# Function-Based Views
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
# Class-Based Views
# =============================================================================


class SitemapIndexView(View):
    """
    Class-based view for rendering sitemap index XML.

    Auto-discovers sitemaps via :func:`swing.sitemap.default_sitemaps`
    when none are explicitly provided.

    Usage::

        from swing.sitemap.views import SitemapIndexView

        urlpatterns = [
            path("sitemap-index.xml", SitemapIndexView.as_view()),
        ]

    With custom sitemaps::

        urlpatterns = [
            path(
                "sitemap-index.xml",
                SitemapIndexView.as_view(sitemaps={"pages": MyPageSitemap}),
            ),
        ]

    Attributes:
        sitemaps: Optional sitemap mapping. Defaults to auto-discovery.
        sitemap_url_name: Name of the per-section URL pattern.

    """

    sitemaps: dict | None = None
    sitemap_url_name: str = "swing-sitemap-section"

    def get_sitemaps(self) -> dict:
        """Return the sitemaps mapping."""
        if self.sitemaps is not None:
            return self.sitemaps
        return default_sitemaps()

    def get_sitemap_url_name(self) -> str:
        """Return the sitemap URL name for sections."""
        return self.sitemap_url_name

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request and render the sitemap index XML."""
        return _index(
            request,
            self.get_sitemaps(),
            sitemap_url_name=self.get_sitemap_url_name(),
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "sitemap_index",
    "SitemapIndexView",
]
