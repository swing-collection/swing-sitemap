# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
WSGI config for demo project.


This module sets up the WSGI application for the `demo` project, allowing it
to be served by WSGI-compatible web servers.

Exposes the WSGI callable as a module-level variable named `application`.

For more details, visit:
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import os

# Import | Libraries
from django.core.wsgi import get_wsgi_application

# Import | Local Modules


# =============================================================================
# WSGI Application Setup
# =============================================================================

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

# Create the WSGI application callable
application = get_wsgi_application()
