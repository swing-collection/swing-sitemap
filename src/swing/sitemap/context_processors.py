# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Context Processors
==================

Inject the sitemap URL into every template context.

Add to your settings::

    TEMPLATES = [{
        "OPTIONS": {
            "context_processors": [
                ...,
                "swing_sitemap.context_processors.sitemap_url",
            ],
        },
    }]

Then ``{{ SITEMAP_URL }}`` is available in any template (typically used
inside a ``robots.txt`` template).
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse


# =============================================================================
# Public API
# =============================================================================


def sitemap_url(request: HttpRequest) -> dict[str, str]:
    """Return ``{"SITEMAP_URL": "<absolute sitemap URL>"}``."""
    try:
        path = reverse("swing-sitemap")
    except NoReverseMatch:
        try:
            path = reverse("sitemap")
        except NoReverseMatch:
            path = "/sitemap.xml"
    return {"SITEMAP_URL": request.build_absolute_uri(path)}


__all__ = ["sitemap_url"]
