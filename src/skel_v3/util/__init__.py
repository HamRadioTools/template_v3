#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:30"

from util.apikeys import is_valid_apikey

# -----------------------------------------------------------------------------
#
# Module design notes:
# Defines utility package exports intended for cross-module reuse.
#
# -----------------------------------------------------------------------------

__all__ = ["is_valid_apikey"]
