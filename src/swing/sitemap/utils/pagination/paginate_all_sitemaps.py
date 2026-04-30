# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Paginate All Sitemaps
=====================

Paginate all sitemaps in a mapping.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Mapping

from django.contrib.sitemaps import Sitemap

from .paginate_sitemap import paginate_sitemap


# =============================================================================
# Functions
# =============================================================================

def paginate_all_sitemaps(
    sitemaps: Mapping[str, Sitemap | type[Sitemap]],
) -> dict[str, Sitemap]:
    """
    Paginate all sitemaps in a mapping.

    Args:
        sitemaps: Mapping of sitemap name -> sitemap instance or class.

    Returns:
        Dict with all sitemaps paginated as needed.
    """
    result: dict[str, Sitemap] = {}

    for name, sitemap in sitemaps.items():
        # Instantiate if class
        if isinstance(sitemap, type):
            sitemap = sitemap()

        # Paginate and merge
        paginated = paginate_sitemap(sitemap, name)
        result.update(paginated)

    return result


# =============================================================================
# Exports
# =============================================================================

__all__ = ["paginate_all_sitemaps"]
