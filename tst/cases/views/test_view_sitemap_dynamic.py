# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_sitemap_dynamic module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

import datetime as _dt

from django.contrib.auth import get_user_model
from django.test import RequestFactory

# Import | Libraries
import pytest

from swing.sitemap.views import DynamicSitemapView

pytestmark = pytest.mark.django_db


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def rf():
    """Provide a RequestFactory."""
    return RequestFactory()


@pytest.fixture
def alice():
    User = get_user_model()
    return User.objects.create_user(
        username="alice", email="alice@example.com", password="x"
    )


# =============================================================================
# Tests
# =============================================================================


class TestDynamicSitemapViewDefaults:
    """Tests for DynamicSitemapView default configuration."""

    def test_default_template_name(self):
        view = DynamicSitemapView()
        assert view.template_name == "swing/sitemap/sitemap.xml"

    def test_default_content_type(self):
        view = DynamicSitemapView()
        assert view.content_type == "application/xml"

    def test_default_sources_are_empty(self):
        view = DynamicSitemapView()
        assert view.get_static_pages() == []
        assert view.get_model_sources() == []
        assert view.get_callable_sources() == []

    def test_default_priority_and_changefreq(self):
        view = DynamicSitemapView()
        assert view.default_priority == "0.5"
        assert view.default_changefreq == "monthly"


class TestGetPagesStaticSources:
    """Tests for DynamicSitemapView.get_pages with static_pages."""

    def test_absolute_path_loc(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [{"loc": "/about/", "priority": "0.8"}]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert len(pages) == 1
        assert pages[0]["loc"] == "http://testserver/about/"
        assert pages[0]["priority"] == "0.8"
        assert pages[0]["changefreq"] == "monthly"
        assert pages[0]["lastmod"]

    def test_full_url_loc_passthrough(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [{"loc": "https://other.example.com/page/"}]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["loc"] == "https://other.example.com/page/"

    def test_unresolvable_name_falls_back_to_path(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [{"loc": "not-a-real-url-name"}]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["loc"] == "http://testserver/not-a-real-url-name"

    def test_lastmod_date_and_datetime_normalized(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [
                {"loc": "/a/", "lastmod": _dt.date(2024, 1, 1)},
                {
                    "loc": "/b/",
                    "lastmod": _dt.datetime(2024, 1, 2, 12, 0, 0),
                },
            ]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["lastmod"] == "2024-01-01"
        assert pages[1]["lastmod"] == "2024-01-02"

    def test_default_priority_and_changefreq_used(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [{"loc": "/plain/"}]
            default_priority = "0.3"
            default_changefreq = "yearly"

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["priority"] == "0.3"
        assert pages[0]["changefreq"] == "yearly"


class TestGetPagesModelSources:
    """Tests for DynamicSitemapView.get_pages with model_sources."""

    def test_model_source_uses_default_queryset(self, rf, alice):
        User = get_user_model()

        class MyView(DynamicSitemapView):
            model_sources = [
                {
                    "model": f"{User._meta.app_label}.{User._meta.model_name}",
                    "url_pattern": "/users/{pk}/",
                    "priority": "0.7",
                },
            ]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert len(pages) == 1
        assert pages[0]["loc"] == f"http://testserver/users/{alice.pk}/"
        assert pages[0]["priority"] == "0.7"

    def test_model_source_with_explicit_queryset(self, rf, alice):
        User = get_user_model()

        class MyView(DynamicSitemapView):
            model_sources = [
                {
                    "model": User,
                    "queryset": User.objects.filter(pk=alice.pk),
                    "url_pattern": "/users/{username}/",
                },
            ]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["loc"] == "http://testserver/users/alice/"

    def test_model_source_lastmod_field(self, rf, alice):
        User = get_user_model()

        class MyView(DynamicSitemapView):
            model_sources = [
                {
                    "model": User,
                    "queryset": User.objects.filter(pk=alice.pk),
                    "url_pattern": "/users/{pk}/",
                    "lastmod_field": "date_joined",
                },
            ]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert pages[0]["lastmod"] == alice.date_joined.date().isoformat()


class TestGetPagesCallableSources:
    """Tests for DynamicSitemapView.get_pages with callable_sources."""

    def test_callable_source_yields_pages(self, rf):
        def extra_pages(request):
            return [{"loc": "/callable-page/", "priority": "0.9"}]

        class MyView(DynamicSitemapView):
            callable_sources = [extra_pages]

        request = rf.get("/sitemap.xml")
        pages = MyView().get_pages(request)

        assert len(pages) == 1
        assert pages[0]["loc"] == "http://testserver/callable-page/"
        assert pages[0]["priority"] == "0.9"


class TestDynamicSitemapViewResponse:
    """Tests for the full GET response."""

    def test_get_request_returns_xml_response(self, rf):
        class MyView(DynamicSitemapView):
            static_pages = [{"loc": "/", "priority": "1.0"}]

        request = rf.get("/sitemap.xml")
        response = MyView.as_view()(request)

        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"
        content = response.render().content.decode()
        assert "<urlset" in content
        assert "http://testserver/" in content

    def test_get_context_data(self, rf):
        request = rf.get("/sitemap.xml")
        view = DynamicSitemapView()
        pages = view.get_pages(request)
        context = view.get_context_data(request, pages)

        assert context["urlset"] == pages
        assert context["request"] is request
