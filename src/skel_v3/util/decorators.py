#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""PACKAGE UTILS"""

__updated__ = "2025-12-16 02:42:57"

import time
import logging
import redis.exceptions
from functools import wraps

from flask import request, jsonify, g

from db.redis_apikeys import get_apikey_metadata
from util.request_id import get_or_create_request_id

logger = logging.getLogger(__name__)


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            logger.info("%s took %.2f ms", func.__name__, elapsed_ms)

    return wrapper


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled error in handler")
            return jsonify({"ok": False, "error": str(exc)}), 500

    return wrapper


def require_apikey(stores: dict | None):
    redis_client = stores.get("redis") if stores else None

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            base_extra = {
                "request_id": get_or_create_request_id(),
                "http_method": request.method,
                "http_path": request.path,
                "remote_ip": request.remote_addr,
            }

            def log(level: int, message: str, **extra_fields):
                payload = dict(base_extra)
                payload.update({k: v for k, v in extra_fields.items() if v is not None})
                logger.log(level, message, extra=payload)

            if redis_client is None:
                log(logging.ERROR, "Redis client not configured for API key validation", redis_status="missing")
                return (
                    jsonify(
                        {"ok": False, "error": "Internal configuration error"},
                    ),
                    500,
                )

            apikey = request.headers.get("X-API-Key")
            log(logging.DEBUG, "Validating API key via Redis", redis_status="query", has_apikey=bool(apikey))

            try:
                metadata = get_apikey_metadata(redis_client, apikey)
            except redis.exceptions.AuthenticationError as exc:
                log(
                    logging.ERROR,
                    f"Redis authentication error during API key lookup: {exc}",
                    redis_status="auth_error",
                )
                return (
                    jsonify(
                        {"ok": False, "error": "API key store authentication error"},
                    ),
                    500,
                )
            except redis.exceptions.RedisError as exc:
                log(logging.ERROR, f"Redis error during API key lookup: {exc}", redis_status="error")
                return (
                    jsonify(
                        {"ok": False, "error": "API key store unavailable"},
                    ),
                    500,
                )

            if metadata is None:
                log(logging.INFO, "Invalid or disabled API key", redis_status="ok", reason="invalid_or_disabled")
                return jsonify({"ok": False, "error": "Unauthorized"}), 401

            g.customer = metadata
            log(logging.DEBUG, "API key validated", redis_status="ok")

            return func(*args, **kwargs)

        return wrapper

    return decorator
