# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - News URL Model
===============================

Provides a sitemap URL model for news entries.

"""


# =============================================================================
# Imports
# =============================================================================

from django.db import models

from swing.sitemap.models.url import URL

# =============================================================================
# Models
# =============================================================================


class NewsSitemapURL(URL):
    """Sitemap URL model for news entries."""

    publication_name = models.CharField(max_length=255)
    publication_language = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    publication_date = models.DateTimeField()

    def get_absolute_url(self) -> str:
        return self.url

    def __str__(self) -> str:
        return f"{self.title} - {self.publication_name}"


# =============================================================================
# Exports
# =============================================================================

__all__ = ["NewsSitemapURL"]
