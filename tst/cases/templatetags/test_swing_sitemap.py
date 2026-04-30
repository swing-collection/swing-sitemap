# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Tests for the {% sitemap_url %} template tag and context processor."""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

from django.template import Context, RequestContext, Template
from django.test import RequestFactory

# =============================================================================
# Tests
# =============================================================================


def test_template_tag_returns_relative_without_request():
    out = Template("{% load swing_sitemap %}{% sitemap_url %}").render(Context())
    assert out == "/sitemap.xml"


def test_template_tag_returns_absolute_with_request():
    req = RequestFactory().get("/", HTTP_HOST="example.com")
    out = Template("{% load swing_sitemap %}{% sitemap_url %}").render(
        RequestContext(req)
    )
    assert out == "http://example.com/sitemap.xml"


def test_context_processor_provides_absolute_url():
    from swing.sitemap.context_processors import sitemap_url

    req = RequestFactory().get("/", HTTP_HOST="example.com")
    ctx = sitemap_url(req)
    assert ctx == {"SITEMAP_URL": "http://example.com/sitemap.xml"}
