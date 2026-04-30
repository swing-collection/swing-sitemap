# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url_standard module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.models import StandardSitemapURL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestStandardSitemapURL:
    """Tests for StandardSitemapURL model."""

    def test_create_standard_url(self):
        """Test creating a StandardSitemapURL instance."""
        url = StandardSitemapURL.objects.create(
            url="https://example.com/page/",
            name="Home Page",
            priority=0.8,
            changefreq="daily",
        )
        assert url.pk is not None
        assert url.url == "https://example.com/page/"
        assert url.name == "Home Page"

    def test_inherits_from_url(self):
        """Test that StandardSitemapURL inherits from URL."""
        from swing.sitemap.models import URL

        assert issubclass(StandardSitemapURL, URL)

    def test_get_absolute_url(self):
        """Test get_absolute_url method."""
        url = StandardSitemapURL(
            url="https://example.com/page/",
            name="Test",
        )
        assert url.get_absolute_url() == "https://example.com/page/"
