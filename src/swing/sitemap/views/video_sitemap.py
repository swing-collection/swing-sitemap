# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Video Sitemap Function-Based View
==================================

Renders a video sitemap XML using the VideoSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import VideoSitemap

# =============================================================================
# Functions
# =============================================================================


def video_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the video sitemap XML."""
    sitemap = VideoSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "swing/sitemap/sitemap_video.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["video_sitemap"]
