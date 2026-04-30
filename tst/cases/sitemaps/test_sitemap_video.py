# -*- coding: utf-8 -*-

"""
Tests for Video Sitemap
=======================
"""

import datetime
from unittest.mock import Mock, patch

import pytest
from django.test import override_settings

from swing.sitemap.sitemaps.sitemap_video import VideoSitemap


class MockVideo:
    """Mock video model for testing."""

    def __init__(
        self,
        pk=1,
        title="Test Video",
        description="Test description",
        thumbnail_url="https://example.com/thumb.jpg",
        video_url="https://example.com/video.mp4",
        duration=300,
        publication_date=None,
    ):
        self.pk = pk
        self.video_title = title
        self.video_description = description
        self.video_thumbnail_url = thumbnail_url
        self.video_content_url = video_url
        self.video_duration = duration
        self.video_publication_date = publication_date or datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def get_absolute_url(self):
        return f"https://example.com/videos/{self.pk}/"


class TestVideoSitemap:
    """Test VideoSitemap class."""

    def test_init_with_queryset(self):
        """Test initialization with queryset."""
        videos = [MockVideo(pk=1), MockVideo(pk=2)]
        sitemap = VideoSitemap(queryset=videos)

        items = list(sitemap.items())
        assert len(items) == 2

    def test_init_with_callable(self):
        """Test initialization with callable queryset."""
        videos = [MockVideo(pk=1)]
        sitemap = VideoSitemap(queryset=lambda: videos)

        items = list(sitemap.items())
        assert len(items) == 1

    def test_location(self):
        """Test location method."""
        video = MockVideo(pk=1)
        sitemap = VideoSitemap(queryset=[video])

        assert sitemap.location(video) == "https://example.com/videos/1/"

    def test_lastmod(self):
        """Test lastmod method."""
        video = MockVideo(pk=1)
        sitemap = VideoSitemap(queryset=[video], date_field="updated_at")

        lastmod = sitemap.lastmod(video)
        assert lastmod is not None
        assert isinstance(lastmod, datetime.datetime)

    def test_video_title(self):
        """Test video_title method."""
        video = MockVideo(pk=1, title="<Test> Video & Title")
        sitemap = VideoSitemap(queryset=[video])

        title = sitemap.video_title(video)
        assert title is not None
        # Should be escaped
        assert "<" not in title
        assert "&" not in title or "&amp;" in title

    def test_video_title_truncation(self):
        """Test video title is truncated to 100 chars."""
        long_title = "A" * 200
        video = MockVideo(pk=1, title=long_title)
        sitemap = VideoSitemap(queryset=[video])

        title = sitemap.video_title(video)
        assert len(title) <= 100

    def test_video_description(self):
        """Test video_description method."""
        video = MockVideo(pk=1, description="Test description")
        sitemap = VideoSitemap(queryset=[video])

        desc = sitemap.video_description(video)
        assert desc == "Test description"

    def test_video_description_truncation(self):
        """Test video description is truncated to 2048 chars."""
        long_desc = "B" * 3000
        video = MockVideo(pk=1, description=long_desc)
        sitemap = VideoSitemap(queryset=[video])

        desc = sitemap.video_description(video)
        assert len(desc) <= 2048

    def test_video_duration(self):
        """Test video_duration method."""
        video = MockVideo(pk=1, duration=300)
        sitemap = VideoSitemap(queryset=[video])

        duration = sitemap.video_duration(video)
        assert duration == 300

    def test_video_duration_clamped(self):
        """Test video duration is clamped to valid range."""
        # Test minimum
        video = MockVideo(pk=1, duration=0)
        sitemap = VideoSitemap(queryset=[video])
        assert sitemap.video_duration(video) == 1

        # Test maximum
        video = MockVideo(pk=2, duration=50000)
        assert sitemap.video_duration(video) == 28800

    def test_video_thumbnail_loc(self):
        """Test video_thumbnail_loc method."""
        video = MockVideo(pk=1, thumbnail_url="https://example.com/thumb.jpg")
        sitemap = VideoSitemap(queryset=[video])

        thumb = sitemap.video_thumbnail_loc(video)
        assert thumb == "https://example.com/thumb.jpg"

    def test_build_video_xml(self):
        """Test _build_video_xml method."""
        video = MockVideo(
            pk=1,
            title="Test Video",
            description="Test description",
            thumbnail_url="https://example.com/thumb.jpg",
            video_url="https://example.com/video.mp4",
            duration=300,
        )
        sitemap = VideoSitemap(queryset=[video])

        xml = sitemap._build_video_xml(video)

        assert "<video:video>" in xml
        assert "</video:video>" in xml
        assert "<video:thumbnail_loc>" in xml
        assert "<video:title>" in xml
        assert "<video:description>" in xml
        assert "<video:content_loc>" in xml
        assert "<video:duration>300</video:duration>" in xml

    def test_urls_includes_video_data(self):
        """Test that _urls method includes video XML."""
        video = MockVideo(pk=1)
        sitemap = VideoSitemap(queryset=[video])

        urls = sitemap._urls(1, "https", "example.com")

        assert len(urls) == 1
        assert "videos" in urls[0]
        assert "<video:video>" in urls[0]["videos"]

    def test_default_priority_and_changefreq(self):
        """Test default priority and changefreq."""
        sitemap = VideoSitemap(queryset=[])

        assert sitemap.priority == 0.8
        assert sitemap.changefreq == "weekly"

    def test_custom_priority_and_changefreq(self):
        """Test custom priority and changefreq."""
        sitemap = VideoSitemap(queryset=[], priority=0.9, changefreq="daily")

        assert sitemap.priority == 0.9
        assert sitemap.changefreq == "daily"

    def test_custom_video_fields(self):
        """Test custom video field mappings."""
        video = Mock()
        video.my_title = "Custom Title"
        video.my_thumb = "https://example.com/custom.jpg"
        video.my_desc = "Custom description"
        video.get_absolute_url = lambda: "https://example.com/video/1/"

        sitemap = VideoSitemap(
            queryset=[video],
            video_fields={
                "title": "my_title",
                "thumbnail_loc": "my_thumb",
                "description": "my_desc",
            },
        )

        assert sitemap.video_title(video) == "Custom Title"
        assert sitemap.video_thumbnail_loc(video) == "https://example.com/custom.jpg"
        assert sitemap.video_description(video) == "Custom description"


@pytest.mark.django_db
class TestVideoSitemapFromSettings:
    """Test VideoSitemap.from_settings method."""

    @override_settings(
        SWING_SITEMAP={
            "video": {
                "model": "auth.User",
                "filters": {"is_active": True},
                "date_field": "date_joined",
            },
        }
    )
    def test_from_settings_video_config(self):
        """Test building from SWING_SITEMAP['video'] config."""
        sitemap = VideoSitemap.from_settings()
        assert sitemap is not None
        assert sitemap.date_field == "date_joined"

    def test_from_settings_missing_model_raises(self):
        """Test that missing model raises ValueError."""
        with pytest.raises(ValueError, match="must define a 'model'"):
            VideoSitemap.from_settings("nonexistent")
