# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Package Initialization
============================

This module serves as the root package initializer for the Swing ecosystem,
a modular application area system for Django. It extends the package path
to support namespace packages across multiple locations.

The Swing package provides infrastructure for managing, creating, and
interacting with modular applications within a Django project environment.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from pkgutil import extend_path

# =============================================================================
# Variables
# =============================================================================

__path__ = extend_path(__path__, __name__)  # type: ignore[assignment,name-defined]
