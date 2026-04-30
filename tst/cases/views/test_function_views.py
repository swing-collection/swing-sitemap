# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for function-based sitemap views."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.test import RequestFactory

# Import | Libraries
import pytest

from swing.sitemap.views.image_sitemap import image_sitemap
from swing.sitemap.views.news_sitemap import news_sitemap
from swing.sitemap.views.static_sitemap import static_sitemap
from swing.sitemap.views.video_sitemap import video_sitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestFunctionBasedViews:
    """Tests for function-based sitemap views."""

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    def test_image_sitemap_view(self, factory, settings):
        """Test image_sitemap function view returns XML."""
        settings.SWING_SITEMAP = {"static": {"views": []}}
        request = factory.get("/sitemap-image.xml")
        response = image_sitemap(request)
        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"

    def test_news_sitemap_view(self, factory, settings):
        """Test news_sitemap function view returns XML."""
        settings.SWING_SITEMAP = {"static": {"views": []}}
        request = factory.get("/sitemap-news.xml")
        response = news_sitemap(request)
        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"

    def test_static_sitemap_view(self, factory, settings):
        """Test static_sitemap function view returns XML."""
        settings.SWING_SITEMAP = {"static": {"views": []}}
        request = factory.get("/sitemap-static.xml")
        response = static_sitemap(request)
        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"

    def test_video_sitemap_view(self, factory, settings):
        """Test video_sitemap function view returns XML."""
        settings.SWING_SITEMAP = {"static": {"views": []}}
        request = factory.get("/sitemap-video.xml")
        response = video_sitemap(request)
        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"
