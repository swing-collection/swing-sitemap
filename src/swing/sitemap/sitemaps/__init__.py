# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Sitemaps Module
================================

Provides sitemap classes for generating various types of XML sitemaps:

- :class:`StaticSitemap` - Named Django views
- :class:`ModelSitemap` - Generic queryset-backed sitemaps
- :class:`VideoSitemap` - Google Video Sitemaps
- :class:`NewsSitemap` - Google News Sitemaps
- :class:`ImageSitemap` - Google Image Sitemaps

Also provides:

- :func:`default_sitemaps` - Factory for canonical sitemaps dict

"""


# =============================================================================
# Imports
# =============================================================================

from swing.sitemap.mixins import HreflangMixin, I18nSitemap
from swing.sitemap.utils.pagination import (
    PaginatedSitemap,
    calculate_pages,
    get_pagination_config,
    paginate_all_sitemaps,
    paginate_sitemap,
    should_paginate,
)

from .get_sitemap_index_urls import get_sitemap_index_urls
from .sitemap_base import BaseSitemap
from .sitemap_defaults import default_sitemaps
from .sitemap_image import ImageSitemap
from .sitemap_model import ModelSitemap
from .sitemap_news import NewsSitemap
from .sitemap_static import StaticSitemap
from .sitemap_video import VideoSitemap


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "BaseSitemap",
    "calculate_pages",
    "default_sitemaps",
    "get_pagination_config",
    "get_sitemap_index_urls",
    "HreflangMixin",
    "I18nSitemap",
    "ImageSitemap",
    "ModelSitemap",
    "NewsSitemap",
    "paginate_all_sitemaps",
    "paginate_sitemap",
    "PaginatedSitemap",
    "should_paginate",
    "StaticSitemap",
    "VideoSitemap",
]
