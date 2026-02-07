#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""LOGGING WITH FORMAT TO STDOUT"""

__updated__ = "2025-12-07 01:45:00"

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
WERKZEUG_REQUEST_RE = re.compile(r"\"([A-Z]+ .+?)\"")


class JsonStdoutHandler(logging.StreamHandler):
    """
    Stream handler that writes logs to STDOUT as structured JSON, including:
    - ISO8601 timestamp in UTC
    - Service name and environment (if provided)
    - Code location (file, line, function)
    - request_id when present via logger.extra
    - Exception details (type, message, stacktrace) when applicable
    """

    def __init__(
        self,
        service_name: Optional[str] = None,
        environment: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.service_name = service_name
        self.environment = environment

    def emit(self, record: logging.LogRecord) -> None:
        try:
            # Timestamp in UTC with ISO8601 format
            ts = datetime.fromtimestamp(record.created, tz=timezone.utc)
            timestamp = ts.isoformat().replace("+00:00", "Z")

            # Strip ANSI color codes if present
            message = ANSI_ESCAPE_RE.sub("", record.getMessage())

            # Adjust Werkzeug request line to look cleaner
            if record.name == "werkzeug":
                message = WERKZEUG_REQUEST_RE.sub(r"[\1] ", message)

            log: Dict[str, Any] = {
                "timestamp": timestamp,
                "level": record.levelname,
                "logger": record.name,
                "message": message,
                # Service context
                "service": self.service_name,
                "env": self.environment,
                # Code location (useful for debugging)
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }

            # Optional request_id (if provided via logger.extra)
            request_id = getattr(record, "request_id", None)
            if request_id is not None:
                log["request_id"] = request_id

            # Additional HTTP / MQTT context when available
            contextual_fields = (
                "http_method",
                "http_path",
                "remote_ip",
                "client_id",
                "auth_result",
                "reason",
                "callsign",
                "canonical_cid",
                "pg_status",
                "redis_status",
            )
            for field in contextual_fields:
                value = getattr(record, field, None)
                if value is not None:
                    log[field] = value

            duration_ms = getattr(record, "duration_ms", None)
            if duration_ms is not None:
                log["duration_ms"] = duration_ms

            # Exception details when present
            if record.exc_info:
                exc_type = record.exc_info[0].__name__ if record.exc_info[0] else None
                log["exception_type"] = exc_type
                log["exception_message"] = str(record.getMessage())
                log["stacktrace"] = logging.Formatter().formatException(record.exc_info)

            self.stream.write(json.dumps(log, ensure_ascii=False) + "\n")
            self.flush()
        except Exception:
            self.handleError(record)
