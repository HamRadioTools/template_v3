#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Health Service"""

__updated__ = "2026-02-07 07:24:13"

from flask import jsonify


def register_health_routes(app, *, config: dict):
    """
    Register basic health/ready endpoints.

    - GET /health  -> simple liveness check
    - GET /ready   -> can be extended to check DB, etc.
    """
    service_name = config.get("SERVICE_NAME", "micro-service")
    service_version = config.get("SERVICE_VERSION", "0.1.0")

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            {
                "status": "ok",
                "service": service_name,
                "version": service_version,
            }
        )

    @app.route("/ready", methods=["GET"])
    def ready():
        # In the future it can be added other checks: DB connectivity, config sanity, etc.
        return jsonify({"status": "ready"})
