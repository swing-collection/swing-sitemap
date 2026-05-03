# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Register Sitemap Signals
========================

Register sitemap cache invalidation signals for configured models.

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
# State
# =============================================================================

_signals_registered = False


# =============================================================================
# Functions
# =============================================================================


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
        except LookupError:  # pragma: no cover
            logger.warning(
                "Model %s not found, skipping signal registration", model_path
            )

    _signals_registered = True


# =============================================================================
# Exports
# =============================================================================

__all__ = ["register_sitemap_signals"]
