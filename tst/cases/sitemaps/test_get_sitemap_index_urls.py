# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


"""
Tests for swing.sitemap.sitemaps.get_sitemap_index_urls module.
"""


# Import | Future
from __future__ import annotations

# Import | Standard Library
from datetime import datetime
from unittest.mock import MagicMock

from django.contrib.sitemaps import Sitemap


class TestGetSitemapIndexUrls:
    """Tests for get_sitemap_index_urls function."""

    def test_empty_sitemaps(self):
        """Test with empty sitemaps dict."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        result = get_sitemap_index_urls({})
        assert result == []

    def test_single_sitemap_instance(self):
        """Test with single sitemap instance."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        class TestSitemap(Sitemap):
            def items(self):
                return ["item"]

            def location(self, item):
                return f"/{item}/"

        result = get_sitemap_index_urls({"test": TestSitemap()})

        assert len(result) == 1
        assert result[0]["name"] == "test"
        assert result[0]["location"] == "sitemap-test.xml"

    def test_sitemap_class_instantiated(self):
        """Test that sitemap classes are instantiated."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        class TestSitemap(Sitemap):
            def items(self):
                return ["item"]

            def location(self, item):
                return f"/{item}/"

        result = get_sitemap_index_urls({"test": TestSitemap})  # Pass class, not instance

        assert len(result) == 1
        assert result[0]["name"] == "test"

    def test_sitemap_with_lastmod(self):
        """Test sitemap with get_latest_lastmod."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        class TestSitemap(Sitemap):
            def items(self):
                return ["item"]

            def location(self, item):
                return f"/{item}/"

            def get_latest_lastmod(self):
                return datetime(2024, 1, 15)

        result = get_sitemap_index_urls({"test": TestSitemap()})

        assert len(result) == 1
        assert result[0]["lastmod"] == datetime(2024, 1, 15)

    def test_sitemap_lastmod_exception_handled(self):
        """Test that lastmod exceptions are handled gracefully."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        mock_sitemap = MagicMock()
        mock_sitemap.get_latest_lastmod.side_effect = Exception("Error")

        result = get_sitemap_index_urls({"test": mock_sitemap})

        assert len(result) == 1
        assert "lastmod" not in result[0]

    def test_multiple_sitemaps(self):
        """Test with multiple sitemaps."""
        from swing.sitemap.sitemaps.get_sitemap_index_urls import (
            get_sitemap_index_urls,
        )

        class Sitemap1(Sitemap):
            def items(self):
                return []

        class Sitemap2(Sitemap):
            def items(self):
                return []

        result = get_sitemap_index_urls({
            "static": Sitemap1(),
            "pages": Sitemap2(),
        })

        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "static" in names
        assert "pages" in names
