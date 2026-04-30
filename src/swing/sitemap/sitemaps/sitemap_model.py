# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Model Sitemap
======================

A generic, settings-aware sitemap for any Django model. Replaces the
hand-written ``django.contrib.sitemaps.Sitemap`` subclasses that wire up
``items()`` / ``location()`` / ``lastmod()`` for a single queryset.

Typical usage::

    from swing_sitemap import ModelSitemap

    work_sitemap = ModelSitemap(
        queryset=lambda: Work.objects.filter(is_published=True),
        date_field="modified_at",
        location_attr="get_absolute_url",
        priority=0.8,
        changefreq="weekly",
    )

Or, driven entirely by settings::

    SWING_SITEMAP = {
        "models": {
            "work": {
                "model": "myapp.WorkModel",
                "filters": {"is_published": True},
                "order_by": ["-work_date"],
                "date_field": "modified_at",
                "location_attr": "get_absolute_url",
                "priority": 0.8,
                "changefreq": "weekly",
            },
        },
    }

    work_sitemap = ModelSitemap.from_settings("work")
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

from django.apps import apps
from django.db.models import Model, QuerySet

from swing_sitemap.conf import get_setting
from swing_sitemap.sitemaps.sitemap_base import BaseSitemap


QuerySetSource = QuerySet | Iterable[Model] | Callable[[], Iterable[Model]]


# =============================================================================
# Class
# =============================================================================


class ModelSitemap(BaseSitemap):
    """
    Generic sitemap built from a Django model queryset.
    """

    changefreq = "monthly"
    priority = 0.5

    def __init__(
        self,
        queryset: QuerySetSource | None = None,
        *,
        date_field: str | None = None,
        location_attr: str | Callable[[Model], str] = "get_absolute_url",
        priority: float | None = None,
        changefreq: str | None = None,
    ) -> None:
        # ``BaseSitemap.__init__`` only stores ``items_list``; we use our
        # own attributes and override :meth:`items` directly.
        super().__init__(items=None)
        self._queryset_source = queryset
        self.date_field = date_field
        self.location_attr = location_attr
        if priority is not None:
            self.priority = priority
        if changefreq is not None:
            self.changefreq = changefreq

    # Construction helpers
    # =========================================================================

    @classmethod
    def from_settings(cls, key: str) -> "ModelSitemap":
        """
        Build a :class:`ModelSitemap` from
        ``SWING_SITEMAP['models'][key]``.

        Required keys: ``model`` (dotted ``"app_label.ModelName"``).
        Optional keys: ``filters``, ``exclude``, ``order_by``,
        ``date_field``, ``location_attr``, ``priority``, ``changefreq``.
        """
        spec = get_setting("models", key, default=None)
        if not spec or "model" not in spec:
            raise ValueError(
                f"SWING_SITEMAP['models'][{key!r}] must define a 'model' "
                "dotted path (e.g. 'myapp.MyModel').",
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
            priority=spec.get("priority"),
            changefreq=spec.get("changefreq"),
        )

    # Sitemap contract
    # =========================================================================

    def items(self) -> Sequence[Model]:  # type: ignore[override]
        source = self._queryset_source
        if source is None:
            return []
        if callable(source):
            source = source()
        return source

    def lastmod(self, obj: Model):  # noqa: D401
        if not self.date_field:
            return None
        return getattr(obj, self.date_field, None)

    def location(self, obj: Model) -> str:
        attr = self.location_attr
        if callable(attr):
            return attr(obj)
        value = getattr(obj, attr)
        return value() if callable(value) else value


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["ModelSitemap", "QuerySetSource"]
