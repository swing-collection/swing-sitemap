# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Submit Sitemap Utility
======================

Notify search-engine endpoints that a sitemap has been published or
updated. Returns a mapping of endpoint name to HTTP status code.

Note:
    Google deprecated its sitemap-ping endpoint in 2023; it remains
    callable but is a no-op. Bing/Yandex still honour it.
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Mapping
import logging

# Import | Libraries
import requests

logger = logging.getLogger(__name__)


# =============================================================================
# Endpoints
# =============================================================================

PING_ENDPOINTS: Mapping[str, str] = {
    "google": "https://www.google.com/ping?sitemap={url}",
    "bing": "https://www.bing.com/ping?sitemap={url}",
}


# =============================================================================
# Public API
# =============================================================================


def submit_sitemap(
    sitemap_url: str,
    *,
    endpoints: Mapping[str, str] | None = None,
    timeout: float = 10.0,
) -> dict[str, int | None]:
    """
    Ping each search-engine endpoint with the given sitemap URL.

    Args:
        sitemap_url: Absolute URL of the sitemap (e.g.
            ``https://example.com/sitemap.xml``).
        endpoints: Optional mapping of name -> URL template containing
            ``{url}``. Defaults to :data:`PING_ENDPOINTS`.
        timeout: Per-request timeout in seconds.

    Returns:
        Mapping of endpoint name to HTTP status code (or ``None`` on
        request failure).
    """
    targets = endpoints or PING_ENDPOINTS
    results: dict[str, int | None] = {}
    for name, template in targets.items():
        url = template.format(url=sitemap_url)
        try:
            response = requests.get(url, timeout=timeout)
            results[name] = response.status_code
        except requests.exceptions.RequestException as exc:
            logger.warning("Sitemap ping to %s failed: %s", name, exc)
            results[name] = None
    return results


__all__ = ["PING_ENDPOINTS", "submit_sitemap"]
