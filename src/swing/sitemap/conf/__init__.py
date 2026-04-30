# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Configuration
=============================

Typed accessor for ``swing_sitemap`` configuration.

All configuration lives under a single ``SWING_SITEMAP`` dict in the
project's Django settings. This module provides defaults plus
backward-compatible shims for the legacy settings names that older
scapepress sites used:

- ``SEO_SITEMAP_PRIORITY``  -> ``SWING_SITEMAP["priority"]`` (per-key dict)
- ``SEO_SITEMAP_CHANGEFREQ`` -> ``SWING_SITEMAP["changefreq"]`` (per-key dict)
- ``VIDEO_SITEMAP_MODEL``   -> ``SWING_SITEMAP["video"]["model"]``

Example settings:

    SWING_SITEMAP = {
        "wagtail": {"priority": 0.7, "changefreq": "monthly"},
        "static":  {"priority": 0.5, "changefreq": "monthly", "views": []},
        "priority":   {"page": 0.7, "work": 0.8},
        "changefreq": {"page": "monthly", "work": "monthly"},
        "models":  {"work": "myapp.WorkModel"},
        "video":   {"model": "myapp.VideoModel"},
    }

"""


# =============================================================================
# Imports
# =============================================================================

from .apply_legacy_shims import apply_legacy_shims
from .defaults import DEFAULTS
from .get_config import get_config
from .get_setting import get_setting


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "apply_legacy_shims",
    "DEFAULTS",
    "get_config",
    "get_setting",
]
