# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.apps module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from swing.sitemap.apps import SwingSitemapConfig


# =============================================================================
# Tests
# =============================================================================


class TestSwingSitemapConfig:
    """Tests for SwingSitemapConfig."""

    def test_app_name(self):
        """Test app name is correct."""
        assert SwingSitemapConfig.name == "swing.sitemap"

    def test_app_label(self):
        """Test app label is correct."""
        assert SwingSitemapConfig.label == "swing_sitemap"

    def test_verbose_name(self):
        """Test verbose name is set."""
        assert SwingSitemapConfig.verbose_name is not None

    def test_default_auto_field(self):
        """Test default auto field is BigAutoField."""
        assert SwingSitemapConfig.default_auto_field == "django.db.models.BigAutoField"
