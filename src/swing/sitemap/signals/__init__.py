# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Signals Module
===============================

Provides signal handlers for automatic sitemap cache invalidation.

Functions:

- :func:`register_sitemap_signals` - Register signals for configured models
- :func:`unregister_sitemap_signals` - Unregister signals
- :func:`invalidate_sitemap_cache` - Manually invalidate cache

"""


# =============================================================================
# Imports
# =============================================================================

from .cancel_debounce import cancel_debounce
from .debounce import debounce
from .invalidate_sitemap_cache import invalidate_sitemap_cache
from .register_sitemap_signals import register_sitemap_signals
from .sitemap_post_delete import sitemap_post_delete
from .sitemap_post_save import sitemap_post_save
from .unregister_sitemap_signals import unregister_sitemap_signals


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "cancel_debounce",
    "debounce",
    "invalidate_sitemap_cache",
    "register_sitemap_signals",
    "sitemap_post_delete",
    "sitemap_post_save",
    "unregister_sitemap_signals",
]
