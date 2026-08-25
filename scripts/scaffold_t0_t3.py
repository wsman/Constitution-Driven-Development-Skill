#!/usr/bin/env python3
"""Create the minimal managed T0-T3 project surface."""

from __future__ import annotations

import argparse
from pathlib import Path

from _governance import emit, resolve_project, scaffold_project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=None, help="Project root; defaults to the current directory")
    parser.add_argument("--force", action="store_true", help="Replace existing managed template files")
    parser.add_argument("--json", action="store_true", help="Emit one JSON object to stdout")
    args = parser.parse_args()
    project = resolve_project(args.project)
    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    payload = scaffold_project(project, template_root, args.force)
    emit(payload, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
