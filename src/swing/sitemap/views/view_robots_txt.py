# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Robots.txt View
===============

A configurable class-based view for rendering robots.txt files.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views import View

# =============================================================================
# Classes
# =============================================================================


class RobotsTxtView(View):
    """
    Robots.txt View
    ===============

    Renders a robots.txt file for search engine crawlers.

    Usage::

        from swing.sitemap.views import RobotsTxtView

        urlpatterns = [
            path("robots.txt", RobotsTxtView.as_view()),
        ]

    Configuration via class attributes::

        class MyRobotsTxtView(RobotsTxtView):
            user_agents = [
                {"name": "*", "allow": ["/"], "disallow": ["/admin/", "/api/"]},
                {"name": "Googlebot", "allow": ["/"], "crawl_delay": 1},
            ]
            sitemap_url = "/sitemap.xml"

    Or via Django settings::

        SWING_SITEMAP = {
            "robots": {
                "user_agents": [
                    {"name": "*", "disallow": ["/admin/"]},
                ],
                "sitemap_url": "/sitemap.xml",
            }
        }

    Attributes:
        template_name: Template for rendering robots.txt.
        content_type: Response content type.
        user_agents: List of user agent rules.
        sitemap_url: URL to the sitemap (will be made absolute).
        extra_lines: Additional lines to include.

    """

    template_name: str = "swing/sitemap/robots.txt"
    content_type: str = "text/plain"

    # Configuration
    user_agents: list[dict[str, Any]] = [
        {
            "name": "*",
            "allow": ["/"],
            "disallow": [],
        }
    ]
    sitemap_url: str | None = "/sitemap.xml"
    extra_lines: list[str] = []

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request and render robots.txt."""
        context = self.get_context_data(request)
        return TemplateResponse(
            request,
            self.get_template_name(),
            context,
            content_type=self.content_type,
        )

    def get_template_name(self) -> str:
        """Return the template name."""
        return self.template_name

    def get_user_agents(self) -> list[dict[str, Any]]:
        """Return user agent rules. Override to customize."""
        # Check Django settings first
        swing_settings = getattr(settings, "SWING_SITEMAP", {})
        robots_settings = swing_settings.get("robots", {})
        if "user_agents" in robots_settings:
            return robots_settings["user_agents"]
        return self.user_agents

    def get_sitemap_url(self, request: HttpRequest) -> str | None:
        """Return the absolute sitemap URL."""
        # Check Django settings first
        swing_settings = getattr(settings, "SWING_SITEMAP", {})
        robots_settings = swing_settings.get("robots", {})
        url = robots_settings.get("sitemap_url", self.sitemap_url)

        if url is None:
            return None

        # Make absolute if relative
        if url.startswith("/"):
            return request.build_absolute_uri(url)
        return url

    def get_extra_lines(self) -> list[str]:
        """Return extra lines to include."""
        swing_settings = getattr(settings, "SWING_SITEMAP", {})
        robots_settings = swing_settings.get("robots", {})
        return robots_settings.get("extra_lines", self.extra_lines)

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Return context for template rendering."""
        return {
            "user_agents": self.get_user_agents(),
            "sitemap_url": self.get_sitemap_url(request),
            "extra_lines": self.get_extra_lines(),
            "request": request,
        }


# =============================================================================
# Exports
# =============================================================================

__all__ = ["RobotsTxtView"]
