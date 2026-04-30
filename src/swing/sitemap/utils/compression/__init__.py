# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Compression Utilities
======================================

Utilities for compressing and decompressing sitemap content.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from .compress_content import compress_content
from .decompress_content import decompress_content


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "compress_content",
    "decompress_content",
]
