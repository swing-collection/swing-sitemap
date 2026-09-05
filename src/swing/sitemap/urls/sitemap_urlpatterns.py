# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap URL Patterns
====================

Generate URL patterns for sitemap endpoints.

Supports two modes:
1. Django's built-in sitemap views (for compatibility)
2. Swing's class-based views (for full control)

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import index as sitemap_index_view
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.urls import URLPattern, path

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps

if TYPE_CHECKING:
    from swing.sitemap.views import DynamicSitemapView

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
    include_health_check: bool = False,
    health_check_url: str = "sitemap/health/",
    include_robots_txt: bool = False,
    robots_txt_url: str = "robots.txt",
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
        include_health_check: If ``True`` add a health check endpoint.
        health_check_url: Path for the health check endpoint.
        include_robots_txt: If ``True`` add a robots.txt endpoint.
        robots_txt_url: Path for the robots.txt endpoint.
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
    if include_health_check:
        # pylint: disable=import-outside-toplevel
        from swing.sitemap.views import health_check

        patterns.append(
            path(
                health_check_url,
                health_check,
                name="swing-sitemap-health",
            ),
        )
    if include_robots_txt:
        # pylint: disable=import-outside-toplevel
        from swing.sitemap.views import RobotsTxtView

        patterns.append(
            path(
                robots_txt_url,
                RobotsTxtView.as_view(),
                name="swing-robots-txt",
            ),
        )
    return patterns


def dynamic_sitemap_urlpatterns(
    sitemap_view_class: type["DynamicSitemapView"] | None = None,
    *,
    sitemap_url: str = "sitemap.xml",
    include_robots_txt: bool = True,
    robots_txt_url: str = "robots.txt",
    include_health_check: bool = False,
    health_check_url: str = "sitemap/health/",
) -> Sequence[URLPattern]:
    """
    Return URL patterns using Swing's DynamicSitemapView.

    This provides more flexibility than Django's built-in sitemap views,
    allowing for dynamic page sources, model querysets, and callables.

    Args:
        sitemap_view_class: Custom DynamicSitemapView subclass. Defaults to
            the base DynamicSitemapView.
        sitemap_url: Path for the sitemap. Default ``sitemap.xml``.
        include_robots_txt: If ``True`` add a robots.txt endpoint.
        robots_txt_url: Path for the robots.txt endpoint.
        include_health_check: If ``True`` add a health check endpoint.
        health_check_url: Path for the health check endpoint.
    """
    # pylint: disable=import-outside-toplevel
    from swing.sitemap.views import DynamicSitemapView, RobotsTxtView

    view_class = sitemap_view_class or DynamicSitemapView

    patterns: list[URLPattern] = [
        path(
            sitemap_url,
            view_class.as_view(),
            name="swing-sitemap",
        ),
    ]

    if include_robots_txt:
        patterns.append(
            path(
                robots_txt_url,
                RobotsTxtView.as_view(),
                name="swing-robots-txt",
            ),
        )

    if include_health_check:
        from swing.sitemap.views import health_check

        patterns.append(
            path(
                health_check_url,
                health_check,
                name="swing-sitemap-health",
            ),
        )

    return patterns


# =============================================================================
# Exports
# =============================================================================

__all__ = ["dynamic_sitemap_urlpatterns", "sitemap_urlpatterns"]
