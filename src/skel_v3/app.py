#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Main app module"""

__updated__ = "2026-03-02 17:25:00"

import logging
import sys
import time
from flask import Flask, g, jsonify, url_for

from config import get_config
from db import init_datastores
from logs import init_logging

from api.example import register_example_routes
from api.health import register_health_routes
from util.request_id import get_or_create_request_id
from worker import run_worker_app

# -----------------------------------------------------------------------------
#
# Module design notes:
# Main composition root for API and worker process modes.
#
# Responsibilities:
# - Read runtime mode (`APP_TYPE`) and dispatch to API or worker execution.
# - Build Flask app with logging, datastore wiring, and route registration.
# - Expose an app factory for Gunicorn `--factory` startup.
#
# Scope boundaries:
# - Keep business rules out of this module.
# - Treat this file as bootstrap/orchestration only.
#
# Operational guidance:
# - Use `APP_TYPE=api` for HTTP service instances.
# - Use `APP_TYPE=worker` for background execution mode.
# - Fail fast on unknown modes to prevent ambiguous runtime state.
#
# -----------------------------------------------------------------------------


###############################################################################
#
# CREATE FLASK APPLICATION, IF THIS IS THE SELECTED EXECUTION MODE
#
###############################################################################


def create_api_app(config: dict) -> Flask:
    """Build the Flask application ready to serve requests.

    Inputs:
    - config: global runtime configuration (logging, environment, datastores).

    Returns:
    - A `Flask` instance with base middleware and routes registered.
    """
    init_logging(config)

    stores = init_datastores(config)

    app = Flask(__name__)
    logging.getLogger("werkzeug").disabled = True

    @app.before_request
    def _log_request_start():
        """Initialize request tracing metadata at request start.

        Inputs:
        - No explicit parameters; uses the active Flask request context.

        Returns:
        - `None`.
        """
        g.request_started_at = time.perf_counter()
        get_or_create_request_id()

    metadata = {
        "service": config.get("SERVICE_NAME"),
        "version": config.get("SERVICE_VERSION"),
        "environment": config.get("SERVICE_ENV"),
    }

    @app.route("/", methods=["GET"])
    def root():
        """Expose a discovery document with API links.

        Inputs:
        - No explicit parameters; operates on the current request context.

        Returns:
        - JSON response with service metadata and available links.
        """
        discovery = {
            "service": metadata["service"],
            "version": metadata["version"],
            "environment": metadata["environment"],
            "links": [
                {
                    "rel": "health",
                    "href": url_for("health", _external=False),
                    "method": "GET",
                    "description": "Liveness probe",
                },
                {
                    "rel": "ready",
                    "href": url_for("ready", _external=False),
                    "method": "GET",
                    "description": "Readiness probe",
                },
                {
                    "rel": "example",
                    "href": url_for("example", _external=False),
                    "method": "GET",
                    "description": "Example endpoint",
                },
            ],
        }
        return jsonify(discovery)

    # Register the endpoints here
    register_health_routes(app, config=config)
    register_example_routes(app, config=config, stores=stores)

    return app


###############################################################################
#
# APPLICATION MAIN
#
###############################################################################


def main() -> None:
    """Process entrypoint for API mode or worker mode.

    Inputs:
    - No parameters; reads runtime configuration from environment.

    Returns:
    - `None`. Starts the selected runtime or exits on invalid configuration.
    """
    config = get_config()
    app_type = config.get("APP_TYPE", "api")

    if app_type == "api":
        app = create_api_app(config)
        app.run(host="0.0.0.0", port=9000)
    elif app_type == "worker":
        run_worker_app(config)
    else:
        # Fail fast but with a clear message
        logging.basicConfig(level=logging.ERROR)
        logging.error(
            "Invalid APP_TYPE %r. Use 'api' or 'worker'. " "Check your environment or .env file.",
            app_type,
        )
        sys.exit(2)


def app_factory() -> Flask:
    """Gunicorn app factory compatible with `--factory`.

    Inputs:
    - No parameters.

    Returns:
    - Configured `Flask` instance for WSGI server execution.
    """
    return create_api_app(get_config())


###############################################################################
#
# APPLICATION ENTRY POINT
#
###############################################################################

if __name__ == "__main__":
    main()
