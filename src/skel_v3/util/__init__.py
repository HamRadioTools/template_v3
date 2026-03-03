#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:30"

from util.apikeys import is_valid_apikey

# -----------------------------------------------------------------------------
#
# Module design notes:
# Utility package public interface.
#
# Responsibilities:
# - Re-export small utility helpers used across modules.
# - Keep package-level imports stable for call sites.
#
# Scope boundaries:
# - No utility implementation logic here.
# - Keep import side effects minimal.
#
# Maintenance guidance:
# - Export only helpers that are intentionally shared.
# - Avoid turning this file into a catch-all dependency hub.
#
# -----------------------------------------------------------------------------

__all__ = ["is_valid_apikey"]
