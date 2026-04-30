# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
WSGI config for demo project.

Exposes the WSGI callable as a module-level variable named `application`.

For more details, visit:
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/

"""


# =============================================================================
# Imports
# =============================================================================

import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application


# =============================================================================
# WSGI Application Setup
# =============================================================================

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

application: WSGIHandler = get_wsgi_application()
