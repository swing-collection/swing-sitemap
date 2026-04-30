# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Debounce
========

Debounce a function call by key.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import threading
from typing import Any, Callable

# =============================================================================
# State
# =============================================================================

_debounce_timers: dict[str, threading.Timer] = {}
_debounce_lock = threading.Lock()


# =============================================================================
# Functions
# =============================================================================


def debounce(key: str, delay: float, func: Callable[[], Any]) -> None:
    """
    Debounce a function call by key.

    If called multiple times within `delay` seconds, only the last call
    executes. Useful for batching rapid model changes.
    """
    with _debounce_lock:
        # Cancel existing timer for this key
        if key in _debounce_timers:
            _debounce_timers[key].cancel()

        # Create new timer
        timer = threading.Timer(delay, func)
        _debounce_timers[key] = timer
        timer.start()


# =============================================================================
# Exports
# =============================================================================

__all__ = ["debounce"]
