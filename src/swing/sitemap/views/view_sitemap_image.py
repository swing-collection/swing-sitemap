# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Image Sitemap View
===================

Renders an image sitemap XML using the ImageSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import ImageSitemap


# =============================================================================
# Views
# =============================================================================


def image_sitemap(request):
    """Render the image sitemap XML."""
    sitemap = ImageSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_image.xml",
        {"urlset": urls},
        content_type="application/xml",
    )
