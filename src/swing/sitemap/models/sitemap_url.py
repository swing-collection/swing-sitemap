# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap URL Model
=================

Simple sitemap URL model.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["SitemapURL"]
