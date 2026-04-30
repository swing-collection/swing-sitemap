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

from swing.sitemap.views.view_sitemap_image import (
    ImageSitemapView,
    image_sitemap,
)
from swing.sitemap.views.view_sitemap_index import (
    SitemapIndexView,
    sitemap_index,
)
from swing.sitemap.views.view_sitemap_news import (
    NewsSitemapView,
    news_sitemap,
)
from swing.sitemap.views.view_sitemap_static import (
    StaticSitemapView,
    static_sitemap,
)
from swing.sitemap.views.view_sitemap_video import (
    VideoSitemapView,
    video_sitemap,
)


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
