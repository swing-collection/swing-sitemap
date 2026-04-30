# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.management.commands.submit_sitemap module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


# =============================================================================
# Tests
# =============================================================================


class TestSubmitSitemapCommand:
    """Tests for submit_sitemap management command."""

    def test_command_exists(self):
        """Test that command can be loaded."""
        from swing.sitemap.management.commands.submit_sitemap import Command

        assert Command is not None

    @patch("swing.sitemap.management.commands.submit_sitemap.submit_sitemap")
    def test_submit_with_url_argument(self, mock_submit):
        """Test submitting with URL argument."""
        mock_submit.return_value = {"google": 200, "bing": 200}

        out = StringIO()
        call_command(
            "submit_sitemap",
            "https://example.com/sitemap.xml",
            stdout=out,
        )

        mock_submit.assert_called_once()

    def test_dry_run_does_not_submit(self):
        """Test that dry run doesn't actually submit."""
        out = StringIO()
        call_command(
            "submit_sitemap",
            "https://example.com/sitemap.xml",
            "--dry-run",
            stdout=out,
        )

        output = out.getvalue()
        assert "Would submit" in output

    def test_missing_url_raises_error(self):
        """Test that missing URL raises error when not configured."""
        with pytest.raises(CommandError):
            call_command("submit_sitemap")
