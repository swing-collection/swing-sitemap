# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url_video module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.sitemap.models import VideoSitemapURL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestVideoSitemapURL:
    """Tests for VideoSitemapURL model."""

    def test_create_video_url(self):
        """Test creating a VideoSitemapURL instance."""
        url = VideoSitemapURL.objects.create(
            url="https://example.com/videos/1/",
            video_thumbnail_url="https://example.com/thumbs/1.jpg",
            video_title="Sample Video",
            video_description="A sample video for testing",
            video_content_url="https://example.com/videos/sample.mp4",
            video_duration=300,
            changefreq="weekly",
        )
        assert url.pk is not None
        assert url.video_title == "Sample Video"

    def test_video_content_url_field(self):
        """Test video_content_url field."""
        url = VideoSitemapURL(
            url="https://example.com/videos/1/",
            video_content_url="https://example.com/videos/sample.mp4",
            video_title="Test",
            video_description="Test",
            video_thumbnail_url="https://example.com/thumb.jpg",
            video_duration=100,
        )
        assert url.video_content_url == "https://example.com/videos/sample.mp4"

    def test_video_duration_field(self):
        """Test video_duration field."""
        url = VideoSitemapURL(
            url="https://example.com/videos/1/",
            video_duration=300,
            video_title="Test",
            video_description="Test",
            video_thumbnail_url="https://example.com/thumb.jpg",
            video_content_url="https://example.com/video.mp4",
        )
        assert url.video_duration == 300

    def test_str_representation(self):
        """Test string representation."""
        url = VideoSitemapURL(
            url="https://example.com/videos/1/",
            video_title="Sample Video",
            video_description="Test",
            video_thumbnail_url="https://example.com/thumb.jpg",
            video_content_url="https://example.com/video.mp4",
            video_duration=100,
        )
        assert "Sample Video" in str(url)
