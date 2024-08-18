# -*- coding: utf-8 -*-


# =============================================================================
# DocString
# =============================================================================

"""
Provides Base Sitemap
=====================

This module defines an abstract base class for generating sitemaps in Django.

Classes:
    - BaseSitemap: Abstract base class for custom sitemaps.

Links:
    - https://github.com/django/django/blob/master/docs/ref/contrib/sitemaps.txt

"""


# =============================================================================
# Imports
# =============================================================================


# Import | Standard Library
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

# Import | Libraries
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.translation import gettext as _

# Import | Local Modules


# =============================================================================
# Base Class
# =============================================================================

class BaseSitemap(Sitemap, ABC):
    """
    Base Sitemap
    ============

    An abstract base class for creating sitemaps in Django. This class provides
    a structure and utility methods for building custom sitemaps.

    Attributes:
        changefreq (str): The frequency with which the content is expected to
            change 
        priority (float): The priority of this URL relative to other URLs.

    """

    # Parameters
    # =========================================================================

    changefreq: str = "weekly"
    priority: float = 0.5

    # Constructor
    # =========================================================================

    def __init__(self, items: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the BaseSitemap with a list of items.

        Args:
            items (Optional[List[Dict[str, Any]]]): A list of dictionaries
                where each dictionary contains the 'view_name' and optional
                'kwargs' for reversing URLs. Defaults to an empty list if not
                provided.
        """
        self.items_list = items or []

    # Abstract Methods
    # =========================================================================

    @abstractmethod
    def items(self) -> List[Dict[str, Any]]:
        """
        Abstract method that should return the list of items to include in the
        sitemap.

        Returns:
            List[Dict[str, Any]]: A list of items where each item is a dictionary
            containing at least a 'view_name' key.
        """
        pass

    def location(self, item: Dict[str, Any]) -> str:
        """
        Return the URL for a given item in the sitemap.

        Args:
            item (Dict[str, Any]): A dictionary containing the 'view_name' and
                optional 'kwargs' for reversing the URL.

        Returns:
            str: The resolved URL for the given item.
        """
        kwargs = item.get("kwargs")
        return reverse(item["view_name"], kwargs=kwargs)


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "BaseSitemap",
]
