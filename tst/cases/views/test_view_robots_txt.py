# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.views.view_robots_txt module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.test import RequestFactory
from django.test.utils import override_settings

# Import | Libraries
import pytest

from swing.sitemap.views import RobotsTxtView

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestRobotsTxtView:
    """Tests for RobotsTxtView class-based view."""

    def test_default_template_name(self):
        """Test default template name."""
        view = RobotsTxtView()
        assert view.template_name == "swing/sitemap/robots.txt"

    def test_default_content_type(self):
        """Test default content type."""
        view = RobotsTxtView()
        assert view.content_type == "text/plain"

    def test_get_user_agents_default(self):
        """Test default user agents allow everything."""
        view = RobotsTxtView()
        agents = view.get_user_agents()
        assert agents == [{"name": "*", "allow": ["/"], "disallow": []}]

    def test_get_user_agents_from_settings(self):
        """Test user agents can be overridden via settings."""
        with override_settings(
            SWING_SITEMAP={
                "robots": {
                    "user_agents": [
                        {"name": "*", "disallow": ["/admin/"]},
                    ],
                },
            }
        ):
            view = RobotsTxtView()
            agents = view.get_user_agents()
            assert agents == [{"name": "*", "disallow": ["/admin/"]}]

    def test_get_sitemap_url_default_is_absolute(self):
        """Test default sitemap URL is made absolute."""
        request = RequestFactory().get("/robots.txt")
        view = RobotsTxtView()
        url = view.get_sitemap_url(request)
        assert url == "http://testserver/sitemap.xml"

    def test_get_sitemap_url_none(self):
        """Test sitemap URL can be disabled entirely."""
        with override_settings(
            SWING_SITEMAP={"robots": {"sitemap_url": None}},
        ):
            request = RequestFactory().get("/robots.txt")
            view = RobotsTxtView()
            assert view.get_sitemap_url(request) is None

    def test_get_sitemap_url_absolute_passthrough(self):
        """Test an already-absolute sitemap URL is left untouched."""
        with override_settings(
            SWING_SITEMAP={
                "robots": {"sitemap_url": "https://other.example.com/sitemap.xml"},
            },
        ):
            request = RequestFactory().get("/robots.txt")
            view = RobotsTxtView()
            assert (
                view.get_sitemap_url(request)
                == "https://other.example.com/sitemap.xml"
            )

    def test_get_extra_lines_default(self):
        """Test default extra lines is empty."""
        view = RobotsTxtView()
        assert view.get_extra_lines() == []

    def test_get_extra_lines_from_settings(self):
        """Test extra lines can be set via settings."""
        with override_settings(
            SWING_SITEMAP={"robots": {"extra_lines": ["Host: example.com"]}},
        ):
            view = RobotsTxtView()
            assert view.get_extra_lines() == ["Host: example.com"]

    def test_get_context_data(self):
        """Test context data includes all expected keys."""
        request = RequestFactory().get("/robots.txt")
        view = RobotsTxtView()
        context = view.get_context_data(request)
        assert set(context) == {
            "user_agents",
            "sitemap_url",
            "extra_lines",
            "request",
        }

    def test_get_request_returns_plain_text_response(self):
        """Test GET request renders a robots.txt response."""
        request = RequestFactory().get("/robots.txt")
        view = RobotsTxtView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain"
        content = response.render().content.decode()
        assert "User-agent: *" in content
        assert "Allow: /" in content
        assert "Sitemap: http://testserver/sitemap.xml" in content

    def test_get_request_includes_disallow_and_crawl_delay(self):
        """Test disallow rules and crawl-delay render correctly."""

        class CustomRobotsTxtView(RobotsTxtView):
            user_agents = [
                {
                    "name": "Googlebot",
                    "allow": ["/"],
                    "disallow": ["/admin/"],
                    "crawl_delay": 5,
                },
            ]

        request = RequestFactory().get("/robots.txt")
        response = CustomRobotsTxtView.as_view()(request)
        content = response.render().content.decode()

        assert "User-agent: Googlebot" in content
        assert "Disallow: /admin/" in content
        assert "Crawl-delay: 5" in content
