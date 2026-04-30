# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for StaticSitemap (str-or-dict items, lastmod, settings defaults)."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import datetime as _dt

from django.test.utils import override_settings

from swing.sitemap.sitemaps.sitemap_static import StaticSitemap

# =============================================================================
# Tests
# =============================================================================


def test_string_item_resolves_to_reverse_url():
    sm = StaticSitemap(["home"])
    assert sm.location("home") == "/"


def test_dict_item_resolves_with_view_name():
    sm = StaticSitemap([{"view_name": "about"}])
    assert sm.location({"view_name": "about"}) == "/about/"


def test_dict_item_lastmod_returned_as_is():
    today = _dt.date.today()
    sm = StaticSitemap([{"view_name": "about", "lastmod": today}])
    assert sm.lastmod({"view_name": "about", "lastmod": today}) == today
    assert sm.lastmod("home") is None


def test_constructor_overrides_take_precedence_over_settings():
    sm = StaticSitemap(["home"], priority=0.1, changefreq="hourly")
    assert sm.priority == 0.1
    assert sm.changefreq == "hourly"


def test_settings_defaults_propagate():
    with override_settings(
        SWING_SITEMAP={
            "static": {"priority": 0.42, "changefreq": "yearly", "views": []}
        }
    ):
        sm = StaticSitemap(["home"])
    assert sm.priority == 0.42
    assert sm.changefreq == "yearly"


def test_from_setting_reads_views_list():
    with override_settings(
        SWING_SITEMAP={"static": {"views": ["home", {"view_name": "about"}]}}
    ):
        sm = StaticSitemap.from_setting()
    assert list(sm.items()) == ["home", {"view_name": "about"}]


def test_from_setting_handles_missing_config():
    with override_settings(SWING_SITEMAP={}):
        sm = StaticSitemap.from_setting()
    assert not list(sm.items())
