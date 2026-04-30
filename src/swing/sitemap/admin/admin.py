# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Admin Registration for Sitemap Models
=====================================

Provides Django admin interfaces for managing sitemap URL entries.

These admin classes are optional - the main swing.sitemap functionality
is settings-driven and doesn't require database models.

To enable admin, add this to your INSTALLED_APPS and the models will
be automatically registered.
"""

# =============================================================================
# Imports
# =============================================================================

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from swing.sitemap.models import (
    CustomSitemapURL,
    ImageSitemapURL,
    NewsSitemapURL,
    StandardSitemapURL,
    VideoSitemapURL,
)


# =============================================================================
# Base Admin
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

    def url_link(self, obj):
        """Display URL as clickable link."""
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)

    url_link.short_description = _("URL")


# =============================================================================
# Model-Specific Admins
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
                "fields": ("image_url", "image_title", "image_caption", "image_license"),
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
# Module Exports
# =============================================================================

__all__ = [
    "BaseSitemapURLAdmin",
    "CustomSitemapURLAdmin",
    "ImageSitemapURLAdmin",
    "NewsSitemapURLAdmin",
    "StandardSitemapURLAdmin",
    "VideoSitemapURLAdmin",
]
