# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Admin Module
=============================

Django admin configuration for sitemap models.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import admin classes to trigger registration
from .admin_sitemap_url_base import BaseSitemapURLAdmin
from .admin_sitemap_url_custom import CustomSitemapURLAdmin
from .admin_sitemap_url_image import ImageSitemapURLAdmin
from .admin_sitemap_url_news import NewsSitemapURLAdmin
from .admin_sitemap_url_standard import StandardSitemapURLAdmin
from .admin_sitemap_url_video import VideoSitemapURLAdmin

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "BaseSitemapURLAdmin",
    "CustomSitemapURLAdmin",
    "ImageSitemapURLAdmin",
    "NewsSitemapURLAdmin",
    "StandardSitemapURLAdmin",
    "VideoSitemapURLAdmin",
]
