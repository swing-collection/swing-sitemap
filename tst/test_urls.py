# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""End-to-end tests for the sitemap URL helpers."""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

import pytest
from django.test import Client

pytestmark = pytest.mark.django_db


# =============================================================================
# Helper Functions
# =============================================================================


def _get(url: str) -> tuple[int, str]:
    resp = Client().get(url, HTTP_HOST="example.com")
    return resp.status_code, resp.content.decode()


# =============================================================================
# Tests
# =============================================================================


def test_sitemap_xml_returns_valid_urlset():
    status, body = _get("/sitemap.xml")
    assert status == 200
    assert body.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<urlset" in body
    assert "http://example.com/" in body
    assert "http://example.com/about/" in body


def test_sitemap_index_links_to_section():
    status, body = _get("/sitemap-index.xml")
    assert status == 200
    assert "<sitemapindex" in body
    assert "http://example.com/sitemap-static.xml" in body


def test_sitemap_section_returns_urlset():
    status, body = _get("/sitemap-static.xml")
    assert status == 200  # noqa: F841
    assert "<urlset" in body
    assert "http://example.com/about/" in body


def test_settings_drive_priority_and_changefreq():
    status, body = _get("/sitemap.xml")
    assert "<priority>0.6</priority>" in body
    assert "<changefreq>weekly</changefreq>" in body
