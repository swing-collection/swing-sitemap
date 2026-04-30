# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.sitemap.urls module init.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

# =============================================================================
# Tests
# =============================================================================


class TestUrlsModuleLazyLoading:
    """Test urls module lazy urlpatterns loading."""

    def test_urlpatterns_lazy_loading(self):
        """Test urlpatterns is lazily loaded."""
        import swing.sitemap.urls as urls_module

        # Clear cached value if exists
        if "urlpatterns" in urls_module.__dict__:
            del urls_module.__dict__["urlpatterns"]

        # Access urlpatterns - should work
        patterns = urls_module.urlpatterns
        assert isinstance(patterns, list)

    def test_urlpatterns_cached(self):
        """Test urlpatterns is cached after first access."""
        import swing.sitemap.urls as urls_module

        # Access twice
        patterns1 = urls_module.urlpatterns
        patterns2 = urls_module.urlpatterns

        # Should be same object (cached)
        assert patterns1 is patterns2

    def test_invalid_attribute(self):
        """Test AttributeError for invalid attributes."""
        import swing.sitemap.urls as urls_module

        with pytest.raises(AttributeError):
            _ = urls_module.nonexistent_attribute_xyz
