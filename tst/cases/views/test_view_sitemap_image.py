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

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.sitemap.sitemaps import ImageSitemap
from swing.sitemap.views import ImageSitemapView

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

    def test_get_request_returns_xml_response(self):
        """Test GET request returns XML response."""
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get("/sitemap-image.xml")

        view = ImageSitemapView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert "application/xml" in response["Content-Type"]
