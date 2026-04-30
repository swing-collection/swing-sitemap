# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Video Sitemap URL Admin
=======================

Admin for video sitemap URLs.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import VideoSitemapURL

# Import | Local
from .admin_sitemap_url_base import BaseSitemapURLAdmin

# =============================================================================
# Classes
# =============================================================================


@admin.register(VideoSitemapURL)
class VideoSitemapURLAdmin(BaseSitemapURLAdmin):
    """Admin for video sitemap URLs."""

    list_display = (
        "url",
        "video_title",
        "video_duration_display",
        "priority",
        "lastmod",
    )
    search_fields = ("url", "video_title", "video_description")
    list_filter = ("changefreq", "priority", "video_publication_date")

    fieldsets = (
        (None, {"fields": ("url",)}),
        (
            _("Video Information"),
            {
                "fields": (
                    "video_title",
                    "video_description",
                    "video_thumbnail_url",
                    "video_content_url",
                ),
            },
        ),
        (
            _("Video Metadata"),
            {
                "fields": (
                    "video_duration",
                    "video_publication_date",
                    "video_expiration_date",
                ),
                "classes": ("collapse",),
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

    def video_duration_display(self, obj):
        """Display video duration in human-readable format."""
        if obj.video_duration:
            minutes, seconds = divmod(obj.video_duration, 60)
            hours, minutes = divmod(minutes, 60)
            if hours:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes:
                return f"{minutes}m {seconds}s"
            return f"{seconds}s"
        return "-"

    video_duration_display.short_description = _("Duration")


# =============================================================================
# Exports
# =============================================================================

__all__ = ["VideoSitemapURLAdmin"]
