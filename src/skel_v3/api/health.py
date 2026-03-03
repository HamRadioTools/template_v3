#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Health Service"""

__updated__ = "2026-02-07 07:24:13"

from flask import jsonify

# -----------------------------------------------------------------------------
#
# Module design notes:
# Exposes lightweight liveness/readiness endpoints for orchestration probes.
#
# -----------------------------------------------------------------------------


def register_health_routes(app, *, config: dict):
    """Register operational health endpoints on the Flask app.

    Inputs:
    - app: Flask application where routes are registered.
    - config: configuration with service metadata for responses.

    Returns:
    - `None`.
    """
    service_name = config.get("SERVICE_NAME", "micro-service")
    service_version = config.get("SERVICE_VERSION", "0.1.0")

    @app.route("/health", methods=["GET"])
    def health():
        """Return a basic liveness response for the HTTP process.

        Inputs:
        - No explicit parameters.

        Returns:
        - JSON con `status`, `service` y `version`.
        """
        return jsonify(
            {
                "status": "ok",
                "service": service_name,
                "version": service_version,
            }
        )

    @app.route("/ready", methods=["GET"])
    def ready():
        """Return a simple readiness response for orchestrators/load balancers.

        Inputs:
        - No explicit parameters.

        Returns:
        - JSON con estado `ready`.
        """
        # In the future it can be added other checks: DB connectivity, config sanity, etc.
        return jsonify({"status": "ready"})
