# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Standard Sitemap URL Admin
==========================

Admin for standard sitemap URLs.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import StandardSitemapURL

# Import | Local
from .admin_sitemap_url_base import BaseSitemapURLAdmin

# =============================================================================
# Classes
# =============================================================================


@admin.register(StandardSitemapURL)
class StandardSitemapURLAdmin(BaseSitemapURLAdmin):
    """Admin for standard sitemap URLs."""

    list_display = ("url", "name", "priority", "changefreq", "lastmod")
    search_fields = ("url", "name", "description")

    fieldsets = (
        (None, {"fields": ("url", "name", "description")}),
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

__all__ = ["StandardSitemapURLAdmin"]
