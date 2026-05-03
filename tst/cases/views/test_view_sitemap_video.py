# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_video module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.sitemap.sitemaps import VideoSitemap
from swing.sitemap.views import VideoSitemapView

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestVideoSitemapView:
    """Tests for VideoSitemapView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = VideoSitemapView()
        assert view.template_name == "swing/sitemap/sitemap_video.xml"

    def test_default_content_type(self):
        """Test default content type."""
        view = VideoSitemapView()
        assert view.content_type == "application/xml"

    def test_default_sitemap_class(self):
        """Test default sitemap class."""
        view = VideoSitemapView()
        assert view.sitemap_class == VideoSitemap

    def test_get_sitemap_returns_instance(self):
        """Test get_sitemap returns sitemap instance."""
        view = VideoSitemapView()
        sitemap = view.get_sitemap()

        assert isinstance(sitemap, VideoSitemap)

    def test_get_request_returns_xml_response(self):
        """Test GET request returns XML response."""
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get("/sitemap-video.xml")

        view = VideoSitemapView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert "application/xml" in response["Content-Type"]
