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
    from swing.sitemap.views import HealthCheckView

    urlpatterns = [
        path("sitemap/health/", HealthCheckView.as_view(), name="sitemap_health"),
    ]

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import logging
import time
from typing import Any

from django.http import HttpRequest, HttpResponseBase, JsonResponse
from django.views import View

from swing.sitemap.conf import get_setting, validate_settings
from swing.sitemap.sitemaps import default_sitemaps

logger = logging.getLogger(__name__)


# =============================================================================
# Classes
# =============================================================================


class HealthCheckView(View):
    """
    Health Check View
    =================

    Health check endpoint for sitemap functionality.

    Returns JSON with status of various components:
    - settings: Configuration validation
    - sitemaps: Sitemap generation capability
    - cache: Cache backend status (if enabled)

    Query Parameters:
        verbose: Include detailed check information
        quick: Skip detailed checks (just confirm endpoint works)

    Usage::

        from swing.sitemap.views import HealthCheckView

        urlpatterns = [
            path("sitemap/health/", HealthCheckView.as_view()),
        ]

    """

    http_method_names = ["get", "head", "options"]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle GET request and return health status."""
        quick = request.GET.get("quick", "").lower() == "true"
        verbose = request.GET.get("verbose", "").lower() == "true"

        if quick:
            return JsonResponse(
                {
                    "status": "healthy",
                    "checks": {},
                    "timestamp": self._now_iso(),
                }
            )

        checks = {}
        overall_status = "healthy"

        # Check settings
        settings_check = self._check_settings(verbose)
        checks["settings"] = settings_check
        if not settings_check["ok"]:
            overall_status = "degraded"

        # Check sitemaps
        sitemaps_check = self._check_sitemaps(verbose)
        checks["sitemaps"] = sitemaps_check
        if not sitemaps_check["ok"]:
            overall_status = (
                "unhealthy" if overall_status != "degraded" else "degraded"
            )

        # Check cache (if enabled)
        cache_config = get_setting("cache", default={})
        if cache_config.get("enabled"):
            cache_check = self._check_cache(verbose)
            checks["cache"] = cache_check
            if not cache_check["ok"]:  # pragma: no cover
                overall_status = "degraded"

        # Check database
        db_check = self._check_database(verbose)
        checks["database"] = db_check
        if not db_check["ok"]:  # pragma: no cover
            overall_status = "unhealthy"

        status_code = (
            200
            if overall_status == "healthy"
            else 503 if overall_status == "unhealthy" else 200
        )

        return JsonResponse(
            {
                "status": overall_status,
                "checks": checks,
                "timestamp": self._now_iso(),
            },
            status=status_code,
        )

    def _now_iso(self) -> str:
        """Return current time as ISO string."""
        from django.utils import (
            timezone,  # pylint: disable=import-outside-toplevel
        )

        return timezone.now().isoformat()

    def _check_settings(self, verbose: bool) -> dict[str, Any]:
        """Check settings validation."""
        start = time.monotonic()
        try:
            is_valid, warnings = validate_settings(raise_errors=False)
            elapsed = time.monotonic() - start

            result: dict[str, Any] = {
                "ok": is_valid,
                "message": "Settings valid" if is_valid else "Settings have issues",
                "duration_ms": round(elapsed * 1000, 2),
            }

            if verbose and warnings:
                result["warnings"] = warnings

            return result

        except Exception as e:  # pragma: no cover  # noqa: BLE001  pylint: disable=broad-exception-caught
            elapsed = time.monotonic() - start
            logger.exception("Health check: settings validation failed")
            return {
                "ok": False,
                "message": f"Settings validation error: {e}",
                "duration_ms": round(elapsed * 1000, 2),
            }

    def _check_sitemaps(self, verbose: bool) -> dict[str, Any]:
        """Check sitemap generation."""
        start = time.monotonic()
        try:
            sitemaps = default_sitemaps()
            elapsed = time.monotonic() - start

            sitemap_count = len(sitemaps)
            total_urls = 0
            sitemap_info: dict[str, dict[str, Any]] = {}

            if verbose:
                for name, sitemap in sitemaps.items():
                    try:
                        if isinstance(sitemap, type):
                            sitemap = sitemap()
                        items = list(sitemap.items())
                        count = len(items)
                        total_urls += count
                        sitemap_info[name] = {"urls": count, "ok": True}
                    except (
                        Exception
                    ) as e:  # noqa: BLE001  pylint: disable=broad-exception-caught
                        sitemap_info[name] = {"ok": False, "error": str(e)}

            result: dict[str, Any] = {
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

    def _check_cache(self, verbose: bool) -> dict[str, Any]:
        """Check cache backend."""
        start = time.monotonic()
        try:
            from django.core.cache import (
                caches,  # pylint: disable=import-outside-toplevel
            )

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

    def _check_database(self, verbose: bool) -> dict[str, Any]:
        """Check database connectivity."""
        start = time.monotonic()
        try:
            from django.db import (
                connection,  # pylint: disable=import-outside-toplevel
            )

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
# Backward Compatibility
# =============================================================================


def health_check(request: HttpRequest) -> HttpResponseBase:
    """
    Legacy function-based health check.

    Deprecated: Use HealthCheckView.as_view() instead.
    """
    return HealthCheckView.as_view()(request)


# =============================================================================
# Exports
# =============================================================================

__all__ = ["health_check", "HealthCheckView"]
