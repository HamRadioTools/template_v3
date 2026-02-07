#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Schema validation"""

__updated__ = "2026-02-01 03:57:17"


from marshmallow import Schema, fields, validate


class AuthRequestSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[A-Za-z0-9_.-]{1,64}$", error="Invalid username"),
    )
    password = fields.Str(load_default="")
    client_id = fields.Str(load_default="")
    ip = fields.Str(load_default="")
