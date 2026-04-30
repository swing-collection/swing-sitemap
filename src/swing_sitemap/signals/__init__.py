# -*- coding: utf-8 -*-

"""
Swing Sitemap - Signals Module
==============================

Provides signal handlers for automatic sitemap cache invalidation.

Functions:
- :func:`register_sitemap_signals` - Register signals for configured models
- :func:`unregister_sitemap_signals` - Unregister signals
- :func:`invalidate_sitemap_cache` - Manually invalidate cache
"""

from swing_sitemap.signals.signal_model import (
    invalidate_sitemap_cache,
    register_sitemap_signals,
    sitemap_post_delete,
    sitemap_post_save,
    unregister_sitemap_signals,
)

__all__ = [
    "invalidate_sitemap_cache",
    "register_sitemap_signals",
    "sitemap_post_delete",
    "sitemap_post_save",
    "unregister_sitemap_signals",
]
