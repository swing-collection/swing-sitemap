# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_index module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.views import SitemapIndexView

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestSitemapIndexView:
    """Tests for SitemapIndexView class-based view."""

    def test_default_sitemap_url_name(self):
        """Test default sitemap URL name."""
        view = SitemapIndexView()
        assert view.sitemap_url_name == "swing-sitemap-section"

    def test_default_sitemaps_is_none(self):
        """Test default sitemaps is None (uses auto-discovery)."""
        view = SitemapIndexView()
        assert view.sitemaps is None

    def test_custom_sitemaps(self):
        """Test view can accept custom sitemaps."""
        custom_sitemaps = {"custom": object}
        view = SitemapIndexView()
        view.sitemaps = custom_sitemaps
        sitemaps = view.get_sitemaps()

        assert sitemaps == custom_sitemaps

    def test_get_sitemap_url_name(self):
        """Test get_sitemap_url_name method."""
        view = SitemapIndexView()
        assert view.get_sitemap_url_name() == "swing-sitemap-section"
