# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Django Management
==========================

Django's command-line utility for administrative tasks for the demo project.

- Adds the `src` directory to the Python path for app discovery.
- Sets the default Django settings module for the demo project.

Usage:
    python manage.py <command>

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import os
import sys
from pathlib import Path


# =============================================================================
# Setup: Extend Python Path
# =============================================================================

DEMO_DIR: Path = Path(__file__).resolve().parent
BASE_DIR: Path = DEMO_DIR.parent

sys.path.append(str(BASE_DIR / "src"))


# =============================================================================
# Functions
# =============================================================================


def main() -> None:
    """Run Django administrative tasks."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    main()
