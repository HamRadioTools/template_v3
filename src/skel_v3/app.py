#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Main app module"""

__updated__ = "2026-02-07 08:00:28"

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


###############################################################################
#
# CREATE FLASK APPLICATION, IF THIS IS THE SELECTED EXECUTION MODE
#
###############################################################################


def create_api_app(config: dict) -> Flask:
    """
    Create the Flask app with logging and datastores initialized.
    """
    init_logging(config)

    stores = init_datastores(config)

    app = Flask(__name__)
    logging.getLogger("werkzeug").disabled = True

    @app.before_request
    def _log_request_start():
        g.request_started_at = time.perf_counter()
        get_or_create_request_id()

    metadata = {
        "service": config.get("SERVICE_NAME"),
        "version": config.get("SERVICE_VERSION"),
        "environment": config.get("SERVICE_ENV"),
    }

    @app.route("/", methods=["GET"])
    def root():
        """
        HATEOAS-style discovery endpoint for automatic clients.
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
    """
    Main entry point: decide whether to launch the API or worker.
    """
    config = get_config()
    app_type = config.get("APP_TYPE", "api")  # this can be api or worker

    if app_type == "api":
        app = create_api_app(config)
        app.run(host="0.0.0.0", port=9000)
    else:
        # Fail fast but with a clear message
        logging.basicConfig(level=logging.ERROR)
        logging.error(
            "Invalid APP_TYPE %r. Use 'api' or 'worker'. " "Check your environment or .env file.",
            app_type,
        )
        sys.exit(2)


###############################################################################
#
# APPLICATION ENTRY POINT
#
###############################################################################

if __name__ == "__main__":
    main()
