# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for signals module."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import time
from unittest.mock import MagicMock, patch

# Import | Libraries
import pytest

from swing.sitemap.signals import (
    cancel_debounce,
    debounce,
    invalidate_sitemap_cache,
    register_sitemap_signals,
    sitemap_post_delete,
    sitemap_post_save,
    unregister_sitemap_signals,
)

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Debounce
# =============================================================================


class TestDebounce:
    """Tests for debounce functionality."""

    def test_debounce_calls_function_after_delay(self):
        """Test debounce calls the function after the delay."""
        callback = MagicMock()
        debounce("test_key", 0.05, callback)
        time.sleep(0.1)
        callback.assert_called_once()

    def test_debounce_cancels_previous_call(self):
        """Test debounce cancels previous call when called again."""
        callback = MagicMock()
        debounce("test_key2", 0.1, callback)
        debounce("test_key2", 0.1, callback)
        time.sleep(0.15)
        # Should only be called once (second call replaces first)
        callback.assert_called_once()

    def test_cancel_debounce_stops_pending_call(self):
        """Test cancel_debounce stops a pending debounced call."""
        callback = MagicMock()
        debounce("test_key3", 0.1, callback)
        cancel_debounce("test_key3")
        time.sleep(0.15)
        callback.assert_not_called()

    def test_cancel_debounce_nonexistent_key(self):
        """Test cancel_debounce with nonexistent key doesn't raise."""
        # Should not raise
        cancel_debounce("nonexistent_key")


# =============================================================================
# Tests - Cache Invalidation
# =============================================================================


class TestInvalidateSitemapCache:
    """Tests for cache invalidation."""

    def test_invalidate_without_model_label(self):
        """Test invalidate_sitemap_cache without model label."""
        # Should not raise
        invalidate_sitemap_cache()

    def test_invalidate_with_model_label(self):
        """Test invalidate_sitemap_cache with model label."""
        # Should not raise
        invalidate_sitemap_cache("myapp.MyModel")


# =============================================================================
# Tests - Signal Registration
# =============================================================================


class TestSignalRegistration:
    """Tests for signal registration."""

    def test_register_with_no_models(self, settings):
        """Test register_sitemap_signals with no models configured."""
        settings.SWING_SITEMAP = {"signals": {"enabled": True, "models": []}}
        # Reset registered state
        from swing.sitemap.signals import register_sitemap_signals
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        reg_module._signals_registered = False
        # Should not raise
        register_sitemap_signals()

    def test_register_when_disabled(self, settings):
        """Test register_sitemap_signals when signals are disabled."""
        settings.SWING_SITEMAP = {"signals": {"enabled": False}}
        from swing.sitemap.signals import register_sitemap_signals
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        reg_module._signals_registered = False
        # Should not raise
        register_sitemap_signals()

    def test_register_already_registered(self, settings):
        """Test register_sitemap_signals when already registered."""
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        reg_module._signals_registered = True
        # Should return early
        register_sitemap_signals()

    def test_register_with_valid_model(self, settings):
        """Test register_sitemap_signals with a valid model."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["contenttypes.ContentType"]}
        }
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        # Save original state
        original_state = reg_module._signals_registered
        reg_module._signals_registered = False
        try:
            # Should not raise - contenttypes.ContentType is always available
            register_sitemap_signals()
        finally:
            # Restore original state
            reg_module._signals_registered = original_state

    def test_register_with_invalid_model(self, settings):
        """Test register_sitemap_signals with an invalid model."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["nonexistent.FakeModel"]}
        }
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        original_state = reg_module._signals_registered
        reg_module._signals_registered = False
        try:
            # Should not raise but should log warning
            register_sitemap_signals()
        finally:
            reg_module._signals_registered = original_state

    def test_register_with_explicit_models_list(self, settings):
        """Test register_sitemap_signals with explicit models parameter."""
        import swing.sitemap.signals.register_sitemap_signals as reg_module

        original_state = reg_module._signals_registered
        reg_module._signals_registered = False
        try:
            # Pass models explicitly
            register_sitemap_signals(models=["contenttypes.ContentType"])
        finally:
            reg_module._signals_registered = original_state

    def test_unregister_signals(self, settings):
        """Test unregister_sitemap_signals."""
        import swing.sitemap.signals.unregister_sitemap_signals as unreg_module

        unreg_module._signals_registered = True
        unregister_sitemap_signals()

    def test_unregister_when_not_registered(self, settings):
        """Test unregister_sitemap_signals when not registered."""
        import swing.sitemap.signals.unregister_sitemap_signals as unreg_module

        unreg_module._signals_registered = False
        # Should return early
        unregister_sitemap_signals()

    def test_unregister_with_models(self, settings):
        """Test unregister_sitemap_signals with configured models."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["contenttypes.ContentType"]}
        }
        import swing.sitemap.signals.unregister_sitemap_signals as unreg_module

        original_state = unreg_module._signals_registered
        unreg_module._signals_registered = True
        try:
            unregister_sitemap_signals()
        finally:
            unreg_module._signals_registered = original_state


# =============================================================================
# Tests - Signal Handlers
# =============================================================================


class TestSignalHandlers:
    """Tests for signal handlers."""

    def test_sitemap_post_save_handler(self, settings):
        """Test sitemap_post_save signal handler."""
        settings.SWING_SITEMAP = {"signals": {"enabled": True}}
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should not raise
        sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_sitemap_post_delete_handler(self, settings):
        """Test sitemap_post_delete signal handler."""
        settings.SWING_SITEMAP = {"signals": {"enabled": True}}
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should not raise
        sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_post_save_when_signals_disabled(self, settings):
        """Test sitemap_post_save when signals disabled."""
        settings.SWING_SITEMAP = {"signals": {"enabled": False}}
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should not raise and should return early
        sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_when_signals_disabled(self, settings):
        """Test sitemap_post_delete when signals disabled."""
        settings.SWING_SITEMAP = {"signals": {"enabled": False}}
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should not raise and should return early
        sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_post_save_model_not_in_list(self, settings):
        """Test sitemap_post_save when model not in configured list."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["other.Model"]}
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should return early without invalidating
        sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_model_not_in_list(self, settings):
        """Test sitemap_post_delete when model not in configured list."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["other.Model"]}
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should return early without invalidating
        sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_post_save_invalidate_on_save_disabled(self, settings):
        """Test sitemap_post_save when invalidate_on_save is False."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "invalidate_on_save": False}
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should return early
        sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_invalidate_on_delete_disabled(self, settings):
        """Test sitemap_post_delete when invalidate_on_delete is False."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "invalidate_on_delete": False}
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        # Should return early
        sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_post_save_with_debounce_zero(self, settings):
        """Test sitemap_post_save with zero debounce."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "debounce_seconds": 0}
        }
        mock_instance = MagicMock()
        # Properly set _meta.label as a string
        mock_instance._meta.label = "myapp.MyModel"
        mock_instance._meta.app_label = "myapp"
        mock_instance._meta.model_name = "mymodel"
        # Patch the cache to avoid cache key issues
        with patch("swing.sitemap.signals.invalidate_sitemap_cache.invalidate_sitemap_cache"):
            sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_with_debounce_zero(self, settings):
        """Test sitemap_post_delete with zero debounce."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "debounce_seconds": 0}
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        mock_instance._meta.app_label = "myapp"
        mock_instance._meta.model_name = "mymodel"
        # Patch the cache to avoid cache key issues
        with patch("swing.sitemap.signals.invalidate_sitemap_cache.invalidate_sitemap_cache"):
            sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_post_save_auto_submit_disabled(self, settings):
        """Test sitemap_post_save without auto_submit."""
        settings.SWING_SITEMAP = {
            "signals": {
                "enabled": True,
                "debounce_seconds": 0,
                "auto_submit": False,  # Explicitly disabled
            }
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        mock_instance._meta.app_label = "myapp"
        mock_instance._meta.model_name = "mymodel"
        # Patch invalidate cache
        with patch("swing.sitemap.signals.invalidate_sitemap_cache.invalidate_sitemap_cache"):
            sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_auto_submit_disabled(self, settings):
        """Test sitemap_post_delete without auto_submit."""
        settings.SWING_SITEMAP = {
            "signals": {
                "enabled": True,
                "debounce_seconds": 0,
                "auto_submit": False,  # Explicitly disabled
            }
        }
        mock_instance = MagicMock()
        mock_instance._meta.label = "myapp.MyModel"
        mock_instance._meta.app_label = "myapp"
        mock_instance._meta.model_name = "mymodel"
        # Patch invalidate cache
        with patch("swing.sitemap.signals.invalidate_sitemap_cache.invalidate_sitemap_cache"):
            sitemap_post_delete(sender=MagicMock, instance=mock_instance)

    def test_unregister_with_invalid_model(self, settings):
        """Test unregister_sitemap_signals with an invalid model."""
        settings.SWING_SITEMAP = {
            "signals": {"enabled": True, "models": ["nonexistent.FakeModel"]}
        }
        import swing.sitemap.signals.unregister_sitemap_signals as unreg_module

        original_state = unreg_module._signals_registered
        unreg_module._signals_registered = True
        try:
            # Should not raise - invalid model should be skipped
            unregister_sitemap_signals()
        finally:
            unreg_module._signals_registered = original_state
