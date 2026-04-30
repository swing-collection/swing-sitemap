# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
News Sitemap View
==================

Renders a news sitemap XML using the NewsSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import NewsSitemap


# =============================================================================
# Views
# =============================================================================


def news_sitemap(request):
    """Render the news sitemap XML."""
    sitemap = NewsSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "sitemap_news.xml",
        {"urlset": urls},
        content_type="application/xml",
    )
