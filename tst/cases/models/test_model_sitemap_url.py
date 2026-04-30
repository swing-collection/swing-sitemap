# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.models import SitemapURL, URL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestSitemapURL:
    """Tests for SitemapURL model."""

    def test_create_sitemap_url(self):
        """Test creating a SitemapURL instance."""
        url = SitemapURL.objects.create(
            url="https://example.com/page/",
            priority=0.5,
            changefreq="weekly",
        )
        assert url.pk is not None
        assert url.url == "https://example.com/page/"

    def test_str_representation(self):
        """Test string representation."""
        url = SitemapURL(url="https://example.com/page/")
        assert str(url) == "https://example.com/page/"

    def test_priority_default(self):
        """Test default priority value."""
        url = SitemapURL(url="https://example.com/")
        assert url.priority == 0.5

    def test_changefreq_choices(self):
        """Test changefreq has valid choices."""
        valid_choices = ["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
        url = SitemapURL(url="https://example.com/", changefreq="weekly")
        assert url.changefreq in valid_choices


class TestURL:
    """Tests for URL model."""

    def test_url_is_abstract(self):
        """Test URL model is abstract."""
        assert URL._meta.abstract is True
