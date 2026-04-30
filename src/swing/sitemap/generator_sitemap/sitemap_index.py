# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index Generator
=======================

Generate sitemap index XML responses.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpResponse
from django.template import loader


# =============================================================================
# Functions
# =============================================================================

def sitemap_index(request):
    """Generate a sitemap index XML response."""
    sitemaps = [
        "sitemap.xml",
        "image_sitemap.xml",
        "video_sitemap.xml",
        "news_sitemap.xml",
    ]
    template = loader.get_template("swing_sitemap/sitemap_index.xml")
    context = {"sitemaps": sitemaps}
    return HttpResponse(template.render(context), content_type="application/xml")


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_index"]
