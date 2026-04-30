# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap URL Context Processor
=============================

Inject the sitemap URL into template context.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse


# =============================================================================
# Functions
# =============================================================================

def sitemap_url(request: HttpRequest) -> dict[str, str]:
    """
    Return ``{"SITEMAP_URL": "<absolute sitemap URL>"}``.

    Add to your settings::

        TEMPLATES = [{
            "OPTIONS": {
                "context_processors": [
                    ...,
                    "swing.sitemap.context_processors.sitemap_url",
                ],
            },
        }]

    Then ``{{ SITEMAP_URL }}`` is available in any template (typically used
    inside a ``robots.txt`` template).
    """
    try:
        path = reverse("swing-sitemap")
    except NoReverseMatch:
        try:
            path = reverse("sitemap")
        except NoReverseMatch:
            path = "/sitemap.xml"
    return {"SITEMAP_URL": request.build_absolute_uri(path)}


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_url"]
