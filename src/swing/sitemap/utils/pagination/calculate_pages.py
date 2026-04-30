# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Calculate Pages
===============

Calculate number of pages needed for pagination.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import math

# Import | Local
from .get_pagination_config import get_pagination_config

# =============================================================================
# Functions
# =============================================================================


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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["calculate_pages"]
