# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap App Config
========================

Django application configuration for ``swing.sitemap``.

Handles:
- Settings validation on startup
- Signal registration for cache invalidation

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


# =============================================================================
# Classes
# =============================================================================

class SwingSitemapConfig(AppConfig):
    """
    Swing Sitemap App Config
    ========================

    Django application configuration for ``swing.sitemap``.
    """

    # Full Python path to the application
    name = "swing.sitemap"

    # Short name for the application
    label = "swing_sitemap"

    # Human-readable name for the application
    verbose_name = _("Swing Sitemap")

    # The implicit primary key type to add to models within this app.
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """
        Hook called when Django starts.

        Performs:
        - Settings validation (logs warnings for issues)
        - Signal registration if enabled in settings
        """
        self._validate_settings()
        self._register_signals()

    def _validate_settings(self) -> None:
        """Validate SWING_SITEMAP settings on startup."""
        try:
            # pylint: disable=import-outside-toplevel
            from swing.sitemap.conf.validate_settings import validate_settings

            is_valid, warnings = validate_settings(raise_errors=False)

            if warnings:
                for warning in warnings:
                    logger.warning("SWING_SITEMAP: %s", warning)

            if is_valid:
                logger.debug("SWING_SITEMAP: Configuration validated successfully")
            else:
                logger.warning(
                    "SWING_SITEMAP: Configuration has issues, check warnings above"
                )
        except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
            # Don't prevent app from loading on validation errors
            logger.error(
                "SWING_SITEMAP: Failed to validate settings: %s",
                e,
                exc_info=True,
            )

    def _register_signals(self) -> None:
        """Register cache invalidation signals if enabled."""        # pylint: disable=import-outside-toplevel        try:
            from swing.sitemap.conf import get_setting

            signals_config = get_setting("signals", default={})
            if not signals_config.get("enabled", False):
                return

            from swing.sitemap.signals import register_sitemap_signals

            models = signals_config.get("models") or []
            if models:
                register_sitemap_signals(models)
                logger.info(
                    "SWING_SITEMAP: Registered signals for %d model(s)",
                    len(models),
                )
        except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
            logger.warning(
                "SWING_SITEMAP: Failed to register signals: %s",
                e,
            )
