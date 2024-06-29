# -*- coding: utf-8 -*-


"""
StaticSitemap
=============

https://github.com/django/django/blob/master/docs/ref/contrib/sitemaps.txt
"""

# Standard Library Modules
# import os.path

# Third-Party Modules
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Local Application Modules


class StaticSitemap(Sitemap):
    """
    Reverse static views for XML sitemap.
    """
    changefreq  = "weekly"
    priority    = 0.9

    def __init__(self, items_in=[]):
        """
        """
        self.items_list = items_in
        # self.lastmod_list = lastmod_in
        # self.items_list = items_in[0]
        # self.lastmod = items_in[1]

    def items(self):
        """
        """
        # Return list of url names for views to include in sitemap
        items = self.items_list
        return items

    # def lastmod(self, obj):
    #     """
    #     """
    #     lastmod = self.lastmod_list
    #     return lastmod

    def location(self, item):
        """
        """
        # if kwargs not in item set as None
        kwargs = item["kwargs"] if "kwargs" in item else None
        return reverse(item["view_name"], kwargs=kwargs)
