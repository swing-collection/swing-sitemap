# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.management.commands.validate_sitemap module.
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
from django.core.management.base import CommandError

# Import | Libraries
import pytest

# =============================================================================
# Tests
# =============================================================================

@pytest.mark.django_db
class TestValidateSitemapCommand:
    """Tests for validate_sitemap management command."""

    def test_command_exists(self):
        """Test that command can be loaded."""
        from swing.sitemap.management.commands.validate_sitemap import Command

        assert Command is not None

    def test_command_has_help_attribute(self):
        """Test that command has help text."""
        from swing.sitemap.management.commands.validate_sitemap import Command

        assert hasattr(Command, "help")
        assert Command.help is not None

    def test_requires_source_or_all(self):
        """Test command requires either source or --all."""
        with pytest.raises(CommandError) as exc_info:
            call_command("validate_sitemap")
        assert "source" in str(exc_info.value).lower() or "all" in str(exc_info.value).lower()

    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(CommandError) as exc_info:
            call_command("validate_sitemap", "/nonexistent/path/sitemap.xml")
        assert "not found" in str(exc_info.value).lower()

    @patch("swing.sitemap.management.commands.validate_sitemap.default_sitemaps")
    def test_validate_all_no_sitemaps(self, mock_sitemaps):
        """Test --all with no sitemaps configured."""
        mock_sitemaps.return_value = {}

        out = StringIO()
        call_command("validate_sitemap", all=True, stdout=out)

        output = out.getvalue()
        assert "no sitemaps" in output.lower()

    def test_command_constants(self):
        """Test command has correct limit constants."""
        from swing.sitemap.management.commands.validate_sitemap import Command

        assert Command.MAX_URLS == 50000
        assert Command.MAX_SIZE_BYTES == 50 * 1024 * 1024
        assert Command.MAX_URL_LENGTH == 2048

    def test_add_arguments(self):
        """Test command adds expected arguments."""
        # Import | Standard Library
        from argparse import ArgumentParser

        from swing.sitemap.management.commands.validate_sitemap import Command

        cmd = Command()
        parser = ArgumentParser()
        cmd.add_arguments(parser)

        # Check parser has the expected options
        actions = {a.dest for a in parser._actions}
        assert "source" in actions
        assert "all" in actions
        assert "strict" in actions
        assert "verbose_output" in actions
