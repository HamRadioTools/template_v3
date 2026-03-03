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
# Request correlation ID resolver for Flask request scope.
#
# Responsibilities:
# - Reuse inbound `X-Request-ID` when provided.
# - Generate UUID fallback when no inbound ID exists.
# - Cache the resolved value on `flask.g` for per-request stability.
#
# Scope boundaries:
# - No persistence or distributed tracing integration here.
# - No header mutation beyond read access.
#
# Operational guidance:
# - Intended to be called early in request lifecycle (for example `before_request`).
# - Helps correlate logs across handlers and middleware.
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
