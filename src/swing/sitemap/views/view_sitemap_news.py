# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
News Sitemap View
==================

Renders a news sitemap XML using the NewsSitemap class.

Provides both function-based and class-based views:

- :func:`news_sitemap` - Function-based view
- :class:`NewsSitemapView` - Class-based view

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from swing.sitemap.sitemaps import NewsSitemap


# =============================================================================
# Function-Based Views
# =============================================================================


def news_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the news sitemap XML."""
    sitemap = NewsSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_news.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Class-Based Views
# =============================================================================


class NewsSitemapView(View):
    """
    Class-based view for rendering news sitemap XML.

    Usage::

        from swing.sitemap.views import NewsSitemapView

        urlpatterns = [
            path("sitemap-news.xml", NewsSitemapView.as_view()),
        ]

    Attributes:
        sitemap_class: The sitemap class to use. Defaults to NewsSitemap.
        template_name: Template for rendering the sitemap XML.
        content_type: Response content type.

    """

    sitemap_class = NewsSitemap
    template_name = "sitemap_news.xml"
    content_type = "application/xml"

    def get_sitemap(self) -> NewsSitemap:
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

__all__ = [
    "news_sitemap",
    "NewsSitemapView",
]
