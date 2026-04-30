# -*- coding: utf-8 -*-
"""Root conftest.py - sets up sys.path before pytest-django.

Portable across swing-* repos. Adds project root and `src/` to sys.path so
imports work both with and without an installed package.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
