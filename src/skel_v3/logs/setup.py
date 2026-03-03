#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""LOGGING WITH FORMAT TO STDOUT"""

__updated__ = "2026-03-02 17:25:00"

import logging

from logs.formatter import JsonStdoutHandler

# -----------------------------------------------------------------------------
#
# Module design notes:
# Initializes process-wide structured logging with deterministic handler setup.
#
# -----------------------------------------------------------------------------


def init_logging(config: dict) -> None:
    """Initialize process-wide logging in JSON format.

    Inputs:
    - config: dictionary with `LOG_LEVEL`, `SERVICE_NAME`, and `SERVICE_ENV`.

    Returns:
    - `None`.
    """
    level_name = config.get("LOG_LEVEL", "INFO").upper()
    service_name = config.get("SERVICE_NAME", "skel-service")
    environment = config.get("SERVICE_ENV", "local")

    root = logging.getLogger()
    root.setLevel(level_name)

    # Avoid duplicates if this function is called more than once
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = JsonStdoutHandler(service_name=service_name, environment=environment)
    root.addHandler(handler)

    logging.getLogger(__name__).info(
        "Logging initialized",
        extra={
            "operation": "logging_init",
            "io_phase": "after",
            "io_target": "stdout",
            "outcome": "ok",
        },
    )
