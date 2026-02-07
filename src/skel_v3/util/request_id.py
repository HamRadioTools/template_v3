#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-07 01:45:51"

import uuid
from flask import request, g


def get_or_create_request_id() -> str:
    """
    Return the current request_id stored in `g`, otherwise:
    - read it from the `X-Request-ID` header if provided by the client
    - or generate a UUID4 when missing.
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
