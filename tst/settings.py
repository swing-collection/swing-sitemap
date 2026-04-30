# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Django settings for tests / type-checking."""


# =============================================================================
# Imports
# =============================================================================

from pathlib import Path


# =============================================================================
# Base Settings
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test"
DEBUG = True
ALLOWED_HOSTS = ["example.com", "testserver", "localhost"]
USE_TZ = True
TIME_ZONE = "UTC"
SITE_ID = 1


# =============================================================================
# Installed Apps
# =============================================================================

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


# =============================================================================
# Middleware
# =============================================================================

MIDDLEWARE: list[str] = []


# =============================================================================
# URLs and Templates
# =============================================================================

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


# =============================================================================
# Database
# =============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =============================================================================
# Static Files
# =============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/swing_test_media"


# =============================================================================
# Third-Party Settings
# =============================================================================

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


# =============================================================================
# Swing Sitemap Configuration
# =============================================================================

SWING_SITEMAP = {
    "static": {
        "views": ["home", "about"],
        "priority": 0.6,
        "changefreq": "weekly",
    },
}


# =============================================================================
# Swing Cookie Consent Settings
# =============================================================================

COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 31536000
COOKIE_CONSENT_DOMAIN: str | None = None
COOKIE_CONSENT_SECURE = False
COOKIE_CONSENT_HTTPONLY = True
COOKIE_CONSENT_SAMESITE = "Lax"
COOKIE_CONSENT_DECLINE = "declined"
COOKIE_CONSENT_OPT_OUT = False
COOKIE_CONSENT_LOG_ENABLED = False
COOKIE_CONSENT_ENABLED = True
COOKIE_CONSENT_CACHE_BACKEND = "default"
