#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:51"

import uuid
from flask import request, g

# -----------------------------------------------------------------------------
#
# Module design notes:
# Provides per-request correlation ID resolution and caching via Flask context.
#
# -----------------------------------------------------------------------------


def get_or_create_request_id() -> str:
    """Get or create the trace identifier for the current request.

    Inputs:
    - No explicit parameters; uses Flask `request` and `g` context.

    Returns:
    - Request id string reused from header or generated via UUID4.
    """
    rid = getattr(g, "request_id", None)
    if rid:
        return rid

    header_rid = request.headers.get("X-Request-ID")
    if header_rid:
        rid = header_rid
    else:
        rid = str(uuid.uuid4())

    g.request_id = rid
    return rid
