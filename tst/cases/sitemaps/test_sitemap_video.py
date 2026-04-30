# -*- coding: utf-8 -*-

"""
Tests for Video Sitemap
=======================
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import datetime
from unittest.mock import Mock, patch

from django.test import override_settings

# Import | Libraries
import pytest

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

    def test_video_rating(self):
        """Test video_rating method."""
        video = Mock()
        video.video_rating = 4.5
        sitemap = VideoSitemap(queryset=[video])

        rating = sitemap.video_rating(video)
        assert rating == 4.5

    def test_video_rating_clamped(self):
        """Test video rating is clamped to valid range."""
        video = Mock()
        video.video_rating = 6.0  # Above max
        sitemap = VideoSitemap(queryset=[video])

        rating = sitemap.video_rating(video)
        assert rating == 5.0

        video.video_rating = -1.0  # Below min
        rating = sitemap.video_rating(video)
        assert rating == 0.0

    def test_video_view_count(self):
        """Test video_view_count method."""
        video = Mock()
        video.video_view_count = 12345
        sitemap = VideoSitemap(queryset=[video])

        count = sitemap.video_view_count(video)
        assert count == 12345

    def test_video_family_friendly(self):
        """Test video_family_friendly method."""
        video = Mock()
        video.video_family_friendly = True
        sitemap = VideoSitemap(queryset=[video])

        result = sitemap.video_family_friendly(video)
        assert result == "yes"

        video.video_family_friendly = False
        result = sitemap.video_family_friendly(video)
        assert result == "no"

    def test_video_restriction(self):
        """Test video_restriction method."""
        video = Mock()
        video.video_restriction = {"relationship": "deny", "countries": "US GB"}
        sitemap = VideoSitemap(queryset=[video])

        result = sitemap.video_restriction(video)
        assert result == {"relationship": "deny", "countries": "US GB"}

    def test_video_platform(self):
        """Test video_platform method."""
        video = Mock()
        video.video_platform = {"relationship": "allow", "platforms": "web mobile"}
        sitemap = VideoSitemap(queryset=[video])

        result = sitemap.video_platform(video)
        assert result == {"relationship": "allow", "platforms": "web mobile"}

    def test_video_tags(self):
        """Test video_tags method."""
        video = Mock()
        video.video_tags = ["tag1", "tag2", "tag3"]
        sitemap = VideoSitemap(queryset=[video])

        tags = sitemap.video_tags(video)
        assert tags == ["tag1", "tag2", "tag3"]

    def test_video_category(self):
        """Test video_category method."""
        video = Mock()
        video.video_category = "Technology"
        sitemap = VideoSitemap(queryset=[video])

        category = sitemap.video_category(video)
        assert category == "Technology"

    def test_video_uploader(self):
        """Test video_uploader method."""
        video = Mock()
        video.video_uploader = {"name": "John Doe", "info": "https://example.com/john"}
        sitemap = VideoSitemap(queryset=[video])

        uploader = sitemap.video_uploader(video)
        assert uploader == {"name": "John Doe", "info": "https://example.com/john"}

    def test_video_live(self):
        """Test video_live method."""
        video = Mock()
        video.video_live = True
        sitemap = VideoSitemap(queryset=[video])

        result = sitemap.video_live(video)
        assert result == "yes"

    def test_video_requires_subscription(self):
        """Test video_requires_subscription method."""
        video = Mock()
        video.video_requires_subscription = True
        sitemap = VideoSitemap(queryset=[video])

        result = sitemap.video_requires_subscription(video)
        assert result == "yes"

    def test_video_player_loc(self):
        """Test video_player_loc method."""
        video = Mock()
        video.video_player_url = "https://example.com/player/1"
        sitemap = VideoSitemap(queryset=[video])

        player = sitemap.video_player_loc(video)
        assert player == "https://example.com/player/1"

    def test_video_expiration_date(self):
        """Test video_expiration_date method."""
        video = Mock()
        video.video_expiration_date = datetime.date(2025, 12, 31)
        sitemap = VideoSitemap(queryset=[video])

        exp_date = sitemap.video_expiration_date(video)
        assert exp_date == "2025-12-31"

    def test_video_publication_date(self):
        """Test video_publication_date method."""
        video = Mock()
        video.video_publication_date = datetime.datetime(2024, 1, 15, 10, 30, 0)
        sitemap = VideoSitemap(queryset=[video])

        pub_date = sitemap.video_publication_date(video)
        assert "2024-01-15" in pub_date

    def test_validate_item_missing_fields(self):
        """Test _validate_item with missing required fields."""
        video = Mock(spec=[])  # No video attributes
        sitemap = VideoSitemap(queryset=[video])

        is_valid, errors = sitemap._validate_item(video)
        assert not is_valid
        assert len(errors) > 0


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
