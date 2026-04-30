# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Get Config
==========

Retrieve merged configuration.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

from django.conf import settings

# Import | Local
from .apply_legacy_shims import apply_legacy_shims
from .defaults import DEFAULTS

# =============================================================================
# Functions
# =============================================================================


def get_config() -> dict[str, Any]:
    """
    Return the merged ``SWING_SITEMAP`` dict, layered on top of
    :data:`DEFAULTS`.

    Top-level keys whose default value is a dict are shallow-merged so
    projects only override the keys they care about.
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
    apply_legacy_shims(merged)
    return merged


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_config"]
