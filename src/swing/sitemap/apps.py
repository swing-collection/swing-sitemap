# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Maps Config Class
==========================
...

Todo:
-----

Links:
------

"""


# =============================================================================
# Import
# =============================================================================

# Import | Libraries
from django.apps import AppConfig
# from django.core.signals import request_finished
from django.utils.translation import gettext_lazy as _

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================

class SwingSitemapConfig(AppConfig):
    """
    Swing Sitemap App Config
    ========================

    Django application configuration for ``swing.sitemap``.
    """

    # Full Python path to the application
    name = "swing.sitemap"

    # Short name for the application
    label = "swing_sitemap"

    # Human-readable name for the application
    verbose_name = _("Swing Sitemap")

    # The implicit primary key type to add to models within this app.
    default_auto_field = "django.db.models.BigAutoField"

    # def ready(self):
    #     """
    #     Apps Config Ready Function
    #     """

        # Implicitly connect signal handlers decorated with @receiver.
        # from .. import signals

        # Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback)
