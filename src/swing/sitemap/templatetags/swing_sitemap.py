# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap Template Tags
===========================

Provides ``{% sitemap_url %}`` for use in templates such as
``robots.txt``::

    {% load swing_sitemap %}
    Sitemap: {% sitemap_url %}

If a ``request`` is in context the URL is built absolutely
(``https://example.com/sitemap.xml``); otherwise a relative path is
returned.

The tag accepts an optional URL name (defaults to ``"swing-sitemap"``)
and falls back to ``"sitemap"`` for projects that registered the URL
themselves with that name.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


# =============================================================================
# Tags
# =============================================================================


@register.simple_tag(takes_context=True)
def sitemap_url(context, name: str = "swing-sitemap") -> str:
    """
    Return the absolute URL of the sitemap (when ``request`` is in
    context) or a relative path otherwise.
    """
    try:
        path = reverse(name)
    except NoReverseMatch:  # pragma: no cover
        # Fall back to the legacy / Django-default name.
        path = reverse("sitemap") if name != "sitemap" else "/sitemap.xml"
    request = context.get("request")
    if request is not None:
        return request.build_absolute_uri(path)
    return path


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_url"]
