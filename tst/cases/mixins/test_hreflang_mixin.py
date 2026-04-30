# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel


"""
Tests for swing.sitemap.mixins.hreflang_mixin module.
"""


# Import | Future
from __future__ import annotations

# Import | Standard Library
from unittest.mock import MagicMock


class TestHreflangMixin:
    """Tests for HreflangMixin class."""

    def test_alternates_returns_empty_dict_by_default(self):
        """Test alternates returns empty dict by default."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        obj = MagicMock()
        result = mixin.alternates(obj)
        assert result == {}

    def test_alternates_uses_hreflang_attr_callable(self):
        """Test alternates uses hreflang_attr when callable."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        mixin.hreflang_attr = "get_alternates"

        obj = MagicMock()
        obj.get_alternates.return_value = {"en": "/en/page/", "de": "/de/page/"}

        result = mixin.alternates(obj)
        assert result == {"en": "/en/page/", "de": "/de/page/"}
        obj.get_alternates.assert_called_once()

    def test_alternates_uses_hreflang_attr_property(self):
        """Test alternates uses hreflang_attr when property."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        mixin.hreflang_attr = "alternates_dict"

        obj = MagicMock()
        # Make it a non-callable attribute
        obj.alternates_dict = {"en": "/en/", "fr": "/fr/"}

        result = mixin.alternates(obj)
        assert result == {"en": "/en/", "fr": "/fr/"}

    def test_alternates_returns_empty_when_attr_is_none(self):
        """Test alternates returns empty when attr value is None."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        mixin.hreflang_attr = "alternates_dict"

        obj = MagicMock()
        obj.alternates_dict = None

        result = mixin.alternates(obj)
        assert result == {}

    def test_build_hreflang_xml_returns_empty_for_no_alts(self):
        """Test _build_hreflang_xml returns empty string when no alternates."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        obj = MagicMock()

        result = mixin._build_hreflang_xml(obj, "https", "example.com")
        assert result == ""

    def test_build_hreflang_xml_generates_links(self):
        """Test _build_hreflang_xml generates proper xhtml:link elements."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        class TestMixin(HreflangMixin):
            def alternates(self, obj):
                return {"en": "/en/page/", "de": "/de/page/"}

        mixin = TestMixin()
        obj = MagicMock()

        result = mixin._build_hreflang_xml(obj, "https", "example.com")

        assert 'hreflang="en"' in result
        assert 'hreflang="de"' in result
        assert 'href="https://example.com/en/page/"' in result
        assert 'href="https://example.com/de/page/"' in result
        assert 'rel="alternate"' in result

    def test_build_hreflang_xml_handles_absolute_urls(self):
        """Test _build_hreflang_xml handles already absolute URLs."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        class TestMixin(HreflangMixin):
            def alternates(self, obj):
                return {"en": "https://other.com/en/page/"}

        mixin = TestMixin()
        obj = MagicMock()

        result = mixin._build_hreflang_xml(obj, "https", "example.com")

        # Should not modify absolute URLs
        assert 'href="https://other.com/en/page/"' in result

    def test_build_hreflang_xml_skips_empty_urls(self):
        """Test _build_hreflang_xml skips empty/None URLs."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        class TestMixin(HreflangMixin):
            def alternates(self, obj):
                return {"en": "/en/", "de": None, "fr": ""}

        mixin = TestMixin()
        obj = MagicMock()

        result = mixin._build_hreflang_xml(obj, "https", "example.com")

        assert 'hreflang="en"' in result
        assert 'hreflang="de"' not in result
        assert 'hreflang="fr"' not in result

    def test_build_hreflang_xml_escapes_special_chars(self):
        """Test _build_hreflang_xml escapes special characters."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        class TestMixin(HreflangMixin):
            def alternates(self, obj):
                return {"en": "/page?a=1&b=2"}

        mixin = TestMixin()
        obj = MagicMock()

        result = mixin._build_hreflang_xml(obj, "https", "example.com")

        # & should be escaped
        assert "&amp;" in result

    def test_urls_adds_hreflang(self):
        """Test _urls method adds hreflang to URL data."""
        from django.contrib.sitemaps import Sitemap

        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        class TestSitemap(HreflangMixin, Sitemap):
            def items(self):
                return ["item1"]

            def location(self, item):
                return f"/{item}/"

            def alternates(self, obj):
                return {"en": "/en/", "de": "/de/"}

        sitemap = TestSitemap()
        urls = sitemap._urls(1, "https", "example.com")

        assert len(urls) > 0
        for url_data in urls:
            if "item" in url_data:
                assert "hreflang" in url_data

    def test_default_attributes(self):
        """Test default attribute values."""
        from swing.sitemap.mixins.hreflang_mixin import HreflangMixin

        mixin = HreflangMixin()
        assert mixin.languages == []
        assert mixin.default_language == "en"
        assert mixin.hreflang_attr is None


class TestI18nSitemap:
    """Tests for I18nSitemap class."""

    def test_get_i18n_alternates_activates_languages(self):
        """Test get_i18n_alternates activates each language."""
        from swing.sitemap.mixins.hreflang_mixin import I18nSitemap

        sitemap = I18nSitemap()
        sitemap.languages = ["en", "de"]
        sitemap.default_language = "en"

        obj = MagicMock()
        obj.get_absolute_url.return_value = "/page/"

        result = sitemap.get_i18n_alternates(obj, "get_absolute_url")

        # Should have entries for both languages plus x-default
        assert "en" in result
        assert "de" in result
        assert "x-default" in result
        assert result["x-default"] == result["en"]

    def test_get_i18n_alternates_handles_property(self):
        """Test get_i18n_alternates handles non-callable attribute."""
        from swing.sitemap.mixins.hreflang_mixin import I18nSitemap

        sitemap = I18nSitemap()
        sitemap.languages = ["en"]
        sitemap.default_language = "en"

        obj = MagicMock()
        obj.absolute_url = "/page/"  # Non-callable

        result = sitemap.get_i18n_alternates(obj, "absolute_url")

        assert "en" in result
        assert result["en"] == "/page/"

    def test_get_i18n_alternates_empty_languages(self):
        """Test get_i18n_alternates with no languages configured."""
        from swing.sitemap.mixins.hreflang_mixin import I18nSitemap

        sitemap = I18nSitemap()
        sitemap.languages = []

        obj = MagicMock()

        result = sitemap.get_i18n_alternates(obj, "get_absolute_url")

        assert result == {}

    def test_get_i18n_alternates_no_method(self):
        """Test get_i18n_alternates when object has no method."""
        from swing.sitemap.mixins.hreflang_mixin import I18nSitemap

        sitemap = I18nSitemap()
        sitemap.languages = ["en"]
        sitemap.default_language = "en"

        obj = MagicMock(spec=[])  # No attributes

        result = sitemap.get_i18n_alternates(obj, "get_absolute_url")

        assert "en" not in result

    def test_get_i18n_alternates_restores_language(self):
        """Test get_i18n_alternates restores original language."""
        from django.utils.translation import activate, get_language

        from swing.sitemap.mixins.hreflang_mixin import I18nSitemap

        sitemap = I18nSitemap()
        sitemap.languages = ["de"]
        sitemap.default_language = "de"

        # Set original language
        activate("en")

        obj = MagicMock()
        obj.get_absolute_url.return_value = "/page/"

        sitemap.get_i18n_alternates(obj, "get_absolute_url")

        # Language should be restored
        assert get_language() == "en"
