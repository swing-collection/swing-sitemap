# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.management.commands.clear_sitemap_cache module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import override_settings

# =============================================================================
# Tests
# =============================================================================


class TestClearSitemapCacheCommand:
    """Tests for clear_sitemap_cache management command."""

    def test_command_exists(self):
        """Test that command can be loaded."""
        from swing.sitemap.management.commands.clear_sitemap_cache import (
            Command,
        )

        assert Command is not None

    def test_warns_when_cache_disabled(self):
        """Test that command warns when caching is disabled."""
        out = StringIO()
        call_command("clear_sitemap_cache", stdout=out)

        output = out.getvalue()
        assert "not enabled" in output.lower() or "caching" in output.lower()

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    def test_dry_run_mode(self):
        """Test dry run mode doesn't clear cache."""
        out = StringIO()
        call_command("clear_sitemap_cache", dry_run=True, stdout=out)

        output = out.getvalue()
        assert "would clear" in output.lower()

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    def test_dry_run_with_section(self):
        """Test dry run with specific section."""
        out = StringIO()
        call_command("clear_sitemap_cache", dry_run=True, section="static", stdout=out)

        output = out.getvalue()
        assert "static" in output.lower()

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    @patch("swing.sitemap.management.commands.clear_sitemap_cache.invalidate_cache")
    def test_clears_all_cache(self, mock_invalidate):
        """Test clearing all cache entries."""
        mock_invalidate.return_value = 5

        out = StringIO()
        call_command("clear_sitemap_cache", stdout=out)

        output = out.getvalue()
        assert "cleared" in output.lower()
        mock_invalidate.assert_called_once_with(None)

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    @patch("swing.sitemap.management.commands.clear_sitemap_cache.invalidate_cache")
    def test_clears_section_cache(self, mock_invalidate):
        """Test clearing specific section cache."""
        mock_invalidate.return_value = 2

        out = StringIO()
        call_command("clear_sitemap_cache", section="video", stdout=out)

        output = out.getvalue()
        assert "cleared" in output.lower()
        mock_invalidate.assert_called_once_with("*video*")

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    @patch("swing.sitemap.management.commands.clear_sitemap_cache.invalidate_cache")
    def test_clears_zero_entries(self, mock_invalidate):
        """Test when no cache entries cleared."""
        mock_invalidate.return_value = 0

        out = StringIO()
        call_command("clear_sitemap_cache", stdout=out)

        output = out.getvalue()
        assert "cleared" in output.lower()

    @override_settings(SWING_SITEMAP={"cache": {"enabled": True}})
    def test_dry_run_does_not_clear(self):
        """Test that dry run doesn't actually clear."""
        out = StringIO()
        call_command("clear_sitemap_cache", "--dry-run", stdout=out)

        output = out.getvalue()
        assert "would" in output.lower()
