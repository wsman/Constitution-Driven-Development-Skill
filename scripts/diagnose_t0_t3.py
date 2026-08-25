#!/usr/bin/env python3
"""Diagnose T0-T3 health and impact-scoped blockers."""

from __future__ import annotations

import argparse

from _governance import diagnose_project, emit, resolve_project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=None, help="Project root; defaults to the current directory")
    parser.add_argument("--json", action="store_true", help="Emit one JSON object to stdout")
    args = parser.parse_args()
    payload = diagnose_project(resolve_project(args.project))
    emit(payload, args.json)
    return 0 if payload["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
