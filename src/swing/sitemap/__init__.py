# -*- coding: utf-8 -*-

"""
swing.sitemap
=============

Reusable, CMS-agnostic Django sitemap toolkit. Exposes a small,
lazy-loaded public API.

Quick start::

    # project/urls.py
    from swing.sitemap.urls import sitemap_urlpatterns
    urlpatterns = [..., *sitemap_urlpatterns()]

    # project/settings.py
    SWING_SITEMAP = {
        "static": {"views": ["home", "about", "contact"]},
        "models": {
            "work": {
                "model": "myapp.WorkModel",
                "filters": {"is_published": True},
                "date_field": "modified_at",
                "priority": 0.8,
            },
        },
    }

Public API::

    BaseSitemap            # subclass to roll your own
    StaticSitemap          # named-view sitemap
    ModelSitemap           # generic queryset-backed sitemap
    default_sitemaps       # build the sitemaps dict from settings
    sitemap_urlpatterns    # drop-in URL patterns
    submit_sitemap         # ping search engines
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

default_app_config = "swing.sitemap.apps.SwingSitemapConfig"

# Lazy export map: public name -> (module path relative to this package, attribute).
_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    # Sitemap classes
    "BaseSitemap": (".sitemaps.sitemap_base", "BaseSitemap"),
    "StaticSitemap": (".sitemaps.sitemap_static", "StaticSitemap"),
    "ModelSitemap": (".sitemaps.sitemap_model", "ModelSitemap"),
    "VideoSitemap": (".sitemaps.sitemap_video", "VideoSitemap"),
    "NewsSitemap": (".sitemaps.sitemap_news", "NewsSitemap"),
    "ImageSitemap": (".sitemaps.sitemap_image", "ImageSitemap"),
    # Utilities
    "default_sitemaps": (".sitemaps.sitemap_defaults", "default_sitemaps"),
    "sitemap_urlpatterns": (".urls", "sitemap_urlpatterns"),
    "submit_sitemap": (".utils.util_submit_sitemap", "submit_sitemap"),
    # Pagination
    "PaginatedSitemap": (".sitemaps.sitemap_index", "PaginatedSitemap"),
    "paginate_sitemap": (".sitemaps.sitemap_index", "paginate_sitemap"),
    "paginate_all_sitemaps": (".sitemaps.sitemap_index", "paginate_all_sitemaps"),
    # Configuration
    "get_config": (".conf", "get_config"),
    "get_setting": (".conf", "get_setting"),
    # Signals
    "register_sitemap_signals": (".signals.signal_model", "register_sitemap_signals"),
    "invalidate_sitemap_cache": (".signals.signal_model", "invalidate_sitemap_cache"),
}


def __getattr__(name: str) -> Any:  # PEP 562
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module 'swing_sitemap' has no attribute {name!r}")
    module_path, attr = target
    module = import_module(module_path, __name__)
    value = getattr(module, attr)
    globals()[name] = value  # cache for subsequent lookups
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_EXPORTS))


# ``__all__`` is populated dynamically from ``_LAZY_EXPORTS`` so PEP 562
# lazy attribute lookup remains the single source of truth for the public
# API surface. Static linters may flag these names as undefined; that is
# expected and harmless at runtime.
__all__ = list(_LAZY_EXPORTS)  # noqa: F822, PLE0604
