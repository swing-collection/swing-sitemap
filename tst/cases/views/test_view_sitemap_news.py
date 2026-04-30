# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_news module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest
from django.test import Client, RequestFactory

from swing.sitemap.views import NewsSitemapView, news_sitemap
from swing.sitemap.sitemaps import NewsSitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestNewsSitemapView:
    """Tests for NewsSitemapView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = NewsSitemapView()
        assert view.template_name == "sitemap_news.xml"

    def test_default_content_type(self):
        """Test default content type."""
        view = NewsSitemapView()
        assert view.content_type == "application/xml"

    def test_default_sitemap_class(self):
        """Test default sitemap class."""
        view = NewsSitemapView()
        assert view.sitemap_class == NewsSitemap

    def test_get_sitemap_returns_instance(self):
        """Test get_sitemap returns sitemap instance."""
        view = NewsSitemapView()
        sitemap = view.get_sitemap()

        assert isinstance(sitemap, NewsSitemap)
