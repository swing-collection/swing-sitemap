# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for ModelSitemap using the built-in auth.User model."""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import datetime as _dt

import pytest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from swing.sitemap.sitemaps.sitemap_model import ModelSitemap

pytestmark = pytest.mark.django_db


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def alice():
    User = get_user_model()
    return User.objects.create_user(
        username="alice", email="alice@example.com", password="x"
    )


# =============================================================================
# Tests
# =============================================================================


def test_callable_queryset_evaluated_lazily(alice):
    User = get_user_model()
    sm = ModelSitemap(queryset=lambda: User.objects.all())
    assert list(sm.items()) == [alice]


def test_queryset_passed_directly(alice):
    User = get_user_model()
    sm = ModelSitemap(queryset=User.objects.all())
    assert list(sm.items()) == [alice]


def test_priority_and_changefreq_overrides(alice):
    sm = ModelSitemap(
        queryset=get_user_model().objects.all(),
        priority=0.9,
        changefreq="daily",
    )
    assert sm.priority == 0.9
    assert sm.changefreq == "daily"


def test_lastmod_reads_date_field(alice):
    sm = ModelSitemap(
        queryset=get_user_model().objects.all(),
        date_field="date_joined",
    )
    value = sm.lastmod(alice)
    assert isinstance(value, _dt.datetime)


def test_lastmod_returns_none_when_no_date_field(alice):
    sm = ModelSitemap(queryset=get_user_model().objects.all())
    assert sm.lastmod(alice) is None


def test_location_uses_callable_attr(alice):
    sm = ModelSitemap(
        queryset=get_user_model().objects.all(),
        location_attr=lambda obj: f"/u/{obj.username}/",
    )
    assert sm.location(alice) == "/u/alice/"


def test_location_uses_string_attr(alice):
    alice.url = "/profile/alice/"  # plain attr, not a method
    sm = ModelSitemap(
        queryset=get_user_model().objects.all(),
        location_attr="url",
    )
    assert sm.location(alice) == "/profile/alice/"


def test_from_settings_builds_from_dotted_model(alice):
    User = get_user_model()
    with override_settings(
        SWING_SITEMAP={
            "models": {
                "user": {
                    "model": f"{User._meta.app_label}.{User._meta.model_name}",
                    "filters": {"username": "alice"},
                    "order_by": ["username"],
                    "date_field": "date_joined",
                    "priority": 0.7,
                    "changefreq": "weekly",
                }
            }
        }
    ):
        sm = ModelSitemap.from_settings("user")
        assert list(sm.items()) == [alice]
        assert sm.priority == 0.7
        assert sm.changefreq == "weekly"
        assert sm.date_field == "date_joined"


def test_from_settings_raises_without_model():
    with override_settings(SWING_SITEMAP={"models": {"x": {}}}):
        with pytest.raises(ValueError):
            ModelSitemap.from_settings("x")
