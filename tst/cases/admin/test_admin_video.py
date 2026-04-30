# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.admin module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from unittest.mock import Mock

from swing.sitemap.admin.admin_sitemap_url_video import VideoSitemapURLAdmin

# =============================================================================
# Tests
# =============================================================================


class TestVideoSitemapURLAdmin:
    """Tests for VideoSitemapURLAdmin."""

    def test_video_duration_display_none(self):
        """Test duration display when duration is None."""
        admin = VideoSitemapURLAdmin(Mock(), Mock())
        obj = Mock()
        obj.video_duration = None

        result = admin.video_duration_display(obj)
        assert result == "-"

    def test_video_duration_display_seconds_only(self):
        """Test duration display with only seconds."""
        admin = VideoSitemapURLAdmin(Mock(), Mock())
        obj = Mock()
        obj.video_duration = 45

        result = admin.video_duration_display(obj)
        assert result == "45s"

    def test_video_duration_display_minutes_and_seconds(self):
        """Test duration display with minutes and seconds."""
        admin = VideoSitemapURLAdmin(Mock(), Mock())
        obj = Mock()
        obj.video_duration = 125  # 2 minutes 5 seconds

        result = admin.video_duration_display(obj)
        assert result == "2m 5s"

    def test_video_duration_display_hours(self):
        """Test duration display with hours."""
        admin = VideoSitemapURLAdmin(Mock(), Mock())
        obj = Mock()
        obj.video_duration = 3725  # 1 hour 2 minutes 5 seconds

        result = admin.video_duration_display(obj)
        assert result == "1h 2m 5s"
