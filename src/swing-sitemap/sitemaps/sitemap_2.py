# -*- coding: utf-8 -*-


"""
Sitemaps
========

https://github.com/django/django/blob/master/docs/ref/contrib/sitemaps.txt
"""

# Standard Library Modules
import os.path

# Third-Party Modules
# from django.contrib.sitemaps.views import sitemap
from django.contrib import sitemaps
# from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
# from sitemaps.sitemaps import StaticViewSitemap
# from django.shortcuts import reverse
from django.urls import reverse

# Local Application Modules
# from engine.apps.projects.models import Project
# from engine.apps.stories.models import Story



# sitemaps.py

class StaticViewSitemap(sitemaps.Sitemap):
    """
    """

    changefreq  = "daily"
    priority    = 0.9

    def items(self):
        """
        """

        items = [
            # "process",
            # "people",
            # "index",
            "connect",
            # "project-index",
            # "story-index",
            ]

        return items


    def location(self, item):
        """
        """

        return reverse(item)




class StorySitemap(GenericSitemap):
    """
    """
# - ``changefreq``
# - ``item``
# - ``lastmod``
# - ``location``
# - ``priority``


    # info_dict    = {
    #         "queryset":     Story.objects.all(),
    #         "date_field":   "updated_date",
    #         }
    # changefreq  = "never"
    # priority    = 0.9
    # def items(self):
    #     """
    #     """
    #     # return Project.objects.filter(is_draft=False)
    #     return Story.objects.filter(published_bool=True)

    # def lastmod(self, obj):
    #     """
    #     """
    #     lastmod = obj.updated_date
    #     return lastmod

    # def location(self, item):
    #     """
    #     """
    #     # return reverse(item.get_absolute_url())
    #     return reverse(item)



class ProjectSitemap(GenericSitemap):
    """
    """

# class StaticViewSitemap(Sitemap):
#     """
#     """

    # def items(self):
    #     """
    #     """
    #     return ["profile"]


    # def location(self, item):
    #     """
    #     """
    #     return reverse(item)
