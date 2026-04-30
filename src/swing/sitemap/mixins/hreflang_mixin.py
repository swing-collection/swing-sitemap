# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hreflang Mixin
==============

Mixin for adding hreflang alternate language links to sitemaps.

This mixin adds support for multi-language sites following Google's
guidelines for indicating alternate language versions:
https://developers.google.com/search/docs/specialty/international/localized-versions

Usage::

    from swing.sitemap import BaseSitemap, HreflangMixin

    class MySitemap(HreflangMixin, BaseSitemap):
        languages = ["en", "de", "fr"]
        default_language = "en"

        def alternates(self, obj):
            # Return dict mapping language codes to URLs
            return {
                "en": obj.get_url_for_language("en"),
                "de": obj.get_url_for_language("de"),
                "fr": obj.get_url_for_language("fr"),
            }

Or use the x-default attribute::

    def alternates(self, obj):
        return {
            "en": obj.get_url_for_language("en"),
            "de": obj.get_url_for_language("de"),
            "x-default": obj.get_url_for_language("en"),  # Fallback
        }

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db.models import Model
from django.utils.html import escape


# =============================================================================
# Classes
# =============================================================================

class HreflangMixin:
    """
    Mixin for adding hreflang alternate links to sitemaps.

    Override the ``alternates`` method to return a dict mapping
    language codes to alternate URLs for each item.

    Attributes:
        languages: List of supported language codes.
        default_language: Default language code for x-default.
        hreflang_attr: Model attribute returning alternates dict.
    """

    languages: list[str] = []
    default_language: str = "en"
    hreflang_attr: str | None = None

    def alternates(self, obj: Model) -> Mapping[str, str]:
        """
        Return alternate language URLs for an item.

        Override this method to provide language alternatives.

        Args:
            obj: The sitemap item.

        Returns:
            Dict mapping language codes (e.g., "en", "de", "x-default")
            to their full absolute URLs.
        """
        # Try to get from model attribute
        if self.hreflang_attr:
            attr = getattr(obj, self.hreflang_attr, None)
            if attr:
                return attr() if callable(attr) else attr

        return {}

    def _build_hreflang_xml(self, obj: Model, protocol: str, domain: str) -> str:
        """
        Build the hreflang xhtml:link elements for an item.

        Args:
            obj: The sitemap item.
            protocol: URL protocol (http/https).
            domain: Site domain.

        Returns:
            XML string with xhtml:link elements.
        """
        alts = self.alternates(obj)
        if not alts:
            return ""

        parts = []
        for lang, url in alts.items():
            # Ensure URL is absolute
            if url and not url.startswith(("http://", "https://")):
                url = f"{protocol}://{domain}{url}"

            if url:
                escaped_url = escape(url)
                parts.append(
                    f'<xhtml:link rel="alternate" hreflang="{lang}" href="{escaped_url}" />'
                )

        return "\n".join(parts)

    def _urls(self, page: Any, protocol: str, domain: str) -> list[dict[str, Any]]:
        """
        Override to add hreflang links to URL data.

        This should be called via super() in the implementing class.
        """
        # Call parent _urls method
        urls = super()._urls(page, protocol, domain)

        for url_data in urls:
            item = url_data.get("item")
            if item:
                url_data["hreflang"] = self._build_hreflang_xml(item, protocol, domain)

        return urls


# =============================================================================
# Convenience Classes
# =============================================================================

class I18nSitemap(HreflangMixin):
    """
    Convenience class combining HreflangMixin with common i18n patterns.

    This class provides utilities for Django's i18n URL handling.

    Usage::

        from django.urls import reverse
        from django.utils.translation import activate

        class MySitemap(I18nSitemap, BaseSitemap):
            languages = ["en", "de", "fr"]

            def alternates(self, obj):
                alts = {}
                for lang in self.languages:
                    activate(lang)
                    alts[lang] = obj.get_absolute_url()
                return alts
    """

    def get_i18n_alternates(
        self,
        obj: Model,
        url_method: str = "get_absolute_url",
    ) -> dict[str, str]:
        """
        Get alternates using Django's i18n URL system.

        Activates each language and calls the URL method.

        Args:
            obj: The model instance.
            url_method: Method name to call for URL.

        Returns:
            Dict mapping language codes to URLs.
        """
        # pylint: disable=import-outside-toplevel
        from django.utils.translation import activate, get_language

        original_lang = get_language()
        alts = {}

        try:
            for lang in self.languages:
                activate(lang)
                method = getattr(obj, url_method, None)
                if method:
                    url = method() if callable(method) else method
                    alts[lang] = url

            # Add x-default pointing to default language
            if self.default_language and self.default_language in alts:
                alts["x-default"] = alts[self.default_language]

        finally:
            # Restore original language
            if original_lang:
                activate(original_lang)

        return alts


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "HreflangMixin",
    "I18nSitemap",
]
