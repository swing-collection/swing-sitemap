# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.utils cache module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.sitemap.utils import (
    compress_content,
    decompress_content,
    get_cache,
    make_cache_key,
)
from swing.sitemap.utils.cache import (
    get_cached_sitemap,
    invalidate_cache,
    set_cached_sitemap,
)

pytestmark = pytest.mark.django_db

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


class TestCacheOperations:
    """Tests for cache get/set/invalidate operations."""

    def test_get_cached_sitemap_returns_none_when_not_cached(self, settings):
        """Test get_cached_sitemap returns None when key not in cache."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True}}
        result = get_cached_sitemap("nonexistent_key")
        assert result is None

    def test_set_and_get_cached_sitemap(self, settings):
        """Test setting and getting cached sitemap."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True, "timeout": 300}}
        key = "test_sitemap_key"
        content = b"<xml>test</xml>"

        set_cached_sitemap(key, content)
        result = get_cached_sitemap(key)

        assert result == content

    def test_set_cached_sitemap_with_timeout(self, settings):
        """Test setting cached sitemap with custom timeout."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True}}
        key = "test_timeout_key"
        content = b"<xml>test</xml>"

        set_cached_sitemap(key, content, timeout=60)
        result = get_cached_sitemap(key)

        assert result == content

    def test_invalidate_cache_all(self, settings):
        """Test invalidating all cache entries."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True}}
        # Should not raise - returns 0 when delete_pattern not supported
        result = invalidate_cache()
        assert result == 0  # LocMemCache doesn't support delete_pattern

    def test_invalidate_cache_by_key(self, settings):
        """Test invalidating specific cache key pattern."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True}}
        # Should not raise - returns 0 when delete_pattern not supported
        result = invalidate_cache("test_*")
        assert result == 0  # LocMemCache doesn't support delete_pattern

    def test_invalidate_cache_when_disabled(self, settings):
        """Test invalidate_cache returns 0 when cache disabled."""
        settings.SWING_SITEMAP = {"cache": {"enabled": False}}
        result = invalidate_cache()
        assert result == 0
