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

from django.contrib import admin

from swing.sitemap.models import (
    CustomSitemapURL,
    ImageSitemapURL,
    NewsSitemapURL,
    StandardSitemapURL,
    VideoSitemapURL,
)


# =============================================================================
# Admin Registration
# =============================================================================

admin.site.register(StandardSitemapURL)
admin.site.register(ImageSitemapURL)
admin.site.register(VideoSitemapURL)
admin.site.register(NewsSitemapURL)
admin.site.register(CustomSitemapURL)
