#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:37"


from typing import Optional

# -----------------------------------------------------------------------------
#
# Module design notes:
# Provides small, explicit API-key validation helpers for handlers/middleware.
#
# -----------------------------------------------------------------------------


def is_valid_apikey(key: Optional[str], expected: str | None) -> bool:
    """Compare a provided API key against the expected value.

    Inputs:
    - key: API key presented by the client.
    - expected: API key expected by configuration or backend.

    Returns:
    - `True` when both keys exist and match exactly.
    - `False` in any other case.
    """
    if key is None or expected is None:
        return False
    return key == expected
