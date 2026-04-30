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

from __future__ import annotations



# =============================================================================
# Tests
# =============================================================================


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
