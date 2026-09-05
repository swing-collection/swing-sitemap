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

# Import | Future
from __future__ import annotations

# Import | Standard Library
from unittest.mock import patch

# Import | Libraries
import pytest

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


class TestSwingSitemapConfigValidation:
    """Tests for SwingSitemapConfig validation methods."""

    def test_validate_settings_with_warnings(self):
        """Test _validate_settings logs warnings."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch(
            "swing.sitemap.conf.validate_settings.validate_settings"
        ) as mock_validate:
            mock_validate.return_value = (True, ["test warning"])
            with patch("swing.sitemap.apps.logger") as mock_logger:
                config._validate_settings()
                mock_logger.warning.assert_called()

    def test_validate_settings_failure(self):
        """Test _validate_settings handles validation failures."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch(
            "swing.sitemap.conf.validate_settings.validate_settings"
        ) as mock_validate:
            mock_validate.return_value = (False, ["critical issue"])
            with patch("swing.sitemap.apps.logger") as mock_logger:
                config._validate_settings()
                # Should log warnings
                assert mock_logger.warning.called

    def test_validate_settings_exception(self):
        """Test _validate_settings handles exceptions gracefully."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch(
            "swing.sitemap.conf.validate_settings.validate_settings"
        ) as mock_validate:
            mock_validate.side_effect = Exception("Test error")
            with patch("swing.sitemap.apps.logger") as mock_logger:
                # Should not raise
                config._validate_settings()
                mock_logger.error.assert_called()

    def test_register_signals_disabled(self):
        """Test _register_signals does nothing when signals disabled."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch("swing.sitemap.conf.get_setting") as mock_get_setting:
            mock_get_setting.return_value = {"enabled": False}
            # Should return early without registering
            config._register_signals()

    def test_register_signals_enabled_with_models(self):
        """Test _register_signals registers when enabled with models."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch("swing.sitemap.conf.get_setting") as mock_get_setting:
            mock_get_setting.return_value = {"enabled": True, "models": ["myapp.MyModel"]}
            with patch(
                "swing.sitemap.signals.register_sitemap_signals"
            ) as mock_register:
                with patch("swing.sitemap.apps.logger") as mock_logger:
                    config._register_signals()
                    mock_register.assert_called_once_with(["myapp.MyModel"])
                    mock_logger.info.assert_called()

    def test_register_signals_exception(self):
        """Test _register_signals handles exceptions gracefully."""
        config = SwingSitemapConfig("swing.sitemap", __import__("swing.sitemap"))

        with patch("swing.sitemap.conf.get_setting") as mock_get_setting:
            mock_get_setting.side_effect = Exception("Test error")
            with patch("swing.sitemap.apps.logger") as mock_logger:
                # Should not raise
                config._register_signals()
                mock_logger.warning.assert_called()


class TestModuleLazyImports:
    """Tests for lazy imports in swing.sitemap."""

    def test_getattr_lazy_import(self):
        """Test __getattr__ lazy import works."""
        import swing.sitemap

        # These should be lazily imported
        assert hasattr(swing.sitemap, "BaseSitemap")
        assert hasattr(swing.sitemap, "ModelSitemap")
        assert hasattr(swing.sitemap, "StaticSitemap")
        assert hasattr(swing.sitemap, "get_setting")

    def test_getattr_invalid_attribute(self):
        """Test __getattr__ raises AttributeError for invalid names."""
        import swing.sitemap

        with pytest.raises(AttributeError):
            _ = swing.sitemap.nonexistent_attribute_xyz

    def test_dir_includes_lazy_exports(self):
        """Test __dir__ includes lazy export names."""
        import swing.sitemap

        dir_result = dir(swing.sitemap)
        assert "BaseSitemap" in dir_result
        assert "ModelSitemap" in dir_result
        assert "get_setting" in dir_result
