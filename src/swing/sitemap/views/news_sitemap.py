# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
News Sitemap Function-Based View
=================================

Renders a news sitemap XML using the NewsSitemap class.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from swing.sitemap.sitemaps import NewsSitemap

# =============================================================================
# Functions
# =============================================================================


def news_sitemap(request: HttpRequest) -> HttpResponse:
    """Render the news sitemap XML."""
    sitemap = NewsSitemap()
    urls = sitemap.get_urls()
    return render(
        request,
        "swing/sitemap/sitemap_news.xml",
        {"urlset": urls},
        content_type="application/xml",
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["news_sitemap"]
