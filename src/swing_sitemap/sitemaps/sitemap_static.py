# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Static Sitemap
=======================

This module provides a `StaticSitemap` class for generating sitemaps of static
views in a Django application. It is based on a custom `BaseSitemap` class,
which provides the core functionality for building sitemaps.

Classes:
    - StaticSitemap: A class for creating sitemaps for static views.

Links:
    - https://github.com/django/django/blob/master/docs/ref/contrib/sitemaps.txt

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict, List

# Import | Libraries
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.translation import gettext as _

# Import | Local Modules
from swing_sitemap.sitemaps.sitemap_base import BaseSitemap


# =============================================================================
# Class
# =============================================================================

class StaticSitemap(BaseSitemap):
    """
    Static Sitemap
    ==============


    A sitemap class for generating URLs of static views to be included in an
    XML sitemap.

    Attributes:
        changefreq (str): The frequency with which the content is expected
            to change.
        priority (float): The priority of this URL relative to other URLs.

    """

    # Parameters
    # =========================================================================

    changefreq = "weekly"
    priority = 0.9


    # Utility Methods
    # =========================================================================

    def items(self) -> List[Dict[str, Any]]:
        """
        Retrieve the list of static views to include in the sitemap.

        Returns:
            List[Dict[str, Any]]: A list of items to include in the sitemap,
                where each item is a dictionary containing the 'view_name' and
                optional 'kwargs'.
        """
        return self.items_list


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "StaticSitemap",
]
