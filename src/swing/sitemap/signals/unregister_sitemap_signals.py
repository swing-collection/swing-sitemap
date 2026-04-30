# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Unregister Sitemap Signals
==========================

Unregister sitemap cache invalidation signals.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging

from django.apps import apps
from django.db.models.signals import post_delete, post_save

from swing.sitemap.conf import get_setting

# Import | Local
from .sitemap_post_delete import sitemap_post_delete
from .sitemap_post_save import sitemap_post_save

logger = logging.getLogger(__name__)


# =============================================================================
# Functions
# =============================================================================


def unregister_sitemap_signals(models: list[str] | None = None) -> None:
    """
    Unregister sitemap cache invalidation signals.

    Args:
        models: Optional list of model paths to unregister.
            If not provided, uses ``SWING_SITEMAP['signals']['models']``.
    """
    # pylint: disable=import-outside-toplevel
    # Import | Local
    from .register_sitemap_signals import _signals_registered

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


# =============================================================================
# Exports
# =============================================================================

__all__ = ["unregister_sitemap_signals"]
