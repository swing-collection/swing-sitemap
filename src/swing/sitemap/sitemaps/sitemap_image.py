# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Image Sitemap
=============

A sitemap class for generating Google Image Sitemaps following the official
specification at https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps

Image sitemaps help Google discover images that might otherwise be missed,
such as images loaded via JavaScript or CSS.

Image metadata per URL:
- Required: loc (image URL)
- Optional: caption, geo_location, title, license

Important Notes:
- Up to 1000 images per URL
- Use separate sitemap or include images in regular sitemap
- Images must be on the same domain or CDN allowed by robots.txt

Usage::

    from swing.sitemap import ImageSitemap

    image_sitemap = ImageSitemap.from_settings("images")

Or with a queryset::

    image_sitemap = ImageSitemap(
        queryset=lambda: Page.objects.filter(has_images=True),
        image_attr="get_images",  # Method returning list of image dicts
    )
"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import datetime as _dt
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any

from django.apps import apps
from django.db.models import Model, QuerySet
from django.utils.html import escape

from swing.sitemap.conf import get_setting
from swing.sitemap.sitemaps.sitemap_base import BaseSitemap


# =============================================================================
# Types
# =============================================================================

QuerySetSource = QuerySet | Iterable[Model] | Callable[[], Iterable[Model]]

# Image data structure
ImageData = dict[str, str | None]


# =============================================================================
# Image Sitemap Class
# =============================================================================


class ImageSitemap(BaseSitemap):
    """
    A Django sitemap class for generating image sitemaps following Google's
    Image Sitemap specification.

    Supports both queryset-based and settings-based configuration.

    Each item in the sitemap can have multiple images. Images are retrieved
    via the `image_attr` which should return a list of dicts with keys:
    - loc (required): Image URL
    - caption (optional): Image caption
    - geo_location (optional): Geographic location
    - title (optional): Image title
    - license (optional): License URL

    Attributes:
        changefreq: Expected change frequency (default: "monthly").
        priority: URL priority relative to other URLs (default: 0.5).
    """

    changefreq: str = "monthly"
    priority: float = 0.5

    # Maximum images per URL per Google spec
    MAX_IMAGES_PER_URL: int = 1000

    def __init__(
        self,
        queryset: QuerySetSource | None = None,
        *,
        date_field: str | None = None,
        location_attr: str | Callable[[Model], str] = "get_absolute_url",
        image_attr: str | Callable[[Model], list[ImageData]] = "get_images",
        priority: float | None = None,
        changefreq: str | None = None,
    ) -> None:
        """
        Initialize ImageSitemap.

        Args:
            queryset: QuerySet or callable returning items.
            date_field: Model attribute for lastmod.
            location_attr: Model attribute or callable for page URL.
            image_attr: Model attribute or callable returning list of image dicts.
                Each dict should have 'loc' (required) and optionally:
                'caption', 'geo_location', 'title', 'license'.
            priority: URL priority (0.0-1.0).
            changefreq: Change frequency string.
        """
        super().__init__(items=None)
        self._queryset_source = queryset
        self.date_field = date_field
        self.location_attr = location_attr
        self.image_attr = image_attr
        if priority is not None:
            self.priority = priority
        if changefreq is not None:
            self.changefreq = changefreq

    # -------------------------------------------------------------------------
    # Construction helpers
    # -------------------------------------------------------------------------

    @classmethod
    def from_settings(cls, key: str = "image") -> "ImageSitemap":
        """
        Build an ImageSitemap from ``SWING_SITEMAP['image']`` or
        ``SWING_SITEMAP['models'][key]``.

        Settings structure::

            SWING_SITEMAP = {
                "image": {
                    "model": "myapp.Page",
                    "filters": {"has_images": True},
                    "exclude": {},
                    "order_by": ["-updated_at"],
                    "date_field": "updated_at",
                    "location_attr": "get_absolute_url",
                    "image_attr": "get_images",
                    "priority": 0.5,
                    "changefreq": "monthly",
                },
            }

        The model should have a method/property that returns a list of image
        dictionaries with 'loc' as the image URL and optional 'caption',
        'geo_location', 'title', 'license' keys.
        """
        # Try image-specific config first, fall back to models config
        spec = get_setting("image", default=None) or {}
        if not spec.get("model"):
            spec = get_setting("models", key, default=None) or {}

        if not spec or "model" not in spec:
            raise ValueError(
                f"SWING_SITEMAP['image'] or SWING_SITEMAP['models'][{key!r}] "
                "must define a 'model' dotted path (e.g. 'myapp.Page')."
            )

        model = apps.get_model(spec["model"])
        filters = spec.get("filters") or {}
        exclude = spec.get("exclude") or {}
        order_by = spec.get("order_by") or ()

        def queryset_factory() -> QuerySet:
            qs = model._default_manager.all()
            if filters:
                qs = qs.filter(**filters)
            if exclude:
                qs = qs.exclude(**exclude)
            if order_by:
                qs = qs.order_by(*order_by)
            return qs

        return cls(
            queryset=queryset_factory,
            date_field=spec.get("date_field"),
            location_attr=spec.get("location_attr", "get_absolute_url"),
            image_attr=spec.get("image_attr", "get_images"),
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

    def lastmod(self, obj: Model) -> _dt.date | _dt.datetime | None:
        if not self.date_field:
            return None
        return getattr(obj, self.date_field, None)

    def location(self, obj: Model) -> str:
        """Return the absolute URL for the page containing images."""
        attr = self.location_attr
        if callable(attr):
            return attr(obj)
        value = getattr(obj, attr)
        return value() if callable(value) else value

    # -------------------------------------------------------------------------
    # Image-specific methods
    # -------------------------------------------------------------------------

    def get_images(self, obj: Model) -> list[ImageData]:
        """
        Get the list of images for an item.

        Returns a list of dicts with keys:
        - loc (required): Image URL
        - caption (optional): Image caption
        - geo_location (optional): Geographic location
        - title (optional): Image title
        - license (optional): License URL
        """
        attr = self.image_attr
        if callable(attr):
            images = attr(obj)
        else:
            value = getattr(obj, attr, None)
            images = value() if callable(value) else value

        if not images:
            return []

        # Normalize and validate images
        normalized: list[ImageData] = []
        for img in images[: self.MAX_IMAGES_PER_URL]:
            if isinstance(img, str):
                # Simple string URL
                normalized.append({"loc": img})
            elif isinstance(img, dict) and img.get("loc"):
                normalized.append({
                    "loc": img["loc"],
                    "caption": img.get("caption"),
                    "geo_location": img.get("geo_location"),
                    "title": img.get("title"),
                    "license": img.get("license"),
                })
            # Skip invalid entries

        return normalized

    def image_loc(self, img: ImageData) -> str:
        """Return the image URL (required)."""
        return img.get("loc", "")

    def image_caption(self, img: ImageData) -> str | None:
        """Return the image caption."""
        caption = img.get("caption")
        return escape(caption) if caption else None

    def image_geo_location(self, img: ImageData) -> str | None:
        """Return the geographic location."""
        geo = img.get("geo_location")
        return escape(geo) if geo else None

    def image_title(self, img: ImageData) -> str | None:
        """Return the image title."""
        title = img.get("title")
        return escape(title) if title else None

    def image_license(self, img: ImageData) -> str | None:
        """Return the license URL."""
        return img.get("license")

    # -------------------------------------------------------------------------
    # URL generation
    # -------------------------------------------------------------------------

    def _urls(self, page, protocol, domain):
        """Override to inject image data into URL entries."""
        urls = super()._urls(page, protocol, domain)
        for url in urls:
            item = url["item"]
            url["images"] = self.get_images(item)
        return urls


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["ImageSitemap", "ImageData"]
