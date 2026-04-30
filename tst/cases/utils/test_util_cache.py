# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.utils.util_cache module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from swing.sitemap.utils.util_cache import (
    compress_content,
    decompress_content,
    get_cache,
    make_cache_key,
)


# =============================================================================
# Tests
# =============================================================================


class TestCacheFunctions:
    """Tests for cache utility functions."""

    def test_make_cache_key(self):
        """Test cache key generation."""
        key = make_cache_key("sitemap", "static")
        assert "sitemap" in key
        assert "static" in key

    def test_make_cache_key_unique(self):
        """Test that different inputs produce different keys."""
        key1 = make_cache_key("sitemap", "static")
        key2 = make_cache_key("sitemap", "news")
        assert key1 != key2

    def test_get_cache_returns_cache(self):
        """Test get_cache returns a cache instance."""
        cache = get_cache()
        assert cache is not None

    def test_compress_content(self):
        """Test content compression."""
        content = b"<xml>test content</xml>" * 100
        compressed = compress_content(content)

        # Compressed should be smaller for repetitive content
        assert len(compressed) < len(content)

    def test_decompress_content(self):
        """Test content decompression."""
        original = b"<xml>test content</xml>"
        compressed = compress_content(original)
        decompressed = decompress_content(compressed)

        assert decompressed == original

    def test_compress_decompress_roundtrip(self):
        """Test compress/decompress roundtrip."""
        original = b"Test sitemap content with various characters: <>&'\""
        compressed = compress_content(original)
        decompressed = decompress_content(compressed)

        assert decompressed == original
