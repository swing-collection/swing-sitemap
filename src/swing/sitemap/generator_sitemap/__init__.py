# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Generator
=========================

Provides views for generating sitemap XML responses.

.. deprecated:: 1.0
    Use :mod:`swing.sitemap.views` instead.

"""


# =============================================================================
# Imports
# =============================================================================

from swing.sitemap.views.template_sitemap_index import (
    sitemap_index as template_sitemap_index,
)

# Backwards compatibility alias
sitemap_index = template_sitemap_index


# =============================================================================
# Exports
# =============================================================================

__all__ = ["sitemap_index", "template_sitemap_index"]
