# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url_news module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest
from django.utils import timezone

from swing.sitemap.models import NewsSitemapURL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestNewsSitemapURL:
    """Tests for NewsSitemapURL model."""

    def test_create_news_url(self):
        """Test creating a NewsSitemapURL instance."""
        url = NewsSitemapURL.objects.create(
            url="https://example.com/news/breaking/",
            publication_name="Example News",
            publication_language="en",
            title="Breaking News Story",
            publication_date=timezone.now(),
            changefreq="always",
        )
        assert url.pk is not None
        assert url.title == "Breaking News Story"

    def test_publication_name_field(self):
        """Test publication_name field."""
        url = NewsSitemapURL(
            url="https://example.com/news/1/",
            publication_name="Daily News",
            publication_language="en",
            title="Test",
            publication_date=timezone.now(),
        )
        assert url.publication_name == "Daily News"

    def test_publication_language_field(self):
        """Test publication_language field."""
        url = NewsSitemapURL(
            url="https://example.com/news/1/",
            publication_name="News",
            publication_language="de",
            title="Test",
            publication_date=timezone.now(),
        )
        assert url.publication_language == "de"

    def test_str_representation(self):
        """Test string representation."""
        url = NewsSitemapURL(
            url="https://example.com/news/1/",
            publication_name="Example News",
            publication_language="en",
            title="Breaking Story",
            publication_date=timezone.now(),
        )
        assert "Breaking Story" in str(url)
