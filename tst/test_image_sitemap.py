# -*- coding: utf-8 -*-

"""
Tests for Image Sitemap
=======================
"""

import datetime
from unittest.mock import Mock

import pytest
from django.test import override_settings

from swing_sitemap.sitemaps.sitemap_image import ImageSitemap


class MockPage:
    """Mock page model with images for testing."""

    def __init__(self, pk=1, updated_at=None, images=None):
        self.pk = pk
        self.updated_at = updated_at or datetime.datetime.now()
        self._images = images or []

    def get_absolute_url(self):
        return f"https://example.com/pages/{self.pk}/"

    def get_images(self):
        return self._images


class TestImageSitemap:
    """Test ImageSitemap class."""

    def test_init_with_queryset(self):
        """Test initialization with queryset."""
        pages = [MockPage(pk=1), MockPage(pk=2)]
        sitemap = ImageSitemap(queryset=pages)

        items = list(sitemap.items())
        assert len(items) == 2

    def test_init_with_callable(self):
        """Test initialization with callable queryset."""
        pages = [MockPage(pk=1)]
        sitemap = ImageSitemap(queryset=lambda: pages)

        items = list(sitemap.items())
        assert len(items) == 1

    def test_location(self):
        """Test location method."""
        page = MockPage(pk=1)
        sitemap = ImageSitemap(queryset=[page])

        assert sitemap.location(page) == "https://example.com/pages/1/"

    def test_lastmod(self):
        """Test lastmod method."""
        page = MockPage(pk=1)
        sitemap = ImageSitemap(queryset=[page], date_field="updated_at")

        lastmod = sitemap.lastmod(page)
        assert lastmod is not None

    def test_get_images_with_dicts(self):
        """Test get_images with dict format."""
        images = [
            {
                "loc": "https://example.com/image1.jpg",
                "caption": "Image 1",
                "title": "First Image",
            },
            {
                "loc": "https://example.com/image2.jpg",
                "caption": "Image 2",
            },
        ]
        page = MockPage(pk=1, images=images)
        sitemap = ImageSitemap(queryset=[page])

        result = sitemap.get_images(page)
        assert len(result) == 2
        assert result[0]["loc"] == "https://example.com/image1.jpg"
        assert result[0]["caption"] == "Image 1"
        assert result[0]["title"] == "First Image"

    def test_get_images_with_strings(self):
        """Test get_images with string URLs."""
        images = [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg",
        ]
        page = MockPage(pk=1, images=images)
        sitemap = ImageSitemap(queryset=[page])

        result = sitemap.get_images(page)
        assert len(result) == 2
        assert result[0]["loc"] == "https://example.com/image1.jpg"

    def test_get_images_limited_to_1000(self):
        """Test images are limited to 1000 per URL per Google spec."""
        images = [f"https://example.com/image{i}.jpg" for i in range(1500)]
        page = MockPage(pk=1, images=images)
        sitemap = ImageSitemap(queryset=[page])

        result = sitemap.get_images(page)
        assert len(result) == 1000

    def test_get_images_skips_invalid(self):
        """Test that invalid image entries are skipped."""
        images = [
            {"loc": "https://example.com/valid.jpg"},
            {"no_loc": "missing"},  # Invalid - no loc
            None,  # Invalid
            "https://example.com/string.jpg",  # Valid string
        ]
        page = MockPage(pk=1, images=images)
        sitemap = ImageSitemap(queryset=[page])

        result = sitemap.get_images(page)
        # Should only have 2 valid images
        assert len(result) == 2

    def test_image_loc(self):
        """Test image_loc method."""
        img = {"loc": "https://example.com/image.jpg"}
        sitemap = ImageSitemap(queryset=[])

        assert sitemap.image_loc(img) == "https://example.com/image.jpg"

    def test_image_caption(self):
        """Test image_caption method with escaping."""
        img = {"loc": "...", "caption": "Test <caption> & text"}
        sitemap = ImageSitemap(queryset=[])

        caption = sitemap.image_caption(img)
        assert "<" not in caption
        assert "&" not in caption or "&amp;" in caption

    def test_image_title(self):
        """Test image_title method."""
        img = {"loc": "...", "title": "Image Title"}
        sitemap = ImageSitemap(queryset=[])

        assert sitemap.image_title(img) == "Image Title"

    def test_image_geo_location(self):
        """Test image_geo_location method."""
        img = {"loc": "...", "geo_location": "New York, NY"}
        sitemap = ImageSitemap(queryset=[])

        assert sitemap.image_geo_location(img) == "New York, NY"

    def test_image_license(self):
        """Test image_license method."""
        img = {"loc": "...", "license": "https://creativecommons.org/licenses/by/4.0/"}
        sitemap = ImageSitemap(queryset=[])

        assert sitemap.image_license(img) == "https://creativecommons.org/licenses/by/4.0/"

    def test_urls_includes_images(self):
        """Test that _urls method includes image data."""
        images = [{"loc": "https://example.com/image.jpg", "caption": "Test"}]
        page = MockPage(pk=1, images=images)
        sitemap = ImageSitemap(queryset=[page])

        urls = sitemap._urls(1, "https", "example.com")

        assert len(urls) == 1
        assert "images" in urls[0]
        assert len(urls[0]["images"]) == 1

    def test_default_priority_and_changefreq(self):
        """Test default priority and changefreq."""
        sitemap = ImageSitemap(queryset=[])

        assert sitemap.priority == 0.5
        assert sitemap.changefreq == "monthly"

    def test_custom_priority_and_changefreq(self):
        """Test custom priority and changefreq."""
        sitemap = ImageSitemap(queryset=[], priority=0.7, changefreq="weekly")

        assert sitemap.priority == 0.7
        assert sitemap.changefreq == "weekly"

    def test_custom_image_attr(self):
        """Test custom image_attr callable."""
        page = Mock()
        page.pk = 1
        page.gallery = [
            {"loc": "https://example.com/gallery1.jpg"},
        ]
        page.get_absolute_url = lambda: "https://example.com/page/1/"

        sitemap = ImageSitemap(
            queryset=[page],
            image_attr=lambda obj: obj.gallery,
        )

        images = sitemap.get_images(page)
        assert len(images) == 1
        assert images[0]["loc"] == "https://example.com/gallery1.jpg"


@pytest.mark.django_db
class TestImageSitemapFromSettings:
    """Test ImageSitemap.from_settings method."""

    @override_settings(
        SWING_SITEMAP={
            "image": {
                "model": "auth.User",
                "date_field": "date_joined",
                "image_attr": "get_images",
            },
        }
    )
    def test_from_settings_image_config(self):
        """Test building from SWING_SITEMAP['image'] config."""
        sitemap = ImageSitemap.from_settings()
        assert sitemap is not None
        assert sitemap.date_field == "date_joined"
        assert sitemap.image_attr == "get_images"

    def test_from_settings_missing_model_raises(self):
        """Test that missing model raises ValueError."""
        with pytest.raises(ValueError, match="must define a 'model'"):
            ImageSitemap.from_settings("nonexistent")
