# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Video Sitemap Class-Based View
===============================

Class-based view for rendering video sitemap XML.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from swing.sitemap.sitemaps import VideoSitemap

# =============================================================================
# Classes
# =============================================================================


class VideoSitemapView(View):
    """
    Class-based view for rendering video sitemap XML.

    Usage::

        from swing.sitemap.views import VideoSitemapView

        urlpatterns = [
            path("sitemap-video.xml", VideoSitemapView.as_view()),
        ]

    Attributes:
        sitemap_class: The sitemap class to use. Defaults to VideoSitemap.
        template_name: Template for rendering the sitemap XML.
        content_type: Response content type.

    """

    sitemap_class = VideoSitemap
    template_name = "swing/sitemap/sitemap_video.xml"
    content_type = "application/xml"

    def get_sitemap(self) -> VideoSitemap:
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

__all__ = ["VideoSitemapView"]
