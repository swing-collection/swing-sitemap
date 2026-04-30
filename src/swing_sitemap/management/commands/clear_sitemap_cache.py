# -*- coding: utf-8 -*-

"""
Clear Sitemap Cache Management Command
======================================

Clear cached sitemap data.

Usage::

    # Clear all sitemap caches
    python manage.py clear_sitemap_cache

    # Clear specific section
    python manage.py clear_sitemap_cache --section static
"""

from django.core.management.base import BaseCommand

from swing_sitemap.conf import get_setting
from swing_sitemap.utils.util_cache import get_cache, invalidate_cache


class Command(BaseCommand):
    help = "Clear cached sitemap data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--section",
            help="Clear cache for specific sitemap section only.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be cleared without actually clearing.",
        )

    def handle(self, *args, **options):
        cache_config = get_setting("cache", default={}) or {}
        if not cache_config.get("enabled", False):
            self.stdout.write(
                self.style.WARNING(
                    "Caching is not enabled. Set SWING_SITEMAP['cache']['enabled'] = True"
                )
            )
            return

        section = options.get("section")
        dry_run = options.get("dry_run", False)

        if dry_run:
            if section:
                self.stdout.write(f"Would clear cache for section: {section}")
            else:
                self.stdout.write("Would clear all sitemap cache entries")
            return

        if section:
            self.stdout.write(f"Clearing cache for section: {section}")
            pattern = f"*{section}*"
        else:
            self.stdout.write("Clearing all sitemap cache entries...")
            pattern = None

        count = invalidate_cache(pattern)

        if count:
            self.stdout.write(
                self.style.SUCCESS(f"Cleared {count} cache entries.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Cache cleared.")
            )
