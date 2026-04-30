# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Sitemap - Default Sitemaps Factory
========================================

Builds the canonical ``sitemaps`` dict that Django's
:func:`django.contrib.sitemaps.views.sitemap` view expects.

Per the project's design decision, ``swing.sitemap`` is **CMS-agnostic**:
the factory ships a ``static`` entry sourced from
``SWING_SITEMAP["static"]["views"]`` and any model entries declared under
``SWING_SITEMAP["models"]``. Sites that need a CMS-page sitemap (e.g.
Wagtail's ``wagtail.contrib.sitemaps.Sitemap``) are expected to merge it
into the dict themselves::

    from swing.sitemap import default_sitemaps
    from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap

    sitemaps = {**default_sitemaps(), "wagtail": WagtailSitemap}

"""

# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from collections.abc import Mapping

from django.contrib.sitemaps import Sitemap

from swing.sitemap.conf import get_setting
from swing.sitemap.sitemaps.sitemap_model import ModelSitemap
from swing.sitemap.sitemaps.sitemap_static import StaticSitemap


# =============================================================================
# Functions
# =============================================================================


def default_sitemaps(
    extra: Mapping[str, Sitemap | type[Sitemap]] | None = None,
) -> dict[str, Sitemap | type[Sitemap]]:
    """
    Return the canonical ``sitemaps`` dict for use with
    :func:`django.contrib.sitemaps.views.sitemap`.

    Includes:

    * ``"static"`` — :class:`~swing.sitemap.StaticSitemap` configured from
      ``SWING_SITEMAP["static"]["views"]``. The entry is omitted if no
      static views are configured.
    * One :class:`~swing.sitemap.ModelSitemap` per key under
      ``SWING_SITEMAP["models"]``. Bad entries are skipped silently with
      a logger warning so a misconfigured model never breaks
      ``/sitemap.xml`` for the rest of the site.

    Args:
        extra: Optional mapping of additional sitemaps (instances or
            classes) to merge in. Keys override the auto-generated ones.
    """
    sitemaps: dict[str, Sitemap | type[Sitemap]] = {}

    static_views = get_setting("static", "views", default=None)
    if static_views:
        sitemaps["static"] = StaticSitemap.from_setting()

    models_config = get_setting("models", default=None) or {}
    for key in models_config:
        try:
            sitemaps[key] = ModelSitemap.from_settings(key)
        except Exception:  # noqa: BLE001  pylint: disable=broad-exception-caught
            import logging

            logging.getLogger(__name__).warning(
                "Skipping sitemap %r: failed to build from settings.",
                key,
                exc_info=True,
            )

    if extra:
        sitemaps.update(extra)

    return sitemaps

# =============================================================================
# Exports
# =============================================================================

__all__ = ["default_sitemaps",]
