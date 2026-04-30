# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
News Sitemap URL Admin
======================

Admin for news sitemap URLs.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import NewsSitemapURL

from .admin_sitemap_url_base import BaseSitemapURLAdmin


# =============================================================================
# Classes
# =============================================================================

@admin.register(NewsSitemapURL)
class NewsSitemapURLAdmin(BaseSitemapURLAdmin):
    """Admin for news sitemap URLs."""

    list_display = (
        "url",
        "title",
        "publication_name",
        "publication_date",
        "lastmod",
    )
    search_fields = ("url", "title", "publication_name")
    list_filter = ("publication_language", "publication_date")
    date_hierarchy = "publication_date"

    fieldsets = (
        (None, {"fields": ("url", "title")}),
        (
            _("Publication Information"),
            {
                "fields": (
                    "publication_name",
                    "publication_language",
                    "publication_date",
                ),
            },
        ),
        (
            _("Sitemap Options"),
            {
                "fields": ("priority", "changefreq"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("lastmod",),
                "classes": ("collapse",),
            },
        ),
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = ["NewsSitemapURLAdmin"]
