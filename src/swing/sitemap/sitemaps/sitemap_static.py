# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Static Sitemap
==============

A sitemap class for generating URLs of static (named) views.

Each ``items`` entry may be either:

* a plain string  — the Django URL name to ``reverse()``, or
* a dict          — ``{"view_name": "...", "kwargs": {...}, "args": [...],
                       "lastmod": <date|datetime>, "priority": float,
                       "changefreq": str}``.

When given a dict, per-item ``lastmod`` / ``priority`` / ``changefreq``
override the sitemap-level defaults.
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Iterable, Sequence
import datetime as _dt

from django.urls import reverse

from swing.sitemap.conf import get_setting
from swing.sitemap.sitemaps.sitemap_base import BaseSitemap

# =============================================================================
# Types
# =============================================================================

#: An entry may be a URL name string or a configuration dict.
StaticItem = str | dict


# =============================================================================
# Class
# =============================================================================


class StaticSitemap(BaseSitemap):
    """Sitemap of named Django views with optional per-entry overrides."""

    # Defaults populated from ``SWING_SITEMAP["static"]`` in ``__init__``.
    changefreq: str = "monthly"
    priority: float = 0.5

    def __init__(
        self,
        items: Iterable[StaticItem] | None = None,
        *,
        priority: float | None = None,
        changefreq: str | None = None,
    ) -> None:
        super().__init__(list(items) if items is not None else [])
        self.priority = (
            priority
            if priority is not None
            else get_setting("static", "priority", default=self.priority)
        )
        self.changefreq = (
            changefreq
            if changefreq is not None
            else get_setting("static", "changefreq", default=self.changefreq)
        )

    # -------------------------------------------------------------------------
    # Construction helpers
    # -------------------------------------------------------------------------

    @classmethod
    def from_setting(cls) -> "StaticSitemap":
        """Build a sitemap from ``SWING_SITEMAP["static"]["views"]``."""
        return cls(get_setting("static", "views", default=[]) or [])

    # -------------------------------------------------------------------------
    # Sitemap protocol
    # -------------------------------------------------------------------------

    # NOTE: BaseSitemap declares items()/location() around dict-shaped
    # entries; this subclass also accepts plain URL-name strings, which
    # mypy flags as a Liskov violation. Properly resolving this would mean
    # making BaseSitemap generic over the item type across the whole
    # sitemaps/ hierarchy - a moderate refactor out of scope for this pass.
    def items(self) -> Sequence[StaticItem]:  # type: ignore[override]
        return self.items_list

    def location(self, item: StaticItem) -> str:
        if isinstance(item, str):
            return reverse(item)
        return reverse(
            item["view_name"],
            args=item.get("args"),
            kwargs=item.get("kwargs"),
        )

    # Per-item overrides (Django's ``Sitemap`` calls these with the item).
    def lastmod(self, item: StaticItem) -> _dt.date | _dt.datetime | None:
        if isinstance(item, dict):
            return item.get("lastmod")
        return None


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["StaticSitemap", "StaticItem"]
