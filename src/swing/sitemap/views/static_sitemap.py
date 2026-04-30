# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Static Sitemap Function-Based View
===================================

Renders a static sitemap XML using the StaticSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import StaticSitemap

# =============================================================================
# Functions
# =============================================================================


def static_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the static sitemap XML."""
    sitemap = StaticSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_static.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["static_sitemap"]
