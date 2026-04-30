# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
URL Helpers
===========

Drop-in URL patterns for sites that want a one-line sitemap setup.

Usage in a project's ``urls.py``::

    from swing.sitemap.urls import sitemap_urlpatterns

    urlpatterns = [
        # ... your patterns ...
        *sitemap_urlpatterns(),
    ]

Or, with custom sitemaps::

    urlpatterns = [
        *sitemap_urlpatterns({"pages": MyPageSitemap}, include_index=True),
    ]
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
# Public API
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


# Default ``urlpatterns`` for projects that prefer ``include()``::
#
#     path("", include("swing.sitemap.urls")),
#
# Computed lazily on first attribute access so importing this module does
# not require Django settings to be configured yet.
def __getattr__(name: str):  # PEP 562
    if name == "urlpatterns":
        value = list(sitemap_urlpatterns())
        globals()["urlpatterns"] = value
        return value
    raise AttributeError(f"module 'swing.sitemap.urls' has no attribute {name!r}")


__all__ = ["sitemap_urlpatterns", "urlpatterns"]  # noqa: F822
