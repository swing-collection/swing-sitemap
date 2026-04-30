# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Static Sitemap View
====================

Renders a static sitemap XML using the StaticSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import StaticSitemap


# =============================================================================
# Views
# =============================================================================


def static_sitemap(request):
    """Render the static sitemap XML."""
    sitemap = StaticSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_static.xml",
        {"urlset": urls},
        content_type="application/xml",
    )
