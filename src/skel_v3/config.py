#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Configuration module"""

__updated__ = "2026-02-07 07:13:47"

import os
from dotenv import load_dotenv, find_dotenv


# Load .env if present (ideal for local development).
# In containers, if .env is missing, environment variables are used as-is.
load_dotenv(find_dotenv())


def str_to_bool(value: str | None, default: bool = True) -> bool:
    """
    Convert strings like "true"/"false"/"1"/"0" to boolean values.
    If value is None, return the provided default.
    """
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "y", "t")


def get_config() -> dict:
    """
    Return the 12-factor configuration as a simple dict.
    Valid for both API and worker modes.
    """

    # --- Service environment ---
    # local, dev, test, staging, prod, ...
    env = os.getenv("SERVICE_ENV", "local")

    # Default log level per environment
    if env in ("local", "dev"):
        default_log_level = "DEBUG"
    else:
        default_log_level = "INFO"

    return {
        # --- Execution mode ---
        # - api: run the Flask API
        # - worker: run the worker
        "APP_TYPE": os.getenv("APP_TYPE", "api"),
        # --- Service ---
        "SERVICE_NAME": os.getenv("SERVICE_NAME", "skel-service"),
        "SERVICE_VERSION": os.getenv("SERVICE_VERSION", "0.1.0"),
        "SERVICE_NAMESPACE": os.getenv("SERVICE_NAMESPACE", "default"),
        "SERVICE_ENV": env,
        # --- Logging ---
        # When LOG_LEVEL is not defined:
        # - local/dev: DEBUG
        # - others: INFO
        "LOG_LEVEL": os.getenv("LOG_LEVEL", default_log_level),
        # --- Postgres ---
        "PG_ENABLED": str_to_bool(os.getenv("PG_ENABLED", "false"), default=False),
        "PG_HOST": os.getenv("PG_HOST", "postgres"),
        "PG_PORT": int(os.getenv("PG_PORT", "5432")),
        "PG_USER": os.getenv("PG_USER", "postgres"),
        "PG_PASSWORD": os.getenv("PG_PASSWORD", "postgres"),
        "PG_DBNAME": os.getenv("PG_DBNAME", "postgres"),
        "PG_MIN_CONN": int(os.getenv("PG_MIN_CONN", "1")),
        "PG_MAX_CONN": int(os.getenv("PG_MAX_CONN", "5")),
        # "PG_SSLMODE": os.getenv("PG_SSLMODE", "prefer"),  # use if TLS is ever required
        # --- Redis ---
        "REDIS_ENABLED": str_to_bool(os.getenv("REDIS_ENABLED", "false"), default=False),
        "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
        "REDIS_PORT": int(os.getenv("REDIS_PORT", "6379")),
        "REDIS_DB": int(os.getenv("REDIS_DB", "0")),
        "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD"),
        "REDIS_MAX_CONN": int(os.getenv("REDIS_MAX_CONN", "20")),
    }
