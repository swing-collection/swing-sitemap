# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Django Management
==========================

This script provides Django's command-line utility for administrative tasks
such as running the development server, making migrations, and more.

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

# Import | Libraries

# Import | Local Modules


# =============================================================================
# Setup: Extend Python Path
# =============================================================================

# Define project directories
DEMO_DIR = Path(__file__).resolve().parent  # Location of manage.py
BASE_DIR = DEMO_DIR.parent  # Root of the project

# Add `src` directory to the Python path
sys.path.append(str(BASE_DIR / "src"))


# =============================================================================
# Functions
# =============================================================================

def main():
    """
    Run Django administrative tasks.

    This function initializes the environment and executes the requested
    management command.

    """

    # Set the default settings module for the project
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    try:
        # Import and execute Django's management utility
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        # Handle cases where Django is not installed or accessible
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line arguments
    execute_from_command_line(sys.argv)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    main()
