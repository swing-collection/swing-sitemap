# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Pagination Config
=================

Get pagination configuration from settings.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

from swing.sitemap.conf import get_setting

# =============================================================================
# Functions
# =============================================================================


def get_pagination_config() -> dict[str, Any]:
    """Get pagination configuration from settings."""
    return get_setting("pagination", default={}) or {
        "enabled": True,
        "max_urls_per_sitemap": 50000,
        "max_size_bytes": 50 * 1024 * 1024,
    }


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_pagination_config"]
