# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Settings Accessor
=================

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

from __future__ import annotations

import warnings
from typing import Any

from django.conf import settings


# =============================================================================
# Defaults
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
# Public API
# =============================================================================

def get_config() -> dict[str, Any]:
    """
    Return the merged ``SWING_SITEMAP`` dict, layered on top of
    :data:`DEFAULTS`. Top-level keys whose default value is a dict are
    shallow-merged so projects only override the keys they care about.
    """
    user = getattr(settings, "SWING_SITEMAP", {}) or {}
    merged: dict[str, Any] = {}
    for key, default_value in DEFAULTS.items():
        if isinstance(default_value, dict):
            merged[key] = {**default_value, **(user.get(key) or {})}
        else:
            merged[key] = user.get(key, default_value)
    # Pass through any keys the user added that we don't know about.
    for key, value in user.items():
        if key not in merged:
            merged[key] = value
    _apply_legacy_shims(merged)
    return merged


def get_setting(*path: str, default: Any = None) -> Any:
    """
    Look up a value by dotted path inside the merged config.

    Example::

        get_setting("wagtail", "priority", default=0.5)
    """
    node: Any = get_config()
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


# =============================================================================
# Backward-compatibility shims
# =============================================================================

def _apply_legacy_shims(config: dict[str, Any]) -> None:
    """
    Fold legacy top-level Django settings into the merged config dict.
    Emits :class:`DeprecationWarning` for each legacy setting still in use.
    """
    legacy_priority = getattr(settings, "SEO_SITEMAP_PRIORITY", None)
    if isinstance(legacy_priority, dict):
        warnings.warn(
            "SEO_SITEMAP_PRIORITY is deprecated; move values into "
            "SWING_SITEMAP['priority'].",
            DeprecationWarning,
            stacklevel=3,
        )
        config["priority"] = {**legacy_priority, **(config.get("priority") or {})}

    legacy_changefreq = getattr(settings, "SEO_SITEMAP_CHANGEFREQ", None)
    if isinstance(legacy_changefreq, dict):
        warnings.warn(
            "SEO_SITEMAP_CHANGEFREQ is deprecated; move values into "
            "SWING_SITEMAP['changefreq'].",
            DeprecationWarning,
            stacklevel=3,
        )
        config["changefreq"] = {
            **legacy_changefreq,
            **(config.get("changefreq") or {}),
        }

    legacy_video_model = getattr(settings, "VIDEO_SITEMAP_MODEL", None)
    if legacy_video_model and not config.get("video", {}).get("model"):
        warnings.warn(
            "VIDEO_SITEMAP_MODEL is deprecated; use "
            "SWING_SITEMAP['video']['model'] instead.",
            DeprecationWarning,
            stacklevel=3,
        )
        config.setdefault("video", {})["model"] = legacy_video_model


__all__ = ["DEFAULTS", "get_config", "get_setting"]
