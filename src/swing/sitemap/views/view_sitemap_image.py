# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Image Sitemap View
===================

Renders an image sitemap XML using the ImageSitemap class.

Provides both function-based and class-based views:

- :func:`image_sitemap` - Function-based view
- :class:`ImageSitemapView` - Class-based view

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from swing.sitemap.sitemaps import ImageSitemap


# =============================================================================
# Function-Based Views
# =============================================================================


def image_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the image sitemap XML."""
    sitemap = ImageSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_image.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Class-Based Views
# =============================================================================


class ImageSitemapView(View):
    """
    Class-based view for rendering image sitemap XML.

    Usage::

        from swing.sitemap.views import ImageSitemapView

        urlpatterns = [
            path("sitemap-image.xml", ImageSitemapView.as_view()),
        ]

    Attributes:
        sitemap_class: The sitemap class to use. Defaults to ImageSitemap.
        template_name: Template for rendering the sitemap XML.
        content_type: Response content type.

    """

    sitemap_class = ImageSitemap
    template_name = "sitemap_image.xml"
    content_type = "application/xml"

    def get_sitemap(self) -> ImageSitemap:
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
    "image_sitemap",
    "ImageSitemapView",
]
