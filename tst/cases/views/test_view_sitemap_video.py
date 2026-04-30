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

from __future__ import annotations

import pytest
from django.test import Client, RequestFactory

from swing.sitemap.views import VideoSitemapView, video_sitemap
from swing.sitemap.sitemaps import VideoSitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Class-Based View Attributes
# =============================================================================


class TestVideoSitemapView:
    """Tests for VideoSitemapView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = VideoSitemapView()
        assert view.template_name == "sitemap_video.xml"

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
