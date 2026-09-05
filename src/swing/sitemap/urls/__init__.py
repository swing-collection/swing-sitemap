# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - URL Helpers
===========================

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

For dynamic sitemaps using DynamicSitemapView::

    from swing.sitemap.urls import dynamic_sitemap_urlpatterns

    urlpatterns = [
        *dynamic_sitemap_urlpatterns(MySitemapView),
    ]

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local
from .sitemap_urlpatterns import dynamic_sitemap_urlpatterns, sitemap_urlpatterns

# =============================================================================
# Lazy urlpatterns
# =============================================================================


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


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "dynamic_sitemap_urlpatterns",
    "sitemap_urlpatterns",
    "urlpatterns",
]  # noqa: F822
