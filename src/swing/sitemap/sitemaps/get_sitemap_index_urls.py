# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Get Sitemap Index URLs
======================

Generate URL entries for a sitemap index.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Mapping
from typing import Any

from django.contrib.sitemaps import Sitemap

# =============================================================================
# Functions
# =============================================================================


def get_sitemap_index_urls(
    sitemaps: Mapping[str, Sitemap | type[Sitemap]],
    protocol: str = "https",
    domain: str | None = None,
) -> list[dict[str, Any]]:
    """
    Generate URL entries for a sitemap index.

    Args:
        sitemaps: Mapping of sitemap name -> sitemap.
        protocol: URL protocol (http or https).
        domain: Domain name. If None, must be set elsewhere.

    Returns:
        List of dicts with 'location' and optional 'lastmod' keys.
    """
    urls = []

    for name, sitemap in sitemaps.items():
        # Instantiate if class
        if isinstance(sitemap, type):
            sitemap = sitemap()

        # Get lastmod if available
        lastmod = None
        if hasattr(sitemap, "get_latest_lastmod"):
            try:
                lastmod = sitemap.get_latest_lastmod()
            except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
                pass

        url_entry = {
            "location": f"sitemap-{name}.xml",
            "name": name,
        }
        if lastmod:
            url_entry["lastmod"] = lastmod

        urls.append(url_entry)

    return urls


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_sitemap_index_urls"]
