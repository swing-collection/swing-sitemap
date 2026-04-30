# -*- coding: utf-8 -*-

"""
Swing Sitemap - Sitemaps Module
===============================

Provides sitemap classes for generating various types of XML sitemaps:

- :class:`StaticSitemap` - Named Django views
- :class:`ModelSitemap` - Generic queryset-backed sitemaps
- :class:`VideoSitemap` - Google Video Sitemaps
- :class:`NewsSitemap` - Google News Sitemaps
- :class:`ImageSitemap` - Google Image Sitemaps

Also provides:
- :func:`default_sitemaps` - Factory for canonical sitemaps dict
"""

from swing.sitemap.sitemaps.sitemap_base import BaseSitemap
from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps
from swing.sitemap.sitemaps.sitemap_image import ImageSitemap
from swing.sitemap.sitemaps.sitemap_model import ModelSitemap
from swing.sitemap.sitemaps.sitemap_news import NewsSitemap
from swing.sitemap.sitemaps.sitemap_static import StaticSitemap
from swing.sitemap.sitemaps.sitemap_video import VideoSitemap

__all__ = [
    "BaseSitemap",
    "default_sitemaps",
    "ImageSitemap",
    "ModelSitemap",
    "NewsSitemap",
    "StaticSitemap",
    "VideoSitemap",
]
