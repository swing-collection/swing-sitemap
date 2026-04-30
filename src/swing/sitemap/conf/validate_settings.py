# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Settings Validation
===================

Validates SWING_SITEMAP configuration on app startup.

Checks for:
- Invalid model paths
- Missing required fields
- Type mismatches
- Invalid values (priorities, changefreqs)

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging
from typing import Any

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

# Import | Local
from .get_config import get_config

logger = logging.getLogger(__name__)


# =============================================================================
# Constants
# =============================================================================

VALID_CHANGEFREQ = frozenset(
    {
        "always",
        "hourly",
        "daily",
        "weekly",
        "monthly",
        "yearly",
        "never",
    }
)


# =============================================================================
# Functions
# =============================================================================


def validate_model_path(path: str, context: str) -> bool:
    """
    Validate a dotted model path is importable.

    Args:
        path: Dotted path like 'myapp.MyModel'.
        context: Description for error messages.

    Returns:
        True if valid, raises ImproperlyConfigured otherwise.
    """
    try:
        apps.get_model(path)
        return True
    except (LookupError, ValueError) as e:
        raise ImproperlyConfigured(
            f"SWING_SITEMAP {context}: Invalid model path '{path}'. " f"Error: {e}"
        ) from e


def validate_priority(value: Any, context: str) -> bool:
    """Validate priority is 0.0-1.0."""
    if value is None:
        return True
    try:
        val = float(value)
        if not 0.0 <= val <= 1.0:
            raise ImproperlyConfigured(
                f"SWING_SITEMAP {context}: priority must be 0.0-1.0, got {val}"
            )
        return True
    except (TypeError, ValueError) as e:
        raise ImproperlyConfigured(
            f"SWING_SITEMAP {context}: priority must be a number, got {type(value).__name__}"
        ) from e


def validate_changefreq(value: Any, context: str) -> bool:
    """Validate changefreq is a valid value."""
    if value is None:
        return True
    if value not in VALID_CHANGEFREQ:
        raise ImproperlyConfigured(
            f"SWING_SITEMAP {context}: changefreq must be one of "
            f"{', '.join(sorted(VALID_CHANGEFREQ))}, got '{value}'"
        )
    return True


def validate_models_config(config: dict[str, Any]) -> list[str]:
    """
    Validate the 'models' section of SWING_SITEMAP.

    Returns list of warning messages.
    """
    warnings_list: list[str] = []
    models_config = config.get("models") or {}

    for key, spec in models_config.items():
        context = f"['models']['{key}']"

        if not isinstance(spec, dict):
            raise ImproperlyConfigured(
                f"SWING_SITEMAP {context}: must be a dict, got {type(spec).__name__}"
            )

        # Validate model path
        if "model" in spec:
            validate_model_path(spec["model"], context)

        # Validate priority/changefreq
        if "priority" in spec:
            validate_priority(spec["priority"], context)
        if "changefreq" in spec:
            validate_changefreq(spec["changefreq"], context)

        # Warn about missing location_attr
        if "model" in spec and "location_attr" not in spec:
            warnings_list.append(
                f"{context}: No 'location_attr' specified, will use 'get_absolute_url'"
            )

    return warnings_list


def validate_special_sitemaps(config: dict[str, Any]) -> list[str]:
    """
    Validate video/news/image sitemap configs.

    Returns list of warning messages.
    """
    warnings_list: list[str] = []

    for sitemap_type in ("video", "news", "image"):
        spec = config.get(sitemap_type) or {}
        if not spec:
            continue

        context = f"['{sitemap_type}']"

        if not isinstance(spec, dict):
            raise ImproperlyConfigured(
                f"SWING_SITEMAP {context}: must be a dict, got {type(spec).__name__}"
            )

        # Validate model if specified
        if "model" in spec:
            validate_model_path(spec["model"], context)

        # Type-specific validations
        if sitemap_type == "news":
            max_age = spec.get("max_age_hours", 48)
            if not isinstance(max_age, (int, float)) or max_age <= 0:
                warnings_list.append(
                    f"{context}: 'max_age_hours' should be positive, got {max_age}"
                )

    return warnings_list


def validate_cache_config(config: dict[str, Any]) -> list[str]:
    """Validate cache configuration."""
    warnings_list: list[str] = []
    cache_config = config.get("cache") or {}

    if cache_config.get("enabled"):
        timeout = cache_config.get("timeout", 3600)
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            warnings_list.append(
                f"['cache']['timeout'] should be positive, got {timeout}"
            )

        backend = cache_config.get("backend", "default")
        try:
            from django.core.cache import (  # pylint: disable=import-outside-toplevel
                caches,
            )

            _ = caches[backend]  # Check cache backend exists
        except Exception as e:
            raise ImproperlyConfigured(
                f"SWING_SITEMAP ['cache']['backend']: Invalid cache backend '{backend}'. "
                f"Error: {e}"
            ) from e

    return warnings_list


def validate_signals_config(config: dict[str, Any]) -> list[str]:
    """Validate signals configuration."""
    warnings_list: list[str] = []
    signals_config = config.get("signals") or {}

    if signals_config.get("enabled"):
        models = signals_config.get("models") or []
        for model_path in models:
            try:
                validate_model_path(model_path, "['signals']['models']")
            except ImproperlyConfigured:
                warnings_list.append(
                    f"['signals']['models']: Model '{model_path}' not found, "
                    "signal registration will fail"
                )

        debounce = signals_config.get("debounce_seconds", 5)
        if not isinstance(debounce, (int, float)) or debounce < 0:
            warnings_list.append(
                f"['signals']['debounce_seconds'] should be non-negative, got {debounce}"
            )

    return warnings_list


def validate_settings(raise_errors: bool = True) -> tuple[bool, list[str]]:
    """
    Validate all SWING_SITEMAP settings.

    Args:
        raise_errors: If True, raise ImproperlyConfigured on errors.
            If False, return errors as warnings.

    Returns:
        Tuple of (is_valid, list of warning messages).
    """
    try:
        config = get_config()
    except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
        if raise_errors:
            raise ImproperlyConfigured(
                f"SWING_SITEMAP: Failed to load configuration: {e}"
            ) from e
        return False, [str(e)]

    all_warnings: list[str] = []

    try:
        # Validate each section
        all_warnings.extend(validate_models_config(config))
        all_warnings.extend(validate_special_sitemaps(config))
        all_warnings.extend(validate_cache_config(config))
        all_warnings.extend(validate_signals_config(config))

        # Log warnings
        for warning in all_warnings:
            logger.warning("SWING_SITEMAP configuration: %s", warning)

        return True, all_warnings

    except ImproperlyConfigured:
        if raise_errors:
            raise
        return False, all_warnings


# =============================================================================
# Exports
# =============================================================================

__all__ = ["validate_settings"]
