# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Image URL Model
================================

Provides a sitemap URL model for image entries.

"""


# =============================================================================
# Imports
# =============================================================================

from django.db import models

from swing.sitemap.models.model_sitemap_url import URL


# =============================================================================
# Models
# =============================================================================


class ImageSitemapURL(URL):
    """Sitemap URL model for image entries."""

    image_url = models.URLField()
    image_caption = models.CharField(max_length=255, blank=True)
    image_title = models.CharField(max_length=255, blank=True)
    image_license = models.URLField(blank=True)

    def get_absolute_url(self) -> str:
        return self.url

    def __str__(self) -> str:
        return f"{self.url} - {self.image_url}"


# =============================================================================
# Exports
# =============================================================================

__all__ = ["ImageSitemapURL"]
