# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.models.model_sitemap_url_image module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest

from swing.sitemap.models import ImageSitemapURL

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestImageSitemapURL:
    """Tests for ImageSitemapURL model."""

    def test_create_image_url(self):
        """Test creating an ImageSitemapURL instance."""
        url = ImageSitemapURL.objects.create(
            url="https://example.com/page/",
            image_url="https://example.com/images/photo.jpg",
            changefreq="weekly",
        )
        assert url.pk is not None
        assert url.image_url == "https://example.com/images/photo.jpg"

    def test_image_caption_field(self):
        """Test image_caption field."""
        url = ImageSitemapURL(
            url="https://example.com/page/",
            image_url="https://example.com/images/photo.jpg",
            image_caption="A beautiful landscape",
        )
        assert url.image_caption == "A beautiful landscape"

    def test_image_title_field(self):
        """Test image_title field."""
        url = ImageSitemapURL(
            url="https://example.com/page/",
            image_url="https://example.com/images/photo.jpg",
            image_title="Sunset Photo",
        )
        assert url.image_title == "Sunset Photo"

    def test_str_representation(self):
        """Test string representation."""
        url = ImageSitemapURL(
            url="https://example.com/page/",
            image_url="https://example.com/images/photo.jpg",
        )
        assert "example.com" in str(url)
