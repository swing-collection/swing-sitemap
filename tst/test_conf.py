# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for the swing_sitemap config accessor.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import warnings

from django.test.utils import override_settings

from swing.sitemap.conf import DEFAULTS, get_config, get_setting

# =============================================================================
# Tests
# =============================================================================


def test_defaults_returned_when_no_user_settings():
    with override_settings(SWING_SITEMAP={}):
        cfg = get_config()
    assert cfg["wagtail"] == DEFAULTS["wagtail"]
    assert cfg["static"]["priority"] == 0.5


def test_user_settings_shallow_merge():
    with override_settings(
        SWING_SITEMAP={"wagtail": {"priority": 0.9}, "models": {"x": "a.B"}}
    ):
        cfg = get_config()
    # overridden key
    assert cfg["wagtail"]["priority"] == 0.9
    # default sibling preserved
    assert cfg["wagtail"]["changefreq"] == "monthly"
    # passthrough nested dict
    assert cfg["models"] == {"x": "a.B"}


def test_get_setting_dotted_lookup_with_default():
    with override_settings(SWING_SITEMAP={"wagtail": {"priority": 0.9}}):
        assert get_setting("wagtail", "priority") == 0.9
        assert get_setting("wagtail", "missing", default="fallback") == "fallback"
        assert get_setting("nope", default=42) == 42


def test_legacy_seo_priority_emits_deprecation_warning():
    with override_settings(SWING_SITEMAP={}, SEO_SITEMAP_PRIORITY={"work": 0.9}):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            cfg = get_config()
    assert cfg["priority"] == {"work": 0.9}
    assert any(
        issubclass(w.category, DeprecationWarning)
        and "SEO_SITEMAP_PRIORITY" in str(w.message)
        for w in caught
    )


def test_legacy_video_model_emits_deprecation_warning():
    with override_settings(SWING_SITEMAP={}, VIDEO_SITEMAP_MODEL="auth.User"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            cfg = get_config()
    assert cfg["video"]["model"] == "auth.User"
    assert any(
        issubclass(w.category, DeprecationWarning)
        and "VIDEO_SITEMAP_MODEL" in str(w.message)
        for w in caught
    )


def test_user_settings_take_precedence_over_legacy():
    with override_settings(
        SWING_SITEMAP={"video": {"model": "auth.User"}},
        VIDEO_SITEMAP_MODEL="legacy.Model",
    ):
        cfg = get_config()
    assert cfg["video"]["model"] == "auth.User"


def test_unknown_user_keys_pass_through():
    with override_settings(SWING_SITEMAP={"custom_key": 123}):
        assert get_config()["custom_key"] == 123
