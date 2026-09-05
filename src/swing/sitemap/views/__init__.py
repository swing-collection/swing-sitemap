# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Views Module
=============================

Django class-based views for serving sitemap XML files.

All views follow the single-symbol-per-file convention.

Class-Based Views:
    - :class:`SitemapIndexView` - Sitemap index view
    - :class:`StaticSitemapView` - Static sitemap view
    - :class:`ImageSitemapView` - Image sitemap view
    - :class:`VideoSitemapView` - Video sitemap view
    - :class:`NewsSitemapView` - News sitemap view
    - :class:`DynamicSitemapView` - Configurable dynamic sitemap view
    - :class:`RobotsTxtView` - Robots.txt view
    - :class:`HealthCheckView` - Health check view

Legacy (deprecated):
    - :func:`health_check` - Health check function (use HealthCheckView)

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local
from .view_health_check import health_check, HealthCheckView
from .view_robots_txt import RobotsTxtView
from .view_sitemap_dynamic import DynamicSitemapView
from .view_sitemap_image import ImageSitemapView
from .view_sitemap_index import SitemapIndexView
from .view_sitemap_news import NewsSitemapView
from .view_sitemap_static import StaticSitemapView
from .view_sitemap_video import VideoSitemapView

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Class-based views
    "DynamicSitemapView",
    "health_check",  # Legacy, deprecated
    "HealthCheckView",
    "ImageSitemapView",
    "NewsSitemapView",
    "RobotsTxtView",
    "SitemapIndexView",
    "StaticSitemapView",
    "VideoSitemapView",
]
