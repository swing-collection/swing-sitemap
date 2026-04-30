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

from .calculate_pages import calculate_pages
from .get_pagination_config import get_pagination_config
from .get_sitemap_index_urls import get_sitemap_index_urls
from .hreflang_mixin import HreflangMixin, I18nSitemap
from .paginate_all_sitemaps import paginate_all_sitemaps
from .paginate_sitemap import paginate_sitemap
from .paginated_sitemap import PaginatedSitemap
from .should_paginate import should_paginate
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
