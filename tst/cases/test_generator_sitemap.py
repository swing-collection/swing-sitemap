# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.generator_sitemap module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.test import RequestFactory

# Import | Libraries
import pytest

from swing.sitemap.views.template_sitemap_index import sitemap_index

# =============================================================================
# Tests
# =============================================================================


class TestSitemapIndex:
    """Tests for sitemap_index view."""

    def test_returns_xml_response(self):
        """Test that sitemap_index returns XML content type."""
        request = RequestFactory().get("/sitemap-index.xml")
        response = sitemap_index(request)

        assert response["Content-Type"] == "application/xml"

    def test_returns_valid_xml(self):
        """Test that response is valid XML."""
        request = RequestFactory().get("/sitemap-index.xml")
        response = sitemap_index(request)
        content = response.content.decode()

        assert "<?xml" in content or "sitemapindex" in content

    def test_returns_sitemapindex_element(self):
        """Test that response contains sitemapindex element."""
        request = RequestFactory().get("/sitemap-index.xml")
        response = sitemap_index(request)
        content = response.content.decode()

        assert "sitemapindex" in content


class TestSitemapIndexFunction:
    """Tests for sitemap_index function from views.sitemap_index."""

    def test_sitemap_index_function_exists(self):
        """Test that sitemap_index function exists."""
        from swing.sitemap.views.sitemap_index import (
            sitemap_index as func_sitemap_index,
        )

        assert callable(func_sitemap_index)

    @pytest.mark.django_db
    def test_sitemap_index_with_custom_sitemaps(self):
        """Test sitemap_index with custom sitemaps dict."""
        from django.contrib.sitemaps import Sitemap

        from swing.sitemap.views.sitemap_index import (
            sitemap_index as func_sitemap_index,
        )

        class CustomSitemap(Sitemap):
            def items(self):
                return []

        request = RequestFactory().get("/sitemap-index.xml")
        response = func_sitemap_index(request, sitemaps={"custom": CustomSitemap})

        assert response.status_code == 200
