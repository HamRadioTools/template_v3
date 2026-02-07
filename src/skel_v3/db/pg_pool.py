#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""DATABASE STORES - Postgres connection pool"""

__updated__ = "2025-12-12 02:51:18"

import logging
from typing import Any, Optional

import psycopg2
from psycopg2 import pool

LOGGER = logging.getLogger(__name__)

minconn = 1  # Minimum number of connections to keep in the pool
maxconn = 20  # Maximum number of connections to keep in the pool


def create_pg_pool(config: dict) -> Optional[Any]:
    """
    Create a psycopg2 SimpleConnectionPool based on configuration.
    Return None if connection fails so the service can fail-open.
    """
    try:
        return pool.SimpleConnectionPool(
            minconn=int(config.get("PG_MIN_CONN", minconn)),
            maxconn=int(config.get("PG_MAX_CONN", maxconn)),
            user=config["PG_USER"],
            password=config["PG_PASSWORD"],
            host=config["PG_HOST"],
            port=config["PG_PORT"],
            database=config["PG_DBNAME"],
        )
    except psycopg2.OperationalError as exc:
        LOGGER.warning(
            "Unable to connect to Postgres; PG pool disabled. Error: %s",
            exc,
            extra={"pg_status": "error"},
        )
        return None
