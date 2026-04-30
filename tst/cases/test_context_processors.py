# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.context_processors module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.test import RequestFactory

from swing.sitemap.context_processors import sitemap_url


# =============================================================================
# Tests
# =============================================================================


class TestSitemapUrlContextProcessor:
    """Tests for sitemap_url context processor."""

    def test_returns_absolute_url(self):
        """Test that context processor returns absolute sitemap URL."""
        request = RequestFactory().get("/", HTTP_HOST="example.com")
        ctx = sitemap_url(request)

        assert "SITEMAP_URL" in ctx
        assert "example.com" in ctx["SITEMAP_URL"]
        assert "sitemap" in ctx["SITEMAP_URL"]

    def test_returns_https_when_secure(self):
        """Test HTTPS is used for secure requests."""
        request = RequestFactory().get("/", HTTP_HOST="example.com", secure=True)
        ctx = sitemap_url(request)

        assert ctx["SITEMAP_URL"].startswith("https://")

    def test_returns_http_when_not_secure(self):
        """Test HTTP is used for non-secure requests."""
        request = RequestFactory().get("/", HTTP_HOST="example.com")
        ctx = sitemap_url(request)

        assert ctx["SITEMAP_URL"].startswith("http://")
