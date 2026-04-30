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

from __future__ import annotations

import datetime as _dt
from collections.abc import Iterable, Sequence

from django.urls import reverse

from swing_sitemap.conf import get_setting
from swing_sitemap.sitemaps.sitemap_base import BaseSitemap

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

    def items(self) -> Sequence[StaticItem]:
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
