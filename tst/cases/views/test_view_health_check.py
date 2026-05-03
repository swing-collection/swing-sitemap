# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


"""
Tests for swing.sitemap.views.view_health_check module.
"""


# Import | Future
from __future__ import annotations

# Import | Standard Library
import json
from unittest.mock import MagicMock, patch

from django.test import RequestFactory

# Import | Libraries
import pytest


@pytest.fixture
def rf():
    """Provide a RequestFactory."""
    return RequestFactory()


@pytest.mark.django_db
class TestHealthCheck:
    """Tests for health_check view."""

    def test_quick_mode_returns_healthy(self, rf):
        """Test quick mode skips detailed checks."""
        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/?quick=true")
        response = health_check(request)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["status"] == "healthy"
        assert data["checks"] == {}
        assert "timestamp" in data

    def test_full_health_check(self, rf):
        """Test full health check with all checks."""
        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/")
        response = health_check(request)

        data = json.loads(response.content)
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "settings" in data["checks"]
        assert "sitemaps" in data["checks"]
        assert "database" in data["checks"]
        assert "timestamp" in data

    def test_verbose_mode(self, rf):
        """Test verbose mode includes extra details."""
        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/?verbose=true")
        response = health_check(request)

        data = json.loads(response.content)
        assert "checks" in data

    @patch("swing.sitemap.views.view_health_check.get_setting")
    def test_cache_check_when_enabled(self, mock_get_setting, rf):
        """Test cache check runs when cache enabled."""
        mock_get_setting.return_value = {"enabled": True, "backend": "default"}

        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/")
        response = health_check(request)

        data = json.loads(response.content)
        assert "cache" in data["checks"]


class TestNowIso:
    """Tests for _now_iso function."""

    def test_returns_iso_string(self):
        """Test returns ISO formatted string."""
        from swing.sitemap.views.view_health_check import _now_iso

        result = _now_iso()
        assert isinstance(result, str)
        # ISO format contains T separator
        assert "T" in result


class TestCheckSettings:
    """Tests for _check_settings function."""

    def test_check_settings_valid(self):
        """Test check_settings with valid settings."""
        from swing.sitemap.views.view_health_check import _check_settings

        result = _check_settings(verbose=False)
        assert result["ok"] is True
        assert "duration_ms" in result

    def test_check_settings_verbose_with_warnings(self):
        """Test check_settings verbose mode shows warnings."""
        from swing.sitemap.views.view_health_check import _check_settings

        result = _check_settings(verbose=True)
        assert result["ok"] is True
        # Warnings may or may not be present depending on config

    @patch("swing.sitemap.views.view_health_check.validate_settings")
    def test_check_settings_handles_exception(self, mock_validate):
        """Test check_settings handles exceptions."""
        mock_validate.side_effect = Exception("Test error")

        from swing.sitemap.views.view_health_check import _check_settings

        result = _check_settings(verbose=False)
        assert result["ok"] is False
        assert "Test error" in result["message"]


class TestCheckSitemaps:
    """Tests for _check_sitemaps function."""

    def test_check_sitemaps_default(self):
        """Test check_sitemaps with default config."""
        from swing.sitemap.views.view_health_check import _check_sitemaps

        result = _check_sitemaps(verbose=False)
        assert result["ok"] is True
        assert "sitemap_count" in result
        assert "duration_ms" in result

    @patch("swing.sitemap.views.view_health_check.default_sitemaps")
    def test_check_sitemaps_verbose(self, mock_sitemaps):
        """Test check_sitemaps verbose mode."""
        mock_sitemap = MagicMock()
        mock_sitemap.items.return_value = ["url1", "url2"]
        mock_sitemaps.return_value = {"test": mock_sitemap}

        from swing.sitemap.views.view_health_check import _check_sitemaps

        result = _check_sitemaps(verbose=True)
        assert result["ok"] is True
        assert "sitemaps" in result
        assert "test" in result["sitemaps"]
        assert result["total_urls"] == 2

    @patch("swing.sitemap.views.view_health_check.default_sitemaps")
    def test_check_sitemaps_handles_exception(self, mock_sitemaps):
        """Test check_sitemaps handles exceptions."""
        mock_sitemaps.side_effect = Exception("Test error")

        from swing.sitemap.views.view_health_check import _check_sitemaps

        result = _check_sitemaps(verbose=False)
        assert result["ok"] is False
        assert "Test error" in result["message"]

    @patch("swing.sitemap.views.view_health_check.default_sitemaps")
    def test_check_sitemaps_verbose_handles_sitemap_error(self, mock_sitemaps):
        """Test check_sitemaps verbose handles individual sitemap errors."""
        mock_sitemap = MagicMock()
        mock_sitemap.items.side_effect = Exception("Sitemap error")
        mock_sitemaps.return_value = {"broken": mock_sitemap}

        from swing.sitemap.views.view_health_check import _check_sitemaps

        result = _check_sitemaps(verbose=True)
        assert result["ok"] is True  # Overall still ok
        assert "broken" in result["sitemaps"]
        assert result["sitemaps"]["broken"]["ok"] is False


@pytest.mark.django_db
class TestCheckCache:
    """Tests for _check_cache function."""

    def test_check_cache_works(self):
        """Test check_cache with default cache."""
        from swing.sitemap.views.view_health_check import _check_cache

        result = _check_cache(verbose=False)
        assert result["ok"] is True
        assert "duration_ms" in result
        assert result["message"] == "Cache working"

    @patch("swing.sitemap.views.view_health_check.get_setting")
    def test_check_cache_handles_exception(self, mock_get_setting):
        """Test check_cache handles exceptions."""
        # Configure to use a non-existent cache backend
        mock_get_setting.return_value = {"backend": "nonexistent_cache_backend"}

        from swing.sitemap.views.view_health_check import _check_cache

        result = _check_cache(verbose=False)
        assert result["ok"] is False
        assert "error" in result["message"].lower()


@pytest.mark.django_db
class TestCheckDatabase:
    """Tests for _check_database function."""

    def test_check_database_works(self):
        """Test check_database with default database."""
        from swing.sitemap.views.view_health_check import _check_database

        result = _check_database(verbose=False)
        assert result["ok"] is True
        assert "duration_ms" in result
        assert result["message"] == "Database connected"

    @patch("django.db.connection")
    def test_check_database_handles_exception(self, mock_conn):
        """Test check_database handles exceptions."""
        mock_conn.cursor.side_effect = Exception("DB error")

        from swing.sitemap.views.view_health_check import _check_database

        result = _check_database(verbose=False)
        assert result["ok"] is False
        assert "DB error" in result["message"]


@pytest.mark.django_db
class TestHealthCheckEdgeCases:
    """Tests for health_check edge cases."""

    @patch("swing.sitemap.views.view_health_check._check_settings")
    def test_health_check_degraded_on_settings_failure(self, mock_check, rf):
        """Test health check returns degraded status on settings issues."""
        mock_check.return_value = {"ok": False, "message": "Settings invalid"}

        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/")
        response = health_check(request)

        data = json.loads(response.content)
        assert data["status"] == "degraded"

    @patch("swing.sitemap.views.view_health_check._check_database")
    def test_health_check_unhealthy_on_db_failure(self, mock_check, rf):
        """Test health check returns unhealthy status on database failure."""
        mock_check.return_value = {"ok": False, "message": "DB unreachable"}

        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/")
        response = health_check(request)

        data = json.loads(response.content)
        assert data["status"] == "unhealthy"
        assert response.status_code == 503

    @patch("swing.sitemap.views.view_health_check._check_sitemaps")
    def test_health_check_on_sitemap_failure(self, mock_check, rf):
        """Test health check handles sitemap check failure."""
        mock_check.return_value = {"ok": False, "message": "Sitemap error"}

        from swing.sitemap.views.view_health_check import health_check

        request = rf.get("/health/")
        response = health_check(request)

        data = json.loads(response.content)
        # Should be unhealthy when sitemaps fail
        assert data["status"] in ["unhealthy", "degraded"]
