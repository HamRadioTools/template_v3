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
# Exposes logging bootstrap helpers as the package public logging interface.
#
# -----------------------------------------------------------------------------

__all__ = ["init_logging"]
