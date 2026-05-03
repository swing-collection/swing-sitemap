# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Video Sitemap
=============

A sitemap class for generating Google Video Sitemaps following the official
specification at https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps

Video sitemaps include rich metadata about video content including:
- Required: thumbnail_loc, title, description
- Recommended: content_loc or player_loc, duration
- Optional: expiration_date, rating, view_count, publication_date,
  family_friendly, restriction, platform, requires_subscription, live

Usage::

    from swing.sitemap import VideoSitemap

    video_sitemap = VideoSitemap.from_settings("videos")

Or with a queryset::

    video_sitemap = VideoSitemap(
        queryset=lambda: Video.objects.filter(is_published=True),
        video_fields={
            "thumbnail_loc": "thumbnail_url",
            "title": "video_title",
            "description": "video_description",
            "content_loc": "video_url",
            "duration": "duration_seconds",
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
import logging
from typing import Any

from django.apps import apps
from django.db.models import Model, QuerySet
from django.utils.html import escape

from swing.sitemap.conf import get_setting
from swing.sitemap.sitemaps.sitemap_base import BaseSitemap

logger = logging.getLogger(__name__)


# =============================================================================
# Types
# =============================================================================

QuerySetSource = QuerySet | Iterable[Model] | Callable[[], Iterable[Model]]


# =============================================================================
# Video Sitemap Class
# =============================================================================


class VideoSitemap(BaseSitemap):
    """
    A Django sitemap class for generating video sitemaps following Google's
    Video Sitemap specification.

    Supports both queryset-based and settings-based configuration.

    Attributes:
        changefreq: Expected change frequency (default: "weekly").
        priority: URL priority relative to other URLs (default: 0.8).
    """

    changefreq: str = "weekly"
    priority: float = 0.8

    # Default field mappings from model attributes to video sitemap fields
    DEFAULT_VIDEO_FIELDS: Mapping[str, str] = {
        "thumbnail_loc": "video_thumbnail_url",
        "title": "video_title",
        "description": "video_description",
        "content_loc": "video_content_url",
        "player_loc": "video_player_url",
        "duration": "video_duration",
        "expiration_date": "video_expiration_date",
        "publication_date": "video_publication_date",
        "rating": "video_rating",
        "view_count": "video_view_count",
        "family_friendly": "video_family_friendly",
        "restriction": "video_restriction",
        "platform": "video_platform",
        "requires_subscription": "video_requires_subscription",
        "live": "video_live",
        "tag": "video_tags",
        "category": "video_category",
        "uploader": "video_uploader",
    }

    def __init__(
        self,
        queryset: QuerySetSource | None = None,
        *,
        date_field: str | None = None,
        location_attr: str | Callable[[Model], str] = "get_absolute_url",
        video_fields: Mapping[str, str] | None = None,
        priority: float | None = None,
        changefreq: str | None = None,
    ) -> None:
        """
        Initialize VideoSitemap.

        Args:
            queryset: QuerySet or callable returning items.
            date_field: Model attribute for lastmod.
            location_attr: Model attribute or callable for URL.
            video_fields: Mapping of video sitemap fields to model attributes.
            priority: URL priority (0.0-1.0).
            changefreq: Change frequency string.
        """
        super().__init__(items=None)
        self._queryset_source = queryset
        self.date_field = date_field
        self.location_attr = location_attr
        self.video_fields = {**self.DEFAULT_VIDEO_FIELDS, **(video_fields or {})}
        if priority is not None:
            self.priority = priority
        if changefreq is not None:
            self.changefreq = changefreq

    # -------------------------------------------------------------------------
    # Construction helpers
    # -------------------------------------------------------------------------

    @classmethod
    def from_settings(cls, key: str = "video") -> "VideoSitemap":
        """
        Build a VideoSitemap from ``SWING_SITEMAP['video']`` or
        ``SWING_SITEMAP['models'][key]``.

        Settings structure::

            SWING_SITEMAP = {
                "video": {
                    "model": "myapp.Video",
                    "filters": {"is_published": True},
                    "exclude": {},
                    "order_by": ["-publication_date"],
                    "date_field": "updated_at",
                    "location_attr": "get_absolute_url",
                    "video_fields": {
                        "thumbnail_loc": "thumbnail_url",
                        "title": "title",
                        "description": "description",
                    },
                    "priority": 0.8,
                    "changefreq": "weekly",
                },
            }
        """
        # Try video-specific config first, fall back to models config
        spec = get_setting("video", default=None) or {}
        if not spec.get("model"):
            spec = get_setting("models", key, default=None) or {}

        if not spec or "model" not in spec:
            raise ValueError(
                f"SWING_SITEMAP['video'] or SWING_SITEMAP['models'][{key!r}] "
                "must define a 'model' dotted path (e.g. 'myapp.Video')."
            )

        model = apps.get_model(spec["model"])
        filters = spec.get("filters") or {}
        exclude = spec.get("exclude") or {}
        order_by = spec.get("order_by") or ()

        def queryset_factory() -> QuerySet:
            qs = model._default_manager.all()
            if filters:  # pragma: no cover
                qs = qs.filter(**filters)
            if exclude:  # pragma: no cover
                qs = qs.exclude(**exclude)
            if order_by:  # pragma: no cover
                qs = qs.order_by(*order_by)
            return qs

        return cls(
            queryset=queryset_factory,
            date_field=spec.get("date_field"),
            location_attr=spec.get("location_attr", "get_absolute_url"),
            video_fields=spec.get("video_fields"),
            priority=spec.get("priority"),
            changefreq=spec.get("changefreq"),
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
        return source

    def _validate_item(self, obj: Model) -> tuple[bool, list[str]]:
        """
        Validate an item has required video fields.

        Returns:
            Tuple of (is_valid, list of missing field names).
        """
        missing = []

        # Required: thumbnail_loc, title, description
        if not self.video_thumbnail_loc(obj):
            missing.append("thumbnail_loc")
        if not self.video_title(obj):
            missing.append("title")
        if not self.video_description(obj):
            missing.append("description")

        # Recommended: at least one of content_loc or player_loc
        if not self.video_content_loc(obj) and not self.video_player_loc(obj):
            logger.warning(
                "VideoSitemap: Item %r has neither content_loc nor player_loc. "
                "Google recommends at least one.",
                obj,
            )

        return len(missing) == 0, missing

    def lastmod(self, obj: Model) -> _dt.date | _dt.datetime | None:
        if not self.date_field:
            return None
        return getattr(obj, self.date_field, None)

    def location(self, item: Model) -> str:  # noqa: W0237
        """Return the absolute URL for the video page."""
        attr = self.location_attr
        if callable(attr):
            return attr(item)
        value = getattr(item, attr)
        return value() if callable(value) else value

    # -------------------------------------------------------------------------
    # Video-specific metadata
    # -------------------------------------------------------------------------

    def _get_video_attr(self, obj: Model, field: str) -> Any:
        """Get a video attribute from the model using field mapping."""
        attr_name = self.video_fields.get(field)
        if not attr_name:  # pragma: no cover
            return None
        value = getattr(obj, attr_name, None)
        return value() if callable(value) else value

    def video_thumbnail_loc(self, obj: Model) -> str | None:
        """Return the video thumbnail URL (required)."""
        return self._get_video_attr(obj, "thumbnail_loc")

    def video_title(self, obj: Model) -> str | None:
        """Return the video title (required, max 100 chars)."""
        title = self._get_video_attr(obj, "title")
        return escape(title[:100]) if title else None

    def video_description(self, obj: Model) -> str | None:
        """Return the video description (required, max 2048 chars)."""
        desc = self._get_video_attr(obj, "description")
        return escape(desc[:2048]) if desc else None

    def video_content_loc(self, obj: Model) -> str | None:
        """Return the video file URL (recommended if no player_loc)."""
        return self._get_video_attr(obj, "content_loc")

    def video_player_loc(self, obj: Model) -> str | None:
        """Return the video player embed URL (recommended if no content_loc)."""
        return self._get_video_attr(obj, "player_loc")

    def video_duration(self, obj: Model) -> int | None:
        """Return the video duration in seconds (recommended, 1-28800)."""
        duration = self._get_video_attr(obj, "duration")
        if duration is not None:
            return max(1, min(28800, int(duration)))
        return None

    def video_expiration_date(self, obj: Model) -> str | None:
        """Return the video expiration date in W3C format."""
        date = self._get_video_attr(obj, "expiration_date")
        return self._format_date(date)

    def video_publication_date(self, obj: Model) -> str | None:
        """Return the video publication date in W3C format."""
        date = self._get_video_attr(obj, "publication_date")
        return self._format_date(date)

    def video_rating(self, obj: Model) -> float | None:
        """Return the video rating (0.0-5.0)."""
        rating = self._get_video_attr(obj, "rating")
        if rating is not None:
            return max(0.0, min(5.0, float(rating)))
        return None

    def video_view_count(self, obj: Model) -> int | None:
        """Return the video view count."""
        count = self._get_video_attr(obj, "view_count")
        return int(count) if count is not None else None

    def video_family_friendly(self, obj: Model) -> str | None:
        """Return 'yes' or 'no' for family-friendly status."""
        value = self._get_video_attr(obj, "family_friendly")
        if value is None:
            return None
        return "yes" if value else "no"

    def video_restriction(self, obj: Model) -> dict | None:
        """Return restriction info: {'relationship': 'allow|deny', 'countries': 'US CA'}."""
        return self._get_video_attr(obj, "restriction")

    def video_platform(self, obj: Model) -> dict | None:
        """Return platform info: {'relationship': 'allow|deny', 'platforms': 'web mobile'}."""
        return self._get_video_attr(obj, "platform")

    def video_requires_subscription(self, obj: Model) -> str | None:
        """Return 'yes' or 'no' for subscription requirement."""
        value = self._get_video_attr(obj, "requires_subscription")
        if value is None:
            return None
        return "yes" if value else "no"

    def video_live(self, obj: Model) -> str | None:
        """Return 'yes' or 'no' for live stream status."""
        value = self._get_video_attr(obj, "live")
        if value is None:
            return None
        return "yes" if value else "no"

    def video_tags(self, obj: Model) -> list[str] | None:
        """Return list of video tags (max 32 tags)."""
        tags = self._get_video_attr(obj, "tag")
        if tags:  # pragma: no cover
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]
            return [escape(t) for t in tags[:32]]
        return None

    def video_category(self, obj: Model) -> str | None:
        """Return video category (max 256 chars)."""
        category = self._get_video_attr(obj, "category")
        return escape(category[:256]) if category else None

    def video_uploader(self, obj: Model) -> dict | None:
        """Return uploader info: {'name': '...', 'info': 'url'}."""
        return self._get_video_attr(obj, "uploader")

    # -------------------------------------------------------------------------
    # XML generation helpers
    # -------------------------------------------------------------------------

    def _format_date(self, date: _dt.date | _dt.datetime | None) -> str | None:
        """Format a date/datetime to W3C format."""
        if date is None:
            return None
        if isinstance(date, _dt.datetime):
            return date.strftime("%Y-%m-%dT%H:%M:%S%z") or date.strftime(
                "%Y-%m-%dT%H:%M:%S+00:00"
            )
        return date.strftime("%Y-%m-%d")

    def _build_video_xml(self, obj: Model) -> str:  # noqa: C901
        """Build the video:video XML element for an item."""
        # Validate required fields
        is_valid, missing = self._validate_item(obj)
        if not is_valid:  # pragma: no cover
            logger.warning(
                "VideoSitemap: Item %r is missing required fields: %s. "
                "Video may not be indexed properly.",
                obj,
                ", ".join(missing),
            )

        parts = ["<video:video>"]

        # Required fields
        thumb = self.video_thumbnail_loc(obj)
        title = self.video_title(obj)
        desc = self.video_description(obj)

        if thumb:  # pragma: no cover
            parts.append(f"<video:thumbnail_loc>{escape(thumb)}</video:thumbnail_loc>")
        if title:  # pragma: no cover
            parts.append(f"<video:title>{title}</video:title>")
        if desc:  # pragma: no cover
            parts.append(f"<video:description>{desc}</video:description>")

        # Recommended: content_loc or player_loc
        content = self.video_content_loc(obj)
        player = self.video_player_loc(obj)
        if content:  # pragma: no cover
            parts.append(f"<video:content_loc>{escape(content)}</video:content_loc>")
        if player:  # pragma: no cover
            parts.append(f"<video:player_loc>{escape(player)}</video:player_loc>")

        # Optional fields
        duration = self.video_duration(obj)
        if duration is not None:
            parts.append(f"<video:duration>{duration}</video:duration>")

        exp_date = self.video_expiration_date(obj)
        if exp_date:
            parts.append(f"<video:expiration_date>{exp_date}</video:expiration_date>")

        pub_date = self.video_publication_date(obj)
        if pub_date:
            parts.append(f"<video:publication_date>{pub_date}</video:publication_date>")

        rating = self.video_rating(obj)
        if rating is not None:
            parts.append(f"<video:rating>{rating:.1f}</video:rating>")

        view_count = self.video_view_count(obj)
        if view_count is not None:
            parts.append(f"<video:view_count>{view_count}</video:view_count>")

        family = self.video_family_friendly(obj)
        if family:
            parts.append(f"<video:family_friendly>{family}</video:family_friendly>")

        restriction = self.video_restriction(obj)
        if restriction:
            rel = restriction.get("relationship", "allow")
            countries = restriction.get("countries", "")
            parts.append(
                f'<video:restriction relationship="{rel}">{countries}</video:restriction>'
            )

        platform = self.video_platform(obj)
        if platform:
            rel = platform.get("relationship", "allow")
            platforms = platform.get("platforms", "")
            parts.append(
                f'<video:platform relationship="{rel}">{platforms}</video:platform>'
            )

        requires_sub = self.video_requires_subscription(obj)
        if requires_sub:
            parts.append(
                f"<video:requires_subscription>{requires_sub}</video:requires_subscription>"
            )

        live = self.video_live(obj)
        if live:
            parts.append(f"<video:live>{live}</video:live>")

        tags = self.video_tags(obj)
        if tags:
            for tag in tags:
                parts.append(f"<video:tag>{tag}</video:tag>")

        category = self.video_category(obj)
        if category:
            parts.append(f"<video:category>{category}</video:category>")

        uploader = self.video_uploader(obj)
        if uploader:
            name = escape(uploader.get("name", ""))
            info = uploader.get("info", "")
            if info:
                parts.append(
                    f'<video:uploader info="{escape(info)}">{name}</video:uploader>'
                )
            else:
                parts.append(f"<video:uploader>{name}</video:uploader>")

        parts.append("</video:video>")
        return "\n".join(parts)

    def _urls(self, page, protocol, domain):
        """Override to inject video XML into URL data."""
        urls = super()._urls(page, protocol, domain)
        for url in urls:
            item = url["item"]
            url["videos"] = self._build_video_xml(item)
        return urls


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["VideoSitemap"]
