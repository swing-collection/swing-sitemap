# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Generator
==========================

Provides views for generating sitemap XML responses.

"""


# =============================================================================
# Imports
# =============================================================================

from django.http import HttpResponse
from django.template import loader


# =============================================================================
# Views
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
