#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""DATABASE STORES"""

__updated__ = "2025-12-07 01:43:22"


from .pg_pool import create_pg_pool  # noqa: F401
from .redis_pool import create_redis_pool, create_redis_client


def init_datastores(config: dict) -> dict:
    """
    Initialize the required datastores (Postgres, Redis).
    Return a dict containing the pools and ready-to-use clients.
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
