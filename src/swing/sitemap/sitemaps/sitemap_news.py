# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
News Sitemap
============

A sitemap class for generating Google News Sitemaps following the official
specification at https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap

News sitemaps include publication-specific metadata:
- Required: publication (name, language), publication_date, title
- Optional: access, genres, keywords, stock_tickers

Important Notes:
- Only include articles published in the last 48 hours
- Max 1000 URLs per news sitemap
- News sitemaps should be submitted separately from regular sitemaps

Usage::

    from swing.sitemap import NewsSitemap

    news_sitemap = NewsSitemap.from_settings("news")

Or with a queryset::

    news_sitemap = NewsSitemap(
        queryset=lambda: Article.objects.filter(
            published_at__gte=timezone.now() - timedelta(hours=48)
        ),
        news_fields={
            "publication_name": "site_name",
            "publication_language": "language_code",
            "title": "headline",
            "publication_date": "published_at",
        },
    )
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Callable, Iterable, Mapping, Sequence
import datetime as _dt
from typing import Any

from django.apps import apps
from django.db.models import Model, QuerySet
from django.utils import timezone
from django.utils.html import escape

from swing.sitemap.conf import get_setting
from swing.sitemap.sitemaps.sitemap_base import BaseSitemap

# =============================================================================
# Types
# =============================================================================

QuerySetSource = QuerySet | Iterable[Model] | Callable[[], Iterable[Model]]


# =============================================================================
# News Sitemap Class
# =============================================================================


class NewsSitemap(BaseSitemap):
    """
    A Django sitemap class for generating news sitemaps following Google's
    News Sitemap specification.

    Attributes:
        changefreq: Not used for news sitemaps.
        priority: Not used for news sitemaps.
        publication_name: Default publication name if not per-article.
        publication_language: Default ISO 639 language code.
    """

    changefreq: str = "always"
    priority: float = 1.0
    publication_name: str = ""
    publication_language: str = "en"

    # Default field mappings from model attributes to news sitemap fields
    DEFAULT_NEWS_FIELDS: Mapping[str, str] = {
        "publication_name": "publication_name",
        "publication_language": "publication_language",
        "title": "title",
        "publication_date": "publication_date",
        "access": "access",
        "genres": "genres",
        "keywords": "keywords",
        "stock_tickers": "stock_tickers",
    }

    # Valid genres per Google News spec
    VALID_GENRES = frozenset(
        {
            "PressRelease",
            "Satire",
            "Blog",
            "OpEd",
            "Opinion",
            "UserGenerated",
        }
    )

    def __init__(
        self,
        queryset: QuerySetSource | None = None,
        *,
        date_field: str | None = None,
        location_attr: str | Callable[[Model], str] = "get_absolute_url",
        news_fields: Mapping[str, str] | None = None,
        publication_name: str | None = None,
        publication_language: str | None = None,
        max_age_hours: int = 48,
    ) -> None:
        """
        Initialize NewsSitemap.

        Args:
            queryset: QuerySet or callable returning items.
            date_field: Model attribute for lastmod.
            location_attr: Model attribute or callable for URL.
            news_fields: Mapping of news sitemap fields to model attributes.
            publication_name: Default publication name.
            publication_language: Default ISO 639 language code.
            max_age_hours: Maximum article age in hours (default 48).
        """
        super().__init__(items=None)
        self._queryset_source = queryset
        self.date_field = date_field
        self.location_attr = location_attr
        self.news_fields = {**self.DEFAULT_NEWS_FIELDS, **(news_fields or {})}
        self.max_age_hours = max_age_hours
        if publication_name:
            self.publication_name = publication_name
        if publication_language:
            self.publication_language = publication_language

    # -------------------------------------------------------------------------
    # Construction helpers
    # -------------------------------------------------------------------------

    @classmethod
    def from_settings(cls, key: str = "news") -> "NewsSitemap":
        """
        Build a NewsSitemap from ``SWING_SITEMAP['news']`` or
        ``SWING_SITEMAP['models'][key]``.

        Settings structure::

            SWING_SITEMAP = {
                "news": {
                    "model": "myapp.Article",
                    "filters": {"is_published": True},
                    "exclude": {},
                    "order_by": ["-publication_date"],
                    "date_field": "publication_date",
                    "location_attr": "get_absolute_url",
                    "publication_name": "My Publication",
                    "publication_language": "en",
                    "max_age_hours": 48,
                    "news_fields": {
                        "title": "headline",
                        "publication_date": "published_at",
                        "genres": "article_genres",
                        "keywords": "tags",
                    },
                },
            }
        """
        # Try news-specific config first, fall back to models config
        spec = get_setting("news", default=None) or {}
        if not spec.get("model"):
            spec = get_setting("models", key, default=None) or {}

        if not spec or "model" not in spec:
            raise ValueError(
                f"SWING_SITEMAP['news'] or SWING_SITEMAP['models'][{key!r}] "
                "must define a 'model' dotted path (e.g. 'myapp.Article')."
            )

        model = apps.get_model(spec["model"])
        filters = spec.get("filters") or {}
        exclude = spec.get("exclude") or {}
        order_by = spec.get("order_by") or ()
        max_age_hours = spec.get("max_age_hours", 48)
        date_field = spec.get("date_field", "publication_date")

        def queryset_factory() -> QuerySet:
            qs = model._default_manager.all()
            # Auto-filter by max age if date_field is specified
            if date_field and max_age_hours:
                cutoff = timezone.now() - _dt.timedelta(hours=max_age_hours)
                qs = qs.filter(**{f"{date_field}__gte": cutoff})
            if filters:
                qs = qs.filter(**filters)
            if exclude:
                qs = qs.exclude(**exclude)
            if order_by:
                qs = qs.order_by(*order_by)
            return qs

        return cls(
            queryset=queryset_factory,
            date_field=date_field,
            location_attr=spec.get("location_attr", "get_absolute_url"),
            news_fields=spec.get("news_fields"),
            publication_name=spec.get("publication_name"),
            publication_language=spec.get("publication_language"),
            max_age_hours=max_age_hours,
        )

    # -------------------------------------------------------------------------
    # Sitemap protocol
    # -------------------------------------------------------------------------

    def items(self) -> Sequence[Model]:
        source = self._queryset_source
        if source is None:
            return []
        if callable(source):
            source = source()
        # Limit to 1000 URLs per Google News spec
        return list(source)[:1000]

    def lastmod(self, obj: Model) -> _dt.date | _dt.datetime | None:
        if not self.date_field:
            return None
        return getattr(obj, self.date_field, None)

    def location(self, item: Model) -> str:  # noqa: W0237
        """Return the absolute URL for the article."""
        attr = self.location_attr
        if callable(attr):
            return attr(item)
        value = getattr(item, attr)
        return value() if callable(value) else value

    # -------------------------------------------------------------------------
    # News-specific metadata
    # -------------------------------------------------------------------------

    def _get_news_attr(self, obj: Model, field: str) -> Any:
        """Get a news attribute from the model using field mapping."""
        attr_name = self.news_fields.get(field)
        if not attr_name:
            return None
        value = getattr(obj, attr_name, None)
        return value() if callable(value) else value

    def news_publication_name(self, obj: Model) -> str:
        """Return the publication name (required)."""
        name = self._get_news_attr(obj, "publication_name")
        return escape(name) if name else escape(self.publication_name)

    def news_publication_language(self, obj: Model) -> str:
        """Return the ISO 639 publication language code (required)."""
        lang = self._get_news_attr(obj, "publication_language")
        return lang if lang else self.publication_language

    def news_title(self, obj: Model) -> str:
        """Return the article title (required)."""
        title = self._get_news_attr(obj, "title")
        return escape(title) if title else ""

    def news_publication_date(self, obj: Model) -> str | None:
        """Return the publication date in W3C format (required)."""
        date = self._get_news_attr(obj, "publication_date")
        return self._format_date(date)

    def news_access(self, obj: Model) -> str | None:
        """Return access type: Subscription, Registration, or empty."""
        access = self._get_news_attr(obj, "access")
        if access in ("Subscription", "Registration"):
            return access
        return None

    def news_genres(self, obj: Model) -> str | None:
        """Return comma-separated genres (PressRelease, Satire, Blog, etc.)."""
        genres = self._get_news_attr(obj, "genres")
        if genres:
            if isinstance(genres, str):
                genres = [g.strip() for g in genres.split(",")]
            # Filter to valid genres only
            valid = [g for g in genres if g in self.VALID_GENRES]
            return ", ".join(valid) if valid else None
        return None

    def news_keywords(self, obj: Model) -> str | None:
        """Return comma-separated keywords (max 10 recommended)."""
        keywords = self._get_news_attr(obj, "keywords")
        if keywords:
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(",")]
            # Limit to 10 keywords
            return ", ".join(escape(k) for k in keywords[:10])
        return None

    def news_stock_tickers(self, obj: Model) -> str | None:
        """Return comma-separated stock tickers (max 5, format: EXCHANGE:TICKER)."""
        tickers = self._get_news_attr(obj, "stock_tickers")
        if tickers:
            if isinstance(tickers, str):
                tickers = [t.strip() for t in tickers.split(",")]
            # Limit to 5 tickers
            return ", ".join(tickers[:5])
        return None

    # -------------------------------------------------------------------------
    # XML generation helpers
    # -------------------------------------------------------------------------

    def _format_date(self, date: _dt.date | _dt.datetime | None) -> str | None:
        """Format a date/datetime to W3C format."""
        if date is None:
            return None
        if isinstance(date, _dt.datetime):
            if date.tzinfo is None:
                # Assume UTC for naive datetimes
                return date.strftime("%Y-%m-%dT%H:%M:%SZ")
            return date.strftime("%Y-%m-%dT%H:%M:%S%z")
        return date.strftime("%Y-%m-%d")

    def _build_news_xml(self, obj: Model) -> str:
        """Build the news:news XML element for an item."""
        parts = ["<news:news>"]

        # Publication (required)
        pub_name = self.news_publication_name(obj)
        pub_lang = self.news_publication_language(obj)
        parts.append("<news:publication>")
        parts.append(f"<news:name>{pub_name}</news:name>")
        parts.append(f"<news:language>{pub_lang}</news:language>")
        parts.append("</news:publication>")

        # Access (optional)
        access = self.news_access(obj)
        if access:
            parts.append(f"<news:access>{access}</news:access>")

        # Genres (optional)
        genres = self.news_genres(obj)
        if genres:
            parts.append(f"<news:genres>{genres}</news:genres>")

        # Publication date (required)
        pub_date = self.news_publication_date(obj)
        if pub_date:
            parts.append(f"<news:publication_date>{pub_date}</news:publication_date>")

        # Title (required)
        title = self.news_title(obj)
        parts.append(f"<news:title>{title}</news:title>")

        # Keywords (optional)
        keywords = self.news_keywords(obj)
        if keywords:
            parts.append(f"<news:keywords>{keywords}</news:keywords>")

        # Stock tickers (optional)
        tickers = self.news_stock_tickers(obj)
        if tickers:
            parts.append(f"<news:stock_tickers>{tickers}</news:stock_tickers>")

        parts.append("</news:news>")
        return "\n".join(parts)

    def _urls(self, page, protocol, domain):
        """Override to inject news XML into URL data."""
        urls = super()._urls(page, protocol, domain)
        for url in urls:
            item = url["item"]
            url["news"] = self._build_news_xml(item)
        return urls


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["NewsSitemap"]
