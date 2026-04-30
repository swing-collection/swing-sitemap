# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Pagination Utilities
=====================================

Utilities for paginating sitemaps.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Local
from .calculate_pages import calculate_pages
from .get_pagination_config import get_pagination_config
from .paginate_all_sitemaps import paginate_all_sitemaps
from .paginate_sitemap import paginate_sitemap
from .paginated_sitemap import PaginatedSitemap
from .should_paginate import should_paginate

# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "calculate_pages",
    "get_pagination_config",
    "paginate_all_sitemaps",
    "paginate_sitemap",
    "PaginatedSitemap",
    "should_paginate",
]
