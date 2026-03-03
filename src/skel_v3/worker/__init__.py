#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""WORKER package"""

__updated__ = "2026-02-07 08:03:39"

from worker.runtime import run_worker_app

# -----------------------------------------------------------------------------
#
# Module design notes:
# Exposes worker runtime entrypoint as the worker package public API.
#
# -----------------------------------------------------------------------------

__all__ = ["run_worker_app"]
