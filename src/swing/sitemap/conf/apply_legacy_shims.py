# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Legacy Shims
============

Backward-compatibility shims for legacy settings.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any
import warnings

from django.conf import settings

# =============================================================================
# Functions
# =============================================================================


def apply_legacy_shims(config: dict[str, Any]) -> None:
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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["apply_legacy_shims"]
