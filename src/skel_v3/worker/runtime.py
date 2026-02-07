#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Functional worker runtime helpers."""

from __future__ import annotations

__updated__ = "2026-02-07 08:02:35"

import logging
import signal
import time
from typing import Any

from db import init_datastores
from logs import init_logging

logger = logging.getLogger(__name__)


def _perform_work(config: dict, stores: dict[str, Any]) -> None:
    """
    Placeholder unit of work to be replaced with domain-specific logic.
    """
    ############################################################################
    #
    # CODE SHOULD COME HERE AND/OR IN ADDITIONAL MODULES IN THIS PACKAGE FOLDER
    #
    ############################################################################
    logger.info("Worker heartbeat", extra={"service": config.get("SERVICE_NAME")})


def _cleanup(config: dict, stores: dict[str, Any]) -> None:
    logger.info("Worker cleanup complete", extra={"service": config.get("SERVICE_NAME")})


def run_worker_app(config: dict) -> None:
    """
    Initialize logging/datastores and run the worker loop.
    """
    init_logging(config)
    stores = init_datastores(config)
    poll_interval = int(config.get("WORKER_POLL_INTERVAL", 5))
    stopping = False

    def _handle_stop(signum, _frame):
        nonlocal stopping
        logger.info("Received signal %s, preparing to stop", signum)
        stopping = True

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    logger.info(
        "Worker starting",
        extra={
            "service": config.get("SERVICE_NAME"),
            "env": config.get("SERVICE_ENV"),
            "poll_interval": poll_interval,
        },
    )
    try:
        while not stopping:
            _perform_work(config, stores)
            time.sleep(poll_interval)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Worker interrupted, shutting down")
    finally:
        _cleanup(config, stores)
