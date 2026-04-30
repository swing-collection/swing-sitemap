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
    def test_dry_run_does_not_clear(self):
        """Test that dry run doesn't actually clear."""
        out = StringIO()
        call_command("clear_sitemap_cache", "--dry-run", stdout=out)

        output = out.getvalue()
        assert "would" in output.lower()
