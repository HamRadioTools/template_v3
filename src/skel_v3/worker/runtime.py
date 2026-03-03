#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

# -----------------------------------------------------------------------------
#
# Worker runtime design and operations guide
#
# This module provides a single runtime entrypoint: ``run_worker_app(config)``.
# It supports two operating modes controlled by ``WORKER_MODE``:
#
# 1) one-shot mode (default)
#    - Intended for job-style workloads.
#    - Process flow:
#      bootstrap -> perform one unit of work -> cleanup -> exit.
#    - Suitable for cron/scheduler/CI/Nomad periodic tasks where each run
#      should terminate after finishing.
#
# 2) loop mode
#    - Intended for daemon-style workloads.
#    - Process flow:
#      bootstrap -> repeated work loop with sleep -> signal-driven shutdown.
#    - The loop interval is controlled by ``WORKER_POLL_INTERVAL`` (seconds).
#    - SIGTERM/SIGINT are trapped for graceful shutdown and cleanup.
#
# Operational recommendations:
# - Prefer ``one-shot`` as baseline for predictable lifecycle and retries.
# - Use ``loop`` only when continuous polling is required by the workload.
# - Keep `_perform_work` idempotent and deterministic when possible.
# - Do not log secrets; use structured metadata in log `extra` fields.
#
# -----------------------------------------------------------------------------

"""Functional worker runtime helpers."""

from __future__ import annotations

__updated__ = "2026-03-02 17:25:00"

import logging
import signal
import time
from typing import Any

from db import init_datastores
from logs import init_logging

# -----------------------------------------------------------------------------
#
# Module design notes:
# Implements worker lifecycle orchestration for one-shot and loop execution.
#
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)


def _perform_work(config: dict, stores: dict[str, Any]) -> None:
    """Execute one unit of worker business logic.

    Inputs:
    - config: general runtime configuration.
    - stores: initialized datastore dependencies (DB/cache/others).

    Returns:
    - `None`.
    """
    ############################################################################
    #
    # CODE SHOULD COME HERE AND/OR IN ADDITIONAL MODULES IN THIS PACKAGE FOLDER
    #
    ############################################################################
    logger.info("Worker heartbeat", extra={"service": config.get("SERVICE_NAME")})


def _cleanup(config: dict, stores: dict[str, Any]) -> None:
    """Perform orderly cleanup when worker execution finishes.

    Inputs:
    - config: general runtime configuration.
    - stores: initialized dependencies that may require cleanup.

    Returns:
    - `None`.
    """
    logger.info("Worker cleanup complete", extra={"service": config.get("SERVICE_NAME")})


def run_worker_app(config: dict) -> None:
    """Start worker runtime in `oneshot` or `loop` mode.

    Inputs:
    - config: runtime settings including `WORKER_MODE` and execution parameters.

    Returns:
    - `None`. Process exits after work completion, signal handling, or error.
    """
    init_logging(config)
    stores = init_datastores(config)
    mode = str(config.get("WORKER_MODE", "oneshot")).strip().lower()

    if mode == "oneshot":
        logger.info(
            "Worker starting (one-shot mode)",
            extra={"service": config.get("SERVICE_NAME"), "env": config.get("SERVICE_ENV"), "worker_mode": mode},
        )
        try:
            _perform_work(config, stores)
        finally:
            _cleanup(config, stores)
        return

    if mode == "loop":
        poll_interval = int(config.get("WORKER_POLL_INTERVAL", 5))
        stopping = False

        def _handle_stop(signum, _frame):
            """Mark graceful stop when a termination signal is received.

            Inputs:
            - signum: captured signal (SIGTERM/SIGINT).
            - _frame: execution frame (unused).

            Returns:
            - `None`.
            """
            nonlocal stopping
            logger.info("Received signal %s, preparing to stop", signum)
            stopping = True

        signal.signal(signal.SIGTERM, _handle_stop)
        signal.signal(signal.SIGINT, _handle_stop)

        logger.info(
            "Worker starting (loop mode)",
            extra={
                "service": config.get("SERVICE_NAME"),
                "env": config.get("SERVICE_ENV"),
                "worker_mode": mode,
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
        return

    raise ValueError(f"Invalid WORKER_MODE {mode!r}. Use 'oneshot' or 'loop'.")
