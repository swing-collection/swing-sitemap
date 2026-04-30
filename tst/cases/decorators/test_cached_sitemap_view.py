# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for cached_sitemap_view decorator."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.http import HttpResponse
from django.test import RequestFactory

# Import | Libraries
import pytest

from swing.sitemap.decorators import cached_sitemap_view

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCachedSitemapView:
    """Tests for cached_sitemap_view decorator."""

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before each test."""
        from django.core.cache import cache

        cache.clear()

    def test_decorator_when_cache_disabled(self, factory, settings):
        """Test decorator passes through when cache disabled."""
        settings.SWING_SITEMAP = {"cache": {"enabled": False}}

        @cached_sitemap_view()
        def view(request):
            return HttpResponse("<xml/>", content_type="application/xml")

        request = factory.get("/sitemap-disabled.xml")
        response = view(request)
        assert response.status_code == 200
        assert "X-Sitemap-Cache" not in response

    def test_decorator_when_cache_enabled_miss(self, factory, settings):
        """Test decorator caches on miss."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True, "timeout": 60}}

        @cached_sitemap_view()
        def view(request):
            return HttpResponse("<xml/>", content_type="application/xml")

        request = factory.get("/sitemap-miss.xml")
        response = view(request)
        assert response.status_code == 200
        assert response.get("X-Sitemap-Cache") == "MISS"

    def test_decorator_with_custom_cache_key_func(self, factory, settings):
        """Test decorator with custom cache key function."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True, "timeout": 60}}

        @cached_sitemap_view(cache_key_func=lambda r: f"custom-{r.path}")
        def view(request):
            return HttpResponse("<xml/>", content_type="application/xml")

        request = factory.get("/sitemap-custom.xml")
        response = view(request)
        assert response.status_code == 200

    def test_decorator_with_timeout_override(self, factory, settings):
        """Test decorator with timeout override."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True, "timeout": 60}}

        @cached_sitemap_view(timeout=120)
        def view(request):
            return HttpResponse("<xml/>", content_type="application/xml")

        request = factory.get("/sitemap-timeout.xml")
        response = view(request)
        assert response.status_code == 200

    def test_decorator_does_not_cache_error_response(self, factory, settings):
        """Test decorator does not cache error responses."""
        settings.SWING_SITEMAP = {"cache": {"enabled": True, "timeout": 60}}

        @cached_sitemap_view()
        def view(request):
            return HttpResponse("Error", status=500)

        # Use unique path to avoid cache conflicts
        request = factory.get("/sitemap-error-test.xml")
        response = view(request)
        assert response.status_code == 500
