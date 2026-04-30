# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Image Sitemap Function-Based View
==================================

Renders an image sitemap XML using the ImageSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import ImageSitemap

# =============================================================================
# Functions
# =============================================================================


def image_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the image sitemap XML."""
    sitemap = ImageSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "swing/sitemap/sitemap_image.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["image_sitemap"]
