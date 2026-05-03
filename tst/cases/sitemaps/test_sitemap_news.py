# -*- coding: utf-8 -*-

"""
Tests for News Sitemap
======================
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import datetime
from unittest.mock import Mock

from django.test import override_settings
from django.utils import timezone

# Import | Libraries
import pytest

from swing.sitemap.sitemaps.sitemap_news import NewsSitemap


class MockArticle:
    """Mock article model for testing."""

    def __init__(
        self,
        pk=1,
        title="Test Article",
        publication_name="Test Publication",
        publication_language="en",
        publication_date=None,
        genres=None,
        keywords=None,
    ):
        self.pk = pk
        self.title = title
        self.publication_name = publication_name
        self.publication_language = publication_language
        self.publication_date = publication_date or timezone.now()
        self.genres = genres
        self.keywords = keywords

    def get_absolute_url(self):
        return f"https://example.com/news/{self.pk}/"


class TestNewsSitemap:
    """Test NewsSitemap class."""

    def test_init_with_queryset(self):
        """Test initialization with queryset."""
        articles = [MockArticle(pk=1), MockArticle(pk=2)]
        sitemap = NewsSitemap(queryset=articles)

        items = list(sitemap.items())
        assert len(items) == 2

    def test_items_limited_to_1000(self):
        """Test that items are limited to 1000 per Google spec."""
        articles = [MockArticle(pk=i) for i in range(1500)]
        sitemap = NewsSitemap(queryset=articles)

        items = list(sitemap.items())
        assert len(items) == 1000

    def test_location(self):
        """Test location method."""
        article = MockArticle(pk=1)
        sitemap = NewsSitemap(queryset=[article])

        assert sitemap.location(article) == "https://example.com/news/1/"

    def test_news_publication_name(self):
        """Test news_publication_name method."""
        article = MockArticle(pk=1, publication_name="Test <Pub>")
        sitemap = NewsSitemap(queryset=[article])

        name = sitemap.news_publication_name(article)
        # Should be escaped
        assert "<" not in name

    def test_news_publication_name_fallback(self):
        """Test publication_name falls back to sitemap default."""
        article = Mock()
        article.publication_name = None
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            publication_name="Default Publication",
            news_fields={"publication_name": "publication_name"},
        )

        name = sitemap.news_publication_name(article)
        assert name == "Default Publication"

    def test_news_publication_language(self):
        """Test news_publication_language method."""
        article = MockArticle(pk=1, publication_language="de")
        sitemap = NewsSitemap(queryset=[article])

        lang = sitemap.news_publication_language(article)
        assert lang == "de"

    def test_news_title(self):
        """Test news_title method."""
        article = MockArticle(pk=1, title="Breaking <News> & Updates")
        sitemap = NewsSitemap(queryset=[article])

        title = sitemap.news_title(article)
        # Should be escaped
        assert "<" not in title
        assert "&" not in title or "&amp;" in title

    def test_news_publication_date(self):
        """Test news_publication_date method."""
        pub_date = timezone.now()
        article = MockArticle(pk=1, publication_date=pub_date)
        sitemap = NewsSitemap(queryset=[article])

        date_str = sitemap.news_publication_date(article)
        assert date_str is not None
        # Should be in ISO format
        assert "T" in date_str

    def test_news_genres_valid(self):
        """Test news_genres with valid genres."""
        article = MockArticle(pk=1, genres="PressRelease, Blog")
        sitemap = NewsSitemap(queryset=[article])

        genres = sitemap.news_genres(article)
        assert "PressRelease" in genres
        assert "Blog" in genres

    def test_news_genres_filters_invalid(self):
        """Test news_genres filters out invalid genres."""
        article = MockArticle(pk=1, genres="PressRelease, InvalidGenre, Blog")
        sitemap = NewsSitemap(queryset=[article])

        genres = sitemap.news_genres(article)
        assert "InvalidGenre" not in genres
        assert "PressRelease" in genres
        assert "Blog" in genres

    def test_news_keywords(self):
        """Test news_keywords method."""
        article = MockArticle(pk=1, keywords="tech, news, breaking")
        sitemap = NewsSitemap(queryset=[article])

        keywords = sitemap.news_keywords(article)
        assert "tech" in keywords
        assert "news" in keywords
        assert "breaking" in keywords

    def test_news_keywords_limited_to_10(self):
        """Test keywords are limited to 10."""
        many_keywords = ", ".join(f"keyword{i}" for i in range(20))
        article = MockArticle(pk=1, keywords=many_keywords)
        sitemap = NewsSitemap(queryset=[article])

        keywords = sitemap.news_keywords(article)
        # Count commas to estimate number of keywords
        assert keywords.count(",") <= 9  # 10 keywords = 9 commas

    def test_build_news_xml(self):
        """Test _build_news_xml method."""
        article = MockArticle(
            pk=1,
            title="Test Article",
            publication_name="Test Pub",
            publication_language="en",
            genres="PressRelease",
            keywords="test, news",
        )
        sitemap = NewsSitemap(queryset=[article])

        xml = sitemap._build_news_xml(article)

        assert "<news:news>" in xml
        assert "</news:news>" in xml
        assert "<news:publication>" in xml
        assert "<news:name>Test Pub</news:name>" in xml
        assert "<news:language>en</news:language>" in xml
        assert "<news:title>" in xml
        assert "<news:genres>PressRelease</news:genres>" in xml
        assert "<news:keywords>" in xml

    def test_urls_includes_news_data(self):
        """Test that _urls method includes news XML."""
        article = MockArticle(pk=1)
        sitemap = NewsSitemap(queryset=[article])

        urls = sitemap._urls(1, "https", "example.com")

        assert len(urls) == 1
        assert "news" in urls[0]
        assert "<news:news>" in urls[0]["news"]

    def test_default_priority_and_changefreq(self):
        """Test default priority and changefreq."""
        sitemap = NewsSitemap(queryset=[])

        assert sitemap.priority == 1.0
        assert sitemap.changefreq == "always"

    def test_max_age_hours(self):
        """Test max_age_hours parameter."""
        # Create articles with different ages
        now = timezone.now()
        old_article = MockArticle(
            pk=1, publication_date=now - datetime.timedelta(hours=72)
        )
        recent_article = MockArticle(
            pk=2, publication_date=now - datetime.timedelta(hours=24)
        )

        # With max_age_hours, from_settings would filter automatically
        # Here we just test the parameter is stored
        sitemap = NewsSitemap(queryset=[], max_age_hours=48)
        assert sitemap.max_age_hours == 48

    def test_news_title_escapes_html(self):
        """Test news title escapes HTML characters."""
        article = MockArticle(pk=1, title="<script>alert('xss')</script>")
        sitemap = NewsSitemap(queryset=[article])

        title = sitemap.news_title(article)
        # Should be escaped
        assert "<script>" not in title

    def test_news_publication_date_handles_date(self):
        """Test news_publication_date handles date objects."""
        article = MockArticle(pk=1)
        article.publication_date = datetime.date(2024, 1, 15)
        sitemap = NewsSitemap(queryset=[article])

        date_str = sitemap.news_publication_date(article)
        assert "2024-01-15" in date_str

    def test_news_genres_as_list(self):
        """Test news_genres handles list input."""
        article = MockArticle(pk=1)
        article.genres = ["PressRelease", "Blog"]
        sitemap = NewsSitemap(queryset=[article])

        genres = sitemap.news_genres(article)
        assert "PressRelease" in genres
        assert "Blog" in genres

    def test_news_keywords_as_list(self):
        """Test news_keywords handles list input."""
        article = MockArticle(pk=1)
        article.keywords = ["tech", "news", "breaking"]
        sitemap = NewsSitemap(queryset=[article])

        keywords = sitemap.news_keywords(article)
        assert "tech" in keywords
        assert "news" in keywords

    def test_news_stock_tickers(self):
        """Test news_stock_tickers method."""
        article = MockArticle(pk=1)
        article.stock_tickers = "NASDAQ:GOOG, NYSE:T"
        sitemap = NewsSitemap(queryset=[article])

        tickers = sitemap.news_stock_tickers(article)
        assert "NASDAQ:GOOG" in tickers


@pytest.mark.django_db
class TestNewsSitemapFromSettings:
    """Test NewsSitemap.from_settings method."""

    @override_settings(
        SWING_SITEMAP={
            "news": {
                "model": "auth.User",
                "publication_name": "Test News",
                "publication_language": "en",
                "date_field": "date_joined",
                "max_age_hours": 48,
            },
        }
    )
    def test_from_settings_news_config(self):
        """Test building from SWING_SITEMAP['news'] config."""
        sitemap = NewsSitemap.from_settings()
        assert sitemap is not None
        assert sitemap.publication_name == "Test News"
        assert sitemap.publication_language == "en"
        assert sitemap.max_age_hours == 48

    def test_from_settings_missing_model_raises(self):
        """Test that missing model raises ValueError."""
        with pytest.raises(ValueError, match="must define a 'model'"):
            NewsSitemap.from_settings("nonexistent")

    @override_settings(
        SWING_SITEMAP={
            "news": {
                "model": "auth.User",
                "publication_name": "Test",
                "publication_language": "en",
                "date_field": "date_joined",
                "max_age_hours": None,  # Disable auto-filtering
                "filters": {"is_active": True},
                "exclude": {"is_superuser": True},
                "order_by": ["-date_joined"],
            },
        }
    )
    def test_from_settings_with_filters_exclude_order_by(self):
        """Test from_settings with filters, exclude, and order_by."""
        sitemap = NewsSitemap.from_settings()
        assert sitemap is not None
        # Call items() to trigger the queryset factory
        items = list(sitemap.items())
        assert isinstance(items, list)


class TestNewsSitemapAdditional:
    """Additional tests for NewsSitemap to improve coverage."""

    def test_location_with_callable_attr(self):
        """Test location method with callable location_attr."""
        article = MockArticle(pk=42)
        sitemap = NewsSitemap(
            queryset=[article],
            location_attr=lambda obj: f"https://custom.com/article/{obj.pk}/",
        )

        assert sitemap.location(article) == "https://custom.com/article/42/"

    def test_news_access(self):
        """Test news_access method."""
        article = Mock()
        article.access = "Subscription"
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={"access": "access"},
        )

        access = sitemap.news_access(article)
        assert access == "Subscription"

    def test_news_access_registration(self):
        """Test news_access with Registration value."""
        article = Mock()
        article.access = "Registration"
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={"access": "access"},
        )

        access = sitemap.news_access(article)
        assert access == "Registration"

    def test_news_access_invalid_returns_none(self):
        """Test news_access with invalid value returns None."""
        article = Mock()
        article.access = "FreeAccess"  # Invalid
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={"access": "access"},
        )

        access = sitemap.news_access(article)
        assert access is None

    def test_news_stock_tickers_as_list(self):
        """Test news_stock_tickers handles list input."""
        article = Mock()
        article.stock_tickers = ["NASDAQ:GOOG", "NYSE:T"]
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={"stock_tickers": "stock_tickers"},
        )

        tickers = sitemap.news_stock_tickers(article)
        assert "NASDAQ:GOOG" in tickers
        assert "NYSE:T" in tickers

    def test_news_stock_tickers_limited_to_5(self):
        """Test stock tickers are limited to 5."""
        article = Mock()
        article.stock_tickers = [f"NASDAQ:TEST{i}" for i in range(10)]
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={"stock_tickers": "stock_tickers"},
        )

        tickers = sitemap.news_stock_tickers(article)
        assert tickers.count(",") == 4  # 5 tickers = 4 commas

    def test_build_news_xml_with_all_optional_fields(self):
        """Test _build_news_xml with all optional fields."""
        article = Mock()
        article.title = "Test Article"
        article.publication_name = "Test Pub"
        article.publication_language = "en"
        article.publication_date = datetime.datetime(2024, 1, 15, 10, 30, 0)
        article.access = "Subscription"
        article.genres = ["PressRelease", "Blog"]
        article.keywords = ["tech", "news"]
        article.stock_tickers = ["NASDAQ:GOOG"]
        article.get_absolute_url = lambda: "https://example.com/news/1/"

        sitemap = NewsSitemap(
            queryset=[article],
            news_fields={
                "title": "title",
                "publication_name": "publication_name",
                "publication_language": "publication_language",
                "publication_date": "publication_date",
                "access": "access",
                "genres": "genres",
                "keywords": "keywords",
                "stock_tickers": "stock_tickers",
            },
        )

        xml = sitemap._build_news_xml(article)

        assert "<news:access>Subscription</news:access>" in xml
        assert "<news:genres>" in xml
        assert "<news:keywords>" in xml
        assert "<news:stock_tickers>" in xml

    def test_format_date_naive_datetime(self):
        """Test _format_date with naive datetime."""
        sitemap = NewsSitemap(queryset=[])

        naive_dt = datetime.datetime(2024, 1, 15, 10, 30, 0)
        result = sitemap._format_date(naive_dt)
        assert "2024-01-15T10:30:00Z" == result
