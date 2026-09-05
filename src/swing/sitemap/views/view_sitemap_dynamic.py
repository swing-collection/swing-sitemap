# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Dynamic Sitemap View
====================

A configurable class-based view for rendering dynamic XML sitemaps.

Supports:
- Static pages with configurable priority and changefreq
- Dynamic pages from model querysets
- Callable page generators
- Django settings-driven configuration

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from collections.abc import Callable, Iterable
from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

if TYPE_CHECKING:
    from django.db.models import Model

# =============================================================================
# Types
# =============================================================================

#: A page entry for the sitemap
PageEntry = dict[str, Any]


# =============================================================================
# Classes
# =============================================================================


class DynamicSitemapView(View):
    """
    Dynamic Sitemap View
    ====================

    A highly configurable class-based view for rendering XML sitemaps.

    Supports multiple page sources:
    - ``static_pages``: List of static page definitions
    - ``model_sources``: List of model/queryset sources for dynamic pages
    - ``callable_sources``: List of callables that return page entries

    Usage::

        from swing.sitemap.views import DynamicSitemapView

        class MySitemapView(DynamicSitemapView):
            static_pages = [
                {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
                {"loc": "/about/", "priority": "0.8", "changefreq": "monthly"},
            ]

            model_sources = [
                {
                    "model": "myapp.Article",
                    "url_pattern": "/articles/{slug}/",
                    "priority": "0.7",
                    "changefreq": "weekly",
                    "lastmod_field": "updated_at",
                },
            ]

    Attributes:
        template_name: Template for rendering the sitemap XML.
        content_type: Response content type.
        static_pages: List of static page definitions.
        model_sources: List of model source configurations.
        callable_sources: List of callables returning page entries.
        default_priority: Default priority for pages without explicit priority.
        default_changefreq: Default changefreq for pages without explicit value.

    """

    template_name: str = "swing/sitemap/sitemap.xml"
    content_type: str = "application/xml"

    # Page sources
    static_pages: list[PageEntry] = []
    model_sources: list[dict[str, Any]] = []
    callable_sources: list[Callable[[HttpRequest], Iterable[PageEntry]]] = []

    # Defaults
    default_priority: str = "0.5"
    default_changefreq: str = "monthly"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request and render the sitemap XML."""
        pages = self.get_pages(request)
        context = self.get_context_data(request, pages)
        return TemplateResponse(
            request,
            self.get_template_name(),
            context,
            content_type=self.content_type,
        )

    def get_template_name(self) -> str:
        """Return the template name."""
        return self.template_name

    def get_pages(self, request: HttpRequest) -> list[PageEntry]:
        """
        Collect all pages from all sources.

        Returns a list of page entries with:
        - loc: The full URL
        - lastmod: Optional last modification date
        - changefreq: How often the page changes
        - priority: Relative priority (0.0 to 1.0)
        """
        pages: list[PageEntry] = []
        host = request.build_absolute_uri("/").rstrip("/")
        today = date.today().isoformat()

        # Collect static pages
        for page in self.get_static_pages():
            pages.append(self._normalize_page(page, host, today))

        # Collect model-based pages
        for source in self.get_model_sources():
            for page in self._pages_from_model(source, host, today):
                pages.append(page)

        # Collect callable-based pages
        for source_callable in self.get_callable_sources():
            for page in source_callable(request):
                pages.append(self._normalize_page(page, host, today))

        return pages

    def get_static_pages(self) -> list[PageEntry]:
        """Return static pages. Override to customize."""
        return self.static_pages

    def get_model_sources(self) -> list[dict[str, Any]]:
        """Return model sources. Override to customize."""
        return self.model_sources

    def get_callable_sources(
        self,
    ) -> list[Callable[[HttpRequest], Iterable[PageEntry]]]:
        """Return callable sources. Override to customize."""
        return self.callable_sources

    def _normalize_page(
        self,
        page: PageEntry,
        host: str,
        today: str,
    ) -> PageEntry:
        """Normalize a page entry with defaults and full URL."""
        loc = page.get("loc", "")

        # Handle different loc formats
        if loc.startswith("http://") or loc.startswith("https://"):
            full_loc = loc
        elif loc.startswith("/"):
            full_loc = f"{host}{loc}"
        else:
            # Assume it's a URL name
            try:
                full_loc = f"{host}{reverse(loc)}"
            except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
                full_loc = f"{host}/{loc}"

        # Get lastmod - could be date, datetime, or string
        lastmod = page.get("lastmod", today)
        if isinstance(lastmod, datetime):
            lastmod = lastmod.date().isoformat()
        elif isinstance(lastmod, date):
            lastmod = lastmod.isoformat()

        return {
            "loc": full_loc,
            "lastmod": lastmod,
            "changefreq": page.get("changefreq", self.default_changefreq),
            "priority": page.get("priority", self.default_priority),
        }

    def _pages_from_model(
        self,
        source: dict[str, Any],
        host: str,
        today: str,
    ) -> Iterable[PageEntry]:
        """Generate page entries from a model source configuration."""
        from django.apps import apps

        # Get model class
        model_path = source.get("model", "")
        if isinstance(model_path, str):
            app_label, model_name = model_path.rsplit(".", 1)
            model_class = apps.get_model(app_label, model_name)
        else:
            model_class = model_path

        # Get queryset
        queryset = source.get("queryset")
        if queryset is None:
            queryset = model_class.objects.all()
        if callable(queryset):
            queryset = queryset()

        # URL pattern
        url_pattern = source.get("url_pattern", "/{pk}/")
        url_name = source.get("url_name")
        priority = source.get("priority", self.default_priority)
        changefreq = source.get("changefreq", self.default_changefreq)
        lastmod_field = source.get("lastmod_field")

        for obj in queryset:
            # Build URL
            if url_name:
                try:
                    loc = f"{host}{reverse(url_name, args=[obj.pk])}"
                except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
                    loc = f"{host}{url_pattern.format(**self._model_to_dict(obj))}"
            else:
                loc = f"{host}{url_pattern.format(**self._model_to_dict(obj))}"

            # Get lastmod
            if lastmod_field and hasattr(obj, lastmod_field):
                lastmod_value = getattr(obj, lastmod_field)
                if isinstance(lastmod_value, datetime):
                    lastmod = lastmod_value.date().isoformat()
                elif isinstance(lastmod_value, date):
                    lastmod = lastmod_value.isoformat()
                else:
                    lastmod = today
            else:
                lastmod = today

            yield {
                "loc": loc,
                "lastmod": lastmod,
                "changefreq": changefreq,
                "priority": priority,
            }

    def _model_to_dict(self, obj: "Model") -> dict[str, Any]:
        """Convert model instance to dict for URL formatting."""
        result: dict[str, Any] = {"pk": obj.pk, "id": obj.pk}
        for field in obj._meta.get_fields():
            if hasattr(field, "attname"):
                result[field.attname] = getattr(obj, field.attname, None)
                # Also add without _id suffix
                name = field.attname.removesuffix("_id")
                if name not in result:
                    result[name] = getattr(obj, field.attname, None)
        # Common slug field
        if hasattr(obj, "slug"):
            result["slug"] = obj.slug
        return result

    def get_context_data(
        self,
        request: HttpRequest,
        pages: list[PageEntry],
    ) -> dict[str, Any]:
        """Return context for template rendering."""
        return {
            "urlset": pages,
            "request": request,
        }


# =============================================================================
# Exports
# =============================================================================

__all__ = ["DynamicSitemapView"]
