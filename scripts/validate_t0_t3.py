#!/usr/bin/env python3
"""Validate the minimal T0-T3 governance contract."""

from __future__ import annotations

import argparse

from _governance import emit, resolve_project, validate_project, validation_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=None, help="Project root; defaults to the current directory")
    parser.add_argument("--json", action="store_true", help="Emit one JSON object to stdout")
    args = parser.parse_args()
    validation = validate_project(resolve_project(args.project))
    emit(validation_payload(validation), args.json)
    return 0 if validation.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
