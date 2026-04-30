# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap URL Patterns
====================

Generate URL patterns for sitemap endpoints.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Mapping, Sequence

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import index as sitemap_index_view
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.urls import URLPattern, path

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps


# =============================================================================
# Functions
# =============================================================================

def sitemap_urlpatterns(
    sitemaps: Mapping[str, Sitemap | type[Sitemap]] | None = None,
    *,
    sitemap_url: str = "sitemap.xml",
    include_index: bool = False,
    index_url: str = "sitemap-index.xml",
    section_url_template: str = "sitemap-<str:section>.xml",
) -> Sequence[URLPattern]:
    """
    Return URL patterns for a single ``sitemap.xml`` (and optionally a
    sitemap index + per-section URLs).

    Args:
        sitemaps: Mapping of section name -> sitemap class/instance.
            Defaults to :func:`~swing.sitemap.default_sitemaps`.
        sitemap_url: Path for the combined sitemap. Default
            ``sitemap.xml``.
        include_index: If ``True`` also expose an index plus per-section
            URLs (recommended for sites with many entries).
        index_url: Path for the sitemap index. Used only when
            ``include_index`` is true.
        section_url_template: URL template (with a ``<str:section>``
            converter) for each per-section sitemap. Used only when
            ``include_index`` is true.
    """
    sm = dict(sitemaps) if sitemaps is not None else default_sitemaps()
    patterns: list[URLPattern] = [
        path(
            sitemap_url,
            sitemap_view,
            {"sitemaps": sm},
            name="swing-sitemap",
        ),
    ]
    if include_index:
        patterns += [
            path(
                index_url,
                sitemap_index_view,
                {
                    "sitemaps": sm,
                    "sitemap_url_name": "swing-sitemap-section",
                },
                name="swing-sitemap-index",
            ),
            path(
                section_url_template,
                sitemap_view,
                {"sitemaps": sm},
                name="swing-sitemap-section",
            ),
        ]
    return patterns


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_urlpatterns"]
