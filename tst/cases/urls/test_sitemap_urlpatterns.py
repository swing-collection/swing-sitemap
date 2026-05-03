# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for swing.sitemap.urls.sitemap_urlpatterns module."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

# =============================================================================
# Tests
# =============================================================================


class TestSitemapUrlpatterns:
    """Tests for sitemap_urlpatterns function."""

    def test_returns_list_of_url_patterns(self):
        """Test sitemap_urlpatterns returns list of URL patterns."""
        from swing.sitemap.urls import sitemap_urlpatterns

        patterns = sitemap_urlpatterns()
        assert isinstance(patterns, list)
        assert len(patterns) >= 1

    def test_without_index(self):
        """Test sitemap_urlpatterns without index."""
        from swing.sitemap.urls import sitemap_urlpatterns

        patterns = sitemap_urlpatterns(include_index=False)
        pattern_names = [p.name for p in patterns]
        assert "swing-sitemap" in pattern_names
        assert "swing-sitemap-index" not in pattern_names

    def test_with_index(self):
        """Test sitemap_urlpatterns with index."""
        from swing.sitemap.urls import sitemap_urlpatterns

        patterns = sitemap_urlpatterns(include_index=True)
        pattern_names = [p.name for p in patterns]
        assert "swing-sitemap" in pattern_names
        assert "swing-sitemap-index" in pattern_names
        assert "swing-sitemap-section" in pattern_names

    def test_with_health_check(self):
        """Test sitemap_urlpatterns with health check enabled."""
        from swing.sitemap.urls import sitemap_urlpatterns

        patterns = sitemap_urlpatterns(include_health_check=True)
        pattern_names = [p.name for p in patterns]
        assert "swing-sitemap-health" in pattern_names

    def test_custom_sitemap_url(self):
        """Test sitemap_urlpatterns with custom URL."""
        from swing.sitemap.urls import sitemap_urlpatterns

        patterns = sitemap_urlpatterns(sitemap_url="custom-sitemap.xml")
        # Find the main sitemap pattern
        main = [p for p in patterns if p.name == "swing-sitemap"][0]
        assert "custom-sitemap.xml" in str(main.pattern)

    def test_with_custom_sitemaps(self):
        """Test sitemap_urlpatterns with custom sitemaps dict."""
        from django.contrib.sitemaps import Sitemap

        from swing.sitemap.urls import sitemap_urlpatterns

        class CustomSitemap(Sitemap):
            def items(self):
                return []

        patterns = sitemap_urlpatterns(sitemaps={"custom": CustomSitemap})
        assert len(patterns) >= 1
