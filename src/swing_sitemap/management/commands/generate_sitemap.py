# -*- coding: utf-8 -*-

"""
Generate Sitemap Management Command
====================================

Generate sitemap XML files to disk or stdout.

Usage::

    # Generate to stdout
    python manage.py generate_sitemap

    # Generate to file
    python manage.py generate_sitemap --output /path/to/sitemap.xml

    # Generate specific sections
    python manage.py generate_sitemap --sections static pages

    # Generate with index
    python manage.py generate_sitemap --output-dir /var/www/sitemaps/ --with-index
"""

import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.test import RequestFactory

from swing_sitemap.conf import get_setting
from swing_sitemap.sitemaps.sitemap_defaults import default_sitemaps
from swing_sitemap.sitemaps.sitemap_index import (
    get_sitemap_index_urls,
    paginate_all_sitemaps,
)


class Command(BaseCommand):
    help = "Generate sitemap XML files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            help="Output file path. Writes to stdout if not provided.",
        )
        parser.add_argument(
            "--output-dir",
            help="Output directory for multiple sitemap files.",
        )
        parser.add_argument(
            "--sections",
            nargs="+",
            help="Specific sitemap sections to generate.",
        )
        parser.add_argument(
            "--with-index",
            action="store_true",
            help="Generate sitemap index file along with section files.",
        )
        parser.add_argument(
            "--domain",
            default="example.com",
            help="Domain name for sitemap URLs (default: example.com).",
        )
        parser.add_argument(
            "--protocol",
            choices=["http", "https"],
            default="https",
            help="URL protocol (default: https).",
        )
        parser.add_argument(
            "--paginate",
            action="store_true",
            help="Automatically paginate large sitemaps.",
        )

    def handle(self, *args, **options):
        # Get sitemaps
        sitemaps = default_sitemaps()

        # Filter to specific sections if requested
        sections = options.get("sections")
        if sections:
            sitemaps = {k: v for k, v in sitemaps.items() if k in sections}
            missing = set(sections) - set(sitemaps.keys())
            if missing:
                self.stderr.write(
                    self.style.WARNING(f"Sections not found: {', '.join(missing)}")
                )

        if not sitemaps:
            raise CommandError("No sitemaps to generate.")

        # Paginate if requested
        if options["paginate"]:
            sitemaps = paginate_all_sitemaps(sitemaps)

        domain = options["domain"]
        protocol = options["protocol"]
        output = options.get("output")
        output_dir = options.get("output_dir")

        # Generate single file
        if output and not output_dir:
            xml_content = self._generate_combined_sitemap(
                sitemaps, domain, protocol
            )
            Path(output).write_text(xml_content)
            self.stdout.write(
                self.style.SUCCESS(f"Sitemap written to: {output}")
            )
            return

        # Generate multiple files
        if output_dir:
            self._generate_sitemap_files(
                sitemaps,
                output_dir,
                domain,
                protocol,
                with_index=options["with_index"],
            )
            return

        # Write to stdout
        xml_content = self._generate_combined_sitemap(sitemaps, domain, protocol)
        self.stdout.write(xml_content)

    def _generate_combined_sitemap(self, sitemaps, domain, protocol):
        """Generate a single combined sitemap XML."""
        from django.contrib.sitemaps.views import sitemap as sitemap_view

        factory = RequestFactory()
        request = factory.get("/sitemap.xml", HTTP_HOST=domain)

        response = sitemap_view(request, sitemaps)
        return response.content.decode("utf-8")

    def _generate_sitemap_files(
        self, sitemaps, output_dir, domain, protocol, with_index=False
    ):
        """Generate separate sitemap files in a directory."""
        from django.contrib.sitemaps.views import sitemap as sitemap_view

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        factory = RequestFactory()
        generated_files = []

        for name, sitemap in sitemaps.items():
            # Generate this section's sitemap
            request = factory.get(
                f"/sitemap-{name}.xml",
                HTTP_HOST=domain,
            )

            response = sitemap_view(request, {name: sitemap})
            content = response.content.decode("utf-8")

            # Write file
            filename = f"sitemap-{name}.xml"
            filepath = output_path / filename
            filepath.write_text(content)
            generated_files.append(filename)

            self.stdout.write(f"Generated: {filepath}")

        # Generate index if requested
        if with_index:
            index_content = self._generate_sitemap_index(
                sitemaps, domain, protocol
            )
            index_path = output_path / "sitemap-index.xml"
            index_path.write_text(index_content)
            self.stdout.write(f"Generated: {index_path}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nGenerated {len(generated_files)} sitemap files in {output_dir}"
            )
        )

    def _generate_sitemap_index(self, sitemaps, domain, protocol):
        """Generate sitemap index XML."""
        urls = get_sitemap_index_urls(sitemaps, protocol, domain)

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]

        for url in urls:
            location = f"{protocol}://{domain}/{url['location']}"
            lines.append("  <sitemap>")
            lines.append(f"    <loc>{location}</loc>")
            if url.get("lastmod"):
                lastmod = url["lastmod"]
                if hasattr(lastmod, "strftime"):
                    lastmod = lastmod.strftime("%Y-%m-%dT%H:%M:%S%z")
                lines.append(f"    <lastmod>{lastmod}</lastmod>")
            lines.append("  </sitemap>")

        lines.append("</sitemapindex>")
        return "\n".join(lines)
