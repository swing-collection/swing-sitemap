# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Custom URL Model
=================================

Provides a flexible sitemap URL model for custom entries.

"""


# =============================================================================
# Imports
# =============================================================================

from django.db import models

from swing.sitemap.models.model_sitemap_url import URL


# =============================================================================
# Models
# =============================================================================


class CustomSitemapURL(URL):
    """Flexible sitemap URL model for custom entries."""

    custom_field = models.CharField(max_length=255)
    custom_data = models.JSONField(default=dict)

    def get_absolute_url(self) -> str:
        return self.url

    def __str__(self) -> str:
        return f"{self.url} - {self.custom_field}"


# =============================================================================
# Exports
# =============================================================================

__all__ = ["CustomSitemapURL"]
