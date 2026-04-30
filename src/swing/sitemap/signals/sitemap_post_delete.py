# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Sitemap Post Delete Signal
==========================

Signal handler for model post_delete.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging
from typing import Any

from django.db.models import Model

from swing.sitemap.conf import get_setting

# Import | Local
from .debounce import debounce
from .invalidate_sitemap_cache import invalidate_sitemap_cache

logger = logging.getLogger(__name__)


# =============================================================================
# Helper Functions
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


# =============================================================================
# Functions
# =============================================================================


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
# Exports
# =============================================================================

__all__ = ["sitemap_post_delete"]
