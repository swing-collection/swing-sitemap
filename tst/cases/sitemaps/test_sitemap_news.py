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
