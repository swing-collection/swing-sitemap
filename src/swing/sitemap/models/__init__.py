# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

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


# =============================================================================
# Imports
# =============================================================================

from .model_sitemap_url_custom import CustomSitemapURL
from .model_sitemap_url_image import ImageSitemapURL
from .model_sitemap_url_news import NewsSitemapURL
from .model_sitemap_url_standard import StandardSitemapURL
from .model_sitemap_url_video import VideoSitemapURL
from .sitemap_url import SitemapURL
from .url import URL


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "CustomSitemapURL",
    "ImageSitemapURL",
    "NewsSitemapURL",
    "SitemapURL",
    "StandardSitemapURL",
    "URL",
    "VideoSitemapURL",
]
