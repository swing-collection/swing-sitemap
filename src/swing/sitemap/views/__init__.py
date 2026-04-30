# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Views Module
=============================

Django views for serving sitemap XML files.

Provides both function-based and class-based views:

Function-Based Views:
    - :func:`sitemap_index` - Sitemap index view
    - :func:`static_sitemap` - Static sitemap view
    - :func:`image_sitemap` - Image sitemap view
    - :func:`video_sitemap` - Video sitemap view
    - :func:`news_sitemap` - News sitemap view

Class-Based Views:
    - :class:`SitemapIndexView` - Sitemap index view
    - :class:`StaticSitemapView` - Static sitemap view
    - :class:`ImageSitemapView` - Image sitemap view
    - :class:`VideoSitemapView` - Video sitemap view
    - :class:`NewsSitemapView` - News sitemap view

"""


# =============================================================================
# Imports
# =============================================================================

from .image_sitemap import image_sitemap
from .image_sitemap_view import ImageSitemapView
from .news_sitemap import news_sitemap
from .news_sitemap_view import NewsSitemapView
from .sitemap_index import sitemap_index
from .sitemap_index_view import SitemapIndexView
from .static_sitemap import static_sitemap
from .static_sitemap_view import StaticSitemapView
from .video_sitemap import video_sitemap
from .video_sitemap_view import VideoSitemapView


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Function-based views
    "image_sitemap",
    "news_sitemap",
    "sitemap_index",
    "static_sitemap",
    "video_sitemap",
    # Class-based views
    "ImageSitemapView",
    "NewsSitemapView",
    "SitemapIndexView",
    "StaticSitemapView",
    "VideoSitemapView",
]
