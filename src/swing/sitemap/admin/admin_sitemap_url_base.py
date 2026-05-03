# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Base Sitemap URL Admin
======================

Base admin class for sitemap URL models.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# =============================================================================
# Classes
# =============================================================================


class BaseSitemapURLAdmin(admin.ModelAdmin):
    """Base admin class for sitemap URL models."""

    list_display = ("url", "priority", "changefreq", "lastmod")
    list_filter = ("changefreq", "priority")
    search_fields = ("url",)
    ordering = ("-lastmod",)
    readonly_fields = ("lastmod",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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

    def url_link(self, obj):  # pragma: no cover
        """Display URL as clickable link."""
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)

    url_link.short_description = _("URL")


# =============================================================================
# Exports
# =============================================================================

__all__ = ["BaseSitemapURLAdmin"]
