# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Health Check View
=================

Health check endpoint for monitoring sitemap functionality.

Checks:
- Settings configuration is valid
- Sitemaps can be generated
- Cache backend is accessible (if enabled)
- Database connectivity

Usage::

    # In urls.py
    from swing.sitemap.views import health_check

    urlpatterns = [
        path("sitemap/health/", health_check, name="sitemap_health"),
    ]

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import logging
import time
from typing import Any

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from swing.sitemap.conf import get_setting, validate_settings
from swing.sitemap.sitemaps import default_sitemaps


logger = logging.getLogger(__name__)


# =============================================================================
# Functions
# =============================================================================

@require_GET
def health_check(request) -> JsonResponse:
    """
    Health check endpoint for sitemap functionality.

    Returns JSON with status of various components:
    - settings: Configuration validation
    - sitemaps: Sitemap generation capability
    - cache: Cache backend status (if enabled)

    Query Parameters:
        verbose: Include detailed check information
        quick: Skip detailed checks (just confirm endpoint works)

    Returns:
        JsonResponse with health status:
        - status: "healthy", "degraded", or "unhealthy"
        - checks: Dict of individual check results
        - timestamp: ISO timestamp
    """
    quick = request.GET.get("quick", "").lower() == "true"
    verbose = request.GET.get("verbose", "").lower() == "true"

    if quick:
        return JsonResponse({
            "status": "healthy",
            "checks": {},
            "timestamp": _now_iso(),
        })

    checks = {}
    overall_status = "healthy"

    # Check settings
    settings_check = _check_settings(verbose)
    checks["settings"] = settings_check
    if not settings_check["ok"]:
        overall_status = "degraded"

    # Check sitemaps
    sitemaps_check = _check_sitemaps(verbose)
    checks["sitemaps"] = sitemaps_check
    if not sitemaps_check["ok"]:
        overall_status = "unhealthy" if overall_status != "degraded" else "degraded"

    # Check cache (if enabled)
    cache_config = get_setting("cache", default={})
    if cache_config.get("enabled"):
        cache_check = _check_cache(verbose)
        checks["cache"] = cache_check
        if not cache_check["ok"]:
            overall_status = "degraded"

    # Check database
    db_check = _check_database(verbose)
    checks["database"] = db_check
    if not db_check["ok"]:
        overall_status = "unhealthy"

    status_code = 200 if overall_status == "healthy" else 503 if overall_status == "unhealthy" else 200

    return JsonResponse(
        {
            "status": overall_status,
            "checks": checks,
            "timestamp": _now_iso(),
        },
        status=status_code,
    )


def _now_iso() -> str:
    """Return current time as ISO string."""
    from django.utils import timezone
    return timezone.now().isoformat()


def _check_settings(verbose: bool) -> dict[str, Any]:
    """Check settings validation."""
    start = time.monotonic()
    try:
        is_valid, warnings = validate_settings(raise_errors=False)
        elapsed = time.monotonic() - start

        result = {
            "ok": is_valid,
            "message": "Settings valid" if is_valid else "Settings have issues",
            "duration_ms": round(elapsed * 1000, 2),
        }

        if verbose and warnings:
            result["warnings"] = warnings

        return result

    except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
        elapsed = time.monotonic() - start
        logger.exception("Health check: settings validation failed")
        return {
            "ok": False,
            "message": f"Settings validation error: {e}",
            "duration_ms": round(elapsed * 1000, 2),
        }


def _check_sitemaps(verbose: bool) -> dict[str, Any]:
    """Check sitemap generation."""
    start = time.monotonic()
    try:
        sitemaps = default_sitemaps()
        elapsed = time.monotonic() - start

        sitemap_count = len(sitemaps)
        total_urls = 0
        sitemap_info = {}

        if verbose:
            for name, sitemap in sitemaps.items():
                try:
                    items = list(sitemap.items())
                    count = len(items)
                    total_urls += count
                    sitemap_info[name] = {"urls": count, "ok": True}
                except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
                    sitemap_info[name] = {"ok": False, "error": str(e)}

        result = {
            "ok": True,
            "message": f"Generated {sitemap_count} sitemap(s)",
            "sitemap_count": sitemap_count,
            "duration_ms": round(elapsed * 1000, 2),
        }

        if verbose:
            result["sitemaps"] = sitemap_info
            result["total_urls"] = total_urls

        return result

    except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
        elapsed = time.monotonic() - start
        logger.exception("Health check: sitemap generation failed")
        return {
            "ok": False,
            "message": f"Sitemap generation error: {e}",
            "duration_ms": round(elapsed * 1000, 2),
        }


def _check_cache(verbose: bool) -> dict[str, Any]:
    """Check cache backend."""
    start = time.monotonic()
    try:
        from django.core.cache import caches

        cache_config = get_setting("cache", default={})
        backend = cache_config.get("backend", "default")
        cache = caches[backend]

        # Test write/read/delete
        test_key = "swing_sitemap_health_check"
        test_value = "ok"

        cache.set(test_key, test_value, timeout=10)
        retrieved = cache.get(test_key)
        cache.delete(test_key)

        elapsed = time.monotonic() - start

        ok = retrieved == test_value
        return {
            "ok": ok,
            "message": "Cache working" if ok else "Cache read/write failed",
            "backend": backend,
            "duration_ms": round(elapsed * 1000, 2),
        }

    except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
        elapsed = time.monotonic() - start
        logger.exception("Health check: cache check failed")
        return {
            "ok": False,
            "message": f"Cache error: {e}",
            "duration_ms": round(elapsed * 1000, 2),
        }


def _check_database(verbose: bool) -> dict[str, Any]:
    """Check database connectivity."""
    start = time.monotonic()
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        elapsed = time.monotonic() - start

        return {
            "ok": True,
            "message": "Database connected",
            "duration_ms": round(elapsed * 1000, 2),
        }

    except Exception as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
        elapsed = time.monotonic() - start
        logger.exception("Health check: database check failed")
        return {
            "ok": False,
            "message": f"Database error: {e}",
            "duration_ms": round(elapsed * 1000, 2),
        }


# =============================================================================
# Exports
# =============================================================================

__all__ = ["health_check"]
