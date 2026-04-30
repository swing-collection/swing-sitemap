# -*- coding: utf-8 -*-

"""
Swing Sitemap - Celery Tasks Module
===================================

Provides Celery tasks for sitemap management.

Tasks:
- :func:`submit_sitemap_task` - Submit sitemap to search engines
- :func:`submit_sitemap_periodic` - Periodic submission task
- :func:`invalidate_sitemap_cache` - Invalidate sitemap cache
"""

from swing_sitemap.tasks.submit_sitemap import (
    invalidate_sitemap_cache,
    submit_sitemap_periodic,
    submit_sitemap_task,
)

__all__ = [
    "invalidate_sitemap_cache",
    "submit_sitemap_periodic",
    "submit_sitemap_task",
]
