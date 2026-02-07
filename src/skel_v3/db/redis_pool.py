#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""DATABASE STORES - Redis connection pool management"""

__updated__ = "2025-12-07 01:44:17"

import redis


def create_redis_pool(config: dict) -> redis.ConnectionPool:
    """
    Create a Redis connection pool from the provided config.
    If REDIS_PASSWORD is None, connect without authentication.
    """
    password = config.get("REDIS_PASSWORD") or None

    return redis.ConnectionPool(
        host=config["REDIS_HOST"],
        port=config["REDIS_PORT"],
        db=config["REDIS_DB"],
        password=password,
        max_connections=int(config.get("REDIS_MAX_CONN", 20)),
        decode_responses=False,  # keep bytes and decode later in redis_apikeys
    )


def create_redis_client(pool: redis.ConnectionPool) -> redis.Redis:
    return redis.Redis(connection_pool=pool)
