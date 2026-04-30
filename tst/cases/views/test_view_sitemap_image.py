# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_image module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.views import ImageSitemapView
from swing.sitemap.sitemaps import ImageSitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestImageSitemapView:
    """Tests for ImageSitemapView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = ImageSitemapView()
        assert view.template_name == "swing/sitemap/sitemap_image.xml"

    def test_default_content_type(self):
        """Test default content type."""
        view = ImageSitemapView()
        assert view.content_type == "application/xml"

    def test_default_sitemap_class(self):
        """Test default sitemap class."""
        view = ImageSitemapView()
        assert view.sitemap_class == ImageSitemap

    def test_get_sitemap_returns_instance(self):
        """Test get_sitemap returns sitemap instance."""
        view = ImageSitemapView()
        sitemap = view.get_sitemap()

        assert isinstance(sitemap, ImageSitemap)
