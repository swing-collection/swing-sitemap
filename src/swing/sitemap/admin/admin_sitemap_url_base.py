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

# Import | Standard Library
from typing import Any, ClassVar

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# =============================================================================
# Classes
# =============================================================================


class BaseSitemapURLAdmin(admin.ModelAdmin):
    """Base admin class for sitemap URL models."""

    # NOTE: Declared as variable-length tuples (rather than the narrower
    # fixed-length tuples mypy would otherwise infer) because subclasses
    # extend these with additional model-specific fields. ClassVar matches
    # how django-stubs types these ModelAdmin attributes (list_display is
    # the one exception - django-stubs deliberately leaves it non-ClassVar).
    list_display: tuple[str, ...] = ("url", "priority", "changefreq", "lastmod")
    list_filter: ClassVar[tuple[str, ...]] = ("changefreq", "priority")
    search_fields: ClassVar[tuple[str, ...]] = ("url",)
    ordering: ClassVar[tuple[str, ...]] = ("-lastmod",)
    readonly_fields: ClassVar[tuple[str, ...]] = ("lastmod",)

    # django-stubs types `fieldsets` against a private `_FieldOpts` TypedDict
    # we can't reference directly, so this uses `Any` for the field-options
    # element rather than fighting that exact shape.
    fieldsets: ClassVar[Any] = (
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

    url_link.short_description = _("URL")  # type: ignore[attr-defined]


# =============================================================================
# Exports
# =============================================================================

__all__ = ["BaseSitemapURLAdmin"]
