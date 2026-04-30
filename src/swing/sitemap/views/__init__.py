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

# Import | Local
from .image_sitemap import image_sitemap
from .image_sitemap_view import ImageSitemapView
from .news_sitemap import news_sitemap
from .news_sitemap_view import NewsSitemapView
from .sitemap_index import sitemap_index
from .sitemap_index_view import SitemapIndexView
from .static_sitemap import static_sitemap
from .static_sitemap_view import StaticSitemapView
from .template_sitemap_index import sitemap_index as template_sitemap_index
from .video_sitemap import video_sitemap
from .video_sitemap_view import VideoSitemapView
from .view_health_check import health_check

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Function-based views
    "health_check",
    "image_sitemap",
    "news_sitemap",
    "sitemap_index",
    "static_sitemap",
    "template_sitemap_index",
    "video_sitemap",
    # Class-based views
    "ImageSitemapView",
    "NewsSitemapView",
    "SitemapIndexView",
    "StaticSitemapView",
    "VideoSitemapView",
]
