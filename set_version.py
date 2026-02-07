#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

"""Set Version"""

__updated__ = "2026-02-01 04:06:41"

import re
from pathlib import Path

init_file = next(Path("src").glob("*/__init__.py"))
pyproject_file = Path("pyproject.toml")

# Read the version from __init__.py
try:
    version_match = re.search(r'__version__ = "(.*?)"', init_file.read_text())
except FileNotFoundError:
    print(f"{init_file} not found")
    exit(1)

# -- Update version in pyproject.toml
if version_match:
    version = version_match.group(1)
    # Update version in pyproject.toml
    try:
        pyproject_content = pyproject_file.read_text()
    except FileNotFoundError:
        print(f"{pyproject_file} not found")
        exit(1)
    pyproject_content = re.sub(r'version = "(.*?)"', f'version = "{version}"', pyproject_content)
    pyproject_file.write_text(pyproject_content)
    print(f"Updated pyproject.toml version to {version}")
