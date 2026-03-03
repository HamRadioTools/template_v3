#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""DATABASE STORES"""

__updated__ = "2025-12-07 01:43:22"


from db.pg_pool import create_pg_pool  # noqa: F401
from db.redis_pool import create_redis_pool, create_redis_client

# -----------------------------------------------------------------------------
#
# Module design notes:
# Builds datastore handles from config and returns them as runtime dependencies.
#
# -----------------------------------------------------------------------------


def init_datastores(config: dict) -> dict:
    """Initialize Postgres/Redis connections based on configuration.

    Inputs:
    - config: configuration dictionary with datastore flags and credentials.

    Returns:
    - Dictionary with `pg_pool`, `redis_pool`, and `redis` client (or `None` when disabled).
    """
    pg_pool = create_pg_pool(config) if config.get("PG_ENABLED", False) else None

    redis_pool = None
    redis_client = None
    if config.get("REDIS_ENABLED", False):
        redis_pool = create_redis_pool(config)
        redis_client = create_redis_client(redis_pool)

    return {
        "pg_pool": pg_pool,
        "redis_pool": redis_pool,
        "redis": redis_client,
    }
