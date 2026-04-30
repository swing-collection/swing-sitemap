# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Decompress Content
==================

Decompress gzip content.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import gzip

# =============================================================================
# Functions
# =============================================================================


def decompress_content(content: bytes) -> bytes:
    """
    Decompress gzip content.

    Args:
        content: Gzip-compressed content.

    Returns:
        Decompressed content bytes.
    """
    return gzip.decompress(content)


# =============================================================================
# Exports
# =============================================================================

__all__ = ["decompress_content"]
