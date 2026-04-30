# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Configuration Defaults
======================

Default configuration values for swing_sitemap.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

# =============================================================================
# Constants
# =============================================================================

DEFAULTS: dict[str, Any] = {
    "wagtail": {
        "priority": 0.7,
        "changefreq": "monthly",
        "protocol": "https",
    },
    "static": {
        "priority": 0.5,
        "changefreq": "monthly",
        "views": [],
    },
    "priority": {},
    "changefreq": {},
    "models": {},
    "video": {},
    "image": {},
    "news": {},
    # Pagination settings
    "pagination": {
        "enabled": True,
        "max_urls_per_sitemap": 50000,
        "max_size_bytes": 50 * 1024 * 1024,  # 50MB
    },
    # Caching settings
    "cache": {
        "enabled": False,
        "timeout": 3600,  # 1 hour
        "backend": "default",
        "key_prefix": "swing_sitemap",
    },
    # Submission settings
    "submit": {
        "sitemap_url": None,
        "endpoints": None,
        "timeout": 10.0,
        "retry_delay": 60,
        "max_retries": 3,
    },
    # Signal settings
    "signals": {
        "enabled": True,
        "models": [],
        "debounce_seconds": 5,
        "invalidate_on_save": True,
        "invalidate_on_delete": True,
        "auto_submit": False,
    },
    # Compression settings
    "compression": {
        "enabled": False,
        "format": "gzip",  # or "none"
    },
}


# =============================================================================
# Exports
# =============================================================================

__all__ = ["DEFAULTS"]
