# -*- coding: utf-8 -*-
"""Django settings for tests / type-checking."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test"
DEBUG = True
ALLOWED_HOSTS = ["example.com", "testserver", "localhost"]
USE_TZ = True
TIME_ZONE = "UTC"
SITE_ID = 1

INSTALLED_APPS: list[str] = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "swing.sitemap.apps.SwingSitemapConfig",
]

MIDDLEWARE: list[str] = []

ROOT_URLCONF = "tst.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/swing_test_media"

# Common third-party / app-specific settings used by source code.
# Defined here so mypy_django_plugin sees them and doesn't raise
# "Settings object has no attribute X" for runtime-only config.
REDIS_HOST = "localhost"
REDIS_PORT = 6379
ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = 9200
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
SITEMAP_URL = "http://example.com/sitemap.xml"
BAIDU_API_TOKEN = "test-token"

# Swing Sitemap configuration for tests
SWING_SITEMAP = {
    "static": {
        "views": ["home", "about"],
        "priority": 0.6,
        "changefreq": "weekly",
    },
}
