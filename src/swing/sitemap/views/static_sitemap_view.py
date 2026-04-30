# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Static Sitemap Class-Based View
================================

Class-based view for rendering static sitemap XML.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from swing.sitemap.sitemaps import StaticSitemap

# =============================================================================
# Classes
# =============================================================================


class StaticSitemapView(View):
    """
    Class-based view for rendering static sitemap XML.

    Usage::

        from swing.sitemap.views import StaticSitemapView

        urlpatterns = [
            path("sitemap-static.xml", StaticSitemapView.as_view()),
        ]

    Attributes:
        sitemap_class: The sitemap class to use. Defaults to StaticSitemap.
        template_name: Template for rendering the sitemap XML.
        content_type: Response content type.

    """

    sitemap_class = StaticSitemap
    template_name = "swing/sitemap/sitemap_static.xml"
    content_type = "application/xml"

    def get_sitemap(self) -> StaticSitemap:
        """Return the sitemap instance."""
        return self.sitemap_class()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle GET request and render the sitemap XML."""
        sitemap = self.get_sitemap()
        urls = sitemap.get_urls()
        return render(
            request,
            self.template_name,
            {"urlset": urls},
            content_type=self.content_type,
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["StaticSitemapView"]
