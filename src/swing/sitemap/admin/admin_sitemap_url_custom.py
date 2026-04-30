# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Custom Sitemap URL Admin
========================

Admin for custom sitemap URLs with JSON data.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import CustomSitemapURL

# Import | Local
from .admin_sitemap_url_base import BaseSitemapURLAdmin

# =============================================================================
# Classes
# =============================================================================


@admin.register(CustomSitemapURL)
class CustomSitemapURLAdmin(BaseSitemapURLAdmin):
    """Admin for custom sitemap URLs with JSON data."""

    list_display = ("url", "custom_field", "priority", "changefreq", "lastmod")
    search_fields = ("url", "custom_field")

    fieldsets = (
        (None, {"fields": ("url",)}),
        (
            _("Custom Data"),
            {
                "fields": ("custom_field", "custom_data"),
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

__all__ = ["CustomSitemapURLAdmin"]
