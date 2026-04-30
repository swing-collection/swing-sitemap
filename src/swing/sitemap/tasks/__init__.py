# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Celery Tasks Module
====================================

Provides Celery tasks for sitemap management.

Tasks:

- :func:`submit_sitemap_task` - Submit sitemap to search engines
- :func:`submit_sitemap_periodic` - Periodic submission task
- :func:`invalidate_sitemap_cache` - Invalidate sitemap cache

"""


# =============================================================================
# Imports
# =============================================================================

from .invalidate_sitemap_cache import invalidate_sitemap_cache
from .submit_sitemap_periodic import submit_sitemap_periodic
from .submit_sitemap_task import submit_sitemap_task


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "invalidate_sitemap_cache",
    "submit_sitemap_periodic",
    "submit_sitemap_task",
]
