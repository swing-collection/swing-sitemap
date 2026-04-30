# -*- coding: utf-8 -*-

"""
Validate Sitemap Management Command
====================================

Validate sitemap XML against Google's specifications.

Usage::

    # Validate local file
    python manage.py validate_sitemap /path/to/sitemap.xml

    # Validate URL
    python manage.py validate_sitemap https://example.com/sitemap.xml

    # Validate all configured sitemaps
    python manage.py validate_sitemap --all
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from pathlib import Path
import re
import urllib.request
from xml.etree import ElementTree

from django.core.management.base import BaseCommand, CommandError

from swing.sitemap.sitemaps.sitemap_defaults import default_sitemaps


class Command(BaseCommand):
    help = "Validate sitemap XML against specifications"

    # Sitemap limits per Google specs
    MAX_URLS = 50000
    MAX_SIZE_BYTES = 50 * 1024 * 1024  # 50MB
    MAX_URL_LENGTH = 2048

    # Namespaces
    NAMESPACES = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "image": "http://www.google.com/schemas/sitemap-image/1.1",
        "video": "http://www.google.com/schemas/sitemap-video/1.1",
        "news": "http://www.google.com/schemas/sitemap-news/0.9",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "source",
            nargs="?",
            help="Path to sitemap file or URL to validate.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Validate all configured sitemaps (generates and validates).",
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Enable strict validation (fails on warnings).",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Show detailed validation output.",
        )

    def handle(self, *args, **options):
        source = options.get("source")
        validate_all = options.get("all")
        strict = options.get("strict", False)
        verbose = options.get("verbose", False)

        if not source and not validate_all:
            raise CommandError(
                "Provide a sitemap source (file path or URL) or use --all"
            )

        if validate_all:
            self._validate_all_sitemaps(strict, verbose)
        else:
            self._validate_source(source, strict, verbose)

    def _validate_all_sitemaps(self, strict, verbose):
        """Validate all configured sitemaps."""
        from django.contrib.sitemaps.views import sitemap as sitemap_view
        from django.test import RequestFactory

        sitemaps = default_sitemaps()
        if not sitemaps:
            self.stdout.write(self.style.WARNING("No sitemaps configured."))
            return

        factory = RequestFactory()
        all_valid = True

        for name, sitemap in sitemaps.items():
            self.stdout.write(f"\nValidating section: {name}")

            # Generate sitemap
            request = factory.get(f"/sitemap-{name}.xml", HTTP_HOST="example.com")
            try:
                response = sitemap_view(request, {name: sitemap})  # type: ignore[arg-type]
                content = response.content
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Failed to generate: {e}"))
                all_valid = False
                continue

            # Validate
            valid = self._validate_content(
                content, f"sitemap-{name}.xml", strict, verbose
            )
            if not valid:
                all_valid = False

        if all_valid:
            self.stdout.write(self.style.SUCCESS("\nAll sitemaps valid!"))
        else:
            self.stdout.write(self.style.ERROR("\nSome sitemaps have issues."))

    def _validate_source(self, source, strict, verbose):
        """Validate a single sitemap source."""
        # Load content
        if source.startswith(("http://", "https://")):
            try:
                with urllib.request.urlopen(source, timeout=30) as response:
                    content = response.read()
            except Exception as e:
                raise CommandError(f"Failed to fetch URL: {e}")
        else:
            path = Path(source)
            if not path.exists():
                raise CommandError(f"File not found: {source}")
            content = path.read_bytes()

        valid = self._validate_content(content, source, strict, verbose)
        if valid:
            self.stdout.write(self.style.SUCCESS("\nSitemap is valid!"))
        else:
            raise CommandError("Sitemap validation failed.")

    def _validate_content(  # noqa: C901
        self, content, source_name, strict, verbose,
    ):
        """Validate sitemap XML content."""
        errors = []
        warnings = []

        # Check size
        size_bytes = len(content)
        if size_bytes > self.MAX_SIZE_BYTES:
            errors.append(
                f"Size {size_bytes:,} bytes exceeds limit of {self.MAX_SIZE_BYTES:,} bytes"
            )
        elif size_bytes > self.MAX_SIZE_BYTES * 0.8:
            warnings.append(
                f"Size {size_bytes:,} bytes is near the limit of {self.MAX_SIZE_BYTES:,} bytes"
            )

        if verbose:
            self.stdout.write(f"  Size: {size_bytes:,} bytes")

        # Parse XML
        try:
            root = ElementTree.fromstring(content)
        except ElementTree.ParseError as e:
            errors.append(f"XML parse error: {e}")
            self._report_results(source_name, errors, warnings)
            return False

        # Check root element
        root_tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if root_tag not in ("urlset", "sitemapindex"):
            errors.append(f"Invalid root element: {root_tag}")
            self._report_results(source_name, errors, warnings)
            return False

        is_index = root_tag == "sitemapindex"

        if verbose:
            self.stdout.write(f"  Type: {'index' if is_index else 'urlset'}")

        # Count and validate entries
        if is_index:
            entries = root.findall("sm:sitemap", self.NAMESPACES)
            entries.extend(
                root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap")
            )
        else:
            entries = root.findall("sm:url", self.NAMESPACES)
            entries.extend(
                root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            )

        url_count = len(entries)
        if verbose:
            self.stdout.write(f"  URLs: {url_count:,}")

        if url_count > self.MAX_URLS:
            errors.append(f"URL count {url_count:,} exceeds limit of {self.MAX_URLS:,}")
        elif url_count > self.MAX_URLS * 0.8:
            warnings.append(
                f"URL count {url_count:,} is near the limit of {self.MAX_URLS:,}"
            )

        # Validate each URL
        for i, entry in enumerate(entries):
            loc = entry.find("sm:loc", self.NAMESPACES)
            if loc is None:
                loc = entry.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")

            if loc is None or not loc.text:
                errors.append(f"Entry {i + 1}: Missing <loc> element")
                continue

            url = loc.text.strip()

            # Check URL length
            if len(url) > self.MAX_URL_LENGTH:
                errors.append(
                    f"Entry {i + 1}: URL length {len(url)} exceeds {self.MAX_URL_LENGTH}"
                )

            # Check URL format
            if not url.startswith(("http://", "https://")):
                errors.append(f"Entry {i + 1}: Invalid URL scheme: {url[:50]}")

            # Check for special characters that should be encoded
            if any(c in url for c in '<>"{}|\\^[]`'):
                warnings.append(
                    f"Entry {i + 1}: URL contains unencoded special characters"
                )

        # Check for duplicate URLs (sample first 1000)
        sample_entries = entries[:1000]
        urls = []
        for entry in sample_entries:
            loc = entry.find("sm:loc", self.NAMESPACES)
            if loc is None:
                loc = entry.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        duplicate_count = len(urls) - len(set(urls))
        if duplicate_count > 0:
            warnings.append(
                f"Found {duplicate_count} duplicate URLs (sampled first 1000)"
            )

        # Report results
        self._report_results(source_name, errors, warnings)

        if strict:
            return len(errors) == 0 and len(warnings) == 0
        return len(errors) == 0

    def _report_results(self, source_name, errors, warnings):
        """Report validation results."""
        if errors:
            self.stdout.write(self.style.ERROR(f"  Errors ({len(errors)}):"))
            for error in errors[:10]:  # Limit output
                self.stdout.write(self.style.ERROR(f"    - {error}"))
            if len(errors) > 10:
                self.stdout.write(
                    self.style.ERROR(f"    ... and {len(errors) - 10} more")
                )

        if warnings:
            self.stdout.write(self.style.WARNING(f"  Warnings ({len(warnings)}):"))
            for warning in warnings[:10]:
                self.stdout.write(self.style.WARNING(f"    - {warning}"))
            if len(warnings) > 10:
                self.stdout.write(
                    self.style.WARNING(f"    ... and {len(warnings) - 10} more")
                )

        if not errors and not warnings:
            self.stdout.write(self.style.SUCCESS("  No issues found."))
