#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Test module"""

__updated__ = "2026-02-07 07:13:29"

import json
import pytest

from skel_v3.app import create_api_app
from skel_v3.config import get_config

# -----------------------------------------------------------------------------
#
# Module design notes:
# Baseline tests for app bootstrap and configuration defaults.
#
# Responsibilities:
# - Validate health endpoint response contract.
# - Validate fallback behavior for missing `APP_TYPE`.
# - Keep tests deterministic by disabling external datastores.
#
# Scope boundaries:
# - No integration coverage for Postgres/Redis/SMTP in this module.
# - Focused on lightweight unit-level behavior only.
#
# Maintenance guidance:
# - Keep tests small, direct, and behavior-oriented.
# - Add new tests when bootstrap contracts change.
#
# -----------------------------------------------------------------------------


@pytest.fixture
def client():
    """Build a Flask test client with external datastores disabled.

    Inputs:
    - No direct parameters.

    Returns:
    - Test `FlaskClient` yielded by the fixture.
    """
    config = get_config()
    config["APP_TYPE"] = "api"
    config["PG_ENABLED"] = False
    config["REDIS_ENABLED"] = False

    app = create_api_app(config)
    app.testing = True
    with app.test_client() as client:
        yield client


def test_health(client):
    """Validate that `/health` returns the expected JSON with status 200.

    Inputs:
    - client: fixture providing HTTP test client.

    Returns:
    - `None`.
    """
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    data = json.loads(resp.data)
    assert data["status"] == "ok"


def test_get_config_defaults_to_api(monkeypatch):
    """Check that default `APP_TYPE` is `api` when env var is missing.

    Inputs:
    - monkeypatch: pytest fixture used to manipulate environment variables.

    Returns:
    - `None`.
    """
    monkeypatch.delenv("APP_TYPE", raising=False)
    config = get_config()
    assert config["APP_TYPE"] == "api"


if __name__ == "__main__":
    pytest.main()
