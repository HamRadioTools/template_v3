#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""LOGGING WITH FORMAT TO STDOUT"""

__updated__ = "2026-02-07 07:22:46"


# re-export to later import as `from module.log import init_logging`
from logs.setup import init_logging

# -----------------------------------------------------------------------------
#
# Module design notes:
# Logging package public interface.
#
# Responsibilities:
# - Re-export logging bootstrap utilities for simple imports.
# - Keep logger setup entrypoints centralized and discoverable.
#
# Scope boundaries:
# - No formatter implementation or runtime bootstrap logic here.
# - This initializer should remain thin and stable.
#
# Maintenance guidance:
# - Only export symbols intended for broad package consumption.
# - Avoid side effects beyond controlled imports.
#
# -----------------------------------------------------------------------------

__all__ = ["init_logging"]
