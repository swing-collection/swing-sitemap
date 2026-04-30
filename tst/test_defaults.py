# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for default_sitemaps factory.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps
from swing.sitemap.sitemaps.sitemap_model import ModelSitemap
from swing.sitemap.sitemaps.sitemap_static import StaticSitemap


# =============================================================================
# Tests
# =============================================================================


def test_only_static_when_no_models_configured():
    sm = default_sitemaps()
    assert "static" in sm
    assert isinstance(sm["static"], StaticSitemap)
    assert "user" not in sm


def test_static_omitted_when_no_views_configured():
    with override_settings(SWING_SITEMAP={}):
        sm = default_sitemaps()
    assert not sm


def test_models_entries_built_from_settings():
    User = get_user_model()
    with override_settings(
        SWING_SITEMAP={
            "static": {"views": ["home"]},
            "models": {
                "user": {
                    "model": f"{User._meta.app_label}.{User._meta.model_name}",
                    "priority": 0.4,
                }
            },
        }
    ):
        sm = default_sitemaps()
    assert "static" in sm
    assert "user" in sm
    assert isinstance(sm["user"], ModelSitemap)
    assert sm["user"].priority == 0.4


def test_extra_overrides_auto_keys():
    sentinel = object()
    sm = default_sitemaps(extra={"static": sentinel})  # type: ignore[arg-type]
    assert sm["static"] is sentinel


def test_bad_model_entry_skipped(caplog):
    with override_settings(
        SWING_SITEMAP={
            "static": {"views": ["home"]},
            "models": {"broken": {"model": "nope.Missing"}},
        }
    ):
        sm = default_sitemaps()
    assert "broken" not in sm
    assert "static" in sm
