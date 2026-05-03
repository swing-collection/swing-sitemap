# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


"""
Tests for swing.sitemap.conf.validate_settings module.
"""


# Import | Future
from __future__ import annotations

# Import | Standard Library
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured

# Import | Libraries
import pytest


class TestValidateModelPath:
    """Tests for validate_model_path function."""

    def test_valid_model_path(self):
        """Test validation passes for existing model."""
        from swing.sitemap.conf.validate_settings import validate_model_path

        # Use a built-in Django model
        result = validate_model_path("contenttypes.ContentType", "test context")
        assert result is True

    def test_invalid_model_path_raises(self):
        """Test validation raises for non-existent model."""
        from swing.sitemap.conf.validate_settings import validate_model_path

        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_model_path("nonexistent.FakeModel", "test context")
        assert "Invalid model path" in str(exc_info.value)


class TestValidatePriority:
    """Tests for validate_priority function."""

    def test_none_priority_valid(self):
        """Test None priority is valid."""
        from swing.sitemap.conf.validate_settings import validate_priority

        assert validate_priority(None, "test") is True

    def test_valid_priority_float(self):
        """Test valid float priority."""
        from swing.sitemap.conf.validate_settings import validate_priority

        assert validate_priority(0.5, "test") is True
        assert validate_priority(0.0, "test") is True
        assert validate_priority(1.0, "test") is True

    def test_valid_priority_int(self):
        """Test valid int priority (0 or 1)."""
        from swing.sitemap.conf.validate_settings import validate_priority

        assert validate_priority(0, "test") is True
        assert validate_priority(1, "test") is True

    def test_priority_out_of_range_raises(self):
        """Test priority > 1.0 raises."""
        from swing.sitemap.conf.validate_settings import validate_priority

        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_priority(1.5, "test")
        assert "must be 0.0-1.0" in str(exc_info.value)

    def test_negative_priority_raises(self):
        """Test negative priority raises."""
        from swing.sitemap.conf.validate_settings import validate_priority

        with pytest.raises(ImproperlyConfigured):
            validate_priority(-0.5, "test")

    def test_non_numeric_priority_raises(self):
        """Test non-numeric priority raises."""
        from swing.sitemap.conf.validate_settings import validate_priority

        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_priority("high", "test")
        assert "must be a number" in str(exc_info.value)


class TestValidateChangefreq:
    """Tests for validate_changefreq function."""

    def test_none_changefreq_valid(self):
        """Test None changefreq is valid."""
        from swing.sitemap.conf.validate_settings import validate_changefreq

        assert validate_changefreq(None, "test") is True

    def test_valid_changefreq_values(self):
        """Test all valid changefreq values."""
        from swing.sitemap.conf.validate_settings import validate_changefreq

        valid_values = ["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
        for value in valid_values:
            assert validate_changefreq(value, "test") is True

    def test_invalid_changefreq_raises(self):
        """Test invalid changefreq raises."""
        from swing.sitemap.conf.validate_settings import validate_changefreq

        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_changefreq("sometimes", "test")
        assert "changefreq must be one of" in str(exc_info.value)


class TestValidateModelsConfig:
    """Tests for validate_models_config function."""

    def test_empty_models_config(self):
        """Test empty models config returns no warnings."""
        from swing.sitemap.conf.validate_settings import validate_models_config

        warnings = validate_models_config({})
        assert warnings == []

    def test_models_config_with_valid_model(self):
        """Test valid model config with existing model."""
        from swing.sitemap.conf.validate_settings import validate_models_config

        config = {
            "models": {
                "contenttypes": {
                    "model": "contenttypes.ContentType",
                    "priority": 0.5,
                    "changefreq": "weekly",
                    "location_attr": "get_absolute_url",
                }
            }
        }
        warnings = validate_models_config(config)
        assert warnings == []

    def test_models_config_warns_missing_location_attr(self):
        """Test warning for missing location_attr."""
        from swing.sitemap.conf.validate_settings import validate_models_config

        config = {
            "models": {
                "contenttypes": {
                    "model": "contenttypes.ContentType",
                }
            }
        }
        warnings = validate_models_config(config)
        assert any("location_attr" in w for w in warnings)

    def test_models_config_non_dict_spec_raises(self):
        """Test non-dict spec raises ImproperlyConfigured."""
        from swing.sitemap.conf.validate_settings import validate_models_config

        config = {"models": {"bad": "string_instead_of_dict"}}
        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_models_config(config)
        assert "must be a dict" in str(exc_info.value)


class TestValidateSpecialSitemaps:
    """Tests for validate_special_sitemaps function."""

    def test_empty_special_sitemaps(self):
        """Test empty config returns no warnings."""
        from swing.sitemap.conf.validate_settings import (
            validate_special_sitemaps,
        )

        warnings = validate_special_sitemaps({})
        assert warnings == []

    def test_video_sitemap_config(self):
        """Test video sitemap config validation."""
        from swing.sitemap.conf.validate_settings import (
            validate_special_sitemaps,
        )

        config = {"video": {"enabled": True}}
        warnings = validate_special_sitemaps(config)
        assert warnings == []

    def test_news_max_age_warning(self):
        """Test warning for invalid news max_age_hours."""
        from swing.sitemap.conf.validate_settings import (
            validate_special_sitemaps,
        )

        config = {"news": {"max_age_hours": -1}}
        warnings = validate_special_sitemaps(config)
        assert any("max_age_hours" in w for w in warnings)

    def test_special_sitemap_non_dict_raises(self):
        """Test non-dict special sitemap raises."""
        from swing.sitemap.conf.validate_settings import (
            validate_special_sitemaps,
        )

        config = {"video": "not_a_dict"}
        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_special_sitemaps(config)
        assert "must be a dict" in str(exc_info.value)


class TestValidateCacheConfig:
    """Tests for validate_cache_config function."""

    def test_empty_cache_config(self):
        """Test empty cache config returns no warnings."""
        from swing.sitemap.conf.validate_settings import validate_cache_config

        warnings = validate_cache_config({})
        assert warnings == []

    def test_cache_disabled_no_warnings(self):
        """Test disabled cache returns no warnings."""
        from swing.sitemap.conf.validate_settings import validate_cache_config

        config = {"cache": {"enabled": False}}
        warnings = validate_cache_config(config)
        assert warnings == []

    def test_cache_enabled_valid(self):
        """Test valid enabled cache config."""
        from swing.sitemap.conf.validate_settings import validate_cache_config

        config = {"cache": {"enabled": True, "timeout": 3600, "backend": "default"}}
        warnings = validate_cache_config(config)
        assert warnings == []

    def test_cache_invalid_timeout_warning(self):
        """Test warning for invalid timeout."""
        from swing.sitemap.conf.validate_settings import validate_cache_config

        config = {"cache": {"enabled": True, "timeout": -1}}
        warnings = validate_cache_config(config)
        assert any("timeout" in w for w in warnings)

    def test_cache_invalid_backend_raises(self):
        """Test invalid cache backend raises."""
        from swing.sitemap.conf.validate_settings import validate_cache_config

        config = {"cache": {"enabled": True, "backend": "nonexistent_cache"}}
        with pytest.raises(ImproperlyConfigured) as exc_info:
            validate_cache_config(config)
        assert "Invalid cache backend" in str(exc_info.value)


class TestValidateSignalsConfig:
    """Tests for validate_signals_config function."""

    def test_empty_signals_config(self):
        """Test empty signals config returns no warnings."""
        from swing.sitemap.conf.validate_settings import (
            validate_signals_config,
        )

        warnings = validate_signals_config({})
        assert warnings == []

    def test_signals_disabled_no_warnings(self):
        """Test disabled signals returns no warnings."""
        from swing.sitemap.conf.validate_settings import (
            validate_signals_config,
        )

        config = {"signals": {"enabled": False}}
        warnings = validate_signals_config(config)
        assert warnings == []

    def test_signals_invalid_model_warning(self):
        """Test warning for invalid model path."""
        from swing.sitemap.conf.validate_settings import (
            validate_signals_config,
        )

        config = {"signals": {"enabled": True, "models": ["nonexistent.FakeModel"]}}
        warnings = validate_signals_config(config)
        assert any("not found" in w for w in warnings)

    def test_signals_negative_debounce_warning(self):
        """Test warning for negative debounce."""
        from swing.sitemap.conf.validate_settings import (
            validate_signals_config,
        )

        config = {"signals": {"enabled": True, "debounce_seconds": -5}}
        warnings = validate_signals_config(config)
        assert any("debounce_seconds" in w for w in warnings)


class TestValidateSettings:
    """Tests for validate_settings function."""

    def test_validate_settings_default_config(self):
        """Test validation with default empty config."""
        from swing.sitemap.conf.validate_settings import validate_settings

        is_valid, warnings = validate_settings(raise_errors=False)
        assert is_valid is True
        assert isinstance(warnings, list)

    @patch("swing.sitemap.conf.validate_settings.get_config")
    def test_validate_settings_raises_on_config_error(self, mock_get_config):
        """Test validation raises on config load error."""
        mock_get_config.side_effect = Exception("Config error")

        from swing.sitemap.conf.validate_settings import validate_settings

        with pytest.raises(ImproperlyConfigured):
            validate_settings(raise_errors=True)

    @patch("swing.sitemap.conf.validate_settings.get_config")
    def test_validate_settings_returns_false_on_config_error(self, mock_get_config):
        """Test validation returns False on config load error when not raising."""
        mock_get_config.side_effect = Exception("Config error")

        from swing.sitemap.conf.validate_settings import validate_settings

        is_valid, warnings = validate_settings(raise_errors=False)
        assert is_valid is False
        assert len(warnings) > 0

    @patch("swing.sitemap.conf.validate_settings.get_config")
    def test_validate_settings_logs_warnings(self, mock_get_config):
        """Test validation logs warnings."""
        # Config that triggers warnings (missing location_attr)
        mock_get_config.return_value = {
            "models": {
                "test": {
                    "model": "contenttypes.ContentType",
                }
            }
        }

        from swing.sitemap.conf.validate_settings import validate_settings

        is_valid, warnings = validate_settings(raise_errors=False)
        assert is_valid is True
        assert len(warnings) > 0
        assert any("location_attr" in w for w in warnings)

    @patch("swing.sitemap.conf.validate_settings.get_config")
    def test_validate_settings_catches_improperly_configured_no_raise(self, mock_get_config):
        """Test validation catches ImproperlyConfigured when raise_errors=False."""
        # Config that triggers ImproperlyConfigured error
        mock_get_config.return_value = {
            "models": {
                "bad": "not_a_dict"  # This should raise ImproperlyConfigured
            }
        }

        from swing.sitemap.conf.validate_settings import validate_settings

        is_valid, warnings = validate_settings(raise_errors=False)
        assert is_valid is False
