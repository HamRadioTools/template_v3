#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Authn Service"""

__updated__ = "2026-02-07 07:40:04"


import logging
from typing import Optional, Dict, Any
from flask import jsonify

logger = logging.getLogger(__name__)


def register_example_routes(app, *, config: dict, stores: Optional[Dict[str, Any]] = None):
    """
    Register an example module
    """
    if stores is None:
        stores = {}

    pg_pool = stores.get("pg_pool")
    if pg_pool is None:
        logger.warning("PG pool is not available; module will always fall back to guest/RO")

    @app.route("/example", methods=["GET"])
    def example():
        """
        Example function
        """
        return jsonify({"module": "example"})
