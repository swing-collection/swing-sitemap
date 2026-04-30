# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Paginated Sitemap
=================

Sitemap wrapper with pagination support.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from django.contrib.sitemaps import Sitemap

from .get_pagination_config import get_pagination_config


# =============================================================================
# Classes
# =============================================================================

class PaginatedSitemap(Sitemap):
    """
    A sitemap wrapper that provides pagination support.

    Wraps an existing sitemap and returns only items for a specific page.
    """

    def __init__(
        self,
        source_sitemap: Sitemap,
        page: int,
        items_per_page: int | None = None,
    ) -> None:
        """
        Initialize PaginatedSitemap.

        Args:
            source_sitemap: The original sitemap to paginate.
            page: Page number (1-indexed).
            items_per_page: Items per page. Uses settings default if None.
        """
        self._source = source_sitemap
        self._page = page
        config = get_pagination_config()
        self._items_per_page = items_per_page or config.get(
            "max_urls_per_sitemap", 50000
        )

        # Copy attributes from source
        if hasattr(source_sitemap, "changefreq"):
            self.changefreq = source_sitemap.changefreq
        if hasattr(source_sitemap, "priority"):
            self.priority = source_sitemap.priority
        if hasattr(source_sitemap, "protocol"):
            self.protocol = source_sitemap.protocol

    def items(self) -> Sequence[Any]:
        """Return items for the current page."""
        all_items = list(self._source.items())
        start = (self._page - 1) * self._items_per_page
        end = start + self._items_per_page
        return all_items[start:end]

    def location(self, item: Any) -> str:
        """Delegate to source sitemap."""
        return self._source.location(item)

    def lastmod(self, item: Any):
        """Delegate to source sitemap."""
        if hasattr(self._source, "lastmod"):
            return self._source.lastmod(item)
        return None

    def get_latest_lastmod(self):
        """Get the latest lastmod from paginated items."""
        items = self.items()
        if not items or not hasattr(self._source, "lastmod"):
            return None

        lastmods = [
            self._source.lastmod(item)
            for item in items
            if self._source.lastmod(item) is not None
        ]
        return max(lastmods) if lastmods else None


# =============================================================================
# Exports
# =============================================================================

__all__ = ["PaginatedSitemap"]
