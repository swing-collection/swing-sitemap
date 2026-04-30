# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_static module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest
from django.test import Client, RequestFactory

from swing.sitemap.views import StaticSitemapView, static_sitemap
from swing.sitemap.sitemaps import StaticSitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestStaticSitemapView:
    """Tests for StaticSitemapView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = StaticSitemapView()
        assert view.template_name == "sitemap_static.xml"

    def test_default_content_type(self):
        """Test default content type."""
        view = StaticSitemapView()
        assert view.content_type == "application/xml"

    def test_default_sitemap_class(self):
        """Test default sitemap class."""
        view = StaticSitemapView()
        assert view.sitemap_class == StaticSitemap

    def test_get_sitemap_returns_instance(self):
        """Test get_sitemap returns sitemap instance."""
        view = StaticSitemapView()
        sitemap = view.get_sitemap()

        assert isinstance(sitemap, StaticSitemap)
