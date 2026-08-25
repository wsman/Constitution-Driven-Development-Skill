from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def scaffold(project: Path) -> dict[str, object]:
    result = run_script("scaffold_t0_t3.py", "--project", str(project), "--json")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.count("\n") == 1
    return json.loads(result.stdout)


def validate(project: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    result = run_script("validate_t0_t3.py", "--project", str(project), "--json")
    assert result.stderr == ""
    assert result.stdout.count("\n") == 1
    return result, json.loads(result.stdout)


def test_scaffold_validate_and_diagnose_happy_path(tmp_path: Path) -> None:
    project = tmp_path / "project"
    payload = scaffold(project)
    assert payload["schema"] == "cdd.t0-t3.scaffold.v1"
    assert payload["created"]

    validation, validation_payload = validate(project)
    assert validation.returncode == 0
    assert validation_payload["verdict"] == "PASS"

    diagnosis = run_script("diagnose_t0_t3.py", "--project", str(project), "--json")
    assert diagnosis.returncode == 0
    parsed = json.loads(diagnosis.stdout)
    assert parsed["schema"] == "cdd.t0-t3.diagnosis.v1"
    assert parsed["verdict"] == "PASS"
    assert parsed["weakestLayer"] == "none"
    assert [gate["status"] for gate in parsed["gates"]] == ["PASS"] * 5 + ["READY", "PASS"]


def test_scaffold_is_create_only_until_force(tmp_path: Path) -> None:
    project = tmp_path / "project"
    scaffold(project)
    active = project / "memory_bank" / "t0_core" / "active_context.md"
    active.write_text("local content\n", encoding="utf-8", newline="\n")

    second = scaffold(project)
    assert active.read_text(encoding="utf-8") == "local content\n"
    assert "memory_bank/t0_core/active_context.md" in second["skipped"]

    forced = run_script("scaffold_t0_t3.py", "--project", str(project), "--force", "--json")
    assert forced.returncode == 0
    assert active.read_text(encoding="utf-8").startswith("# Active Context")
    assert "memory_bank/t0_core/active_context.md" in json.loads(forced.stdout)["replaced"]


def test_project_defaults_to_current_directory(tmp_path: Path) -> None:
    result = run_script("scaffold_t0_t3.py", "--json", cwd=tmp_path)
    assert result.returncode == 0
    assert json.loads(result.stdout)["project"] == str(tmp_path.resolve())


def test_usage_error_is_exit_two_and_does_not_emit_json(tmp_path: Path) -> None:
    result = run_script("validate_t0_t3.py", "--project", str(tmp_path), "--unknown")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "unrecognized arguments" in result.stderr


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("missing_t0", "T0_MISSING"),
        ("malformed_yaml", "SUPPORT_PARSE"),
        ("stale_t2", "T2_STALE_ROUTE"),
        ("incomplete_support", "SUPPORT_COVERAGE"),
        ("t3_authority_leak", "T3_AUTHORITY_LEAK"),
    ],
)
def test_validation_failures_are_specific(tmp_path: Path, mutation: str, expected_code: str) -> None:
    project = tmp_path / mutation
    scaffold(project)
    support_path = project / "memory_bank" / "module_support_map.yaml"
    if mutation == "missing_t0":
        (project / "memory_bank" / "t0_core" / "active_context.md").unlink()
    elif mutation == "malformed_yaml":
        support_path.write_text("modules: [\n", encoding="utf-8", newline="\n")
    elif mutation == "stale_t2":
        (project / "memory_bank" / "t2_standards" / "DS-999_unrouted.md").write_text(
            "# Unrouted\n", encoding="utf-8", newline="\n"
        )
    elif mutation == "incomplete_support":
        support = yaml.safe_load(support_path.read_text(encoding="utf-8"))
        support["modules"]["example-module"]["t2Refs"][1]["coverage"].remove("evidence")
        support_path.write_text(yaml.safe_dump(support, sort_keys=False), encoding="utf-8", newline="\n")
    elif mutation == "t3_authority_leak":
        path = project / "memory_bank" / "t0_core" / "active_context.md"
        path.write_text(path.read_text(encoding="utf-8") + "T3 is authoritative for release.\n", encoding="utf-8", newline="\n")

    result, payload = validate(project)
    assert result.returncode == 1
    assert payload["verdict"] == "FAIL"
    assert expected_code in {issue["code"] for issue in payload["errors"]}


def test_plain_output_uses_stderr_only(tmp_path: Path) -> None:
    project = tmp_path / "project"
    scaffold(project)
    result = run_script("validate_t0_t3.py", "--project", str(project))
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr.startswith("PASS:")
