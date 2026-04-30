# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Base URL Model
==============================

Provides base models for sitemap URL entries.

"""


# =============================================================================
# Imports
# =============================================================================

from django.db import models


# =============================================================================
# Models
# =============================================================================


class SitemapURL(models.Model):
    """
    Simple sitemap URL model.

    Stores URL entries for sitemap generation.
    """

    url = models.URLField()
    priority = models.FloatField(default=0.5)
    changefreq = models.CharField(
        max_length=10,
        choices=[
            ("always", "Always"),
            ("hourly", "Hourly"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
            ("never", "Never"),
        ],
    )
    lastmod = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.url)


class URL(models.Model):
    """
    Abstract base model for sitemap URLs.

    Provides common fields for all URL types.
    """

    url = models.URLField()
    priority = models.FloatField(default=0.5)
    changefreq = models.CharField(
        max_length=10,
        choices=[
            ("always", "Always"),
            ("hourly", "Hourly"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
            ("never", "Never"),
        ],
    )
    lastmod = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.url)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "SitemapURL",
    "URL",
]
