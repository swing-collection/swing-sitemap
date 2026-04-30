"""Minimal URLConf for test Django project."""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from swing.sitemap.urls import sitemap_urlpatterns


def home_view(request):
    return HttpResponse("Home")


def about_view(request):
    return HttpResponse("About")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    *sitemap_urlpatterns(include_index=True),
]
