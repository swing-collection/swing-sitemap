# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Get Setting
===========

Look up a configuration value by dotted path.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

# Import | Local
from .get_config import get_config

# =============================================================================
# Functions
# =============================================================================


def get_setting(*path: str, default: Any = None) -> Any:
    """
    Look up a value by dotted path inside the merged config.

    Example::

        get_setting("wagtail", "priority", default=0.5)
    """
    node: Any = get_config()
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


# =============================================================================
# Exports
# =============================================================================

__all__ = ["get_setting"]
