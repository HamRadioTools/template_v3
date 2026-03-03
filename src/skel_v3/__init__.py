#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Main initalization"""

__updated__ = "2026-03-03 02:20:52"

# Expose get_config at package level if useful
from config import get_config  # noqa: F401

# -----------------------------------------------------------------------------
#
# Module design notes:
# Package root metadata and public surface definition.
#
# Responsibilities:
# - Expose stable package metadata (`__version__`, `__all__`).
# - Re-export selected helpers that callers may import directly from package root.
#
# Scope boundaries:
# - No runtime bootstrapping, datastore wiring, or HTTP behavior here.
# - Keep imports minimal to avoid side effects during package import.
#
# Maintenance guidance:
# - Add exports here only when they are intended as public API.
# - Avoid leaking internal module structure through broad re-exports.
#
# -----------------------------------------------------------------------------

__version__ = "0.1.0"
__all__ = ["get_config"]
