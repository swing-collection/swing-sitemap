# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.management.commands.generate_sitemap module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from io import StringIO
from unittest.mock import MagicMock, patch

from django.contrib.sitemaps import Sitemap
from django.core.management import call_command
from django.core.management.base import CommandError

# Import | Libraries
import pytest

# =============================================================================
# Tests
# =============================================================================

class SimpleSitemap(Sitemap):
    """Simple sitemap for testing."""
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["page1", "page2"]

    def location(self, item):
        return f"/{item}/"


@pytest.mark.django_db
class TestGenerateSitemapCommand:
    """Tests for generate_sitemap management command."""

    def test_command_exists(self):
        """Test that command can be loaded."""
        from swing.sitemap.management.commands.generate_sitemap import Command

        assert Command is not None

    def test_command_has_help_attribute(self):
        """Test that command has help text."""
        from swing.sitemap.management.commands.generate_sitemap import Command

        assert hasattr(Command, "help")
        assert Command.help is not None

    @patch("swing.sitemap.management.commands.generate_sitemap.default_sitemaps")
    def test_no_sitemaps_raises_error(self, mock_sitemaps):
        """Test error when no sitemaps configured."""
        mock_sitemaps.return_value = {}

        with pytest.raises(CommandError) as exc_info:
            call_command("generate_sitemap")
        assert "no sitemaps" in str(exc_info.value).lower()

    @patch("swing.sitemap.management.commands.generate_sitemap.default_sitemaps")
    def test_warns_about_missing_sections(self, mock_sitemaps):
        """Test warning when requested sections not found."""
        mock_sitemaps.return_value = {"static": MagicMock()}

        err = StringIO()
        with pytest.raises(CommandError):
            call_command("generate_sitemap", sections=["nonexistent"], stderr=err)

    def test_add_arguments(self):
        """Test command adds expected arguments."""
        # Import | Standard Library
        from argparse import ArgumentParser

        from swing.sitemap.management.commands.generate_sitemap import Command

        cmd = Command()
        parser = ArgumentParser()
        cmd.add_arguments(parser)

        # Check parser has the expected options
        actions = {a.dest for a in parser._actions}
        assert "output" in actions
        assert "output_dir" in actions
        assert "sections" in actions
        assert "with_index" in actions
        assert "domain" in actions
        assert "protocol" in actions
        assert "paginate" in actions

    def test_generate_sitemap_index_method(self):
        """Test _generate_sitemap_index method."""
        # Import | Standard Library

        from swing.sitemap.management.commands.generate_sitemap import Command

        cmd = Command()
        sitemaps = {"static": SimpleSitemap}

        result = cmd._generate_sitemap_index(sitemaps, "example.com", "https")

        assert "sitemapindex" in result
        assert "https://example.com" in result

    def test_generate_sitemap_index_with_lastmod(self):
        """Test _generate_sitemap_index includes lastmod."""
        # Import | Standard Library
        from datetime import datetime

        from swing.sitemap.management.commands.generate_sitemap import Command

        cmd = Command()

        class SitemapWithLastmod(SimpleSitemap):
            def get_latest_lastmod(self):
                return datetime(2024, 1, 15, 10, 30)

        sitemaps = {"static": SitemapWithLastmod}

        with patch(
            "swing.sitemap.management.commands.generate_sitemap.get_sitemap_index_urls"
        ) as mock_get_urls:
            mock_get_urls.return_value = [
                {"location": "sitemap-static.xml", "lastmod": datetime(2024, 1, 15)}
            ]
            result = cmd._generate_sitemap_index(sitemaps, "example.com", "https")

            assert "lastmod" in result
            assert "2024" in result
