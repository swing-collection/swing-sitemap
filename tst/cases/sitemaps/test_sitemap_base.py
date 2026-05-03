# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.sitemaps.sitemap_base module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.contrib.sitemaps import Sitemap

from swing.sitemap.sitemaps.sitemap_base import BaseSitemap

# =============================================================================
# Tests
# =============================================================================


class TestBaseSitemap:
    """Tests for BaseSitemap class."""

    def test_inherits_from_django_sitemap(self):
        """Test that BaseSitemap inherits from Django's Sitemap."""
        assert issubclass(BaseSitemap, Sitemap)

    def test_is_abstract(self):
        """Test that BaseSitemap is abstract (ABC)."""
        # Import | Standard Library
        from abc import ABC

        assert issubclass(BaseSitemap, ABC)

    def test_has_items_method(self):
        """Test that BaseSitemap has items method."""
        assert hasattr(BaseSitemap, "items")

    def test_has_location_method(self):
        """Test that BaseSitemap has location method."""
        assert hasattr(BaseSitemap, "location")

    def test_location_with_kwargs(self):
        """Test location method resolves URL with kwargs."""
        from django.urls import path, reverse

        # Create a concrete sitemap class
        class TestSitemap(BaseSitemap):
            def items(self):
                return [
                    {"view_name": "swing-sitemap-index"},
                    {"view_name": "swing-sitemap-section", "kwargs": {"section": "static"}},
                ]

        sitemap = TestSitemap()

        # Test without kwargs
        items = sitemap.items()
        url1 = sitemap.location(items[0])
        assert url1 == reverse("swing-sitemap-index")

        # Test with kwargs
        url2 = sitemap.location(items[1])
        assert "static" in url2
