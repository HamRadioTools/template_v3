#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""DATABASE STORES - Redis API key management"""

__updated__ = "2025-12-07 01:44:00"

"""
Suggested Redis hash shape for API keys:

apikey:{apikey}
    customer_id         → string (required)
    tier                → string (free / pro / enterprise)
    rate_limit          → int (requests per minute)
    quota_daily         → int (daily limit)
    disabled            → 0/1
    allowed_endpoints   → JSON array with allowed routes
    metadata            → optional JSON map

Example (Redis CLI):

redis-cli HSET apikey:abcd1234 \
  customer_id "c001" \
  tier "pro" \
  rate_limit "800" \
  quota_daily "10000" \
  disabled "0" \
  allowed_endpoints "[\"/hello\", \"/calc\"]" \
  metadata "{\"country\":\"ES\",\"contact\":\"admin@example.com\"}"
"""


import json
import redis
from typing import Optional, Dict


def get_apikey_metadata(r: redis.Redis, apikey: str) -> Optional[Dict]:
    """
    Return a dict with API key metadata if present and enabled,
    or None if it does not exist or is disabled.

    r: existing Redis client (redis.Redis)
    """
    if not apikey:
        return None

    key = f"apikey:{apikey}"
    data = r.hgetall(key)  # dict {b'field': b'value'}

    if not data:
        return None

    decoded = {k.decode(): v.decode() for k, v in data.items()}

    # 1) Check disabled flag first
    if decoded.get("disabled") == "1":
        return None

    # 2) Convert numeric fields
    for field in ("rate_limit", "quota_daily"):
        if field in decoded:
            decoded[field] = int(decoded[field])

    # 3) Parse JSON fields
    if "allowed_endpoints" in decoded:
        try:
            decoded["allowed_endpoints"] = json.loads(decoded["allowed_endpoints"])
        except json.JSONDecodeError:
            decoded["allowed_endpoints"] = []

    if "metadata" in decoded:
        try:
            decoded["metadata"] = json.loads(decoded["metadata"])
        except json.JSONDecodeError:
            decoded["metadata"] = {}

    return decoded
