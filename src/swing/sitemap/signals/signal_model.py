# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Model Signals for Sitemap Cache Invalidation
=============================================

Provides signal handlers that automatically invalidate sitemap caches
when model instances are created, updated, or deleted.

Configuration via Django settings::

    SWING_SITEMAP = {
        "signals": {
            "enabled": True,
            "models": ["myapp.Article", "myapp.Page"],
            "debounce_seconds": 5,
            "invalidate_on_save": True,
            "invalidate_on_delete": True,
            "auto_submit": False,
        },
    }

To enable signals for your app, call :func:`register_sitemap_signals` in
your app's ``ready()`` method::

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        def ready(self):
            from swing.sitemap.signals import register_sitemap_signals
            register_sitemap_signals()
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging
import threading
from typing import Any, Callable

from django.apps import apps
from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_delete, post_save

from swing.sitemap.conf import get_setting

logger = logging.getLogger(__name__)


# =============================================================================
# Debouncing
# =============================================================================

_debounce_timers: dict[str, threading.Timer] = {}
_debounce_lock = threading.Lock()


def debounce(key: str, delay: float, func: Callable[[], Any]) -> None:
    """
    Debounce a function call by key.

    If called multiple times within `delay` seconds, only the last call
    executes. Useful for batching rapid model changes.
    """
    with _debounce_lock:
        # Cancel existing timer for this key
        if key in _debounce_timers:
            _debounce_timers[key].cancel()

        # Create new timer
        timer = threading.Timer(delay, func)
        _debounce_timers[key] = timer
        timer.start()


def cancel_debounce(key: str) -> None:
    """Cancel a pending debounced function."""
    with _debounce_lock:
        if key in _debounce_timers:
            _debounce_timers[key].cancel()
            del _debounce_timers[key]


# =============================================================================
# Cache Invalidation
# =============================================================================


def invalidate_sitemap_cache(model_label: str | None = None) -> None:
    """
    Invalidate sitemap cache entries.

    Args:
        model_label: Optional model label (e.g. 'myapp.Article') to
            invalidate only that model's cache entries. If None,
            invalidates all sitemap caches.
    """
    cache_config = get_setting("cache", default={}) or {}
    prefix = cache_config.get("key_prefix", "swing_sitemap")

    if model_label:
        cache_key = f"{prefix}:{model_label.replace('.', '_')}"
        cache.delete(cache_key)
        logger.debug("Invalidated sitemap cache for %s", model_label)
    else:
        # Try to clear all sitemap cache keys
        try:
            cache.delete_pattern(f"{prefix}:*")
            logger.debug("Invalidated all sitemap cache entries")
        except AttributeError:
            # Fallback: clear known cache keys
            logger.debug("Cache backend doesn't support delete_pattern")

    # Also invalidate the main sitemap cache
    cache.delete(f"{prefix}:sitemap")
    cache.delete(f"{prefix}:sitemap_index")


# =============================================================================
# Signal Handlers
# =============================================================================


def _get_model_label(instance: Model) -> str:
    """Get the app_label.model_name string for a model instance."""
    return f"{instance._meta.app_label}.{instance._meta.model_name}"


def _should_invalidate(instance: Model) -> bool:
    """Check if this model change should trigger cache invalidation."""
    signals_config = get_setting("signals", default={}) or {}
    if not signals_config.get("enabled", True):
        return False

    # Check if model is in the configured list
    configured_models = signals_config.get("models", [])
    if configured_models:
        model_label = _get_model_label(instance)
        # Check both exact match and case-insensitive
        if not any(m.lower() == model_label.lower() for m in configured_models):
            return False

    return True


def sitemap_post_save(sender: type, instance: Model, **kwargs: Any) -> None:
    """
    Signal handler for model post_save.

    Invalidates sitemap cache when a model instance is saved.
    """
    if not _should_invalidate(instance):
        return

    signals_config = get_setting("signals", default={}) or {}
    if not signals_config.get("invalidate_on_save", True):
        return

    model_label = _get_model_label(instance)
    debounce_seconds = signals_config.get("debounce_seconds", 5)

    def do_invalidate():
        invalidate_sitemap_cache(model_label)
        logger.info("Sitemap cache invalidated after save: %s", model_label)

        # Optionally trigger sitemap submission
        if signals_config.get("auto_submit", False):
            try:
                # pylint: disable=import-outside-toplevel
                from swing.sitemap.tasks.submit_sitemap import (
                    submit_sitemap_task,
                )

                submit_sitemap_task.delay()
            except ImportError:
                logger.warning("Celery not available for auto_submit")

    if debounce_seconds > 0:
        debounce(f"sitemap_invalidate:{model_label}", debounce_seconds, do_invalidate)
    else:
        do_invalidate()


def sitemap_post_delete(sender: type, instance: Model, **kwargs: Any) -> None:
    """
    Signal handler for model post_delete.

    Invalidates sitemap cache when a model instance is deleted.
    """
    if not _should_invalidate(instance):
        return

    signals_config = get_setting("signals", default={}) or {}
    if not signals_config.get("invalidate_on_delete", True):
        return

    model_label = _get_model_label(instance)
    debounce_seconds = signals_config.get("debounce_seconds", 5)

    def do_invalidate():
        invalidate_sitemap_cache(model_label)
        logger.info("Sitemap cache invalidated after delete: %s", model_label)

    if debounce_seconds > 0:
        debounce(f"sitemap_invalidate:{model_label}", debounce_seconds, do_invalidate)
    else:
        do_invalidate()


# =============================================================================
# Registration
# =============================================================================


_signals_registered = False


def register_sitemap_signals(models: list[str] | None = None) -> None:
    """
    Register sitemap cache invalidation signals for configured models.

    Args:
        models: Optional list of model paths (e.g. ['myapp.Article']).
            If not provided, uses ``SWING_SITEMAP['signals']['models']``.

    Call this function in your AppConfig.ready() method::

        class MyAppConfig(AppConfig):
            def ready(self):
                from swing.sitemap.signals import register_sitemap_signals
                register_sitemap_signals()
    """
    global _signals_registered  # noqa: PLW0603  pylint: disable=global-statement

    if _signals_registered:
        return

    signals_config = get_setting("signals", default={}) or {}
    if not signals_config.get("enabled", True):
        logger.debug("Sitemap signals disabled in settings")
        return

    model_paths = models or signals_config.get("models", [])
    if not model_paths:
        logger.debug("No models configured for sitemap signals")
        return

    for model_path in model_paths:
        try:
            model = apps.get_model(model_path)
            post_save.connect(sitemap_post_save, sender=model, weak=False)
            post_delete.connect(sitemap_post_delete, sender=model, weak=False)
            logger.info("Registered sitemap signals for %s", model_path)
        except LookupError:
            logger.warning(
                "Model %s not found, skipping signal registration", model_path
            )

    _signals_registered = True


def unregister_sitemap_signals(models: list[str] | None = None) -> None:
    """
    Unregister sitemap cache invalidation signals.

    Args:
        models: Optional list of model paths to unregister.
            If not provided, uses ``SWING_SITEMAP['signals']['models']``.
    """
    global _signals_registered  # noqa: PLW0603  pylint: disable=global-statement

    signals_config = get_setting("signals", default={}) or {}
    model_paths = models or signals_config.get("models", [])

    for model_path in model_paths:
        try:
            model = apps.get_model(model_path)
            post_save.disconnect(sitemap_post_save, sender=model)
            post_delete.disconnect(sitemap_post_delete, sender=model)
            logger.info("Unregistered sitemap signals for %s", model_path)
        except LookupError:
            pass

    _signals_registered = False


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cancel_debounce",
    "debounce",
    "invalidate_sitemap_cache",
    "register_sitemap_signals",
    "sitemap_post_delete",
    "sitemap_post_save",
    "unregister_sitemap_signals",
]
