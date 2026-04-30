# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Should Paginate
===============

Check if pagination is needed.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from .get_pagination_config import get_pagination_config


# =============================================================================
# Functions
# =============================================================================

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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["should_paginate"]
