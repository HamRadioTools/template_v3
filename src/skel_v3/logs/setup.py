#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""LOGGING WITH FORMAT TO STDOUT"""

__updated__ = "2026-02-07 07:16:21"

import logging

from .formatter import JsonStdoutHandler


def init_logging(config: dict) -> None:
    """
    Configure global logging:
    - Log level taken from config["LOG_LEVEL"]
    - Single JsonStdoutHandler writing to STDOUT
    """
    level_name = config.get("LOG_LEVEL", "INFO").upper()
    service_name = config.get("SERVICE_NAME", "micro-service")
    environment = config.get("SERVICE_ENV", "local")

    root = logging.getLogger()
    root.setLevel(level_name)

    # Avoid duplicates if this function is called more than once
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = JsonStdoutHandler(service_name=service_name, environment=environment)
    root.addHandler(handler)
