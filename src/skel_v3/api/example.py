#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Authn Service"""

__updated__ = "2026-02-07 07:40:04"


import logging
from typing import Optional, Dict, Any
from flask import jsonify

# -----------------------------------------------------------------------------
#
# Module design notes:
# Reference example for organizing API route modules.
#
# Responsibilities:
# - Register a minimal endpoint that proves route wiring and JSON response flow.
# - Demonstrate optional datastore dependency access in a safe way.
#
# Scope boundaries:
# - This module is illustrative and intentionally domain-neutral.
# - No authentication, persistence writes, or complex validation here.
#
# Extension guidance:
# - Use this file as a template for new route modules.
# - Keep endpoint registration and module-local helpers close together.
#
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)


def register_example_routes(app, *, config: dict, stores: Optional[Dict[str, Any]] = None):
    """Register sample routes that demonstrate the API module pattern.

    Inputs:
    - app: Flask application where the endpoint is registered.
    - config: service configuration (reserved for module-specific behavior).
    - stores: optional datastore dependencies (for example, `pg_pool`).

    Returns:
    - `None`.
    """
    if stores is None:
        stores = {}

    pg_pool = stores.get("pg_pool")
    if pg_pool is None:
        logger.warning("PG pool is not available; module will always fall back to guest/RO")

    @app.route("/example", methods=["GET"])
    def example():
        """Return a minimal response to verify module wiring.

        Inputs:
        - No explicit parameters.

        Returns:
        - Static JSON payload with module metadata.
        """
        return jsonify({"module": "example"})
