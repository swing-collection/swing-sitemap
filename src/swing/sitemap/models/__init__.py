# -*- coding: utf-8 -*-

"""
Swing Sitemap - Models Module
=============================

Provides optional database models for storing sitemap URL entries.

These models are designed for sites that need database-driven sitemap
management rather than settings-based configuration.

Available Models:
- :class:`SitemapURL` - Base model for sitemap URLs
- :class:`URL` - Abstract base class with common fields
- :class:`StandardSitemapURL` - Standard sitemap entries
- :class:`ImageSitemapURL` - Image sitemap entries
- :class:`VideoSitemapURL` - Video sitemap entries
- :class:`NewsSitemapURL` - News sitemap entries
- :class:`CustomSitemapURL` - Custom/flexible sitemap entries
"""

from swing.sitemap.models.model_sitemap_url import SitemapURL, URL
from swing.sitemap.models.model_sitemap_url_custom import CustomSitemapURL
from swing.sitemap.models.model_sitemap_url_image import ImageSitemapURL
from swing.sitemap.models.model_sitemap_url_news import NewsSitemapURL
from swing.sitemap.models.model_sitemap_url_standard import StandardSitemapURL
from swing.sitemap.models.model_sitemap_url_video import VideoSitemapURL

__all__ = [
    "CustomSitemapURL",
    "ImageSitemapURL",
    "NewsSitemapURL",
    "SitemapURL",
    "StandardSitemapURL",
    "URL",
    "VideoSitemapURL",
]
