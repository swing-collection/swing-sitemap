# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Video Sitemap View
===================

Renders a video sitemap XML using the VideoSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import VideoSitemap


# =============================================================================
# Views
# =============================================================================


def video_sitemap(request):
    """Render the video sitemap XML."""
    sitemap = VideoSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_video.xml",
        {"urlset": urls},
        content_type="application/xml",
    )
