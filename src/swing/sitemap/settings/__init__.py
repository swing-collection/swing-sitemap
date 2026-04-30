# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Settings Example
================================

Example settings for swing_sitemap configuration.

Usage::

    # In your Django settings.py
    VIDEO_SITEMAP_MODEL = 'myapp.MyVideoModel'

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local
from .video_sitemap_model import VIDEO_SITEMAP_MODEL

# =============================================================================
# Exports
# =============================================================================

__all__ = ["VIDEO_SITEMAP_MODEL"]
