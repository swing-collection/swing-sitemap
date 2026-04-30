# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Submit Sitemap Management Command
=================================

Submit sitemap to search engine ping endpoints.

Usage::

    # Submit with URL from settings
    python manage.py submit_sitemap

    # Submit specific URL
    python manage.py submit_sitemap https://example.com/sitemap.xml

    # Submit to specific endpoints
    python manage.py submit_sitemap --endpoints google bing

"""


# =============================================================================
# Imports
# =============================================================================

from django.core.management.base import BaseCommand, CommandError

from swing.sitemap.conf import get_setting
from swing.sitemap.utils.submission import PING_ENDPOINTS, submit_sitemap

# =============================================================================
# Command
# =============================================================================


class Command(BaseCommand):
    help = "Submit sitemap to search engine ping endpoints"

    def add_arguments(self, parser):
        parser.add_argument(
            "sitemap_url",
            nargs="?",
            help="Sitemap URL to submit. Uses SWING_SITEMAP['submit']['sitemap_url'] if not provided.",
        )
        parser.add_argument(
            "--endpoints",
            nargs="+",
            choices=list(PING_ENDPOINTS.keys()),
            help="Specific endpoints to submit to. Defaults to all configured endpoints.",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=10.0,
            help="Request timeout in seconds (default: 10).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be submitted without actually submitting.",
        )

    def handle(self, *args, **options):  # pragma: no cover
        # Get sitemap URL
        sitemap_url = options.get("sitemap_url")
        if not sitemap_url:
            submit_config = get_setting("submit", default={}) or {}
            sitemap_url = submit_config.get("sitemap_url")

        if not sitemap_url:
            raise CommandError(
                "No sitemap URL provided. Either pass it as an argument or "
                "configure SWING_SITEMAP['submit']['sitemap_url']."
            )

        # Get endpoints
        endpoint_names = options.get("endpoints")
        if endpoint_names:
            endpoints = {k: v for k, v in PING_ENDPOINTS.items() if k in endpoint_names}
        else:
            endpoints = dict(PING_ENDPOINTS)

        timeout = options["timeout"]

        # Dry run
        if options["dry_run"]:
            self.stdout.write(f"Would submit sitemap: {sitemap_url}")
            self.stdout.write(f"To endpoints: {', '.join(endpoints.keys())}")
            self.stdout.write(f"Timeout: {timeout}s")
            return

        # Submit
        self.stdout.write(f"Submitting sitemap: {sitemap_url}")
        self.stdout.write(f"Endpoints: {', '.join(endpoints.keys())}")

        results = submit_sitemap(sitemap_url, endpoints=endpoints, timeout=timeout)

        # Report results
        success_count = 0
        for name, status in results.items():
            if status is None:
                self.stdout.write(
                    self.style.ERROR(f"  {name}: FAILED (connection error)")
                )
            elif status >= 400:
                self.stdout.write(self.style.WARNING(f"  {name}: HTTP {status}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"  {name}: HTTP {status}"))
                success_count += 1

        # Summary
        if success_count == len(results):
            self.stdout.write(
                self.style.SUCCESS(f"\nAll {success_count} submissions successful!")
            )
        elif success_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\n{success_count}/{len(results)} submissions successful."
                )
            )
        else:
            self.stdout.write(self.style.ERROR("\nAll submissions failed!"))
