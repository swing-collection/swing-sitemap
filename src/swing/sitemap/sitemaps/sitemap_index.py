# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Index with Pagination
=============================

Provides utilities for generating sitemap indexes with automatic pagination
when sitemaps exceed Google's limits (50,000 URLs or 50MB uncompressed).

Usage::

    from swing.sitemap.sitemaps.sitemap_index import paginate_sitemap

    # Automatically paginate large sitemaps
    sitemaps = paginate_sitemap(my_large_sitemap, max_urls=50000)
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

from django.contrib.sitemaps import Sitemap

from swing.sitemap.conf import get_setting

T = TypeVar("T")


# =============================================================================
# Pagination Utilities
# =============================================================================


def get_pagination_config() -> dict[str, Any]:
    """Get pagination configuration from settings."""
    return get_setting("pagination", default={}) or {
        "enabled": True,
        "max_urls_per_sitemap": 50000,
        "max_size_bytes": 50 * 1024 * 1024,
    }


def should_paginate(item_count: int) -> bool:
    """
    Check if pagination is needed based on item count.

    Args:
        item_count: Number of items in the sitemap.

    Returns:
        True if the sitemap should be paginated.
    """
    config = get_pagination_config()
    if not config.get("enabled", True):
        return False
    max_urls = config.get("max_urls_per_sitemap", 50000)
    return item_count > max_urls


def calculate_pages(item_count: int) -> int:
    """
    Calculate the number of pages needed for pagination.

    Args:
        item_count: Total number of items.

    Returns:
        Number of pages.
    """
    config = get_pagination_config()
    max_urls = config.get("max_urls_per_sitemap", 50000)
    return math.ceil(item_count / max_urls) if item_count > 0 else 1


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


def paginate_sitemap(
    sitemap: Sitemap,
    name: str = "sitemap",
) -> dict[str, Sitemap]:
    """
    Paginate a sitemap into multiple sitemaps if needed.

    Args:
        sitemap: The sitemap to paginate.
        name: Base name for the paginated sitemaps.

    Returns:
        Dict of sitemap name -> sitemap instance. If pagination is not
        needed, returns {name: sitemap}. Otherwise returns
        {name-1: page1, name-2: page2, ...}.
    """
    try:
        all_items = list(sitemap.items())
    except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
        # If we can't get items, return as-is
        return {name: sitemap}

    item_count = len(all_items)

    if not should_paginate(item_count):
        return {name: sitemap}

    # Create paginated sitemaps
    num_pages = calculate_pages(item_count)
    result: dict[str, Sitemap] = {}

    for page in range(1, num_pages + 1):
        page_name = f"{name}-{page}"
        result[page_name] = PaginatedSitemap(sitemap, page)

    return result


def paginate_all_sitemaps(
    sitemaps: Mapping[str, Sitemap | type[Sitemap]],
) -> dict[str, Sitemap]:
    """
    Paginate all sitemaps in a mapping.

    Args:
        sitemaps: Mapping of sitemap name -> sitemap instance or class.

    Returns:
        Dict with all sitemaps paginated as needed.
    """
    result: dict[str, Sitemap] = {}

    for name, sitemap in sitemaps.items():
        # Instantiate if class
        if isinstance(sitemap, type):
            sitemap = sitemap()

        # Paginate and merge
        paginated = paginate_sitemap(sitemap, name)
        result.update(paginated)

    return result


# =============================================================================
# Index Generation
# =============================================================================


def get_sitemap_index_urls(
    sitemaps: Mapping[str, Sitemap | type[Sitemap]],
    protocol: str = "https",
    domain: str | None = None,
) -> list[dict[str, Any]]:
    """
    Generate URL entries for a sitemap index.

    Args:
        sitemaps: Mapping of sitemap name -> sitemap.
        protocol: URL protocol (http or https).
        domain: Domain name. If None, must be set elsewhere.

    Returns:
        List of dicts with 'location' and optional 'lastmod' keys.
    """
    urls = []

    for name, sitemap in sitemaps.items():
        # Instantiate if class
        if isinstance(sitemap, type):
            sitemap = sitemap()

        # Get lastmod if available
        lastmod = None
        if hasattr(sitemap, "get_latest_lastmod"):
            try:
                lastmod = sitemap.get_latest_lastmod()
            except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
                pass

        url_entry = {
            "location": f"sitemap-{name}.xml",
            "name": name,
        }
        if lastmod:
            url_entry["lastmod"] = lastmod

        urls.append(url_entry)

    return urls


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "PaginatedSitemap",
    "calculate_pages",
    "get_pagination_config",
    "get_sitemap_index_urls",
    "paginate_all_sitemaps",
    "paginate_sitemap",
    "should_paginate",
]
