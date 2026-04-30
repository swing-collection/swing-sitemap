# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cancel Debounce
===============

Cancel a pending debounced function.

"""


# =============================================================================
# Imports
# =============================================================================

from __future__ import annotations

from .debounce import _debounce_lock, _debounce_timers


# =============================================================================
# Functions
# =============================================================================

def cancel_debounce(key: str) -> None:
    """Cancel a pending debounced function."""
    with _debounce_lock:
        if key in _debounce_timers:
            _debounce_timers[key].cancel()
            del _debounce_timers[key]


# =============================================================================
# Exports
# =============================================================================

__all__ = ["cancel_debounce"]
