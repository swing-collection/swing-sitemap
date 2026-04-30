# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Image Sitemap URL Admin
=======================

Admin for image sitemap URLs.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import ImageSitemapURL

# Import | Local
from .admin_sitemap_url_base import BaseSitemapURLAdmin

# =============================================================================
# Classes
# =============================================================================


@admin.register(ImageSitemapURL)
class ImageSitemapURLAdmin(BaseSitemapURLAdmin):
    """Admin for image sitemap URLs."""

    list_display = ("url", "image_url", "image_title", "priority", "lastmod")
    search_fields = ("url", "image_url", "image_title", "image_caption")

    fieldsets = (
        (None, {"fields": ("url",)}),
        (
            _("Image Information"),
            {
                "fields": (
                    "image_url",
                    "image_title",
                    "image_caption",
                    "image_license",
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

__all__ = ["ImageSitemapURLAdmin"]
