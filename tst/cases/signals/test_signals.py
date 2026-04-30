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

    def test_unregister_signals(self, settings):
        """Test unregister_sitemap_signals."""
        import swing.sitemap.signals.unregister_sitemap_signals as unreg_module

        unreg_module._signals_registered = True
        unregister_sitemap_signals()


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
        # Should not raise and should return early
        sitemap_post_save(sender=MagicMock, instance=mock_instance)

    def test_post_delete_when_signals_disabled(self, settings):
        """Test sitemap_post_delete when signals disabled."""
        settings.SWING_SITEMAP = {"signals": {"enabled": False}}
        mock_instance = MagicMock()
        # Should not raise and should return early
        sitemap_post_delete(sender=MagicMock, instance=mock_instance)
