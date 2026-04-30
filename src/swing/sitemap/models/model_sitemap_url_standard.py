# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Standard URL Model
===================================

Provides a standard sitemap URL model with name and description.

"""


# =============================================================================
# Imports
# =============================================================================

from django.db import models

from swing.sitemap.models.url import URL

# =============================================================================
# Models
# =============================================================================


class StandardSitemapURL(URL):
    """Standard sitemap URL with name and description."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def get_absolute_url(self) -> str:
        return self.url


# =============================================================================
# Exports
# =============================================================================

__all__ = ["StandardSitemapURL"]
