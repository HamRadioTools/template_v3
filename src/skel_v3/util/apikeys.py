#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:37"


from typing import Optional


def is_valid_apikey(key: Optional[str], expected: str | None) -> bool:
    if key is None or expected is None:
        return False
    return key == expected
