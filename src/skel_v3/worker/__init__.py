#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""WORKER package"""

__updated__ = "2026-02-07 08:03:39"

from worker.runtime import run_worker_app

# -----------------------------------------------------------------------------
#
# Module design notes:
# Worker package public interface.
#
# Responsibilities:
# - Re-export worker runtime entrypoint for import simplicity.
# - Keep worker API surface explicit.
#
# Scope boundaries:
# - No worker execution logic belongs here.
# - Avoid adding side-effect imports.
#
# Maintenance guidance:
# - Keep this initializer thin and stable.
# - Add exports only for intentionally public worker symbols.
#
# -----------------------------------------------------------------------------

__all__ = ["run_worker_app"]
