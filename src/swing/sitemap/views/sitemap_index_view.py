# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index Class-Based View
===============================

Class-based view for rendering sitemap index XML.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

from django.contrib.sitemaps.views import index as _index
from django.http import HttpRequest, HttpResponse
from django.views import View

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps

# =============================================================================
# Classes
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

__all__ = ["SitemapIndexView"]
