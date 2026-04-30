# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url_custom module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.models import CustomSitemapURL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCustomSitemapURL:
    """Tests for CustomSitemapURL model."""

    def test_create_custom_url(self):
        """Test creating a CustomSitemapURL instance."""
        url = CustomSitemapURL.objects.create(
            url="https://example.com/custom/page/",
            custom_field="custom_value",
            priority=0.9,
            changefreq="hourly",
        )
        assert url.pk is not None
        assert url.url == "https://example.com/custom/page/"

    def test_inherits_from_url(self):
        """Test that CustomSitemapURL inherits from URL."""
        from swing.sitemap.models import URL

        assert issubclass(CustomSitemapURL, URL)

    def test_custom_data_field(self):
        """Test custom_data JSON field."""
        url = CustomSitemapURL(
            url="https://example.com/custom/",
            custom_field="test",
            custom_data={"key": "value"},
        )
        assert url.custom_data == {"key": "value"}

    def test_str_representation(self):
        """Test string representation."""
        url = CustomSitemapURL(
            url="https://example.com/custom/",
            custom_field="my_field",
        )
        assert "example.com" in str(url)
