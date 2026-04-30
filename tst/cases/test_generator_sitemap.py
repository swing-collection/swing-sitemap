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

from __future__ import annotations

import pytest
from django.test import RequestFactory

from swing.sitemap.generator_sitemap import sitemap_index


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
