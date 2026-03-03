#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:37"


from typing import Optional

# -----------------------------------------------------------------------------
#
# Module design notes:
# Minimal API-key helper primitives.
#
# Responsibilities:
# - Provide explicit equality-based API-key checks.
# - Keep validation logic readable and easy to test.
#
# Scope boundaries:
# - No datastore lookups or cryptographic transformations here.
# - No request/response behavior in this module.
#
# Extension guidance:
# - Add additional helper functions only when they remain generic and reusable.
# - Keep this module free from service-specific policy branching.
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
