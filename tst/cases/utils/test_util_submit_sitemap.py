# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.utils.util_submit_sitemap module.
"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from swing.sitemap.utils.util_submit_sitemap import PING_ENDPOINTS, submit_sitemap


# =============================================================================
# Tests
# =============================================================================


class TestPingEndpoints:
    """Tests for PING_ENDPOINTS constant."""

    def test_google_endpoint_exists(self):
        """Test Google ping endpoint is defined."""
        assert "google" in PING_ENDPOINTS

    def test_bing_endpoint_exists(self):
        """Test Bing ping endpoint is defined."""
        assert "bing" in PING_ENDPOINTS

    def test_endpoints_contain_url_placeholder(self):
        """Test endpoints contain {url} placeholder."""
        for name, url in PING_ENDPOINTS.items():
            assert "{url}" in url, f"{name} endpoint missing {{url}} placeholder"


class TestSubmitSitemap:
    """Tests for submit_sitemap function."""

    @patch("swing.sitemap.utils.util_submit_sitemap.requests.get")
    def test_submit_returns_dict(self, mock_get):
        """Test that submit_sitemap returns a dictionary."""
        mock_get.return_value = MagicMock(status_code=200)

        result = submit_sitemap("https://example.com/sitemap.xml")

        assert isinstance(result, dict)

    @patch("swing.sitemap.utils.util_submit_sitemap.requests.get")
    def test_submit_to_all_endpoints(self, mock_get):
        """Test that submit_sitemap pings all endpoints."""
        mock_get.return_value = MagicMock(status_code=200)

        result = submit_sitemap("https://example.com/sitemap.xml")

        assert len(result) == len(PING_ENDPOINTS)

    @patch("swing.sitemap.utils.util_submit_sitemap.requests.get")
    def test_submit_to_specific_endpoints(self, mock_get):
        """Test submitting to specific endpoints."""
        mock_get.return_value = MagicMock(status_code=200)

        result = submit_sitemap(
            "https://example.com/sitemap.xml",
            endpoints={"google": PING_ENDPOINTS["google"]},
        )

        assert "google" in result
        assert len(result) == 1

    @patch("swing.sitemap.utils.util_submit_sitemap.requests.get")
    def test_submit_handles_connection_error(self, mock_get):
        """Test that submit_sitemap handles connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = submit_sitemap(
            "https://example.com/sitemap.xml",
            timeout=1.0,
        )

        # Should return None for failed requests
        for status in result.values():
            assert status is None

    @patch("swing.sitemap.utils.util_submit_sitemap.requests.get")
    def test_submit_returns_status_codes(self, mock_get):
        """Test that submit_sitemap returns status codes."""
        mock_get.return_value = MagicMock(status_code=200)

        result = submit_sitemap("https://example.com/sitemap.xml")

        for status in result.values():
            assert status == 200
