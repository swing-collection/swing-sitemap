# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Minimal URLConf for test Django project."""


# =============================================================================
# Imports
# =============================================================================

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from swing.sitemap.urls import sitemap_urlpatterns

# =============================================================================
# Views
# =============================================================================


def home_view(request):
    """Home page view."""
    return HttpResponse("Home")


def about_view(request):
    """About page view."""
    return HttpResponse("About")


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    *sitemap_urlpatterns(include_index=True),
]
