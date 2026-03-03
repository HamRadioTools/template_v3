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

# -----------------------------------------------------------------------------
#
# Module design notes:
# Houses reusable decorators for timing, error handling, and API-key gating.
#
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)


def measure_time(func):
    """Decorator that measures execution time and logs it.

    Inputs:
    - func: target function to instrument.

    Returns:
    - Wrapper function preserving the logical signature of `func`.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Execute the decorated function while timing total duration.

        Inputs:
        - *args, **kwargs: original arguments for the decorated function.

        Returns:
        - Value returned by the decorated function.
        """
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            logger.info("%s took %.2f ms", func.__name__, elapsed_ms)

    return wrapper


def handle_errors(func):
    """Decorator that catches unhandled exceptions in HTTP handlers.

    Inputs:
    - func: function/handler to protect.

    Returns:
    - Wrapper that returns a JSON `500` response on exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Run the handler and map unhandled errors to a standard response.

        Inputs:
        - *args, **kwargs: original handler arguments.

        Returns:
        - Handler result or `(json_error, 500)` tuple on failure.
        """
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled error in handler")
            return jsonify({"ok": False, "error": str(exc)}), 500

    return wrapper


def require_apikey(stores: dict | None):
    """Decorator factory that enforces API key validation through Redis.

    Inputs:
    - stores: dependency map; uses `stores["redis"]` when available.

    Returns:
    - Decorator usable on Flask handlers.
    """
    redis_client = stores.get("redis") if stores else None

    def decorator(func):
        """Wrap the handler with API key validation.

        Inputs:
        - func: Flask handler to protect.

        Returns:
        - Wrapper that allows or blocks execution based on validation result.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Validate `X-API-Key` header and decide request authorization.

            Inputs:
            - *args, **kwargs: original handler arguments.

            Returns:
            - Error response (`401`/`500`) or authorized handler result.
            """
            base_extra = {
                "request_id": get_or_create_request_id(),
                "http_method": request.method,
                "http_path": request.path,
                "remote_ip": request.remote_addr,
            }

            def log(level: int, message: str, **extra_fields):
                """Local helper for structured logging with request context.

                Inputs:
                - level: logging level (INFO/ERROR/...).
                - message: log message text.
                - **extra_fields: additional fields merged into `extra`.

                Returns:
                - `None`.
                """
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
