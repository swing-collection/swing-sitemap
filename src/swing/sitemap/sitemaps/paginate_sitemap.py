# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Paginate Sitemap
================

Paginate a sitemap into multiple sitemaps.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.contrib.sitemaps import Sitemap

from .calculate_pages import calculate_pages
from .paginated_sitemap import PaginatedSitemap
from .should_paginate import should_paginate


# =============================================================================
# Functions
# =============================================================================

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
    except Exception:
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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["paginate_sitemap"]
