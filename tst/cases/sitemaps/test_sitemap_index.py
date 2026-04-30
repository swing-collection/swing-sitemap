# -*- coding: utf-8 -*-

"""
Tests for Pagination Support
============================
"""

from django.contrib.sitemaps import Sitemap
from django.test import override_settings

from swing.sitemap.sitemaps import (
    calculate_pages,
    paginate_all_sitemaps,
    paginate_sitemap,
    PaginatedSitemap,
    should_paginate,
)


class SimpleSitemap(Sitemap):
    """Simple sitemap for testing."""

    changefreq = "daily"
    priority = 0.7

    def __init__(self, items):
        self._items = items

    def items(self):
        return self._items

    def location(self, item):
        return f"https://example.com/{item}/"


class TestShouldPaginate:
    """Test should_paginate function."""

    def test_should_paginate_small_sitemap(self):
        """Test small sitemaps don't need pagination."""
        assert should_paginate(1000) is False
        assert should_paginate(49999) is False

    def test_should_paginate_large_sitemap(self):
        """Test large sitemaps need pagination."""
        assert should_paginate(50001) is True
        assert should_paginate(100000) is True

    @override_settings(SWING_SITEMAP={"pagination": {"enabled": False}})
    def test_should_paginate_disabled(self):
        """Test pagination can be disabled."""
        assert should_paginate(100000) is False


class TestCalculatePages:
    """Test calculate_pages function."""

    def test_calculate_pages_single(self):
        """Test single page calculation."""
        assert calculate_pages(100) == 1
        assert calculate_pages(50000) == 1

    def test_calculate_pages_multiple(self):
        """Test multiple pages calculation."""
        assert calculate_pages(50001) == 2
        assert calculate_pages(100000) == 2
        assert calculate_pages(150001) == 4

    def test_calculate_pages_empty(self):
        """Test empty sitemap."""
        assert calculate_pages(0) == 1


class TestPaginatedSitemap:
    """Test PaginatedSitemap class."""

    def test_paginated_sitemap_first_page(self):
        """Test first page of paginated sitemap."""
        items = list(range(100))
        source = SimpleSitemap(items)
        paginated = PaginatedSitemap(source, page=1, items_per_page=30)

        result = list(paginated.items())
        assert len(result) == 30
        assert result == list(range(30))

    def test_paginated_sitemap_second_page(self):
        """Test second page of paginated sitemap."""
        items = list(range(100))
        source = SimpleSitemap(items)
        paginated = PaginatedSitemap(source, page=2, items_per_page=30)

        result = list(paginated.items())
        assert len(result) == 30
        assert result == list(range(30, 60))

    def test_paginated_sitemap_last_page(self):
        """Test last page with partial items."""
        items = list(range(100))
        source = SimpleSitemap(items)
        paginated = PaginatedSitemap(source, page=4, items_per_page=30)

        result = list(paginated.items())
        assert len(result) == 10
        assert result == list(range(90, 100))

    def test_paginated_sitemap_inherits_attributes(self):
        """Test that paginated sitemap inherits source attributes."""
        source = SimpleSitemap([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        assert paginated.changefreq == "daily"
        assert paginated.priority == 0.7

    def test_paginated_sitemap_location(self):
        """Test location method delegates to source."""
        source = SimpleSitemap([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        assert paginated.location(1) == "https://example.com/1/"

    def test_paginated_sitemap_lastmod(self):
        """Test lastmod method delegates to source."""
        source = SimpleSitemap([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        # SimpleSitemap doesn't have lastmod, so should return None
        result = paginated.lastmod(1)
        assert result is None

    def test_paginated_sitemap_lastmod_with_source(self):
        """Test lastmod delegates to source when source has lastmod."""
        # Import | Standard Library
        from datetime import datetime

        class SitemapWithLastmod(SimpleSitemap):
            def lastmod(self, item):
                return datetime(2024, 1, item)

        source = SitemapWithLastmod([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        result = paginated.lastmod(2)
        assert result == datetime(2024, 1, 2)

    def test_paginated_sitemap_get_latest_lastmod_no_items(self):
        """Test get_latest_lastmod returns None for empty items."""
        source = SimpleSitemap([])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        assert paginated.get_latest_lastmod() is None

    def test_paginated_sitemap_get_latest_lastmod_no_lastmod(self):
        """Test get_latest_lastmod returns None when source has no lastmod."""
        source = SimpleSitemap([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        assert paginated.get_latest_lastmod() is None

    def test_paginated_sitemap_get_latest_lastmod(self):
        """Test get_latest_lastmod returns max date."""
        # Import | Standard Library
        from datetime import datetime

        class SitemapWithLastmod(SimpleSitemap):
            def lastmod(self, item):
                if item == 2:
                    return None  # Test None filtering
                return datetime(2024, 1, item)

        source = SitemapWithLastmod([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        result = paginated.get_latest_lastmod()
        assert result == datetime(2024, 1, 3)

    def test_paginated_sitemap_generator_items(self):
        """Test pagination with generator source."""

        class GeneratorSitemap:
            changefreq = "weekly"
            priority = 0.5

            def items(self):
                # Return a generator (not sliceable)
                return (x for x in range(100))

            def location(self, item):
                return f"https://example.com/{item}/"

        source = GeneratorSitemap()
        paginated = PaginatedSitemap(source, page=2, items_per_page=30)

        # This should still work by converting to list
        result = list(paginated.items())
        assert len(result) == 30
        assert result == list(range(30, 60))

    def test_paginated_sitemap_no_changefreq(self):
        """Test pagination when source has no changefreq/priority."""

        class MinimalSitemap:
            def items(self):
                return [1, 2, 3]

            def location(self, item):
                return f"https://example.com/{item}/"

        source = MinimalSitemap()
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        # Should not raise, just not have these attributes
        assert not hasattr(paginated, "changefreq")
        assert not hasattr(paginated, "priority")

    def test_paginated_sitemap_protocol(self):
        """Test that protocol is inherited from source."""

        class SitemapWithProtocol(SimpleSitemap):
            protocol = "https"

        source = SitemapWithProtocol([1, 2, 3])
        paginated = PaginatedSitemap(source, page=1, items_per_page=10)

        assert paginated.protocol == "https"


class TestPaginateSitemap:
    """Test paginate_sitemap function."""

    def test_paginate_small_sitemap(self):
        """Test small sitemap returns unchanged."""
        items = list(range(100))
        source = SimpleSitemap(items)

        result = paginate_sitemap(source, "test")

        assert len(result) == 1
        assert "test" in result
        assert result["test"] is source

    @override_settings(SWING_SITEMAP={"pagination": {"max_urls_per_sitemap": 30}})
    def test_paginate_large_sitemap(self):
        """Test large sitemap is paginated."""
        items = list(range(100))
        source = SimpleSitemap(items)

        result = paginate_sitemap(source, "test")

        assert len(result) == 4
        assert "test-1" in result
        assert "test-2" in result
        assert "test-3" in result
        assert "test-4" in result

    def test_paginate_sitemap_names(self):
        """Test paginated sitemap names."""
        items = list(range(100))
        source = SimpleSitemap(items)

        result = paginate_sitemap(source, "pages")

        # Should have original name since it's small
        assert "pages" in result


class TestPaginateAllSitemaps:
    """Test paginate_all_sitemaps function."""

    @override_settings(SWING_SITEMAP={"pagination": {"max_urls_per_sitemap": 30}})
    def test_paginate_multiple_sitemaps(self):
        """Test paginating multiple sitemaps."""
        sitemaps = {
            "small": SimpleSitemap(list(range(10))),
            "large": SimpleSitemap(list(range(100))),
        }

        result = paginate_all_sitemaps(sitemaps)

        # Small should be unchanged
        assert "small" in result

        # Large should be paginated
        assert "large-1" in result
        assert "large-2" in result
        assert "large-3" in result
        assert "large-4" in result

    def test_paginate_handles_classes(self):
        """Test that sitemap classes are instantiated."""

        class TestSitemapClass(Sitemap):
            def items(self):
                return [1, 2, 3]

            def location(self, item):
                return f"/{item}/"

        sitemaps = {"test": TestSitemapClass}
        result = paginate_all_sitemaps(sitemaps)

        assert "test" in result
        assert not isinstance(result["test"], type)
